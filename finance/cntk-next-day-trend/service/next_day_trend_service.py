import sys
import logging

import multiprocessing

import grpc
import concurrent.futures as futures

from service import common
from service.next_day_trend import NextDayTrend

# Importing the generated codes from buildproto.sh
from service.service_spec import next_day_trend_pb2_grpc as grpc_bt_grpc
from service.service_spec.next_day_trend_pb2 import Output

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("next_day_trend_service")


def mp_asset_trend(obj, return_dict):
    return_dict["response"] = obj.asset_trend()


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class NextDayTrendServicer(grpc_bt_grpc.NextDayTrendServicer):
    def __init__(self):
        self.source = ""
        self.contract = ""
        self.start = ""
        self.end = ""
        self.target_date = ""
        log.info("NextDayTrendServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def trend(self, request, context):
        # In our case, request is a Input() object (from .proto file)
        self.source = request.source
        self.contract = request.contract
        self.start = request.start
        self.end = request.end
        self.target_date = request.target_date

        ndt = NextDayTrend(self.source,
                           self.contract,
                           self.start,
                           self.end,
                           self.target_date)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=mp_asset_trend, args=(ndt, return_dict))
        p.start()
        p.join()

        response = return_dict.get("response", None)
        if not response or "error" in response:
            error_msg = response.get("error", None) if response else None
            log.error(error_msg)
            context.set_details(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            return Output()

        log.info("asset_trend({},{},{},{},{})={}".format(self.source,
                                                         self.contract,
                                                         self.start,
                                                         self.end,
                                                         self.target_date,
                                                         response["trend"]))
        return Output(response=response["trend"])


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=4, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_NextDayTrendServicer_to_server(NextDayTrendServicer(), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


if __name__ == "__main__":
    """
    Runs the gRPC server to communicate with the Snet Daemon.
    """
    parser = common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    common.main_loop(serve, args)
