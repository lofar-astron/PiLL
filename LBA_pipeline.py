#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""See http://www.astron.nl/citt/genericpipeline/ for further information on parsets."""

import os, sys
import logging
import optparse
from factor import process

_version = '1.0'

os.system('clear')
print '\033[30;1m################################################'
print '## LOFAR LBA calibration and imaging pipeline ##'
print '################################################\033[0m'

def add_coloring_to_emit_ansi(fn):

	def new(*args):
		levelno = args[0].levelno
		if(levelno>=50):
			color = '\x1b[31m' # red
			pass
		elif(levelno>=40):
			color = '\x1b[31m' # red
			pass
		elif(levelno>=30):
			color = '\x1b[33m' # yellow
			pass
		elif(levelno>=20):
			color = '\x1b[32m' # green
			pass
		elif(levelno>=10):
			color = '\x1b[35m' # pink
			pass
		else:
			color = '\x1b[0m' # normal
			pass
		args[0].msg = color + args[0].msg +  '\x1b[0m'  # normal
		return fn(*args)
		pass
	return new
	pass

def create_clusterdesc(working_directory):
  
	os.system('sed "s/\/any/localhost/g" $LOFARROOT/share/local.clusterdesc > ' + working_directory + '/pipeline.clusterdesc')
	pass
    
    
def create_pipeline_config(working_directory):

	try:
		lofarroot = os.environ['LOFARROOT']
		local_dir = os.getcwd()
		pass
	except KeyError:
		logging.error('The LOFAR root directory could not be determined. Please check your installation.')
		sys.exit(1)
		pass
	      
	try:
		default_config      = lofarroot + '/share/pipeline/pipeline.cfg'
		default_runtime     = os.popen('grep runtime_directory  ' + default_config + ' | cut -f2- -d"="').readlines()[0].rstrip('\n').replace(' ','')
		default_working     = os.popen('grep working_directory  ' + default_config + ' | cut -f2- -d"="').readlines()[0].rstrip('\n').replace(' ','')
		default_recipes     = os.popen('grep recipe_directories ' + default_config + ' | cut -f2- -d"="').readlines()[0].rstrip('\n').replace(' ','')
		default_clusterdesc = os.popen('grep clusterdesc '        + default_config + ' | cut -f2- -d"="').readlines()[0].rstrip('\n').replace(' ','')
		default_logfile     = os.popen('grep log_file '           + default_config + ' | cut -f2- -d"="').readlines()[0].rstrip('\n').replace(' ','')
		default_xml         = os.popen('grep xml_stat_file '      + default_config + ' | cut -f2- -d"="').readlines()[0].rstrip('\n').replace(' ','')
		pipeline_cfg        = working_directory + '/pipeline.cfg'
		with open(pipeline_cfg, 'w') as outfile:
			with open(default_config, 'r') as infile:
				outfile.write('[DEFAULT]\n')
				outfile.write('local_directory = ' + local_dir + '\n')
				for line in infile:
					if '[DEFAULT]' in line:
						continue
						pass
					outfile.write(line.replace(default_runtime, working_directory)\
							  .replace(default_working, '%(runtime_directory)s')\
							  .replace(default_recipes, '[%(pythonpath)s/lofarpipe/recipes,%(local_directory)s]')\
							  .replace(default_clusterdesc, '%(working_directory)s/pipeline.clusterdesc')\
							  .replace(default_logfile, '%(runtime_directory)s/%(job_name)s/logs/%(start_time)s/pipeline.log')\
							  .replace(default_xml, '%(runtime_directory)s/%(job_name)s/logs/%(start_time)s/statistics.xml'))
					pass

		try:
			max_per_node    = os.popen('nproc').readlines()[0].rstrip('\n')
			os.system('echo >> '                                     + pipeline_cfg)
			os.system('echo [remote] >> '                            + pipeline_cfg)
			os.system('echo method = local >> '                      + pipeline_cfg)
			os.system('echo max_per_node = ' + max_per_node + ' >> ' + pipeline_cfg)
			pass
		except IndexError:
			logging.error('The number of available CPUs could not be determined. Please check your installation of nproc.')
			sys.exit(1)
			pass

	except IOError or IndexError:
		logging.error('LOFAR pipeline configuration not found. Please check your installation.')
		sys.exit(1)
		pass
	
	infile.close()
	outfile.close()
	
	pass

