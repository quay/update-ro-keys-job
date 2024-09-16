FROM registry.access.redhat.com/ubi8/python-39@sha256:2979f218fed8aaa46f65df87ce6d370d6ebc532970446b456e9513bf7c9449d1

RUN pip install pymysql

ADD update_ro_keys.py /

ENTRYPOINT [ "python", "/update_ro_keys.py" ]
