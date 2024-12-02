FROM registry.redhat.io/ubi8/python-39@sha256:39ded558fb5a9de976b0ec01470138b54ea7482b3eb0f46b3abf35e7bac97aa4

RUN pip install pymysql

ADD update_ro_keys.py /

ENTRYPOINT [ "python", "/update_ro_keys.py" ]
