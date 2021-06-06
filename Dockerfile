FROM python

COPY python-mnemonic/mnemonic/ ./mnemonic/
COPY secret-sharing /tmp/secret-sharting
RUN pip install /tmp/secret-sharting
COPY main.py ./main.py
ENTRYPOINT ["python", "main.py"]
