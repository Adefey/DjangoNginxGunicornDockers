FROM fedora:36

COPY ./requirements.txt /home/

RUN cd /home/ && \
    dnf upgrade -y --refresh && \
    dnf -y install python && \
    dnf -y install pip && \
    pip install -r /home/requirements.txt

CMD ["uvicorn", "--app-dir", "/home/", "--host", "0.0.0.0", "--port", "14565", "app:FASTAPI_APP"]
