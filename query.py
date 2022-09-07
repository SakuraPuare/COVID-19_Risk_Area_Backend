import time
from typing import Dict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import version


def main() -> Dict:
	url = 'http://bmfw.www.gov.cn/yqfxdjcx/risk.html'

	desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
	desired_capabilities["pageLoadStrategy"] = "none"

	driver = webdriver.Chrome()
	driver.maximize_window()
	driver.get(url)

	loading = driver.find_element(By.CLASS_NAME, 'loading')
	while loading.get_attribute('style') != 'display: none;':
		time.sleep(0.5)

	title = driver.find_element(By.CLASS_NAME, 'tabs-header').text
	title_list = title.split(' ')
	time_f = f"{title_list[0][2:]}-{title_list[1].split('，')[:-1][0]}"

	if version.has_version(time_f):
		return version.load_version(time_f)

	area_type_list = ['high', 'mid', 'low']
	risk_list = {}
	for i in area_type_list:
		risk_list[i] = {}
	try:
		for t, area_type in enumerate(area_type_list):
			if t != 0:
				driver.execute_script('document.documentElement.scrollTop = 0')
				elements = driver.find_elements(By.CLASS_NAME, 'tabs-header-tab')
				element = elements[t]
				element.click()
				time.sleep(1)

				loading = driver.find_element(By.CLASS_NAME, 'loading')
				while loading.get_attribute('style') != 'display: none;':
					time.sleep(0.5)
			while True:
				next_page = driver.find_element(By.ID, 'nextPage')
				risk_dom = driver.find_elements(By.CLASS_NAME, 'risk-info-table')
				for i in risk_dom:
					soup = BeautifulSoup(i.get_attribute('innerHTML'), 'html.parser')
					name = soup.div.contents[0].text
					area_list = []
					for _ in soup.findAll("tr"):
						count = 1
						for line in soup.findAll("td"):
							if count % 2 == 0:
								continue
							else:
								area_list.append(line.text)
								count += 1
					risk_list[area_type][name] = list(set(area_list))
					driver.execute_script('document.documentElement.scrollTop = 1000000')
					next_page = driver.find_element(By.ID, 'nextPage')
				if next_page.get_attribute('disabled') is not None:
					break
				else:
					next_page.click()
					time.sleep(0.2)

		version.save_version(time_f, risk_list)
		return risk_list
	except StaleElementReferenceException:
		driver.quit()
		return main()


if __name__ == '__main__':
	response = main()
	t_now = time.strftime("%Y-%m-%d-%H时", time.localtime())
	# 2022-09-07-16时
	version.save_version(t_now, response)
	pass
