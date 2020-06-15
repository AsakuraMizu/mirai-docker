FROM alpine

WORKDIR /app

RUN apk add --no-cache tzdata python3 py3-pip openjdk8-jre && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ADD requirements.txt /app
RUN pip3 install -r requirements.txt

ADD . /app
RUN python3 bootstrap.py && \
    echo Pure > /app/content/.wrapper.txt

CMD python3 bootstrap.py && \
    java -Dmirai.account=$MIRAI_ACCOUNT -Dmirai.password=$MIRAI_PASSWORD -jar mirai-console-wrapper-*.jar --update KEEP
