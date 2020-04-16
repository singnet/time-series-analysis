import sys
import grpc

# import the generated classes
import service.service_spec.fbprophet_forecast_pb2_grpc as grpc_bt_grpc
import service.service_spec.fbprophet_forecast_pb2 as grpc_bt_pb2

from service import registry


TEST_URL = "http://bh.singularitynet.io:7000/Resources/example_wp_log_peyton_manning.csv"

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        grpc_port = registry["fbprophet_forecast_service"]["grpc"]
        endpoint = input("Endpoint (localhost:{}): ".format(grpc_port)) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(grpc_port)

        # Open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))

        grpc_method = input("Method (forecast): ") if not test_flag else ""
        if grpc_method == "":
            grpc_method = "forecast"

        url = input("CSV (URL): ") if not test_flag else TEST_URL
        if url == "":
            url = TEST_URL

        period = input("Period (10): ") if not test_flag else 10
        if period == "":
            period = 10

        points = input("Points (10): ") if not test_flag else 365
        if points == "":
            points = 365

        if grpc_method == "forecast":
            stub = grpc_bt_grpc.ForecastStub(channel)
            response = stub.forecast(grpc_bt_pb2.Input(url=url,
                                                       period=int(period),
                                                       points=int(points)))
            print("\nresponse:")
            print("len(response.observed): {}".format(len(response.observed)))
            print("len(response.seasonal): {}".format(len(response.seasonal)))
            print("len(response.forecast): {}".format(len(response.forecast)))
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)
