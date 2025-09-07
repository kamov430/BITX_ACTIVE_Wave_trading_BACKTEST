#!/home/kamov430/SOXL_ACTIVE_Wave_trading/WAVE/bin/python3
#/usr/bin/python3
import ta.momentum
from keys import key, secret, acc_no
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import datetime
import os
import pprint
import pandas as pd
import numpy as np
import math
from time import sleep
import shutil
import copy
import importlib
from telegram.error import TimedOut


NASDAQ_broker = mojito_edit.KoreaInvestment(
	api_key = key,
	api_secret=secret,
	acc_no=acc_no,
	exchange='나스닥'
)

AMEX_broker = mojito_edit.KoreaInvestment(
	api_key = key,
	api_secret=secret,
	acc_no=acc_no,
	exchange='아멕스'
)

# 차트 데이터 가져오기
def gen_kline(symbol,timeframe):
	ohlcv = NASDAQ_broker.fetch_ohlcv(
		symbol=symbol,
		timeframe=timeframe,
		adj_price=True
	)
	print(ohlcv)
	return ohlcv

# QQQ rsi 구하기
def get_QQQ_rsi() -> pd.Series:
	df = pd.read_csv("QQQ_Historical_Data_Weekly.csv")
	
	df = df.set_index('Date')
	df = df.astype(float)
	df = df[::-1]
	window = 14
	
	# 가격 변화량 계산
	delta = df["Price"].diff()

	# 상승분과 하락분 분리
	gains = delta.where(delta > 0, 0)
	losses = -delta.where(delta < 0, 0)

	# Cutler 방식은 단순이동평균(SMA) 사용
	avg_gain = gains.rolling(window=window, min_periods=window).mean()
	avg_loss = losses.rolling(window=window, min_periods=window).mean()

	# RSI 계산
	rs = avg_gain / avg_loss
	rsi = 100 - (100 / (1 + rs))
	rsi.name = 'rsi'
	return rsi


# mode 구하기 용 df 만들기
def make_mode_df():
	rsi = get_QQQ_rsi()
	# print(rsi)
	df = rsi.to_frame()
	# print(df)
	df["prev_rsi_1"] = df["rsi"].shift(1)
	df["prev_rsi_2"] = df["rsi"].shift(2)
	df["trading_mode"] = ""
	prev_result = ""
	# print(df)
	for index, row in df.iterrows():
		rsi_1w_ago = row['prev_rsi_1']
		rsi_2w_ago = row['prev_rsi_2']
		if 65 < rsi_2w_ago and rsi_1w_ago < rsi_2w_ago:
			df.at[index, "trading_mode"] = "Safe"
			prev_result = "Safe"
		elif 40 < rsi_2w_ago < 50 and rsi_1w_ago < rsi_2w_ago:
			df.at[index, "trading_mode"] = "Safe"
			prev_result = "Safe"
		elif 50 < rsi_2w_ago and rsi_1w_ago < 50:
			df.at[index, "trading_mode"] = "Safe"
			prev_result = "Safe"
		elif rsi_2w_ago < 35 and rsi_2w_ago < rsi_1w_ago:
			df.at[index, "trading_mode"] = "Aggressive"
			prev_result = "Aggressive"
		elif 50 < rsi_2w_ago < 60 and rsi_2w_ago < rsi_1w_ago:
			df.at[index, "trading_mode"] = "Aggressive"
			prev_result = "Aggressive"
		elif rsi_2w_ago < 50 and 50 < rsi_1w_ago:
			df.at[index, "trading_mode"] = "Aggressive"
			prev_result = "Aggressive"
		else:
			df.at[index, "trading_mode"] = prev_result
	return df


if __name__ == "__main__":
	# init setting ##################################################################
	mode_df = make_mode_df()
	print(mode_df)
	mode_df.to_csv("output.csv", index=True)
	# Free space ####################################################################
	# 데이터 불러오기
	df_daily = pd.read_csv("BITX_Historical_Data.csv")
	df_weekly = pd.read_csv("output.csv")

	# 날짜를 datetime으로 변환
	df_daily["Date"] = pd.to_datetime(df_daily["Date"])
	df_weekly["Date"] = pd.to_datetime(df_weekly["Date"])

	# 주봉 데이터를 날짜 기준으로 정렬
	df_weekly = df_weekly.sort_values("Date")

	# 각 일봉 날짜에 대해, 해당 날짜보다 '작거나 같은' 가장 최근 주봉 날짜 찾기
	df_daily["Mode"] = df_daily["Date"].apply(
		lambda x: df_weekly.loc[df_weekly["Date"] <= x, "trading_mode"].iloc[-1]
			if (df_weekly["Date"] <= x).any() else None
	)

	# 결과 확인
	print(df_daily.head(15))
	df_daily.to_csv("merged.csv", index=True)