from bs4 import BeautifulSoup
import requests
import os
import datetime

from DataStore.MySQLClient import MySQLClient

def getnews(user,password):
	dns = {
		'user': 'root',
		'host': 'localhost',
		'password':'mysql',
		'database': 'mysql',
		'use_unicode':'True',
		'charset':'utf8'
	}
	db = MySQLClient(**dns)

	# 認証プロキシを指定
	user = user
	pw = password
	proxyurl = "http://" + user + ":" + pw + <プロキシサーバ:ポート番号>

	# 環境変数に設定
	os.environ["http_proxy"] = proxyurl
	os.environ["https_proxy"] = proxyurl

	try:
		# yahooニュースからのwebスクレイピング
		r = requests.get("https://news.yahoo.co.jp/",verify=False)
	except requests.exceptions.ProxyError:
		pass
	else:
		# NEWS_TBLのレコード情報を削除
		stmt = 'TRUNCATE TABLE NEWS_TBL'
		db.addquery(stmt)
		soup = BeautifulSoup(r.content, "html.parser")

		#主要ニューストピック情報を取得
		topics = soup.select('.topicsListItem')

		i = 1
		for topic in topics:
			stmt = 'INSERT INTO NEWS_TBL VALUES (' + str(i) + ",'" + topic.next.next + "','" + topic.next.attrs.get("href") + "')"
			db.addquery(stmt)
			i = i + 1

		file = open('updatetime.txt', 'w')
		file.write(str(datetime.datetime.now()))
		file.close()
		
if __name__ == '__main__':
	getnews()
