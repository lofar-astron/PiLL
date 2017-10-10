#!/usr/bin/env python

import numpy as np

def main(wscskymodel, col_to_delete):
    new_model=[] #store the altered model ready to write to file.
    
    #Fetch the filtered skymodel
    with open(wscskymodel, 'r') as f:
        g=f.readlines()
        
    #First check whether the column is actually there, return if not.    
    if col_to_delete not in g[0]:
        # logger.error("LogarithmicSI column could not be found! The skymodel was not changed.")
        raise Exception('LogarithmicSI column could not be found!')
    #Now we need to remove the column but also account for the possibility of a multi-component SpectralIndex
    else:
        split_format=g[0].rstrip().split(",")       #Split the format line by commas
        num_cols=len(split_format)                  #Obtain what the length of each source should be
        del_col_index=[i for i,j in enumerate(split_format) if col_to_delete in j][0]   #Find the index of LogarithmicSI column
        si_col_index=[i for i,j in enumerate(split_format) if "SpectralIndex" in j][0]  #Find the index of the SpectralIndex column
        #Remove the LogarithmicSI column from the format header and append to new_model
        del split_format[del_col_index]
        new_model.append(split_format)
        #Now loop through the sources
        for source in g[1:]:
            #Just in case of blank lines or comments
            if source=="\n" or source.startswith("# "):
                continue
            source_split=source.rstrip().split(",")     #Split by comma again
            source_len=len(source_split)
            if source_len==num_cols:
                #The source has the expected number of columns. Great! It can be stored.
                del source_split[del_col_index]
                new_model.append(source_split)
            
            #A check that the source is not shorter as this would break things (should never be the case)
            elif source_len < num_cols:
                logger.error("Source {} is strange! Skipping!".format(source_split[0]))
                continue
            
            #If it's longer, the difference means we have an extra DIFF number of SI components.
            elif source_len > num_cols:
                diff=source_len-num_cols    #Find the diff value
                si=[source_split[i] for i in range(si_col_index, si_col_index+diff+1)]  #Gather all the SI components into one list.
                truesi=",".join(si)         #Generate the True Spec Index component by combining those obtained above.
                #Sanity check that it starts with [ and ends with ]
                if truesi.startswith("[") and truesi.endswith("]"):
                    pass
                else:
                    #Just skip if something is wrong.
                    logger.error("SpectralIndex doesn't seem correct. Skipping {}!.".format(source_split[0]))
                    continue
                #Now we have the trueSI component the index is set as this value.
                source_split[si_col_index]=truesi
                #Now remove the extra DIFF SI columns
                for i in range(diff):
                    del source_split[si_col_index+1] #Column falls back to the same number when deleting, hence no need to change the index
                #Finally not forgetting to actually remove the LogarithmicSI column, and store.
                del source_split[del_col_index]
                new_model.append(source_split)
    
    new_model=np.array(new_model)       #convert to numpy array
    # print new_model
    #Write the new skymodel (it overwrites)
    np.savetxt(wscskymodel, new_model, delimiter=",", fmt='%s')      #save the new skymodel replacing the old one
    
    pass


########################################################################
if __name__ == '__main__':
  
    import argparse
    from argparse import RawTextHelpFormatter
    
    descriptiontext = "Delete a column from a WSClean source list skymodel.\n"
    parser = argparse.ArgumentParser(description=descriptiontext, formatter_class=RawTextHelpFormatter)
    
    parser.add_argument('--skymodel', type=str, help='Input WSClean source list')
    parser.add_argument('--column-to-delete', type=str, help='Column to delete from the skymodel')

    args = parser.parse_args()

    main(wscskymodel=args.skymodel, col_to_delete=args.column_to_delete)
    
    pass
