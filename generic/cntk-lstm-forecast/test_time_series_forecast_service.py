import sys
import grpc

# import the generated classes
import service.service_spec.time_series_forecast_pb2_grpc as grpc_bt_grpc
import service.service_spec.time_series_forecast_pb2 as grpc_bt_pb2

from service import registry

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        # Service ONE - Arithmetic
        endpoint = input("Endpoint (localhost:{}): ".format(registry["time_series_forecast_service"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(registry["time_series_forecast_service"]["grpc"])

        # Open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))

        grpc_method = input("Method (forecast): ") if not test_flag else "forecast"
        if grpc_method == "":
            grpc_method = "forecast"

        window_len = input("Window length (24): ") if not test_flag else 24
        if window_len == "":
            window_len = 24
        word_len = input("Word length (8): ") if not test_flag else 8
        if word_len == "":
            word_len = 8
        alphabet_size = input("Alphabet size (5): ") if not test_flag else 5
        if alphabet_size == "":
            alphabet_size = 5

        # CSV or Financial
        source_type = input("Source Type (finance): ") if not test_flag else "financial"
        if source_type == "":
            source_type = "financial"
        source = input("Source (yahoo): ") if not test_flag else "yahoo"
        if source == "":
            source = "yahoo"

        # Financial data
        contract = input("Contract (SPY): ") if not test_flag else "SPY"
        if contract == "":
            contract = "SPY"
        start_date = input("Start date (2012-01-01): ") if not test_flag else "2012-01-01"
        if start_date == "":
            start_date = "2012-01-01"
        end_date = input("End date (2018-12-10): ") if not test_flag else "2018-12-10"
        if end_date == "":
            end_date = "2018-12-10"

        if grpc_method == "forecast":
            stub = grpc_bt_grpc.ForecastStub(channel)
            request = grpc_bt_pb2.Input(window_len=window_len,
                                        word_len=word_len,
                                        alphabet_size=alphabet_size,
                                        source_type=source_type,
                                        source=source,
                                        contract=contract,
                                        start_date=start_date,
                                        end_date=end_date)
            response = stub.forecast(request)
            print("\nresponse:")
            print("last_sax_word           : {}".format(response.last_sax_word))
            print("forecast_sax_letter     : {}".format(response.forecast_sax_letter))
            print("position_in_sax_interval: {}".format(round(response.position_in_sax_interval, 2)))
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)