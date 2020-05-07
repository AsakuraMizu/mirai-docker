FROM alpine

WORKDIR /app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
    apk add --no-cache python3 openjdk8-jre

ADD . /app
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install -r requirements.txt && \
    python3 bootstrap.py && \
    echo Pure > /app/content/.wrapper.txt

CMD python3 bootstrap.py && \
    java -Dmirai.account=$MIRAI_ACCOUNT -Dmirai.password=$MIRAI_PASSWORD -jar mirai-console-wrapper-*.jar --update KEEP
