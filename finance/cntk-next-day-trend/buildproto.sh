#! /bin/bash
/root/anaconda3/envs/cntk-py35/bin/python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service/service_spec/next_day_trend.proto
