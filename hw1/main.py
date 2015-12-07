__author__ = 'mikhail'
alphFile = open('letters_IPA.csv','r', encoding='UTF-8')

letterIpa = {}

for line in alphFile:
    line = line.split('\t')
    #print(line[0],line[3])
    letterIpa[line[0]] = line[3]

alphFile.close()

inFile = open('infile.txt','r',encoding = 'UTF-8')
outFile = open('outfile.txt','w',encoding = 'UTF-8')

for line in inFile:
    for letter in line:
        if letter in letterIpa:
            outFile.write(letterIpa[letter])
        else:
            outFile.write(letter)


inFile.close()
outFile.close()
