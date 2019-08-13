# 从拉取基础镜像
FROM python:3.6.7
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

COPY . /app
WORKDIR /app
EXPOSE 5006
RUN pip3 install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
CMD ["python3", "/app/server.py","run-as-server"]
