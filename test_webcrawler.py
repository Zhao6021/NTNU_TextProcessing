import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'

for i in range(10): #往上爬3頁
	#print(url)
	response = requests.get(url)
	if response.status_code == requests.codes.ok:
		soup = BeautifulSoup(response.text, "html.parser")

		titles = soup.find_all("div", class_="title")
		#print(titles)
		for title in titles:
			a_title = title.select_one("a")
			if a_title:
				name = a_title.getText()
				resultLIST=re.findall(r"(?<=\[).+?(?=\])",name)
				if '影評' in resultLIST or all([label.find('雷')!=-1 for label in resultLIST]):
					print(name)
				href = title.select_one("a").get("href")
		u = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
		url = "https://www.ptt.cc"+ u[1]["href"] #組合出上一頁的網址

		#print(soup.prettify())  #輸出排版後的HTML內容
	else:
		print('request error')
