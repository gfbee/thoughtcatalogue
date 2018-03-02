import sys

print("Attempting to print")
fileP = open("newfile", "w")
fileP.write("Does this work?")
fileP.write("Are we sure?")
fileP.close()
