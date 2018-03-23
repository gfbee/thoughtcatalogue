import os
import getopt, sys
import shutil
import hashlib
import pickle
import copy

''' Version 0.8:
	Deletion is now basically coded (although not optimized)

	The code can also unionize and intersect tags as a filtering operation.

	The Addition functions are stable.

	Coded by Sean al-Baroudi (sean.al.baroudi@gmail.com)

'''

helpString = '''Usage of thoughtcat:

thoughtcat -h -v -O [outputFile] -B -t -P [file] -r [tag] -d [hash/tagname] -D [file] - I -U [tags...]
	- h: help.
	- v: version and my info.
	- O: specify output filename.
	- B: output all of the blobs!
	- a: retrieve a list of tags, with their associated hash values.
	- t: output a new line separated list of all tags.
	- p: print all datastructures (diagnostic).
	- P:: takes in a file with blobs and associated tags.
	- r: retrieves every blob associated to a particular tag.
	- d: delete a tag, blob or link.
	- I:: Form the intersection of all textblobs associated to a list of tags.
	- U:: Form the union of all textblobs associated to a list of tags.

Other Notes:
	- if -O not specified, 'output.txt' will be used for the output file name.

'''

versionString = '''

thoughtcat v0.8. Created by Sean al-Baroudi (sean.al.baroudi@gmail.com).
'''

#Our getopt global variables:
outputFile = "./output.txt" #This is used for tag list, and regular output; we can only do one thing at a time, after all.
repoFileLocation = "./repository"

pickleHashTableName = "pickleHash"
pickleTagDictName = "tagdict"
pickleCountDictName = "countdict"

#Our Repository of Tags and text blobs:
textBlobDict = {} #Dictionary of Hash Values -> Strings
tagDict = {}  #Dictionary of Strings -> Lists of Hash Values
countDict ={} #Used to keep track of orphened Blobs; if Tag list is empty, it is considered an orphan as well.

'''
Purpose: Process our command line arguments, and execute properly.
'''
def processargs():
	global outputFile
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvBatpP:r:d:O:IU")
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	for o, a in opts:
		if o == "-h":  #Done
			print(helpString)
			sys.exit(2)
			break
		elif o == "-v":
			print(versionString)
			break
		elif (o == "-O" and  a != ""):
			outputFile = a
		elif o == "-B":
			printalltextblobs()
			break
		elif o == "-a":
			writetaglists()
			break
		elif o == "-t":
			writetagstofile()
			break
		elif o == "-p":
			printstructures()
			break
		elif (o == "-P" and  a != ""):
			pump(a)
			break
		elif (o == "-r" and  a != ""):
			retrievesingletag(a)
			break
		elif (o == "-d" and  a != ""):
			removesingleitem(a)
			break
		elif (o == "-I"):
			intersecttags(args)
			break
		elif (o == "-U"):
			uniontags(args)
		else:
			print("ERROR: An unrecognized option or format has appeared. Please check your argument string.")
			sys.exit(2)

'''
Signature: List -> Void
Purpose: Given a list of tags, just take the union and pump out to an output file.
'''
def uniontags(argList):
	if(len(argList) < 2):
		print("Error:: UnionTags: arg list needs at least two tags:")
		sys.exit(2)

	for tag in argList:
		if (tag not in tagDict):
			print("Error: UniontTags: Tag:" + tag + "is not in tagDict. Aborting operation.")
			sys.exit(2)
		if (len(tagDict[tag]) == 0):
			print("Error: UniontTags: Tag:" + tag + "has zero length list associated with it. Aborting operation.")
			sys.exit(2)
	#Unionize
	unionList = []
	for tag in argList:
		for hashVal in tagDict[tag]:
			if (hashVal not in unionList): #keeps items unique.
				unionList.append(hashVal)
	writeoplist(argList, unionList)

'''
Signature: Iterable Iterable -> List
Purpose: Given two iterables, return a list of all values [with repetition] of the first iterable that occur
          at least once in the second iterable.
'''
def intersect(iterable1, iterable2):
	return [e for e in iterable1 if e in iterable2]
        # return list(set(iterable1).intersection(iterable2))
	# That wouldn't include duplicates in iterable1.
	# Consider not converting to lists, using sets where duplicates aren't expected anyway.

