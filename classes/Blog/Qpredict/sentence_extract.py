input = open('wikipedia-first.txt').readlines()
output = open('sentences.txt','w')
lc = 0
for line in input:
	if lc % 3 == 1:
		print(line.replace('\n',''))
		output.write(line)
	lc = lc + 1
