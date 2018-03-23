import sys

print("Attempting to print")
with open("newfile", "w") as fileP:
    fileP.write("Does this work?")
    fileP.write("Are we sure?")
