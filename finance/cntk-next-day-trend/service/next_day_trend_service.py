import sys
import logging

import grpc
import concurrent.futures as futures

from service import common
from service.next_day_trend import NextDayTrend

# Importing the generated codes from buildproto.sh
from service.service_spec import next_day_trend_pb2_grpc as grpc_bt_grpc
from service.service_spec.next_day_trend_pb2 import Output

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("next_day_trend_service")


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class NextDayTrendServicer(grpc_bt_grpc.NextDayTrendServicer):
    def __init__(self):
        self.source = ""
        self.contract = ""
        self.start = ""
        self.end = ""
        self.target_date = ""

        self.output = ""

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

        # To respond we need to create a Output() object (from .proto file)
        self.output = Output()

        sp = NextDayTrend(self.source, self.contract, self.start, self.end, self.target_date)
        self.output.response = str(sp.asset_trend()).encode("utf-8")
        log.info("asset_trend({},{},{},{},{})={}".format(self.source,
                                                         self.contract,
                                                         self.start,
                                                         self.end,
                                                         self.target_date,
                                                         self.output.response))
        return self.output


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
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
