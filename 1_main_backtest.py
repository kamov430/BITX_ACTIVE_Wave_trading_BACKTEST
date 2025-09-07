#!/home/kamov430/SOXL_ACTIVE_Wave_trading/WAVE/bin/python3
#/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from parameter_settings import *
import pandas as pd

import ta.momentum
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import datetime
import os
import pprint

import numpy as np
import math
from time import sleep
import shutil
import copy
import importlib

def gen_BITX_close_chart():
	df = pd.read_csv("BITX_Merged_Data.csv")

	colors = df["Mode"].map({"Safe": "blue", "Aggressive": "red"})
	df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
	plt.scatter(df["Date"], df["Close"], c=colors)
	plt.plot(df["Date"], df["Close"], alpha=0.5, color="gray")

	# X축을 1년 단위로 설정
	plt.gca().xaxis.set_major_locator(mdates.YearLocator(1))   # 1년마다
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))  # 연도만 표시

	plt.xticks(rotation=45)

	plt.title("BITX Daily Close with Mode")
	plt.xlabel("Date")
	plt.ylabel("Close Price")
	plt.show()

if __name__ == "__main__":
	# range setting ##################################################################
	# safe_mode_setting_split_num = range(,)
	# safe_mode_setting_max_holding = range(,)
	# safe_mode_setting_buy_condition = range(,)
	# safe_mode_setting_sell_condition = range(,)

	# aggressive_mode_setting_split_num = range(,)
	# aggressive_mode_setting_max_holding = range(,)
	# aggressive_mode_setting_buy_condition = range(,)
	# aggressive_mode_setting_sell_condition = range(,)

	# for i in safe_mode_setting_split_num:
	# 	safe_mode_setting["split_num"] = i
	# 	print(safe_mode_setting)

	# start backtest #################################################################
	# 완성된 data를 기반으로 Backtest 시작
	df = pd.read_csv("BITX_Merged_Data.csv")

	df = df.iloc[::-1].reset_index(drop=True) # 날짜 거꾸로 뒤집기
	
	for i in range(len(df)):
		row = df.iloc[i]
		buy_signal = False

		# 모드 check
		mode = row["Mode"]
		if mode == "Safe":
			mode_setting = safe_mode_setting
		elif mode == "Aggressive":
			mode_setting = aggressive_mode_setting
		
		# 매수조건 check
		close_1day_ago = df.iloc[i-1]["Close"] if i-1 >= 0 else 1000000
		if round((1+mode_setting["buy_condition"])*close_1day_ago,2) > row["Close"] or close_1day_ago == None:
			buy_signal = True
		
		print(1+mode_setting["buy_condition"], close_1day_ago, round((1+mode_setting["buy_condition"])*close_1day_ago,2), buy_signal)
		print(row["Date"], row["Close"], row["Mode"])
		# sleep(1)