'''
Signature: List List -> Void
Purpose: write our list to output file. Used with our set operations on tags.
'''
def  writeoplist(argList, gatherList):
	intFile = open("./" + outputFile, "w") #start fresh.

	tagString = ""
	for tag in argList:
		tagString = tagString + tag + ":"
	intFile.write(tagString + ":: \n")

	for hashVal in gatherList:
		intFile.write(textBlobDict[hashVal] + "\n")
	intFile.close()

'''
Signature: List[String] -> Void
Purpose: Given a List of Tags, we intesect the tag hash lists and return an output file.
'''
def intersecttags(argList):
	if(len(argList) < 2):
		print("Error:: IntersectTags: arg list needs at least two tags:")
		sys.exit(2)

	for tag in argList:
		if (tag not in tagDict):
			print("Error: IntersectTags: Tag:" + tag + "is not in tagDict. Aborting operation.")
			sys.exit(2)
		if (len(tagDict[tag]) == 0):
			print("Error: IntersectTags: Tag:" + tag + "has zero length list associated with it. Aborting operation.")
			sys.exit(2)
	#Now we start.
	gatherList = intersect(tagDict[argList[0]],tagDict[argList[1]])
	for nextTag in argList[2:]:
		gatherList = intersect(gatherList, tagDict[nextTag])
	writeoplist(argList, gatherList)

'''
Signature: String String -> void
Purpose: Simply excise a hash value from our tagDict list.
Note: I don't delete empty tags; they might be useful later.
'''
def removehash(hKey, tag):
	global tagDict
	if (hKey in tagDict[tag]):
		hList = tagDict[tag]
		hList.remove(hKey)
		tagDict[tag] = hList
	else:
		print("Warning: RemoveHash: hkey not in tag list at all; no action taken.")

'''
Signature: String String String -> Void
Purpose: This is our main synchronized method to prune links in our repo.
'''
def removelink(hKey, tag):
	global textBlobDict, tagDict, countDict

	#Check state.
	hEx = (hKey in textBlobDict)
	tEx = (tag in tagDict)
	if (hKey in countDict):
		keyCount = countDict[hKey]
	else:
		if (hEx):
			print("WARNING: RemoveLink: hash key in countDict but not textBlobDict; Repo corrupted.")
		else:
			print("RemoveLink: hash key not in text or count Dict; no alteration made")


	if (hEx and tEx):
		if (keyCount  >1):
			print("RemoveLink: count greater than 1.")
			countDict[hKey] = countDict[hKey] - 1
			removehash(hKey,tag)
		elif(keyCount == 1):
			print("RemoveLink: count is  1.")
			holdDrop = countDict.pop(hKey)
			holdDrop = textBlobDict.pop(hKey)
			removehash(hKey, tag)
		elif(keyCount == 0):
			print("Warning: RemoveLink: keyCount already zero.")
		else:
			print("Warning: RemoveLink: keyCount has negative value; Repo Corrupted.")
	elif ((not hEx) and tEx): #we have an potential orphan.
		removehash(hKey,tag)
		print("RemoveLink: Tag found, but no hKey for Blob. Orphan Case")
	elif (hEx and (not tEx)): #other things might point to it, or blob just not connectd to tag in the first place.
		print("RemoveLink: hash pressent, but tag is not.")
	elif ((not hEx) and (not tEx)):
		print("RemoveLink: No tag or hash key exists. No alteration made.")

'''
Signature: String -> void
Purpose: Obv.
Note: If you try to alter the list you are looping on (with a function call), you will get
strange results. This is why a deep copy is made.
'''
def removeonetag(aTag):
	if(aTag in tagDict):
		holdList = copy.deepcopy(tagDict[aTag])
		for hashStr in holdList:
				removelink(hashStr, aTag)
	else:
		print("RemoveOneTag: tag not found.")

