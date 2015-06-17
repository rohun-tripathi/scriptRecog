import sys, time, os
from os import walk

def unnecessaryfunc(d, function):
	if function == "train":
		return 1, len(d)
	elif function == "test":
		return 0,1

def main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputs, debug = False):
	print "Starting work in TamData"
	time.sleep(2)
	
	path = "/home/riot/Videos/scriptrecog/TamData/"

	topdir = []
	for (dirpath, dirnames, filenames) in walk(path):
		topdir.extend(dirnames)
		break
	if debug == True: print "topdir = \n", topdir

	#Now for inside each folder

	#For now I have two sets. The first-> function = train and second function  = test. Later we can add more for val and so on
	for folder in topdir:
		pathtemp = path + str(folder) + "/"
		d = []
		for (dirpath, dirnames, filenames) in walk(pathtemp):
			d.extend(dirnames)
			break
		if debug == True: print d
		start,end = unnecessaryfunc(d,function)

		for k in d[start:end]:
			t = pathtemp + k + "/"

			if debug == True: print t
			
			# print t
			# using t for the new directory
			f = []
			for (dirpath, dirnames,filenames) in walk(t):	
				f.extend(filenames)
				break#only one iteraion cause all lines are same in the ascii
			
			for index, onefile in enumerate(f):
				seqTags.append(onefile)#appending to seqtags
				print onefile

				names = onefile.split("t")
				
				# Same for now
				word = "tamil"
				wordmod = "tamil"


				#they are appended here as they have to be done for each stroke file
				wordTargetStrings.append(word)
				targetStrings.append(wordmod)
				
				firstlinechk = 0;
				#to make the first points have output 1.0 instead of 0.0
				oldlen = len(inputs)
				thirdval = 0.0
				for line in file(t + onefile).readlines():
					line= line.strip()
					if firstlinechk == 0 and line != ".PEN_DOWN":
						continue
					elif line == ".PEN_DOWN":
						firstlinechk = 1
						thirdval = 1.0
					elif line == ".PEN_UP":
						continue
					else:
						coor = line.split();

						inputs.append([float(coor[0]), float(coor[1]), thirdval])
						thirdval = 0.0
					
				# print "Input = " , inputs, "\n\n\n\n"
				
				seqLengths.append(len(inputs) - oldlen)
				seqDims.append([seqLengths[-1]])
				if debug == True: print "Sequence lengths ", [seqLengths[-1]], "\n"
				##and this is the point it shud stop inside the folder

				##here the loop for the respective folder shud stop
				




				############################
				if index == 1:
					break
				#This to reduce the size of the file ryt now for easy check out