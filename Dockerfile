FROM python

COPY python-mnemonic /tmp/python-mnemonic
COPY secret-sharing /tmp/secret-sharing
RUN pip install /tmp/secret-sharing /tmp/python-mnemonic
COPY main.py ./main.py
ENTRYPOINT ["python", "main.py"]
