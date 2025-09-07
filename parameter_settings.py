# 이익복리율 (%)
PCR = 0.80
# 손실복리율 (%)
LCR = 0.30
# 투자금갱신주기
update_cycle = 10
# 초기투자금
initial_investment = 100000 #10만불 시작 (약 1억3천만원)


### safe mode setting
safe_mode_setting = {
	# 분할수
	"split_num" : 7,
	# 최대보유기간
	"max_holding" : 28,
	# 매수조건 (%)
	"buy_condition" : 0.042, #4.2%
	# 매도조건 (%)
	"sell_condition" : 0.050 #5.0%
}

### aggressive mode setting
aggressive_mode_setting = {
	# 분할수
	"split_num" : 7,
	# 최대보유기간
	"max_holding" : 7,
	# 매수조건 (%)
	"buy_condition" : 0.131, #13.1%
	# 매도조건 (%)
	"sell_condition" : 0.066 #6.6%
}

