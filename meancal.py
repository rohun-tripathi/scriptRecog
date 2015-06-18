#!/usr/bin/env python

import sys, time, os, numpy
from optparse import OptionParser

import tamil_extract as TE

import hindi_extract as HE


def cal(name):
	xterms = []
	yterms = []

	xrang = []
	yrang = []
	pendownterms = []
	iters = 0
	rang = 0


	#Here begins the module functional call for each of the respective indic scripts

	#Tamil data is  TamData
	if name == "tamil":
		TE.meancal(xterms, yterms, xrang, yrang, pendownterms)
	elif name == "hindi":
		HE.meancal(xterms, yterms, xrang, yrang, pendownterms)
	else:
		print "Language out of scope"
		sys.exit(1)

	xmean = numpy.mean(xterms)
	ymean = numpy.mean(yterms)
	pendownmean = numpy.mean(pendownterms)
	#this is because our system is diff from the one created by the example python code

	print "iters = " , len(xterms)
	print "xmean = " , xmean
	print "ymean = " , ymean
	print "pendownmean = " , pendownmean

	print "xvar = " , numpy.sqrt(numpy.var(xterms))
	print "yvar = " , numpy.sqrt(numpy.var(yterms))
	print "penvar = " , numpy.sqrt(numpy.var(pendownterms))


	f1= open("details_test_"+name+".txt", 'w')

	print >> f1, "iters = " , len(xterms)
	print >> f1, "xmean = " , xmean
	print >> f1, "ymean = " , ymean
	print >> f1, "pendownmean = " , pendownmean

	print >> f1, "xvar = " , numpy.sqrt(numpy.var(xterms))
	print >> f1, "yvar = " , numpy.sqrt(numpy.var(yterms))
	print >> f1, "penvar = " , numpy.sqrt(numpy.var(pendownterms))

	#Now calculatin the range average
	#Reusing the variable
	xmean = numpy.mean(xrang)
	ymean = numpy.mean(yrang)

	print "xrang mean = " , xmean
	print "yrang mean = " , ymean
	print >> f1, "xrang mean = " , xmean
	print >> f1, "yrang mean = " , ymean

	#Now calculatin the range max
	#Reusing the variable
	xmean = numpy.amax(xrang)
	ymean = numpy.amax(yrang)

	print "xrang max = " , xmean
	print "yrang max = " , ymean
	print >> f1, "xrang max = " , xmean
	print >> f1, "yrang max = " , ymean

parser = OptionParser()
(options, args) = parser.parse_args()

if (len(args)<1):
	print "usage: hindi/tamil/otherlanguage"
	sys.exit(2)

cal(args [0])