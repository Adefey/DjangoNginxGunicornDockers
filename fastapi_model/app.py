import os
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import KNNImputer
import sys
from fastapi import FastAPI
from pydantic import BaseModel, conlist

FASTAPI_APP = FastAPI()

class FeaturesModel(BaseModel):
    feature : str

class PredictResultModel(BaseModel):
    result: str

class Mdl:
    def __init__(self, mdl, tkzr):
        self.user_len = 1
        self.chat_history_ids = torch.zeros((1, 0), dtype=torch.int)
        self.new_user_input_ids = torch.zeros((1, 0), dtype=torch.int)
        self.mdl = mdl
        self.tkzr = tkzr
        self.mdl.to('cpu')
        # self.mdl.eval()

    def get_length_param(self, text, tokenizer) -> str:
        tokens_count = len(tokenizer.encode(text))
        if tokens_count <= 15:
            len_param = '1'
        elif tokens_count <= 50:
            len_param = '2'
        elif tokens_count <= 256:
            len_param = '3'
        else:
            len_param = '-'
        return len_param

    def get_user_param(self, text: dict, machine_name_in_chat: str) -> str:
        if text['from'] == machine_name_in_chat:
            return '1'  # post
        else:
            return '0'  # comment

    def predict(self, sentence):
        self.user_len = self.get_length_param(sentence, self.tkzr)
        self.new_user_input_ids = self.tkzr.encode(f"|0|{self.user_len}|"
                                                   + sentence + self.tkzr.eos_token, return_tensors="pt")
        self.chat_history_ids = torch.cat(
            [self.chat_history_ids, self.new_user_input_ids], dim=-1)

        self.new_user_input_ids = self.tkzr.encode(
            f"|1|{self.user_len}|", return_tensors="pt")
        self.chat_history_ids = torch.cat(
            [self.chat_history_ids, self.new_user_input_ids], dim=-1)

        input_len = self.chat_history_ids.shape[-1]
        self.chat_history_ids = self.mdl.generate(
            self.chat_history_ids,
            num_return_sequences=1,
            max_length=512,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.6,
            eos_token_id=self.tkzr.eos_token_id,
            pad_token_id=self.tkzr.pad_token_id,
        )

        answer = self.tkzr.decode(
            self.chat_history_ids[:, input_len:][0], skip_special_tokens=True)
        self.chat_history_ids = torch.zeros((1, 0), dtype=torch.int)
        self.new_user_input_ids = torch.zeros((1, 0), dtype=torch.int)
        return answer

trained_model = None

@FASTAPI_APP.on_event("startup")
def prepare_models():
    global trained_model
    try:
        trained_model = torch.load("mdl.pkl")
    except Exception as e:
        class TrainedModelMock:
            def __init__(self):
                self.error_msg = str(e)
                self.attrs = dir(__name__)

            def predict(self, text):
                cwd = os.getcwd()
                contents = os.listdir(cwd)
                return f"Файл данных поврежден и/или отсутствует в {cwd} и возникла ошибка :( Ошибка: {self.error_msg}"
        trained_model = TrainedModelMock()


@FASTAPI_APP.get("/predict", response_model=PredictResultModel)
def predict(data : FeaturesModel):
    input = data.feature
    result = trained_model.predict(input)
    return PredictResultModel(result=result)


