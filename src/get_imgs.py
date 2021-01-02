import ee



# preprocess locations to access
# for now, just select britain, but in future: 
# define percentage of chunks to sample - reciprocal gives number of chunks to skip. eg, 0.2 means measuring every 5th chunk. 
# define chunk size - this is a certain level of trial and error based on resolution and sample size
# define sample/filter set based on coordinates, pass to get_chunked_ee_data.py 
#   rough region bounding - only iterate through regions that contain the limits of our analysis
#   fine region bounding - if coord is not in bounds, skip it
#   sample skipping - if coord modulo percentage = value, skip (there has to be a better way - see above functional method to look for ee.filter methods that fix this)

#from here, move to other script and call it using %get_chunked_ee_data.py (or whatever I call it) in a for loop. 

# get ee auth instance and coord filters from parent - can I pass methods as parameters? 
# pass out ee.imagecollection (or whatever it is)
# ee.export
# write it out into a file 