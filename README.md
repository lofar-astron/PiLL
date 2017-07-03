# PiLL #
## Pipeline for LOFAR LBA ##

`PiLL` is a pipeline to automatically reduce and calibrate LOFAR LBA data which have been observed in dual beam mode.
The parset provided here is used as an input for the genericpipeline.

Currently available parts of the pipeline:
------------------------------------------
* calibrator
* time_split
* selfcal (first imaging)

Installation and Usage
----------------------
In order to use `PiLL` you simply need to clone this repository and call the genericpipeline with the parset file `LBA_pipeline.parset`:

    git clone https://github.com/lofar-astron/PiLL.git
    genericpipeline.py -v -c pipeline.cfg LBA_pipeline.parset

The script `LBA_pipeline.py` automatically creates the `pipeline.cfg` and `pipeline.clusterdesc` in a convenient way (for single node use only).

    ./LBA_pipeline.py LBA_pipeline.parset /data/scratch/working_directory/
    
If you do not use `LBA_pipeline.py` make sure that the plugins folder is properly listed in your `pipeline.cfg` and that you have altered all necessary directories in the main parset file according to your system.
The script `H5parm_exporter.py` has been altered in order to accept ; as separator (to make it work with the genericpipeline).

### Dependencies

* LOFAR Software (version >= 2.20_0)
* [LoSoTo](https://github.com/revoltek/losoto) (version 0.5)
* [wsclean](https://sourceforge.net/projects/wsclean) (version 2.4)
* [PyBDSF](https://github.com/lofar-astron/PyBDSF)
* [astropy](http://www.astropy.org/) (version >= 1.3.2)
* [LSMTool](https://github.com/darafferty/LSMTool) (version 1.1)
