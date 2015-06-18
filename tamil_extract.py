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

def meancal(xterms, yterms, xrang, yrang, pendownterms, debug = False):
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

		for k in d:
			t = pathtemp + k + "/"

			if debug == True: print t
			
			# print t
			# using t for the new directory
			f = []
			for (dirpath, dirnames,filenames) in walk(t):	
				f.extend(filenames)
				break#only one iteraion cause all lines are same in the ascii
			
			for index, onefile in enumerate(f):				
				if debug == True: print onefile
				
				firstlinechk = 0 			# To make sure that the lines of code before the data lines are avoided when necessary
				thirdval = 0.0
				
				ymin = 5000
				xmin = 5000
				xmax = 0
				ymax = 0
				
				k = open(t + onefile).readlines()
				for line in k:
					line = line.strip()
					coor = line.split()
					if len(coor) == 0: continue
					
					if firstlinechk == 0 and line != ".PEN_DOWN":		#Skip these lines as they donot have needed info
						continue
					elif line == ".PEN_DOWN":
						firstlinechk = 1 			#Nolonger the firstlines part, now all the information is relevant
						thirdval = 1.0 				#Stores the value for the third column of the first point in the stroke to signify "PENDOWN"
					elif line == ".PEN_UP":
						continue
					else:
						xterms.append(float(coor[0]))
						yterms.append(float(coor[1]))	
						pendownterms.append(thirdval)

						if xmax < float(coor[0]): xmax = float(coor[0])
						if xmin > float(coor[0]): xmin = float(coor[0])

						if ymax < float(coor[1]): ymax = float(coor[1])
						if ymin > float(coor[1]): ymin = float(coor[1])

						thirdval = 0.0
				
				xrang.append( xmax - xmin )
				yrang.append( ymax - ymin )
			
			