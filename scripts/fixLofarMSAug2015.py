#!/usr/bin/python
#
# Script to add missing tables in the MS to conform with CASA standards and 
# to make a fix in the MeasInfo in the spectral window table.
#
# Explanation by Jan David Mol:
# 
# The LOFAR Measurement Set is written in a manner inconsistent with the 
# MS definition v2.
# Two additional tables (STATE,PROCESSOR) need to be added because since 
# release 2.0 a check is done by CASA causing a failure.
#
# Explanation by Ger van Diepen:
# 
# The TableMesRefDesc problem is caused by a change in the coordinates 
# by NRAO some time ago; a type Undefined has been added.
# Basically it means that an MS produced with a newer casacore 
# is not readable by old CASA. I must confess I'm not exactly sure 
# in which casacore release it was introduced. 
# Later I've changed casacore such that it did not stumble anymore on 
# this issue, so the upcoming CASA release should be fine. 
# The CASA group had never merged back my change into their (old) casacore 
# repository used for the previous CASA release.
#
# Authors: A.P. Schoenmakers, M. Iacobelli
#
# Date: Aug 25, 2015
#

import os,sys
import pyrap.tables as pt

if (len(sys.argv) <= 1):
  print "This script will add a line in the STATE and PROCESSOR tables, fix an issue" 
  print "in the SPECTRAL_WINDOW table that causes backward incompatibility with"
  print "Casacore versions <2 ."
  print "To use it, please provide an MS name"
  exit(0)

msin=sys.argv[1]
msin_state=msin+"/STATE"
t_state=pt.table(msin_state,ack=False);
if t_state.nrows() == 0:
  try:
    pt.taql('insert into '+str(msin)+'/STATE set SIG=True, REF=False, CAL=0, LOAD=0, SUB_SCAN=0, OBS_MODE="", FLAG_ROW=False')
    print "Added a row in the empty STATE table"
  except:
    print "Error in adding a row in the empty STATE table"
    exit(1)

msin_proc=msin+"/PROCESSOR"
t_proc=pt.table(msin_proc,ack=False);
if t_proc.nrows() == 0:
  try:
    pt.taql('insert into '+str(msin)+'/PROCESSOR set TYPE="CORRELATOR", SUB_TYPE="LOFAR-COBALT", TYPE_ID=-1, MODE_ID=-1, FLAG_ROW=False')
    print "Added a row in the empty PROCESSOR table"
  except:
    print "Error in adding a row in the empty PROCESSOR table"
    exit(1)

msin_spw=msin+"/SPECTRAL_WINDOW"
try:
   t=pt.table(msin_spw, readonly=False,ack=False)
except:
   print "Cannot find or open",msin_spw
   exit(1)

for colnm in ['CHAN_FREQ','REF_FREQUENCY']:
  tc=t.col(colnm)
  meas=tc.getkeyword('MEASINFO')
  tc.putkeyword('MEASINFO-sav', meas) #save the original keywords
  TabRefTypes_indx=[] ; TabRefCodes_indx=[]
  for indx in range(len(meas)):
    if meas.items()[indx][0] == 'TabRefTypes': TabRefTypes_indx.append(indx)
    if meas.items()[indx][0] == 'TabRefCodes': TabRefCodes_indx.append(indx)
  if len(TabRefTypes_indx) != 0: meas.__delitem__('TabRefTypes') ; print 'Column %s: Deleted TabRefTypes' % colnm
  if len(TabRefCodes_indx) != 0: meas.__delitem__('TabRefCodes') ; print 'Column %s: Deleted TabRefCodes' % colnm
  tc.putkeyword('MEASINFO', meas)

try:
  t.flush() 
  t.close()
except:
  print "Failed to update", msin
  exit(1)

if len(TabRefTypes_indx) != 0 or len(TabRefCodes_indx) != 0:
  print "Done fixing",msin
else:
  print "None fixing",msin
