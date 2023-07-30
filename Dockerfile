FROM python:3.10-slim
WORKDIR /app
ADD . /app

# 更换为清华大学镜像
RUN set -xe; \
    echo 'deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free' > /etc/apt/sources.list; \
    echo 'deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free' >> /etc/apt/sources.list; \
    echo 'deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free' >> /etc/apt/sources.list; \
    echo 'deb http://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free' >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    build-essential cmake \
    && rm -rf /var/lib/apt/lists/*

RUN pip install Flask
RUN pip install -U chatglm-cpp

CMD ["python", "chatglm_server.py"]
