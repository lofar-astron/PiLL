#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 - Alexander Drabent
#

def main(MSlist,MSconcat):

    """

  
    Parameters
    ----------
    MSlist : str
        A list of measurement sets
    MSconcat : str
        Output MS
    
    """    

	import pyrap.tables
	try:
		pyrap.tables.msutil.msconcat(MSlist, MSconcat, concatTime = False)
		pass
	except:
		ValueError('Unable to concatenate the provided MSs')
		pass



########################################################################
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Virtually concatenate a list of MSs')
    
	parser.add_argument('MSlist', type=str, nargs='+', help='A list of measurement sets')
	parser.add_argument('MSconcat', type=str, help='Output MS')

	args = parser.parse_args()
   
	main(args.MSlist,args.MSconcat)
	pass
