import os
import arcpy
from arcpy import env
from distutils.dir_util import copy_tree

#set variables
tractpath = 'D:/F_Data/data/kwaechte/tracts/completed/'
chunk ='c/'
chunkrefplain = 'c'
summarypath = '{0}/LiDAR_Analyst/LosAngeles1301_CA/Summary/'
devplanespath = 'summary.gdb/developable_planes'
uploadfolderpath = 'pg_upload'

# make a list of tract folders within the given chunk folder
tract_list = []
for folder in os.listdir(tractpath + chunk):
	tract_list.append(folder)

#how many tracts are there in the chunk folder?
print('{0} tracts in chunk dir'.format(len(tract_list)))

# issue tracts
issue_tracts = []
issuefile = open(tractpath + chunkrefplain + "_issues.txt", 'w')

#------------------------ VALIDATE OUTPUT ---------------------------------#
#------------- check to see if later stage file exists --------------------#

# loop through tracts, if end file does not exist, add to a list of issue tracts 
for tract in tract_list:
	summarypath = '{0}/LiDAR_Analyst/LosAngeles1301_CA/Summary/'
	path = tractpath + chunk + summarypath.format(tract)
	#redopath = 'D:/F_Data/data/kwaechte/tracts/rerun/'
	summgdb = '{0}/summary.gdb'.format(path)		#may have to insert in combew  (LiDAR_Analyst/LosAngeles1301_CA/Combine/)
	if not os.path.exists(summgdb):
		issue_tracts.append(summgdb)
		print(tract)
	#	copy_tree(tractpath+chunk+tract, redopath+tract)		#use to copy issue tract folders to the rerun folder
	issuefile = open(tractpath + chunkrefplain + "_issues.txt", 'a')  #a= append mode, appends to last line
	try:
		issuefile.close()
	except: 
		pass
print('There are {0} total tracts that are missing summary geodatabases'.format(len(issue_tracts)))

for tract in tract_list:
	combinepath = '{0}/LiDAR_Analyst/LosAngeles1301_CA/Combine'
	path = tractpath + chunk + combinepath.format(tract)
	redopath = 'D:/F_Data/data/kwaechte/tracts/rerun/'
	combew = '{0}/combew'.format(path)		#may have to insert in combew  (LiDAR_Analyst/LosAngeles1301_CA/Combine/)
	if not os.path.exists(combew):
		issue_tracts.append(combew)
		print(tract)
		copy_tree(tractpath+chunk+tract, redopath+tract)		#use to copy issue tract folders to the rerun folder
	issuefile = open(tractpath + chunkrefplain + "_issues.txt", 'a')  #a= append mode, appends to last line
	try:
		issuefile.close()
	except: 
		pass
print('There are {0} total tracts that are missing combew rasters'.format(len(issue_tracts)))
#print('\n'+str("Now moving file from tract folder to upload folder"))

#------------------------ MOVE VALIDATED DATA TO UPLOAD FOLDER ---------------------------------#
#------------- copy developable planes fc to new gdb populated with tract fcs --------------------#

#example path to copy from D:\F_Data\data\kwaechte\tracts\completed\a\101110\LiDAR_Analyst\LosAngeles1301_CA\Summary\summary.gdb

# #make functions
# def rename_planes(tract):
# 	#set workspace
# 	env.workspace = tractpath + chunk + summarypath + 'summary.gdb'
# 	#local vars
# 	in_data1 = tractpath + chunk + summarypath + devplanespath
# 	out_data1 = tractpath + uploadfolderpath
# 	data_type1 = "FeatureClass"
# 	#execute rename to tract fips code
# 	arcpy.Rename_management(in_data1, out_data1, data_type1)

# def planes_to_pgupload(planes):

# #if end file exists, rename feature class (rename_planes) then copy to gdb for postgres upload (planes_to_pgupload)
# for tract in tract_list: 
# 	path = tractpath + chunk + "/" + combinepath.format(tract)
# 	combew = '{0}/combew'.format(path)		#may have to insert in combew  (LiDAR_Analyst/LosAngeles1301_CA/Combine/)

# 	error_file = open(tractpath + "export_issues_" + chunk +".txt")
# 	in_data = ''
# 	out_data = tractpath + "pg_upload"
# 	if os.path.exists(combew):
		
# 		copy completed feature classes to validated data folder
# 		arcpy.Copy_management(in_data, out_data)



# #rename developable planes to tract fips
# #copy tract fips planes to gdb in validated folder
