
'''For our first test, we will write a script to do the following:

1) Open a file with some text strings
2) Read every line of the file (using itertools)
3) pass each element though a hash function.
4) Set up a dictionary with hash <--.> String pairs
5) Pickle the dictionary we saved to a file.
6) Unpickle the dictionary, and print it back to console (formatting differences)?

'''

import pickle
import hashlib


#Create a dictionary:
strDict = {}

sampleFile = open('./testfile.txt','r')


for line in sampleFile:
	if (line != "\n"):
		strDict[str(hash(line))] = line
	

sampleFile.close()

for hsh in list(strDict.keys()):
	print(hsh +  "::" + strDict[hsh]) 

#Now lets pickle for the winter...
outputFile = open ('pickletest','wb')

print(type(strDict))
pickle.dump(strDict, outputFile)

outputFile.close()

#Now lets import the file back:

pickleFile = open('pickletest', 'rb')

ourData = pickle.load(pickleFile)

#This shows that we get a dictionary: unpickling is a perfectly invertable operation
print(type(ourData))

print(ourData)

