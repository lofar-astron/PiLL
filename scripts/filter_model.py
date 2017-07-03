#! /usr/bin/env python
import numpy as np

#from scripts.lib_pipeline import *
from scripts.lib_pipeline import *
    
def main(ms,skymodel,maskname,skymodel_cut,keep_in_beam=True):
    
    # make beam
    phasecentre = get_phase_centre(ms)
    make_beam_reg(phasecentre[0], phasecentre[1], 8, 'beam.reg')
    
    # prepare mask
    blank_image_reg(maskname, 'beam.reg', inverse=keep_in_beam, blankval=0) # if keep_in_beam set to 0 everything outside beam.reg

    # apply mask
    logger.info('Predict (apply mask)...')
    lsm = lsmtool.load(skymodel)
    lsm.select('%s == True' % maskname)
    fluxes = lsm.getColValues('I')
    lsm.remove(np.abs(fluxes) < 5e-4) # TEST
    lsm.write(skymodel_cut, format='makesourcedb', clobber=True)
    del lsm
    pass


########################################################################
if __name__ == '__main__':
  
    import argparse
    from argparse import RawTextHelpFormatter
    
    descriptiontext = "Filter a CC model with a given mask.\n"
    parser = argparse.ArgumentParser(description=descriptiontext, formatter_class=RawTextHelpFormatter)
    
    parser.add_argument('--ms', type=str, nargs='+', help='Input MS')
    parser.add_argument('--output', type=str, nargs='+', help='Output BBS skymodel')
    parser.add_argument('-m','--mask', nargs='+', type=str, help='A mask to filter input CC model')
    parser.add_argument('-s','--skymodel', nargs='+', type=str, help='Input BBS skymodel')

    
    args = parser.parse_args()
    
    main(ms=args.ms,skymodel=args.skymodel,maskname=args.mask,skymodel_cut=args.output)
    
    pass
      
