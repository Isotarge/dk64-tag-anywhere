import os
import subprocess

def compressGZipFile(inputFile, outputFile, byteFlipCompressed):
	if os.path.exists(inputFile):
		with open(inputFile,"rb") as tempInputFile:
			f_end = len(tempInputFile.read())
			tempInputFile.seek(f_end)
			size = f_end
			tempBuffer = []
			for x in range(size + 0x10):
				tempBuffer.append(0)
			tempInputFile.seek(0)
			file_bytes = tempInputFile.read()
			for x in range(len(file_bytes)):
				tempBuffer[x] = file_bytes[x]
			if os.path.exists("tempgh9.bin"):
				os.remove("tempgh9.bin")
			with open("tempgh9.bin","wb") as tempOutputFile:
				compressedSize = size
				if (compressedSize % 0x10) != 0:
					compressedSize = ((compressedSize - (compressedSize % 0x10)) + 0x10)
				bytes_to_write = file_bytes[:compressedSize]
				tempOutputFile.write(bytes_to_write)
			tempBuffer = []
			result = subprocess.check_output(["./build/gzip.exe", "-f", "-q", "-9", "tempgh9.bin"])
			if os.path.exists("tempgh9.bin.gz"):
				with open("tempgh9.bin.gz","rb") as inputFileName:
					sizeNew = len(inputFileName.read())
					inputFileName.seek(0)
					tempBufferNew = []
					for x in range(sizeNew):
						tempBufferNew.append(0)
					new_file_bytes = inputFileName.read()
					for x in range(len(new_file_bytes)):
						tempBufferNew[x] = new_file_bytes[x]
					if os.path.exists(outputFile):
						os.remove(outputFile)
					with open(outputFile, "w+b") as outputFileName:
						start = 0x16
						# DK64-Specific stuff
						start = start - 0xA
						tempBufferNew[start] = 0x1F
						tempBufferNew[start + 1] = 0x8B
						tempBufferNew[start + 2] = 0x08
						tempBufferNew[start + 3] = 0x00
						tempBufferNew[start + 4] = 0x00
						tempBufferNew[start + 5] = 0x00
						tempBufferNew[start + 6] = 0x00
						tempBufferNew[start + 7] = 0x00
						tempBufferNew[start + 8] = 0x02
						tempBufferNew[start + 9] = 0x03
						if byteFlipCompressed:
							if (sizeNew % 2) == 1:
								tempBufferNew[sizeNew - 0x8] = 0
								sizeNew = sizeNew + 1
							for x in range(sizeNew / 2):
								tempSpot = tempBufferNew[x * 2]
								tempBufferNew[x * 2] = tempBufferNew[(x * 2) + 1]
								tempBufferNew[(x * 2) + 1] = tempSpot
						new_bytes_to_write = tempBufferNew[start:(sizeNew - 8)]
						outputFileName.write(bytearray(new_bytes_to_write))
						fileSizeNew = sizeNew-(start + 8)
						if (fileSizeNew & 8) != 0:
							writeBuffer = []
							for x in range(8-(fileSizeNew % 8)):
								writeBuffer.append(0)
							outputFileName.seek(0)
							curr_size = len(outputFileName.read())
							outputFileName.seek(curr_size)
							outputFileName.write(bytearray(writeBuffer))
	if os.path.exists("tempgh9.bin"):
		os.remove("tempgh9.bin")
	if os.path.exists("tempgh9.bin.gz"):
		os.remove("tempgh9.bin.gz")