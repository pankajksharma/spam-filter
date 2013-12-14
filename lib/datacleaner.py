from cleaning import *
class DataClean:
	def __init__(self,text):
		
		words=seperateWords(text)
		words=convertToLower(words) # convert words to lowercase
		words=applyStemming(words)
		words=removeStopWords(words) # remove stop words
		words=removeSmallWords(words)
		self.filtered_words = words

	def remove_freq_one(self):
		t = {}
		for word in self.filtered_words:
			try:
				t[word] += 1
			except:
				t[word] = 1
		self.filtered_words = [w for w in self.filtered_words if t[w] > 1]
		
	def GetData(self):
		self.remove_freq_one()
		return self.filtered_words

