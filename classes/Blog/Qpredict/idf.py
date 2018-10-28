import math
import operator
input = open('sentences.txt').readlines()

doc_count={}
for line in input:
	tokens = line.lower().replace('\n','').replace(',','').split(' ')
	for key in tokens:
		if key not in doc_count.keys():
			doc_count[key] = 1
		else:
			doc_count[key] = doc_count[key]+1


out_file = open('idf.txt', 'w', encoding="utf-8")

idf={}
for key in doc_count.keys():
	idf_=math.log(len(input)/doc_count[key])
	idf[key]=idf_

sorted_idf= sorted(idf.items(), key=operator.itemgetter(1))	
for item in sorted_idf:
	out_file.write(item[0]+","+str(item[1])+"\n")
out_file.close()
