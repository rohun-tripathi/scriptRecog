#!/usr/bin/env python

import netcdf_helpers
from scipy import *
from optparse import OptionParser
from xml.dom.minidom import parse
import sys, time, os

import tamil_extract as TE


#command line options
parser = OptionParser()
(options, args) = parser.parse_args()
if (len(args)<1):
	print "usage: test/train/val/edited"
	sys.exit(2)
function = args [0]
if not function in ["test",  "train", "val", "edited"]:
	print "usage: test/train/val/edited"
	sys.exit(2)

labels =  ["tamil", "hindi"]

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

#later
# inputMeans = array([1054.11664783, 1455.79299719, 0.0196859027344])
# inputStds = array([413.688579765, 643.506710495, 0.138918565959])

#Here begins the module functional call for each of the respective indic scripts

#Tamil data is  TamData
TE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputs, True)

#Later
#inputs = ((array(inputs)-inputMeans)/inputStds).tolist()

#print inputs
# print len(labels), labels
# print labels

#create a new .nc file
ncFilename = "combine" + function + ".nc"
file = netcdf_helpers.NetCDFFile(ncFilename, 'w')

#create the dimensions
netcdf_helpers.createNcDim(file,'numSeqs',len(seqLengths))
netcdf_helpers.createNcDim(file,'numTimesteps',len(inputs))
netcdf_helpers.createNcDim(file,'inputPattSize',len(inputs[0]))
netcdf_helpers.createNcDim(file,'numDims',1)
netcdf_helpers.createNcDim(file,'numLabels',len(labels))

#create the variables
netcdf_helpers.createNcStrings(file,'seqTags',seqTags,('numSeqs','maxSeqTagLength'),'sequence tags')
netcdf_helpers.createNcStrings(file,'labels',labels,('numLabels','maxLabelLength'),'labels')
netcdf_helpers.createNcStrings(file,'targetStrings',targetStrings,('numSeqs','maxTargStringLength'),'target strings')
netcdf_helpers.createNcStrings(file,'wordTargetStrings',wordTargetStrings,('numSeqs','maxWordTargStringLength'),'word target strings')
netcdf_helpers.createNcVar(file,'seqLengths',seqLengths,'i',('numSeqs',),'sequence lengths')
netcdf_helpers.createNcVar(file,'seqDims',seqDims,'i',('numSeqs','numDims'),'sequence dimensions')
netcdf_helpers.createNcVar(file,'inputs',inputs,'f',('numTimesteps','inputPattSize'),'input patterns')

#write the data to disk
print "closing file", ncFilename
file.close()
