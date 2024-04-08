FROM registry.redhat.io/ubi8/python-39@sha256:519f2258d9475f881009a6da084de94a06dd822913bde3ec99225e502c8417c5

RUN pip install pymysql

ADD update_ro_keys.py /

ENTRYPOINT [ "python", "/update_ro_keys.py" ]
