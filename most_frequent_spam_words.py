import json

MODEL_DIR = "models/"

data_model = json.load(open(MODEL_DIR+"words.json", 'r'))

sorted_data = sorted(data_model, key=data_model.get)

sorted_data.reverse()

for word in sorted_data[:100]:
	print word, data_model[word]