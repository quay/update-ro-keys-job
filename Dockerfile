FROM registry.access.redhat.com/ubi8/python-39@sha256:6db74a276af9a6934a918b2c0117b74f185f3776882d5b7ae42e26128bfe13c9

RUN pip install pymysql

ADD update_ro_keys.py /

ENTRYPOINT [ "python", "/update_ro_keys.py" ]
