import glob
import os
import subprocess
import random

files =  os.listdir("2016_split")
print len(files)

# for file in files:
# 	print "splitting file: ", file
# 	subprocess.call(['split', '-l90000', '2016_data/'+file, "2016_split/"+file])
file_names = []
for i in range(100):
	choice = random.choice(files)
	print choice
	subprocess.call(['cp', "2016_split/"+choice, '2016_used/'])
	# file_names.append(random.choice(files))


