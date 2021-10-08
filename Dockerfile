FROM quay.io/bitnami/python

RUN pip install pymysql

ADD update_ro_keys.py /

ENTRYPOINT [ "python", "/update_ro_keys.py" ]
