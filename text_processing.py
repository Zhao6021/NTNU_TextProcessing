import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
resultDICT = {'好評':0, '普通':0, '負評':0}
finalLIST = []
count = 0
find_name = '神力女超人'

for i in range(50): #往上爬3頁
	response = requests.get(url)
	if response.status_code == requests.codes.ok:
		soup = BeautifulSoup(response.text, "html.parser")

		titles = soup.find_all("div", class_="title")
		for title in titles:
			is_find = False
			a_title = title.select_one("a")
			if a_title:
				name = a_title.getText()
				resultLIST=re.findall(r"(?<=\[).+?(?=\])",name)
				if '影評' in resultLIST or all([label.find('雷')!=-1 for label in resultLIST]):
					count+=1
					if name.find(find_name)!=-1:
						is_find = True
						if all([label.find('好')!=-1 or label.find('優')!=-1 for label in resultLIST]):
							resultDICT['好評']+=1
						elif all([label.find('負')!=-1 or label.find('爛')!=-1 for label in resultLIST]):
							resultDICT['負評']+=1
						else:
							resultDICT['普通']+=1

				###
				if is_find:				
					answerDICT = {'文章':0, '推':0, '箭頭':0, '噓':0}
					href = "https://www.ptt.cc" + title.select_one("a").get("href")
					response_2 = requests.get(href)
					if response_2.status_code == requests.codes.ok:
						soup_2 = BeautifulSoup(response_2.text, "html.parser")

						pushes = soup_2.find_all("div", class_="push")
						#print(pushes)
						userid = []
						for push in pushes:
							id = push.select_one(".push-userid").getText()
							if id not in userid:
								userid.append(id)
								push_tag = push.select_one(".push-tag").getText()
								if push_tag == '推 ':
									answerDICT['推'] += 1
								elif push_tag == '→ ':
									answerDICT['箭頭'] += 1
								elif push_tag == '噓 ':
									answerDICT['噓'] += 1
					finalLIST.append(answerDICT)
						#print(userid)
					#print(href)
					
		u = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
		url = "https://www.ptt.cc"+ u[1]["href"] #組合出上一頁的網址

		#print(soup.prettify())  #輸出排版後的HTML內容
	else:
		print('request error')

print(resultDICT)
for i in finalLIST:
	print(i)
