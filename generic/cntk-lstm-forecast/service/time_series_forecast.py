import cntk as C

import os
import pandas as pd
import numpy as np
import time
import yfinance

from saxpy.sax import sax_via_window

import logging
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("time_series_forecast")


class Forecast:

    def __init__(self, window_len, word_len, alphabet_size, source_type, source, contract, start_date, end_date):
        self.window_len = window_len
        self.word_len = word_len
        self.alphabet_size = alphabet_size

        # CSV or Financial
        self.source_type = source_type
        self.source = source

        # Financial data
        self.contract = contract
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def _next_batch(x, y, ds, batch_size):
        """get the next batch for training"""
        def as_batch(p_data, start, count):
            return p_data[start:start + count]
        for i in range(0, len(x[ds]), batch_size):
            yield as_batch(x[ds], i, batch_size), as_batch(y[ds], i, batch_size)

    @staticmethod
    def _create_model(x_local, h_dims):
        """Create the model for time series prediction"""
        with C.layers.default_options(initial_state=0.1):
            m = C.layers.Recurrence(C.layers.LSTM(h_dims))(x_local)
            m = C.sequence.last(m)
            m = C.layers.Dropout(0.2)(m)
            m = C.layers.Dense(1)(m)
            return m

    @staticmethod
    def _get_letter(n, alpha_to_num):
        alpha_list = sorted(alpha_to_num)
        for a in alpha_list[::-1]:
            if n >= alpha_to_num[a][0]:
                return a
        return -1

    def _get_asset_data(self):
        retry_cnt, max_num_retry = 0, 3
        while retry_cnt < max_num_retry:
            try:
                df = yfinance.download(tickers=[self.contract], start=self.start_date, end=self.end_date)
                df.reset_index(inplace=True, drop=False)
                return df
            except Exception as e:
                log.error(e)
                retry_cnt += 1
                time.sleep(np.random.randint(1, 10))
        log.error("{} is not reachable".format(self.source))
        return []

    def _get_pred(self, model, input_node, word, alpha_to_num):
        x = {"pred": []}
        y = {"pred": []}
        num_list = [np.float32(alpha_to_num[char][1]) for char in word]
        increment_list = []
        for num in num_list:
            increment_list.append(num)
            x["pred"].append(np.array(increment_list))
        results = []
        for x_batch, _ in self._next_batch(x, y, "pred", self.window_len):
            pred = model.eval({input_node: x_batch})
            results.extend(pred[:, 0])

        position_in_sax_interval = -1
        if results:
            pred = results[-1]
            alpha_list = sorted(alpha_to_num)
            for a in alpha_list[::-1]:
                if pred >= alpha_to_num[a][0]:
                    step = alpha_to_num[a][2] - alpha_to_num[a][0]
                    pred_delta = pred - alpha_to_num[a][0]
                    position_in_sax_interval = float(pred_delta / step)
                    if position_in_sax_interval < 0:
                        position_in_sax_interval = 0
                    if position_in_sax_interval > 1:
                        position_in_sax_interval = 1
                    break
            return results[-1], position_in_sax_interval
        return [], position_in_sax_interval

    def _prepare_data(self, alpha_to_num):

        result_x = result_y = dict()
        last_sax_word = ""
        sax_ret = dict()
        if self.source_type == "csv":
            if "http://" in self.source or "https://" in self.source:
                csv_file = "tmp.csv"
                urlretrieve(self.source, csv_file)
                ts_data = pd.read_csv(csv_file)
                if "input" in ts_data:
                    ts_data["input"] = pd.to_numeric(ts_data["input"], downcast='float')
                    sax_ret = sax_via_window(ts_data["input"].values,
                                             self.window_len,
                                             self.word_len,
                                             alphabet_size=self.alphabet_size,
                                             nr_strategy="none",
                                             z_threshold=0.01)
                os.remove(csv_file)
            else:
                log.error("Error: Invalid Link.")
                return result_x, result_y, last_sax_word
        elif self.source_type == "financial":
            ts_data = self._get_asset_data()
            if "Close" in ts_data:
                close_tag = "Close"
            elif "close" in ts_data:
                close_tag = "close"
            else:
                log.error("Error: Couldn't find Close data.")
                return result_x, result_y, last_sax_word

            ts_data["input"] = ts_data[close_tag]
            sax_ret = sax_via_window(ts_data["input"].values,
                                     self.window_len,
                                     self.word_len,
                                     alphabet_size=self.alphabet_size,
                                     nr_strategy="none",
                                     z_threshold=0.01)
        else:
            log.error("Invalid 'source_type'!")
            return result_x, result_y, last_sax_word

        if sax_ret:
            my_sax = dict()
            for k, v in sax_ret.items():
                for i in v:
                    my_sax[i] = k

            tmp_d = {"x": [], "y": []}
            for i in range(len(my_sax)):
                word = my_sax[i]
                if i < len(my_sax) - 1:
                    pred = my_sax[i + 1][-1]
                    num_list = [np.float32(alpha_to_num[char][1]) for char in word]
                    increment_list = []
                    for num in num_list:
                        increment_list.append(num)
                        tmp_d["x"].append(np.array(increment_list))
                        tmp_d["y"].append(np.array([np.float32(alpha_to_num[pred][1])]))

            result_x = {"train": tmp_d["x"]}
            result_y = {"train": np.array(tmp_d["y"])}
            if my_sax:
                last_sax_word = my_sax[len(my_sax) - 1]
            else:
                log.error("Not enough SAX data!")
        else:
            log.error("Not enough data!")

        return result_x, result_y, last_sax_word

    def forecast(self):

        # Mapping each letter to number between 0-1
        alpha_to_num_step = float(1 / self.alphabet_size)
        alpha_to_num_shift = float(alpha_to_num_step / 2)

        # Dict = [floor, point, celling]
        alpha_to_num = dict()
        for i in range(self.alphabet_size):
            step = (alpha_to_num_step * i)
            alpha_to_num[chr(97 + i)] = [step,
                                         step + alpha_to_num_shift,
                                         step + alpha_to_num_step]

        x, y, last_sax_word = self._prepare_data(alpha_to_num)

        response = {
            "last_sax_word": "Fail",
            "forecast_sax_letter": "Fail",
            "position_in_sax_interval": -1
        }
        
        if not x or not y or not last_sax_word:
            error_msg = "Error while preparing data!"
            log.error(error_msg)
            response["error"] = error_msg
            return response

        # Trying to optimize settings for training.
        # Forbidding heavy training (max 100k input rows from CSV or Financial data)
        batch_size = self.window_len * self.word_len
        if batch_size != 1152:
            batch_size = 1152
        h_dims = self.word_len + 1

        epochs = 100
        if len(x["train"]) > 200000:
            error_msg = "Configured data set too large (max: 200k): {}".format(len(x["train"]))
            log.error(error_msg)
            response["error"] = error_msg
            return response
        if len(x["train"]) < 100000:
            epochs = 250
        if len(x["train"]) < 40000:
            epochs = 500
        if len(x["train"]) < 20000:
            epochs = 1000

        log.debug("Training Info:")
        log.debug("len(x[train]): {}".format(len(x["train"])))
        log.debug("Epochs       : {}".format(epochs))
        log.debug("Batch Size   : {}".format(batch_size))

        if x and y:
            input_node = C.sequence.input_variable(1)
            z = self._create_model(input_node, h_dims)
            var_l = C.input_variable(1, dynamic_axes=z.dynamic_axes, name="y")
            learning_rate = 0.005
            lr_schedule = C.learning_parameter_schedule(learning_rate)
            loss = C.squared_error(z, var_l)
            error = C.squared_error(z, var_l)
            momentum_schedule = C.momentum_schedule(0.9, minibatch_size=batch_size)
            learner = C.fsadagrad(z.parameters,
                                  lr=lr_schedule,
                                  momentum=momentum_schedule)
            trainer = C.Trainer(z, (loss, error), [learner])

            # training
            loss_summary = []

            start = time.time()
            for epoch in range(0, epochs):
                for x_batch, l_batch in self._next_batch(x, y, "train", batch_size):
                    trainer.train_minibatch({input_node: x_batch, var_l: l_batch})

                if epoch % (epochs / 10) == 0:
                    training_loss = trainer.previous_minibatch_loss_average
                    loss_summary.append(training_loss)
                    log.debug("epoch: {}, loss: {:.4f} [time: {:.1f}s]".format(epoch,
                                                                               training_loss,
                                                                               time.time() - start))

            pred, position_in_sax_interval = self._get_pred(z, input_node, last_sax_word, alpha_to_num)
            forecast_sax_letter = self._get_letter(pred, alpha_to_num)
            log.debug("================= PRED =====================")
            log.debug("last_sax_word           : {}".format(last_sax_word))
            log.debug("pred                    : {}".format(pred))
            log.debug("forecast_sax_letter     : {}".format(forecast_sax_letter))
            log.debug("position_in_sax_interval: {}".format(position_in_sax_interval))
            log.debug("============================================")

            response["last_sax_word"] = last_sax_word
            response["forecast_sax_letter"] = forecast_sax_letter
            response["position_in_sax_interval"] = position_in_sax_interval
        else:
            error_msg = "X and/or Y with no length: {} and {}".format(len(x), len(y))
            log.error(error_msg)
            response["error"] = error_msg
        return response