'''
Signature: String[hash] -> void
Purpose: Obv. We remove blob from countDict and textBlob dict
We don't worry about the tagDict having undefined links; these are
dealt with during access of tags. This avoids an O(mn) time Repo search.

'''
#we don't default to the remove link, as we want to avoid an O(mn) tagDict search; we deal with missing links during the
##access request of the code.
def removeoneblob(hshstr):
	global textBlobDict, countDict
	if (hshstr in textBlobDict):
		holdDump = textBlobDict.pop(hshstr) #these return values, so I will catch them but not use them.
		holdDump = countDict.pop(hshstr)
	else:
		print("RemoveOneBlob: The blob to be removed did not exist.")

'''
Signature: String -> Void
Purpose: Determine if we have a tag, hash or link and delete accordingly
Note: An "item" is any one of: tag, hash or link itself.

'''
def removesingleitem(arg):
	if(arg.startswith("Tag:")):
		removeonetag(arg.replace("Tag:",""))
	elif(arg.startswith("Blob:")):
		removeoneblob(arg.replace("Blob:", "")) #we check if hash exists inside this function [***]
	elif(arg.startswith("Link::")):
		argPart = arg.replace("Link::", "")
		argList = argPart.split(":")
		removelink(argList[0],argList[1]) #must check if hash exists on its own [***]
	else:
		print("Error: Input for -d option not recognized.")

'''
Signature: String -> Void (output file)
Purpose: We take a single tag, search for every hash value associated with it, and retrieve the blobs.
'''
def retrievesingletag(tag):
	if(tag not in tagDict):
		print("Error: Tag not found. Check spelling?")
	else:
		blobFile = open("./" + outputFile, "w")
		blobFile.write("Tag:" + tag + "\n")
		for hkey in tagDict[tag]:
			blobFile.write(textBlobDict[hkey] + "\n")
		blobFile.close()

'''
Purpose: Obv.
'''
def printalltextblobs():
	blobOut = open("./" + outputFile, "w")
	for hkey in list(textBlobDict.keys()):
		blobOut.write(hkey + "::" + "\n" + "------\n" + textBlobDict[hkey])
		blobOut.write("\n")
	blobOut.close()

'''
Signature: String -> Void
Purpose: Wrapper function to minimize code reusage.

'''
def writerepo():
	writedicttofile(repoFileLocation + "/" + pickleHashTableName ,textBlobDict)
	writedicttofile(repoFileLocation + "/" + pickleTagDictName, tagDict)
	writedicttofile(repoFileLocation + "/" + pickleCountDictName, countDict)

'''
Signature: String -> Void
Purpose: This Pickles one dictionary structure at a time; path and name as arguments
'''
def writedicttofile(apath, theDict):
	#Note: we don't need to check if file exists: 'w' mode will truncate and overwrite anyways.
	newPickleFile = open(apath, "wb")
	pickle.dump(theDict, newPickleFile)
	newPickleFile.close()

'''
Signature: String -> Void
Purpose: Recover Repo datastructures from pickled storage files.
'''

def loadrepo():
	global textBlobDict,tagDict,countDict

	pickleFile = open(repoFileLocation + "/" + pickleHashTableName, "rb")
	textBlobDict = pickle.load(pickleFile)
	pickleFile.close()

	pickleFile = open(repoFileLocation + "/" + pickleTagDictName, "rb") #binary mode needed for pickle to work!
	tagDict = pickle.load(pickleFile)
	pickleFile.close()

	pickleFile = open(repoFileLocation + "/" + pickleCountDictName, "rb") #binary mode needed for pickle to work!
	countDict = pickle.load(pickleFile)
	pickleFile.close()

'''
Signature: String -> Void
Purpose: We open the input File, parse it, and add valid entries to our global dictionary and hash table.
Note: I have a try/catch here but not with other file code because the other cases don't involve user error.
'''
def pump(inputPath):
	currBlob = ""
	currTagLine = ""
	inputFile = ""

	try:
		inputFile = open(inputPath,"r")
	except IOError as e:
		print('Input file not opened. Error: %s' % e)

	#Lets define our token "States" here
	openQuote = "OQ"
	textBody = "TB"
	tagLine="TL"
	newLine="NL"

	lSTup = (openQuote, "") #doesnt matter that 2nd element is empty when we step into the loop

	for line in inputFile: #remove hardcoding [***]
		s = lSTup[0]
		if (s == openQuote and line =="\'\'\'\n"):
			lSTup = (textBody, line)
		elif (s == textBody):
			if (line == "\'\'\'\'\n"):
				lSTup = (tagLine, line)
			elif (line != ""): #Build blob.
				lSTup = (textBody, line)
				currBlob = currBlob + line
		elif (s == tagLine and (":" in line)): #split the tag line
			lSTup = (newLine, line)
			currTagLine = (line.replace("\n","")).split(":")  #need to dump the newLine character at the end [***]
		elif (s == newLine and (line == "\n")): #Commit the new tags and blob.
			lSTup = (openQuote, line)
			addtostorage(currBlob,currTagLine)
			currBlob = ""
			currTagLine = "" #reset.
		else:
			print("Parse Error: Improper formatting on following line: " + line)
			sys.exit(2)
	return

