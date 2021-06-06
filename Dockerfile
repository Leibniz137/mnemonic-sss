FROM python

COPY python-mnemonic/mnemonic/ ./mnemonic/
COPY main.py ./main.py
COPY secret-sharing /tmp/secret-sharting
RUN pip install /tmp/secret-sharting
ENTRYPOINT ["python", "main.py"]
