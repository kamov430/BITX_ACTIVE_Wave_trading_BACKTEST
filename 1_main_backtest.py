#!/home/kamov430/SOXL_ACTIVE_Wave_trading/WAVE/bin/python3
#/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import ta.momentum
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import mojito_edit
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

if __name__ == "__main__":
	# init setting ##################################################################
	df = pd.read_csv("BITX_Merged_Data.csv")
	print(df)
	# Free space ####################################################################
	# 데이터 불러오기

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