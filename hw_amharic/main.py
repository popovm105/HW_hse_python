__author__ = 'mikhail'

toIPAFile = open('alp.csv', 'r',encoding = 'UTF-8')
lines = toIPAFile.readlines()

# vowels = lines[0][0:].strip('\n').split('\t')
consonants = []
for i in range(len(lines)):
    consonants.append(lines[i][0])

letterToSyllable = {}
counter = 1
for line in lines[1:]:
    line = line.split()
    for i in range(1,len(line)):
        letterToSyllable[line[i]] = line[0] + consonants[i]



toIPAFile.close()

inFile = open('infile.txt','r',encoding = 'UTF-8')
outFile = open('outfile.txt','w', encoding = 'UTF-8')

for line in inFile:
    for symbol in line:
        if symbol in letterToSyllable:
            outFile.write(letterToSyllable[symbol])
        else:
            outFile.write(symbol)

inFile.close()
outFile.close()


