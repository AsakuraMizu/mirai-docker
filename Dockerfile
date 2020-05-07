FROM python:alpine AS build

WORKDIR /mirai

ADD requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

ADD . /mirai
RUN python bootstrap.py



FROM java:alpine

WORKDIR /app

COPY --from=build /mirai/plugins /app/plugins
COPY --from=build /mirai/content /app/content
COPY --from=build /mirai/mirai-console-wrapper-*.jar /app
ADD MiraiAPIHTTP.yml plugins/MiraiAPIHTTP/setting.yml
RUN echo Pure > /app/content/.wrapper.txt

CMD java -Dmirai.account=$ACCOUNT -Dmirai.password=$PASSWORD -jar mirai-console-wrapper-*.jar --update KEEP
