import os, json
from lib.mysql import connection

MODEL_DIR = "models/"
cursor = connection.cursor()

data_model = json.load(open(MODEL_DIR+"words.json", 'r'))
md_model = json.load(open(MODEL_DIR+"meta.json", 'r'))

query = "SELECT * from `data_mail` limit 3000,1000"
cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
	data = json.loads(row[2])
	meta = json.loads(row[3])
	weight = 0
	for word in data:
		try:
			weight += data_model[word]
		except:
			pass
	for md in meta:
		try:
			weight += 10*md_model[md]
		except:
			pass
	print weight
