import sys
import grpc

# import the generated classes
from service.service_spec import stock_prediction_pb2_grpc as grpc_bt_grpc
from service.service_spec import stock_prediction_pb2 as grpc_bt_pb2

from service import registry

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "test":
                test_flag = True

        endpoint = input("Endpoint (localhost:{}): ".format(registry["next_day_trend_service"]["grpc"]))
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

        start_date = input("Start Date(2000-01-01): ") if not test_flag else ""
        if start_date == "":
            start_date = "2018-01-01"

        end_date = input("End Date(2009-01-01): ") if not test_flag else ""
        if end_date == "":
            end_date = "2018-11-01"

        target_date = input("Target Date(2018-11-12): ") if not test_flag else ""
        if target_date == "":
            target_date = "2018-11-12"

        if grpc_method == "predict":
            stub = grpc_bt_grpc.NextDayTrendStub(channel)
            grpc_input = grpc_bt_pb2.Input(source=source,
                                           contract=contract,
                                           start=start_date,
                                           end=end_date,
                                           target_date=target_date)
            grpc_output = stub.trend(grpc_input)
            print(grpc_output.response)
        else:
            print("Invalid method!")

    except Exception as e:
        print(e)
