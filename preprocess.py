import os, json, email, MySQLdb, re
from urlparse import urlparse
from lib.mysql import connection
from lib.datacleaner import DataClean

CWD = os.getcwd()
DATA_DIR = CWD+"/data/"
UNWANTED_CHARS = [',', '.', '!', '(', ')', '?', '\n']
EMAIL_CHECK_TYPES = ['from', 'reply-to', 'return-path']

cursor = connection.cursor()

def get_files(data_dir):
	files = []
	for year in os.listdir(data_dir):
		for month in os.listdir(data_dir+year):
			files += [ data_dir+year+"/"+month+"/"+f for f in os.listdir(data_dir+year+"/"+month)]
	return files

def get_domain(url):
	urlp = urlparse(url)
	return urlp.netloc

def get_ips(text):
	return re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)

def get_email(text):
	return re.findall(r'[\w|\.]+@[\w|\.]+', text)[0]

all_files = get_files(DATA_DIR)
for file in all_files:
	print file
	f = open(file, 'r')
	body = ''
	meta_data = []
	msg = email.message_from_string(f.read().lower())
	if msg.is_multipart():
	    for payload in msg.get_payload():
	    	for p in payload.get_payload():
	        	body += p.get_payload()
	else:
	    body = msg.get_payload()
	try:
		for url in re.findall(r'[a-zA-Z]+://[^\s<>"]+|www\.[^\s<>"]+', body):
			meta_data.append(get_domain(url))
		print re.replace(r'<[/]?[^>]+>', '', body)
	except:
		pass
	for typ in EMAIL_CHECK_TYPES:
		if msg[typ]:
			mail = get_email(msg[typ])
			if mail not in meta_data:
				meta_data.append(mail)

	recv_info = str(msg.get_all('received'))
	meta_data += get_ips(recv_info)
	print meta_data

	for char in UNWANTED_CHARS:
		body.replace(char, '')
	body = DataClean(body).GetData()
	query = "INSERT INTO `data_mail` (`path`,`data`, `meta-data`) VALUES ('%s','%s','%s')" %(file, json.dumps(body).replace('\'', '\\\''), json.dumps(meta_data).replace('\'', '\\\''))
	cursor.execute(query)
	connection.commit()
