import sys
import gradio as gr
from kats.consts import TimeSeriesData
from kats.models.prophet import ProphetModel, ProphetParams
import yfinance as yf

def forecast(ticker, start_day, start_month, start_year, end_day, end_month, end_year):
    tick = yf.Ticker(ticker)

    start_date = str(int(start_year)) + "-" + str(int(start_month)) + "-" + str(int(start_day))
    end_date = str(int(end_year)) + "-" + str(int(end_month)) + "-" + str(int(end_day))
    try:
        tick_history = tick.history(start=start_date, end=end_date)

    except Exception as e:
        raise Exception("Invalid date")

    tick_history.reset_index(level=0, inplace=True) # Since Date is an Index column
    #print(tick_history.columns)
    tick_main = tick_history[["Date", "Close"]]
    #print(tick_main.columns)
    tick_in_ts = TimeSeriesData(tick_main, time_col_name="Date")

    params = ProphetParams(seasonality_mode='multiplicative') # additive mode gives worse results

    # create a prophet model instance
    m = ProphetModel(tick_in_ts, params)

    # fit model simply by calling m.fit()
    m.fit()

    # make prediction for next year
    m.predict(steps=12, freq="MS")
    #print(fcst)
    pl = m.plot()
    print(type(pl))

    return pl

gr.Interface(forecast, 
            inputs=["text", "number", "number", "number", "number", "number", "number"], 
            outputs=["plot"], 
            examples=[["SPY", 1, 1, 2020, 31, 12, 2020]]).launch()