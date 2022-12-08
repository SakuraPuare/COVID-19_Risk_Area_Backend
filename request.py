import hashlib
import json
import time
from typing import Dict, List

import httpx

import version

timestamp = str(int(time.time()))

token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
nonce = '123456789abcdefg'
pass_id = 'zdww'
key = "3C502C97ABA40D0A60FBEE50FAAD1DA"


def get_zdww_signature() -> str:
	zdww_sign = timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + 'QkjjtiLM2dCratiA' + timestamp
	hl = hashlib.sha256()
	hl.update(zdww_sign.encode('utf-8'))
	zdww_signature = hl.hexdigest().upper()
	return zdww_signature


def get_signature_header() -> str:
	hl = hashlib.sha256()
	sign_header = timestamp + token + nonce + timestamp
	hl.update(sign_header.encode('utf-8'))
	signature_header: str = hl.hexdigest().upper()
	return signature_header


def main() -> Dict[str, Dict[str, List[str]]]:
	url = 'http://bmfw.www.gov.cn/bjww/interface/interfaceJson'

	headers = {
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"Connection": "keep-alive",
		"Content-Type": "application/json; charset=UTF-8",
		"Host": "bmfw.www.gov.cn",
		"Origin": "http://bmfw.www.gov.cn",
		"Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
		"User-Agent": "Chrome/80.0.3987.87",
		"x-wif-nonce": "QkjjtiLM2dCratiA",
		"x-wif-paasid": "smt-application",
		"x-wif-signature": get_zdww_signature(),
		"x-wif-timestamp": timestamp
	}

	params = {
		'appId': "NcApplication",
		'paasHeader': "zdww",
		'timestampHeader': timestamp,
		'nonceHeader': "123456789abcdefg",
		'signatureHeader': get_signature_header(),
		'key': "3C502C97ABDA40D0A60FBEE50FAAD1DA"
	}

	resp = httpx.post(url, headers=headers, json=params)
	resp_json = json.loads(resp.content)['data']
	type_list = ['high', 'mid', 'low']
	risk_area = {}
	for t in type_list:
		risk_area[t] = {}
		if t == 'high':
			name = 'highlist'
		elif t == 'mid':
			name = 'middlelist'
		elif t == 'low':
			name = 'lowlist'
		else:
			return {}
		for i in resp_json[name]:
			risk_area[t][i['area_name']] = i['communitys']
	return risk_area


if __name__ == '__main__':
	response = main()
	t_now = time.strftime("%Y-%m-%d-%H时", time.localtime())
	print(response)
	version.save_version(t_now, response)