'''
Signature: String -> String
Purpose: Get an MD5 hash value for a string

'''
def getstringhash(tBlob):
	hashObj = hashlib.md5(tBlob.encode())
	return hashObj.hexdigest()

'''
Signature: String List -> Void
Purpose: Given a textBlob and Tags, add to our Hash Table and Dictionary of Lists.
'''
def addtostorage(textBlob, tagList):
	newHash = getstringhash(textBlob)
	for tag in tagList:
		addlink(newHash,textBlob,tag)

'''
Signature: String[Hash] String  String -> Void
Purpose: This is the synchronized add function for the entire script.

'''
def addlink(hKey, tBlob, tag):
	global textBlobDict, tagDict, countDict

	#Check state.
	hEx = (hKey in textBlobDict)
	tEx = (tag in tagDict)

	if(hEx and tEx):
		if(hKey not in tagDict[tag]): #both objects exist, but blob is not in tag list.
			tagDict[tag].append(hKey)
			countDict[hKey] = countDict[hKey] + 1
			print("AddLink: Both hash and tag exist, but hash not in tag list; adding.")
		else:
			print("AddLink: Tag and Blob already in Repo. Redundant Link not added.")
	elif((not hEx) and tEx): #this case occurs if we have a new blog, with its first relational tag already in the database
		print("AddLink: Blob not present, but tag exists.")
		textBlobDict[hKey] = tBlob
		countDict[hKey] = 1
		tagDict[tag].append(hKey)
	if(hEx and (not tEx)):
		print("AddLink: Tag not present, but blob is. ")
		tagDict[tag] = [hKey]
		countDict[hKey] = countDict[hKey] + 1
	if(hEx == False and tEx == False):
		print('AddLink: Adding. ' + 'Tag:' + tag + " tBlob:" + tBlob[:15])
		textBlobDict[hKey] = tBlob
		countDict[hKey] = 1
		tagDict[tag] = [hKey]

def writetagstofile():
	tagFile = open( "./" + outputFile, "w") #start fresh.
	for tag in  list(tagDict.keys()):
			tagFile.write(tag + "\n")

'''
Purpose: Obvious.
'''
def writetaglists():
	tagFile = open("./" + outputFile, "w") #start fresh.
	for tag in  list(tagDict.keys()):
		tagFile.write(tag + ":: \n")
		for item in tagDict[tag]:
			tagFile.write("\t\t" + item + "\n")
	tagFile.close()

'''
Signature: Void -> String
Purpose: Use this to quickly see the state of both structures at a glance. Use for debugging.
'''
def printstructures():
	print(textBlobDict)
	print("\n")
	print(tagDict)
	print("\n")
	print(countDict)

'''
Purpose: Specifically, we attempt to load the Repository. If it doesn't load, we warn the user
and start fresh.
'''
def initialize():
	#load the repo using the pickle methods.
	tPath = repoFileLocation + "/"
	tempPath1 =  tPath + pickleHashTableName
	tempPath2 = tPath + pickleTagDictName
	tempPath3 = tPath  + pickleCountDictName

	if (os.path.isfile(tempPath1) and os.path.isfile(tempPath2) and os.path.isfile(tempPath3)):
		loadrepo()
	else:
		print("WARNING: Repository files not found. Starting fresh with EMPTY datastructures.")

'''
Purpose: Obvious
'''
def main():
	initialize()
	processargs()
	writerepo()

if __name__ == "__main__":
	main()
