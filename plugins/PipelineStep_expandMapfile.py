import os
from lofarpipe.support.data_map import DataMap
from lofarpipe.support.data_map import DataProduct
from lofarpipe.support.data_map import MultiDataMap
from lofarpipe.support.data_map import MultiDataProduct

# mandatory arguments:
# cmdline for type of mapfile creation
# options: mapfile-dir, filename, identifier(name in parsetparset)


def plugin_main(args, **kwargs):
    #print 'PLUGIN KWARG: ', kwargs
    result = {}
    datamap = None
    fileid = kwargs['mapfile_in']
    fileid2 = kwargs['mapfile_ref']
    datamap = MultiDataMap.load(fileid)
    datamap2 = DataMap.load(fileid2)
    newmap = []
    for item in datamap2:
        entry = {}
        entry['host'] = item.host
        entry['file'] = datamap.data[0].file
        entry['skip'] = item.skip
        newmap.append(entry)

    outfileid = os.path.join(kwargs['mapfile_dir'], kwargs['filename'])
    outmap = open(outfileid, 'w')
    outmap.write(repr(newmap))
    outmap.close()

    result['mapfile'] = outfileid
    return result
