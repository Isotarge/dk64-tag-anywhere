import os
import subprocess

def compressGZipFile(inputFile):
	if os.path.exists(inputFile):
		result = subprocess.check_output(["./build/gzip.exe", "-f", "-n", "-q", "-9", inputFile])
		if os.path.exists(inputFile + ".gz"):
			with open(inputFile + ".gz","r+b") as outputFile:
				# Chop off footer
				outputFile.truncate(len(outputFile.read()) - 8)