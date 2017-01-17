import requests
import re
import time
import random
from bs4 import BeautifulSoup

GOOGLE_ACCOUNT_USERNAME = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
GOOGLE_ACCOUNT_PASSWORD = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

USER_AGENTS = [
	'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	'Mozilla/4.61 [en] (X11; U; ) - BrowseX (2.0.0 Windows)',
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en; rv:1.8.1.6) Gecko/20070809 Camino/1.5.1',
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-US) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/3.0.183 Safari/531.0',
	'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19',
	'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20051111 Firefox/1.5 BAVM/1.0.0',
	'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)',
	'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.1.14) Gecko/20080821 Firefox/2.0.0.14',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Meridio for Excel 5.0.251; Meridio for PowerPoint 5.0.251; Meridio for Word 5.0.251; Meridio Protocol; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Business Everywhere 7.1.2; GTB6; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)',
	'Mozilla/1.22 (compatible; MSIE 2.0; Windows 95)',
]

class SessionGoogle:
# REFERENCED :- http://stackoverflow.com/questions/6754709/logging-in-to-google-using-python
	def __init__(self, url_login, url_auth):
		self.ses = requests.session()
		login_html = self.ses.get(url_login)
		soup_login = BeautifulSoup(login_html.content, "lxml").find('form').find_all('input')
		my_dict = {}
		for u in soup_login:
			if u.has_attr('value'):
				my_dict[u['name']] = u['value']
		my_dict['Email'] = GOOGLE_ACCOUNT_USERNAME
		my_dict['Passwd'] = GOOGLE_ACCOUNT_PASSWORD
		headers={"User-agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-US) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/3.0.183 Safari/531.0"}
		self.ses.post(url_auth, data=my_dict, headers=headers)

	def get(self, URL):
		times = [2, 3, 4]
		time.sleep(random.choice(times))
		headers={"User-agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-US) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/3.0.183 Safari/531.0"}
		return self.ses.get(URL, headers=headers).text

def trend(session, topicID):
	target_url = "https://www.google.com/trends/fetchComponent?hl=en-US&q=%s&cid=TIMESERIES_GRAPH_0&export=3"%topicID
	req = session.get(target_url)
	code = req
	question = "(\"v\":)[0-9]+"
	matches = re.finditer(question, code)
	values = []
	for match in matches:
		value = int(match.group(0).split(":")[1])
		values.append(value)
	return(sum(values))

if __name__ == '__main__':
	url_login = "https://accounts.google.com/ServiceLogin"
	url_auth = "https://accounts.google.com/ServiceLoginAuth"
	session = SessionGoogle(url_login, url_auth, GOOGLE_ACCOUNT_USERNAME, GOOGLE_ACCOUNT_PASSWORD)
	print(trend(session, "/m/04gttgp"))
