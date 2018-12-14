import sys
import grpc

# import the generated classes
from service.service_spec import next_day_trend_pb2_grpc as grpc_bt_grpc
from service.service_spec import next_day_trend_pb2 as grpc_bt_pb2

from service import registry

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        endpoint = input("Endpoint (localhost:{}): ".format(registry["next_day_trend_service"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(registry["next_day_trend_service"]["grpc"])

        # Open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))

        grpc_method = input("Method (trend): ") if not test_flag else ""
        if grpc_method == "":
            grpc_method = "trend"

        source = input("Source(yahoo): ") if not test_flag else ""
        if source == "":
            source = "yahoo"

        contract = input("Contract(SPY): ") if not test_flag else ""
        if contract == "":
            contract = "SPY"

        start = input("Start Date(2000-01-01): ") if not test_flag else ""
        if start == "":
            start = "2018-01-01"

        end = input("End Date(2009-01-01): ") if not test_flag else ""
        if end == "":
            end = "2018-11-01"

        target_date = input("Target Date(2018-11-12): ") if not test_flag else ""
        if target_date == "":
            target_date = "2018-11-12"

        if grpc_method == "trend":
            stub = grpc_bt_grpc.NextDayTrendStub(channel)
            grpc_input = grpc_bt_pb2.Input(source=source,
                                           contract=contract,
                                           start=start,
                                           end=end,
                                           target_date=target_date)
            grpc_output = stub.trend(grpc_input)
            print(grpc_output.response)
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)
