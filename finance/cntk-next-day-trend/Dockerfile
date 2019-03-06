FROM microsoft/cntk:latest

ARG git_owner="singnet"
ARG git_repo="time-series-analysis"
ARG git_branch="master"
ARG snetd_version

ENV SINGNET_REPOS=/opt/singnet
ENV git_repo=${git_repo}
ENV FINANCE_FOLDER=${SINGNET_REPOS}/${git_repo}/finance
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
    git clone -b ${git_branch} https://github.com/${git_owner}/${git_repo}.git

RUN cd ${FINANCE_FOLDER}/${SERVICE_NAME} && \
    /root/anaconda3/envs/cntk-py35/bin/python -m pip install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${FINANCE_FOLDER}/${SERVICE_NAME}
