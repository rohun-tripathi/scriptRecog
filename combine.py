#!/usr/bin/env python

import netcdf_helpers
from scipy import *
from optparse import OptionParser
from xml.dom.minidom import parse
import sys, time, os

import tamil_extract as TE

import hindi_extract as HE

#command line options
parser = OptionParser()
(options, args) = parser.parse_args()
if (len(args)<1):
	print "usage: test/train/val"
	sys.exit(2)
function = args [0]
if not function in ["test",  "train", "val"]:
	print "usage: test/train/val"
	sys.exit(2)

labels =  ["tamil", "hindi"]

seqDims = []
seqLengths = []
targetStrings = []
wordTargetStrings = []
seqTags = []
inputs = []

#Here begins the module functional call for each of the respective indic scripts

#Tamil data is  TamData
inputtamil = []
TE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputtamil, True)

inputMeans = array([3128.0719366, 978.47630676, 0.0165447506061])
inputStds = array([1647.70825592, 247.932763513, 0.127557915604])
inputtamil = ((array(inputtamil)-inputMeans)/inputStds).tolist()
inputs.extend(inputtamil)

inputhindi = []
HE.main(function, labels, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputhindi, True)

inputMeans = array([3464.31656682, 5373.91794672, 0.0315004541232])
inputStds = array([2047.47960179, 2844.88270614, 0.174665896827])
inputhindi = ((array(inputhindi)-inputMeans)/inputStds).tolist()
inputs.extend(inputhindi)

# print inputs
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
