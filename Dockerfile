# 使用支持CUDA的Ubuntu基础镜像
FROM ubuntu:22.04

# 设置工作目录
WORKDIR /app

# 避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive

# 更换软件源为阿里云源
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 安装系统依赖
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    wget \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# 确保使用 Python 3.10
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.10 /usr/bin/python

# 升级pip并配置pip源
RUN python3 -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ && \
    mkdir -p ~/.pip && \
    echo "[global]" > ~/.pip/pip.conf && \
    echo "index-url = https://mirrors.aliyun.com/pypi/simple/" >> ~/.pip/pip.conf && \
    echo "trusted-host = mirrors.aliyun.com" >> ~/.pip/pip.conf

# 安装PyTorch和CUDA依赖
RUN pip3 install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0

# 安装其他Python依赖
RUN pip3 install \
    opencv-python \
    pillow \
    numpy \
    ultralytics

# 设置环境变量
ENV PYTHONPATH=/app
ENV CUDA_VISIBLE_DEVICES=0

# 创建工作目录
WORKDIR /app/Door_Window_Detect

# 使用 tail -f /dev/null 保持容器运行
CMD ["tail", "-f", "/dev/null"]