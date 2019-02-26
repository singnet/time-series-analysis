FROM microsoft/cntk:latest

ARG git_owner
ARG git_repo
ARG git_branch
ARG snetd_version="v0.1.7"

ENV SINGNET_REPOS=/opt/singnet
ENV TS_REPO_NAME=${git_repo}
ENV FINANCE_FOLDER=${SINGNET_REPOS}/${TS_REPO_NAME}/finance
ENV SERVICE_NAME=cntk-next-day-trend

RUN mkdir -p ${SINGNET_REPOS}

RUN apt-get update && \
    apt-get install -y apt-utils

RUN apt-get install -y \
    git \
    wget \
    nano

RUN cd ${SINGNET_REPOS} && \
    mkdir snet-daemon && \
    cd snet-daemon && \
    wget https://github.com/singnet/snet-daemon/releases/download/${snetd_version}/snet-daemon-${snetd_version}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${snetd_version}-linux-amd64.tar.gz && \
    mv snet-daemon-${snetd_version}-linux-amd64/snetd /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone -b ${git_branch} https://github.com/${git_owner}/${TS_REPO_NAME}.git

RUN cd ${FINANCE_FOLDER}/${SERVICE_NAME} && \
    /root/anaconda3/envs/cntk-py35/bin/python -m pip install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${FINANCE_FOLDER}/${SERVICE_NAME}
