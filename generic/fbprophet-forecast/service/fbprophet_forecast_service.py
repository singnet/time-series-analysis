import sys

import grpc
import concurrent.futures as futures

import multiprocessing
import logging

from service import common

# Importing the generated codes from buildproto.sh
from service.service_spec import fbprophet_forecast_pb2_grpc as grpc_bt_grpc
from service.service_spec.fbprophet_forecast_pb2 import Output

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("fbprophet_forecast")


def mp_forecast(request, return_dict):
    from service.fbprophet_forecast import FBProphetForecast
    obj = FBProphetForecast()
    return_dict["response"] = obj.run(request.url,
                                      request.ds,
                                      request.y,
                                      request.period,
                                      request.points)


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class ForecastServicer(grpc_bt_grpc.ForecastServicer):
    def __init__(self):
        log.info("ForecastServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    @staticmethod
    def forecast(request, context):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
    
        p = multiprocessing.Process(target=mp_forecast, args=(request, return_dict))
        p.start()
        p.join()

        response = return_dict.get("response", None)
        if not response or "error" in response:
            error_msg = response.get("error", None) if response else None
            log.error(error_msg)
            context.set_details(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            return Output()

        log.info("forecast({})={},{}".format(len(request.y),
                                             len(response["seasonal"]),
                                             len(response["forecast"])))

        return Output(observed=response["observed"],
                      trend=response["trend"],
                      seasonal=response["seasonal"],
                      forecast=response["forecast"],
                      forecast_ds=response["forecast_ds"],
                      forecast_lower=response["forecast_lower"],
                      forecast_upper=response["forecast_upper"])


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=2, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_ForecastServicer_to_server(ForecastServicer(), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


if __name__ == "__main__":
    """
    Runs the gRPC server to communicate with the Snet Daemon.
    """
    parser = common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    common.main_loop(serve, args)
