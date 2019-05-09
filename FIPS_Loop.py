#script to run through tracts in LA
#import arcpy
import os
import os.path
import time
import sys
import fnmatch
from shutil import copyfile
from distutils.dir_util import copy_tree
##import threading
##from pvroof import combine_lidar

# Set environment settings
dPath = 'D:/F_Data/data/kwaechte/'
fipspath = dPath+'tracts/' 
all_footprints = '/la_dl/building_footprints/chunks/'
all_dsms = '/la_dl/first_return_raw/chunks/'
modelpath = dPath+'/PV_Rooftop_Model/'

if not os.path.exists(fipspath):
    os.mkdir(fipspath, 0777)

print "mkdir done"

footprintpath = str(dPath)+str(all_footprints)  #D:/F_Data/data/kwaechte/la_dl/building_footprints/chunks
dsmpath = str(dPath)+str(all_dsms)  #D:/F_Data/data/kwaechte/la_dl/first_return_raw/chunks

tract_fips_list = []
for file in os.listdir(footprintpath):
    if file.endswith('.shp'):
        this_fips = file.replace('.shp','').split('_')[-1]
        this_fips_path = fipspath+this_fips
        tract_fips_list.append(this_fips)
        if not os.path.exists(this_fips_path):
            os.mkdir(this_fips_path, 0777)
            copy_tree(modelpath, this_fips_path)
            
print tract_fips_list
    
def movefiles(move_fips):
    for file in os.listdir(footprintpath):
        if fnmatch.fnmatch(file, '*'+move_fips+'*'):
            #move the file
            copyfile(footprintpath+file, fipspath+move_fips+'/LiDAR_Analyst/LosAngeles1301_CA/Buildings/'+file)
            print str(file)+" moved to tract directories."
    for file in os.listdir(dsmpath):
        if fnmatch.fnmatch(file, '*'+move_fips+'*'):
            #move the file
            copyfile(dsmpath+file, fipspath+'/'+move_fips+'/LiDAR_Analyst/LosAngeles1301_CA/reflective_surface/'+file)
            print str(file)+" moved to tract directories."

for tract_fips in tract_fips_list:
    movefiles(tract_fips)
    
'''
threads = []
for i in tract_fips_list:
    t = threading.Thread(target=pvroof.combine_lidar, args=(i,))
    threads.append()
    t.start()
    print i+" started."    

except Exception as e:
    print e.message
    arcpy.AddError(e.message)
'''
