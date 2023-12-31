#! /bin/python
import os
import time
import unicodedata

# Modified 5:07PM


def searchFiles(rootDirectory, modifyDateLimit, excludedFiles):
    # iterate through all top level folders seperately

    for dir in os.listdir(rootDirectory):
        # get path for next level and make sure path is a directory (not a file)
        fileFound = False
        foundFilePath = ""
        foundFileModifiedDate = ""

        dirPath = os.path.join(rootDirectory, dir)

        if not os.path.isdir(dirPath):
            continue

        # traverse all branches of the path using os.walk
        for root, dirs, files in os.walk(dirPath, topdown=True, followlinks=False):
            # fileFound = False
            # foundFilePath = ""
            # foundFileModifiedDate = ""

            for name in files:
                filePath = os.path.join(root, name)

                if not os.path.isfile(filePath):
                    continue

                if name in excludedFiles:
                    continue

                # get the time the file was modified in seconds (float)
                modifyTime = os.path.getmtime(filePath)

                # convert modifyTime and modifyDate to time.struct_time object
                # in order to compare them

                modifyDateTime = time.localtime(modifyTime)

                # set fileFound to true and break if a file is found to be
                # modified after the given modify date

                if modifyDateTime > modifyDateLimit:
                    fileFound = True
                    foundFilePath = filePath
                    foundFileModifiedDate = modifyDateTime
                    # Break out of file loop
                    break

            if fileFound:
                # Since we found a file that was modified after the given
                # modify date, we can break out of the os.walk loop
                break

            # print the name of the top level folder
            # if previous break statement was triggered

        if fileFound:
            print(
                unicodedata.normalize("NFC", dirPath),
                " ",
                unicodedata.normalize("NFC", foundFilePath),
                " ",
                time.strftime("%m/%d/%Y", foundFileModifiedDate),
            )

            with open(outputFile, "a") as f:
                f.write(
                    '"'
                    + unicodedata.normalize("NFC", dirPath)
                    + '","'
                    + time.strftime("%m/%d/%Y", foundFileModifiedDate)
                    + '","'
                    + unicodedata.normalize("NFC", foundFilePath)
                    + '"\n'
                )

        else:
            print(
                unicodedata.normalize("NFC", dirPath),
                " - no modification found after ",
                time.strftime("%m/%d/%Y", modifyDateLimit),
            )

            with open(outputFile, "a", encoding="utf8") as f:
                f.write(
                    '"'
                    + unicodedata.normalize("NFC", dirPath)
                    + '","No modification found",\n'
                )


dateLimit = "01/01/2016"
modifyDateLimit = time.strptime(dateLimit, "%m/%d/%Y")

excludedFiles = [
    "Thumbs.db",
    "desktop.ini",
    "Icon\r",
    "$RECYCLE.BIN",
    "System Volume Information",
    ".DS_Store",
]

# take user input for the root directory and output file name

directory = input("Input root directory to parse:\n")
outputFile = input("Input output file name:\n")


# write header to output file
with open(outputFile, "w", encoding="utf8") as f:
    f.write("Folder Name,Last Modified,File\n")

try:
    searchFiles(directory, modifyDateLimit, excludedFiles)

except OSError as e:
    print(f"Error: {e}")
