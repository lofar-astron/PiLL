# Alexander Drabent, July 2017
# prepare mapfiles for PiLL direction-independent selfcal loop

import os
from lofarpipe.support.data_map import DataMap
from lofarpipe.support.data_map import DataProduct


def plugin_main(args, **kwargs):

    infile_map   = kwargs['infile']
    mapfile_dir  = kwargs['mapfile_dir']
    jobname      = kwargs['jobname']
    filename     = kwargs['filename']
    current_loop = str(int(kwargs['counter'])+1)
    data         = DataMap.load(infile_map)	# these are actual MS files
    datalist     = [data[i].file for i in xrange(len(data))]
    
    globaldb_map     = os.path.join(mapfile_dir, filename + '_globaldb')     # this file holds all the globaldbs
    globaldbtec_map  = os.path.join(mapfile_dir, filename + '_globaldbtec')  # this file holds all the globaldbs
    globaldbtec2_map = os.path.join(mapfile_dir, filename + '_globaldbtec2') # this file holds all the globaldbs
    globaldbFR_map   = os.path.join(mapfile_dir, filename + '_globaldbFR')   # this file holds all the globaldbs
    globaldbCD_map   = os.path.join(mapfile_dir, filename + '_globaldbCD')   # this file holds all the globaldbs
    globaldbamp_map  = os.path.join(mapfile_dir, filename + '_globaldbamp')  # this file holds all the globaldbs
    h5parmtec_map    = os.path.join(mapfile_dir, filename + '_h5parmtec')    # this file holds all the h5parms
    h5parmtec2_map   = os.path.join(mapfile_dir, filename + '_h5parmtec2')   # this file holds all the h5parms
    h5parmFR_map     = os.path.join(mapfile_dir, filename + '_h5parmFR')     # this file holds all the h5parms
    h5parmCD_map     = os.path.join(mapfile_dir, filename + '_h5parmCD')     # this file holds all the h5parms
    h5parmamp_map    = os.path.join(mapfile_dir, filename + '_h5parmamp')    # this file holds all the h5parms
    
    map_out_globaldb     = DataMap([])
    map_out_globaldbtec  = DataMap([])
    map_out_globaldbtec2 = DataMap([])
    map_out_globaldbFR   = DataMap([])
    map_out_globaldbCD   = DataMap([])
    map_out_globaldbamp  = DataMap([])
    map_out_h5parmtec    = DataMap([])
    map_out_h5parmtec2   = DataMap([])
    map_out_h5parmFR     = DataMap([])
    map_out_h5parmCD     = DataMap([])
    map_out_h5parmamp    = DataMap([])

    map_out_globaldb.data.append(DataProduct( data[0].host, jobname + '.globaldb_loop' + current_loop, False))
    map_out_globaldbtec.data.append(DataProduct( data[0].host, jobname + '.globaldbtec_loop' + current_loop, False))
    map_out_globaldbtec2.data.append(DataProduct( data[0].host, jobname + '.globaldbtec2_loop' + current_loop, False))
    map_out_globaldbFR.data.append(DataProduct( data[0].host, jobname + '.globaldbFR_loop' + current_loop, False))
    map_out_globaldbCD.data.append(DataProduct( data[0].host, jobname + '.globaldbCD_loop' + current_loop, False))
    map_out_globaldbamp.data.append(DataProduct( data[0].host, jobname + '.globaldbamp_loop' + current_loop, False))
    map_out_h5parmtec.data.append(DataProduct( data[0].host, jobname + '_loop' + current_loop + '.h5parmtec', False)) 
    map_out_h5parmtec2.data.append(DataProduct( data[0].host, jobname + '_loop' + current_loop + '.h5parmtec2', False)) 
    map_out_h5parmFR.data.append(DataProduct( data[0].host, jobname + '_loop' + current_loop + '.h5parmFR', False)) 
    map_out_h5parmCD.data.append(DataProduct( data[0].host, jobname + '_loop' + current_loop + '.h5parmCD', False))
    map_out_h5parmamp.data.append(DataProduct( data[0].host, jobname + '_loop' + current_loop + '.h5parmamp', False))
    
    globaldbFR_folder  = jobname + '.globaldbFR_loop'  + current_loop
    globaldbCD_folder  = jobname + '.globaldbCD_loop'  + current_loop
    globaldbamp_folder = jobname + '.globaldbamp_loop' + current_loop
    
    image_high1        = jobname + '_image_high1_loop'        + current_loop
    image_high2        = jobname + '_image_high2_loop'        + current_loop
    image_mask         = jobname + '_mask_high1_loop'           + current_loop
    filter_model       = jobname + '_filter_model_loop'         + current_loop
    sourcedb_target    = jobname + '-make_sourcedb_target_loop' + current_loop
    
    image_high1_pattern = image_high1 + '-MFS-image.fits'
    image_high2_sources = image_high2 + '-sources.txt'
        
    map_out_globaldb.save(globaldb_map)
    map_out_globaldbtec.save(globaldbtec_map)
    map_out_globaldbtec2.save(globaldbtec2_map)
    map_out_globaldbFR.save(globaldbFR_map)
    map_out_globaldbCD.save(globaldbCD_map)
    map_out_globaldbamp.save(globaldbamp_map)
    map_out_h5parmtec.save(h5parmtec_map)
    map_out_h5parmtec2.save(h5parmtec2_map)
    map_out_h5parmFR.save(h5parmFR_map)
    map_out_h5parmCD.save(h5parmCD_map)
    map_out_h5parmamp.save(h5parmamp_map)

    result = {'globaldb':globaldb_map, 'globaldbtec':globaldbtec_map, 'globaldbtec2':globaldbtec2_map, 'globaldbFR':globaldbFR_map, 'globaldbCD':globaldbCD_map, 'globaldbamp':globaldbamp_map, 'h5parmtec':h5parmtec_map, 'h5parmtec2':h5parmtec2_map, 'h5parmFR':h5parmFR_map, 'h5parmCD':h5parmCD_map, 'h5parmamp':h5parmamp_map, 'plotstec': 'plots-tec' + current_loop, 'plotstec2': 'plots-tec2' + current_loop, 'plotsFR': 'plots-fr' + current_loop, 'plotsCD': 'plots-cd' + current_loop, 'plotsamp': 'plots-amp' + current_loop, 'globaldbFR_folder': globaldbFR_folder, 'globaldbCD_folder': globaldbCD_folder, 'globaldbamp_folder': globaldbamp_folder, 'image_high1': image_high1, 'image_high1_pattern': image_high1_pattern, 'image_mask': image_mask, 'image_high2': image_high2, 'image_high2_sources': image_high2_sources, 'filter_model': filter_model, 'sourcedb_target': sourcedb_target}
    return result
    pass
