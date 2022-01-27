import pandas as pd
import numpy as np
import pandas_market_calendars as mcal
import yfinance

from fbprophet import Prophet
from statsmodels.tsa.seasonal import STL

import time
import datetime
import base64
import tempfile
import logging

pd.plotting.register_matplotlib_converters()


logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("series_decomposition")


class FBProphetForecast:
    def __init__(self):
        log.debug("FBProphetForecast created.")

    @staticmethod
    def get_ticker_data(ticker, start_date, end_date):
        retry_cnt, max_num_retry = 0, 3
        while retry_cnt < max_num_retry:
            try:
                df = yfinance.download(tickers=[ticker], start=start_date, end=end_date)
                df.reset_index(inplace=True, drop=False)
                return df
            except Exception as e:
                log.warning(e)
                retry_cnt += 1
                time.sleep(np.random.randint(1, 10))
        log.error("yahoo is not reachable")
        return pd.DataFrame()

    def get_ticker_stl(self, ticker, start_date="2015-01-01", end_date=None, period=None):
        if not end_date:
            end_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
        df = self.get_ticker_data(ticker, start_date, end_date)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        try:
            # Try to use the input period, force 5 in failure.
            stl = STL(df["Close"], period=period).fit()
        except Exception as e:
            log.warning(e)
            stl = STL(df["Close"], period=5).fit()
        return df, stl

    @staticmethod
    def process_csv_url(url):
        # Link
        if "http://" in url or "https://" in url:
            return pd.read_csv(url)
        # Base64
        elif len(url) > 500:
            csv_data = base64.b64decode(url)
            with tempfile.NamedTemporaryFile(mode="ab+") as temp:
                temp.write(csv_data)
                temp.seek(0)
                return pd.read_csv(temp.name)
        return pd.DataFrame()

    def run(self, url, ds, y, period, points):
        response = dict()

        if (period and period > 300) or (points and points > 500):
            error_msg = "Too many forecast/period points! (max 300/500)"
            response["error"] = error_msg
            log.error(error_msg)
            return response
        
        if url:
            df = self.process_csv_url(url)
            if "ds" not in df or "y" not in df:
                error_msg = "Error while processing CSV from URL!"
                response["error"] = error_msg
                log.error(error_msg)
                return response
            ds = list(df["ds"].values)
            y = list(df["y"].values)
        
        if len(ds) != len(y) or len(ds) > 3000 or len(ds) > 3000:
            error_msg = "The length of DS and Y must be equal and <= 3000."
            response["error"] = error_msg
            log.error(error_msg)
            return response

        try:
            # Financial Series, first element of ds must by the Ticker
            if len(ds) == 1:
                ticker = ds[0]
                df, stl = self.get_ticker_stl(ticker, period=period)
                df = df.reset_index()
                ds = df["Date"].values
                y = df["Close"].values
                financial = True
            else:
                try:
                    # Try to use the input period, force 5 in failure.
                    stl = STL(y, period=period).fit()
                except Exception as e:
                    log.warning(e)
                    stl = STL(y, period=5).fit()
                financial = False
            log.info("Forecasting...")
            # Prophet
            df = pd.DataFrame(data={"ds": ds, "y": y})
            df["ds"] = pd.to_datetime(df["ds"])
            m = Prophet()
            m.fit(df)
            if financial:
                nyse = mcal.get_calendar('NYSE')
                start_date = datetime.datetime.today()
                end_date = start_date + datetime.timedelta(days=points)
                valid_days = nyse.valid_days(start_date=start_date, end_date=end_date)
                future = pd.DataFrame(data={"ds": [v.date() for v in valid_days]})
                future = pd.DataFrame(data={"ds": df["ds"].append(future["ds"], ignore_index=True)})
            else:
                future = m.make_future_dataframe(periods=points)
            forecast = m.predict(future)
            forecast_df = []
            for dt in forecast["ds"].values:
                ts = pd.to_datetime(dt)
                forecast_df.append(ts.strftime('%Y-%m-%d'))
    
            return {
                "observed": list(stl.observed),
                "trend": list(stl.trend),
                "seasonal": list(stl.seasonal),
                "forecast": list(forecast["yhat"].values),
                "forecast_ds": list(forecast_df),
                "forecast_lower": list(forecast["yhat_lower"].values),
                "forecast_upper": list(forecast["yhat_upper"].values)
            }

        except Exception as e:
            log.error(e)
            response["error"] = str(e)
            return response
