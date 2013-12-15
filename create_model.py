import os, json
from lib.mysql import connection

MODEL_DIR = "models/"

cursor = connection.cursor()
query = "SELECT * from `data_mail` limit 2000"

cursor.execute(query)
rows = cursor.fetchall()

data_model = {}
md_model = {}

for row in rows:
	print row[1]
	data = json.loads(row[2])
	meta = json.loads(row[3])
	for word in data:
		try:
			data_model[word] += 1
		except:
			data_model[word] = 1
	for md in meta:
		try:
			md_model[md] += 1
		except:
			md_model[md] = 1

f = open(MODEL_DIR+"words.json", 'w')
json.dump(data_model, f)
f.close()

f = open(MODEL_DIR+"meta.json", 'w')
json.dump(md_model, f)
f.close()
