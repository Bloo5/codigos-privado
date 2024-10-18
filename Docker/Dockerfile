ARG CUDA_VERSION=11.4.3
ARG CUDNN_VERSION=8
ARG UBUNTU_VERSION=20.04

FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-runtime-ubuntu${UBUNTU_VERSION}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # python
        python3 \
        python3-venv \
        python3-pip \
        python3-opencv \
        python3-dev \
    # dependencies
        build-essential \
        udev \
        libavformat-dev \
        libavcodec-dev \
        libavdevice-dev \
        libavutil-dev \
        libswscale-dev \
        libswresample-dev \
        libavfilter-dev \
        pkg-config \
    # cleanup
    && apt-get clean && apt-get purge --auto-remove && rm -rf /var/lib/apt/lists/*

# venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
COPY c.txt c.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install wheel && \
    PIP_CONSTRAINT=c.txt python3 -m pip install av==10.0.0 --no-binary av && \
    python3 -m pip install --no-cache-dir -r requirements.txt

WORKDIR /WmDetection

COPY Models Models
COPY Parameters Parameters
COPY src src

ENV MODE="src.Systems.Wavemaker"
EXPOSE 15300

CMD python3 -m $MODE
