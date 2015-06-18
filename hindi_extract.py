import sys, time, os
from os import walk

def unnecessaryfunc(d, function):		#Separation of files for the train/test/val so on
	if function == "train":
		return 0,90
	elif function == "test":
		return 90,110

def main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputs, debug = False):
	print "Starting work in HinData"
	time.sleep(2)

	path = "/home/riot/Videos/scriptrecog/HinData/"
	topdir = []
	for (dirpath, dirnames, filenames) in walk(path):
		topdir.extend(dirnames)
		break
	if debug == True: print "Topdir = \n", topdir

	#For now I have two sets. The first-> function = train and second function  = test. Later we can add more for val and so on
	start,end = unnecessaryfunc(topdir,function)

	for k in topdir[start:end]:
		#print "Directory == ", k
		pathname = path.rstrip("/") + "/" + k + "/"
		
		f = []
		for (dirpath, dirnames,filenames) in walk(pathname):	
			f.extend(filenames)
			break#only one iteraion cause all lines are same

		for index, onefile in enumerate(f):				#Running for each data file
				
			if ".txt" in onefile: continue
			
			seqTags.append(onefile)#appending to seqtags
			if debug == True: print onefile
			
			# Same for now
			word = "hindi"
			wordmod = "hindi"
			#they are appended here as they have to be done for each stroke file
			wordTargetStrings.append(word)
			targetStrings.append(wordmod)

			firstlinechk = 0 			# To make sure that the lines of code before the data lines are avoided when necessary
			oldlen = len(inputs)
			thirdval = 0.0

			k = open(pathname + onefile).readlines()
			for line in k:
				line = line.strip()
				parts = line.split()
				if len(parts) == 0: continue
				
				if firstlinechk == 0 and line != ".PEN_DOWN":		#Skip these lines as they donot have needed info
					continue
				elif line == ".PEN_DOWN":
					firstlinechk = 1 			#Nolonger the firstlines part, now all the information is relevant
					thirdval = 1.0 				#Stores the value for the third column of the first point in the stroke to signify "PENDOWN"
				elif line == ".PEN_UP":
					continue
				else:
					coor = line.split();
					inputs.append([float(coor[0]), float(coor[1]), thirdval])	#append the point to the others of this stroke
					thirdval = 0.0

			seqLengths.append(len(inputs) - oldlen)
			seqDims.append([seqLengths[-1]])
			if debug == True: print "Sequence lengths ", [seqLengths[-1]], "\n"
			##and this is the point it shud stop inside the folder

			##here the loop for the respective folder shud stop

def meancal(xterms, yterms, xrang, yrang, pendownterms, debug = False):
	if debug == True: print "Starting work in HinData"

	path = "/home/riot/Videos/scriptrecog/HinData/"
	topdir = []
	for (dirpath, dirnames, filenames) in walk(path):
		topdir.extend(dirnames)
		break
	if debug == True: print "Topdir = \n", topdir

	
	for k in topdir:
		if debug == True: print "Directory == ", k
		pathname = path.rstrip("/") + "/" + k + "/"
		
		f = []
		for (dirpath, dirnames,filenames) in walk(pathname):	
			f.extend(filenames)
			break#only one iteraion cause all lines are same
		for index, onefile in enumerate(f):				#Running for each data file
				
			if ".txt" in onefile: continue
			#if debug == True: print onefile
			
			firstlinechk = 0 			# To make sure that the lines of code before the data lines are avoided when necessary
			thirdval = 0.0
			
			ymin = 5000
			xmin = 5000
			xmax = 0
			ymax = 0
			
			k = open(pathname + onefile).readlines()
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
		
		