def create_pipeline_parset(working_directory):
      
	pipeline_parset = working_directory + '/pipeline.parset'
	local_directory = os.getcwd()
	#job_directory   = working_directory + '/' + os.path.splitext(os.path.basename(args[0]))[0]
	job_directory   = working_directory + '/pipeline'
	lofarroot       = os.environ['LOFARROOT']
	archive         = os.popen('grep !archive ' + args[0] + ' | cut -f2- -d"="').readlines()[0].rstrip('\n').replace(' ','')
	
	
	try:
		max_per_node = os.popen('nproc').readlines()[0].rstrip('\n')
		pass
	except IndexError:
		logging.error('The number of available CPUs could not be determined. Please check your installation of nproc.')
		sys.exit(1)
		pass
	     
	try:
		with open(pipeline_parset, 'w') as outfile:
			with open(args[0], 'r') as infile:
				for line in infile:
					outfile.write(line.replace('input.output.working_directory', working_directory)\
							  .replace('input.output.job_dir', job_directory)\
							  .replace('input.output.local_directory', local_directory)\
							  .replace('input.output.lofarroot', lofarroot))
					pass
				pass
			pass
		      
	except IOError or IndexError:
		logging.error('LOFAR pipeline configuration not found. Please check your installation.')
		sys.exit(1)
		pass
	      
	infile.close()
	outfile.close()
	
	pass
            
if __name__=='__main__':
	# Get command-line options.
	opt = optparse.OptionParser(usage='%prog <pipeline.parset> <output_directory> ', version='%prog '+_version, description=__doc__)
	(options, args) = opt.parse_args()

	logging.root.setLevel(logging.INFO)
	log    = logging.StreamHandler()
	format = logging.Formatter('\033[1m%(levelname)s\033[0m: %(message)s')
	log.setFormatter(format)
	log.emit = add_coloring_to_emit_ansi(log.emit)
	
	logging.root.addHandler(log)
  
	# Get inputs
	if len(args) != 2:
		logging.error('Wrong number of arguments.')
		opt.print_help()
		sys.exit(1)
		pass
	logging.info('Checking pipeline parset: \033[34m' + args[0])
	if not os.path.isfile(args[0]):
		logging.error('Pipeline parset does not exist.')	        
		sys.exit(1)
		pass
	working_directory = args[1].rstrip('.').rstrip('/')
	logging.info('Checking working directory: \033[34m' + working_directory)
	if os.path.isdir(working_directory):
		prompt = "\033[1;35mWARNING\033[0m: Output directory already exists. Press enter to clobber or 'q' to quit : "
		answer = raw_input(prompt)
		while answer != '':
			if answer == 'q':
				sys.exit(0)
				pass
			answer = raw_input(prompt)      
			pass
		logging.info('Cleaning working directory \033[5m...')
		os.system('rm -rfv ' + working_directory)
		pass
	os.system('mkdir -pv ' + working_directory)
	
	# creating cluster description file
	create_clusterdesc(working_directory)
	logging.info('Created local cluster description file: \033[34m' + working_directory + '/pipeline.clusterdesc')
	
	# creating pipeline configuration
	create_pipeline_config(working_directory)
	logging.info('Created pipeline configuration file: \033[34m' + working_directory + '/pipeline.cfg')

	# creating pipeline parameter set
	create_pipeline_parset(working_directory)
	logging.info('Created pipeline configuration file: \033[34m' + working_directory + '/pipeline.parset')

	# starting of generic pipeline
	logging.info('Calibration is starting \033[5m...')
	os.system('genericpipeline.py ' + working_directory + '/pipeline.parset -v -c ' + working_directory + '/pipeline.cfg')
	
	# calibration has been finished
	logging.info('\033[30;4mCalibration has been finished.')
	
	sys.exit(0)
	pass
