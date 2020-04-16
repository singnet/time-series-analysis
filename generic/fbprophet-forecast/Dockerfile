FROM ubuntu:18.04

ARG git_owner="singnet"
ARG git_repo="time-series-analysis"
ARG git_branch="master"
ARG snetd_version

ENV SINGNET_REPOS=/opt/singnet
ENV GENERIC_FOLDER=${SINGNET_REPOS}/${git_repo}/generic
ENV SERVICE_NAME=fbprophet-forecast

RUN mkdir -p ${SINGNET_REPOS}

RUN apt-get update && \
    apt-get install -y apt-utils

RUN apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    curl \
    git \
    wget \
    nano

# Installing SNET Daemon
RUN SNETD_GIT_VERSION=`curl -s https://api.github.com/repos/singnet/snet-daemon/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")' || echo "v3.1.6"` && \
    SNETD_VERSION=${snetd_version:-${SNETD_GIT_VERSION}} && \
    cd /tmp && \
    wget https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone -b ${git_branch} https://github.com/${git_owner}/${git_repo}.git

RUN cd ${GENERIC_FOLDER}/${SERVICE_NAME} && \
    pip3 install Cython && \
    pip3 install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${GENERIC_FOLDER}/${SERVICE_NAME}
