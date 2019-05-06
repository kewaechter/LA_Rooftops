##
## Basic requirements
## Must contain folder in accordance with the naming conventions used in the "City_1" field of the "Altitude.shp".
## This folder must have two sub folders i.e. (1) "reflective_surface" having the grid "refsurf", (2) Buildings having "City_1_2d_buildings.shp" (keep only one file in this folder) file.
## Base_map folder having files "Zip.shp" and "ShadeThreshold.shp" files.
## LDR.gdb Database having feature layers "Altitude.shp", & "Azimuth.shp"
##

import os
import arcpy
import os.path
from arcpy import env
from arcpy import da
from arcpy.sa import *
import time
import shutil
import gc

##from distutils.dir.util import copy_tree


def combine_lidar(tract_fips):

        import os
        import arcpy
        import os.path
        from arcpy import env
        from arcpy import da
        from arcpy.sa import *
        import time
        import shutil
        import gc
        ##from distutils.dir.util import copy_tree

        # Set environment settings
        arcpy.ImportToolbox('C:/Program Files (x86)/ArcGIS/Desktop10.2/ArcToolbox/Toolboxes/Data Management Tools.tbx', 'management') 
        arcpy.env.overwriteOutput = True
        arcpy.CheckOutExtension("Spatial")
        zFactor = 1
        outMeasurement = "DEGREE"

        dPath = "D:/F_Data/data/kwaechte/tracts/c/"+str(tract_fips)+"/LiDAR_Analyst/"
        zPath = "D:/F_Data/data/kwaechte/tracts/c/"+str(tract_fips)+"/LiDAR_Analyst/Temp/"
        bPath = "D:/F_Data/data/kwaechte/tracts/c/"+str(tract_fips)+"/"
        dsm = "/reflective_surface/losangeles_ca_2013_firstreturn_26911_"+str(tract_fips)+".tif"
        #changed path from C:/ to /gisdata/staff/kwaechte
        arcpy.env.workspace  = (str(dPath))
        
        try:
                StartTime = time.clock()
                inTable  = "D:/F_Data/data/kwaechte/tracts/c/"+str(tract_fips)+"/Base_map/LDR.gdb/Altitude"
                #changed path from C:/ to /gisdata/staff/kwaechte
                inTablez = "D:/F_Data/data/kwaechte/tracts/c/"+str(tract_fips)+"/Base_map/LDR.gdb/Azimuth"
                #changed path from C:/ to /gisdata/staff/kwaechte
        #
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                print "made it to first calcfieldmgmt"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                print "here"
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)       
        #
        #==============================================.Query for City Name.================================================>
        #      
                print "                            LIDAR PV DATA ANALYST                          "
                print "========================================================================"
                print
                
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        print "*********************: The City Quad being analyzed  :*********************"               
                        print
                        print cityq
                        print 

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))
                inRaster = (str(dPath)+str(cityq)+str(dsm))

        #Check if the Raster layer is in projected space
                desc = arcpy.Describe(inRaster)
                #print inRaster
                # Get the spatial reference 
                sr = desc.spatialReference
                # Check if the Rastger is in projected space
                if sr.type == "Projected":
                    print    
                    print "*********************:         PROJECTION            :*********************"
                    print
                    #print "Raster layer "+str(inRaster)+ " has Projection: " +str(sr.Name)
                    print "Raster layer: " +str(sr.Name)
                    
                else:
                    print "ERROR.....The Projection of Raster layer is: " +str(sr.Name)
                    print "Please assign projection to: " +str(inRaster)
                    print "LiDAR Analyst is going to exit now."
                    sys.exit()
        ## Buildings layer
        ##
                arcpy.env.workspace  = (str(dPath)+str(cityq)+"/Buildings/")
                fcs = arcpy.ListFeatureClasses()
                for fc in fcs:
                    fc2 = fc
                inMaskData = fc2               #Building layer

        #Check if the buidlings layer is in projected space
                desc = arcpy.Describe(inMaskData)
                # Get the spatial reference 
                sr = desc.spatialReference
                # Check if the feature class is in projected space
                if sr.type == "Projected":
                    #print "Buildings layer "+str(inMaskData)+ " has Projection: " +str(sr.Name)
                    print "Buildings layer: " +str(sr.Name)
                    print
                else:
                    print "ERROR.....The Projection of buildings layer " +str(inMaskData)+ " is: " +str(sr.Name)
                    print "Please assign projection to: " +str(inMaskData)
                    print "LiDAR Analyst is going to exit now."
                    sys.exit()

        #=================================================.Creating Folders.=================================================>
              
                outfolderPath1 = str(dPath)+str(cityq)
                folderName1    = "HillShade"
                arcpy.CreateFolder_management(outfolderPath1,folderName1) # creates folder by the name of HillShade       
                folderName2    = "Reclass"
                arcpy.CreateFolder_management(outfolderPath1,folderName2) # creates folder by the name of Reclass         
                folderName5    = "Slope"
                arcpy.CreateFolder_management(outfolderPath1,folderName5) # creates folder by the name of sumRec_year for year         
                folderName6    = "Aspect"
                arcpy.CreateFolder_management(outfolderPath1,folderName6) # creates folder by the name of Aspect for year            
                folderName7    = "Summary"
                arcpy.CreateFolder_management(outfolderPath1,folderName7) # creates folder by the name of Summary for year
                folderName8    = "Combine"
                arcpy.CreateFolder_management(outfolderPath1,folderName8) # creates folder by the name of Combine
                outfolderPath2 = str(dPath)+str(cityq)+"/Combine/"
                folderName3    = "sumRec_month"
                arcpy.CreateFolder_management(outfolderPath2,folderName3) # creates folder by the name of sumRec_month for month                
                folderName4    = "sumRec_year"
                arcpy.CreateFolder_management(outfolderPath2,folderName4) # creates folder by the name of sumRec_year for year
                print "Folders (Aspect, Combine, Hillshade, Reclass, Slope, & Summary) created for the city :" +str(cityq)
                print
                print "*********************:    HILLSHADE CALCULATION      :*********************"
                print

        #
        #================================================.Selecting the data based on City Query.===============================>
        #
                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)
                lyrz2 = arcpy.MakeFeatureLayer_management(inTablez,"lyrz")
                inTablez2 = arcpy.SelectLayerByAttribute_management(lyrz2,"NEW_SELECTION",qry1)
                cnt = arcpy.GetCount_management(inTablez2)
                #print "number of selected record is:"+str(cnt)
        #
        #=================================================.Hillshade calculation.==============================================>        
        #
                fName = []   # Name of the fields                                                          #Line 5
                nAlt  = []   # Altitude
                aZi   = []   # Azimuth
                rows = arcpy.SearchCursor(inTable2)
                rowsz = arcpy.SearchCursor(inTablez2)
                cols = arcpy.ListFields(inTable2,"*","DOUBLE")
                for row,rowz in zip (rows,rowsz):
                    for col in cols:
                        fName.append(col.name)
                        nAlt.append(row.getValue(col.name))
                        aZi.append(rowz.getValue(col.name))
                count = 0
                inRaster = (str(dPath)+str(cityq)+str(dsm))  #LiDAR Raster
                #print inRaster
                for N,A,Z in zip (fName,nAlt,aZi):
                    # Set local variables
                    inRaster = "refsurf"
                    Altitude = A
                    Azimuth = Z
                    modelShadows = "SHADOWS"
                    zFactor = 1
                    # Execute HillShade (HillShade calculation)
                    inRaster = (str(dPath)+str(cityq)+str(dsm))
                    if Azimuth > 0 or Altitude > 0:
                            outHillShade = Hillshade(inRaster, Azimuth, Altitude, modelShadows, zFactor) 
                            # Save the output
                            outHS = str(dPath)+str(cityq)+"/HillShade/"+str(N)
                            #print outHS
                            outHillShade.save(outHS)  #................ Integer
                            del outHillShade  
                            #print "Hillshade calculated for: City:"+str(cityq),  "Month_Day: "+str(N),"Altitude:"+str(A),"Azimuth:"+str(Z)
                            print "Day: "+str(N)+" ,","Altitude:"+str(A)+" ,","Azimuth:"+str(Z)
                    count += 1
                print
                print "Processed step 1, Hillshade calculation completed." # for the all the months for City:" +str(cityq) #+ "is" +str(count)
                print "Now Running LiDARP2 script to process steps 2-4"

        # SCRIPT 2
        #=========================================.Hillshade reclassification.==========================================================> 
        #
                print
                print "*********************:  Hillshade reclassification   :*********************"
                print
                env.workspace = str(dPath)+str(cityq)+"/HillShade/"                                             
                datapath1 = str(dPath)+str(cityq)+"/HillShade/"
                print datapath1
                inRasterList1 = arcpy.ListRasters('mar*','')
                reclassField = "VALUE"
                print inRasterList1
                for inRaster1 in inRasterList1:
                        print "1:" +str(inRaster1)
                        print "Reclassifying raster: %s" %os.path.join("dataPath1",inRaster1)
                        print inRaster1
                        remap1 = RemapValue([[0,153,0],[153,254,1]])      # March
                        print "2:" +str(inRaster1)
                        outReclassify = Reclassify(inRaster1, reclassField, remap1, "NODATA")
                        print "3:" +str(inRaster1)
                        outReclassify.save(str(dPath)+str(cityq)+"/Reclass/"+str(inRaster1)+str("rec"))
                        del outReclassify
                        print "4:" +str(inRaster1)
                datapath2 = str(dPath)+str(cityq)+"/HillShade/"
                inRasterList2 = arcpy.ListRasters('jun*','')
                #reclassField = "VALUE"
                for inRaster2 in inRasterList2:
                        #print "Reclassifying raster: %s" %os.path.join("dataPath2",inRaster2)
                        print inRaster2
                        remap2 = RemapValue([[0,178.5,0],[178.5,254,1]])  # June
                        outReclassify = Reclassify(inRaster2, reclassField, remap2, "NODATA")
                        outReclassify.save(str(dPath)+str(cityq)+"/Reclass/"+str(inRaster2)+str("rec"))
                        del outReclassify
                datapath3 = str(dPath)+str(cityq)+"/HillShade/"
                inRasterList3 = arcpy.ListRasters('sep*','')
                #reclassField = "VALUE"
                for inRaster3 in inRasterList3:
                        #print "Reclassifying raster: %s" %os.path.join("dataPath3",inRaster3)
                        print inRaster3
                        remap3 = RemapValue([[0,153,0],[153,254,1]])      # September                        
                        outReclassify = Reclassify(inRaster3, reclassField, remap3, "NODATA")
                        outReclassify.save(str(dPath)+str(cityq)+"/Reclass/"+str(inRaster3)+str("rec"))
                        del outReclassify
                datapath4 = str(dPath)+str(cityq)+"/HillShade/"
                inRasterList4 = arcpy.ListRasters('dec*','')
                #reclassField = "VALUE"
                for inRaster4 in inRasterList4:
                        #print "Reclassifying raster: %s" %os.path.join("dataPath4",inRaster4)
                        print inRaster4
                        remap4 = RemapValue([[0,127.5,0],[127.5,254,1]])  # December                         
                        outReclassify = Reclassify(inRaster4, reclassField, remap4, "NODATA")
                        outReclassify.save(str(dPath)+str(cityq)+"/Reclass/"+str(inRaster4)+str("rec"))
                        del outReclassify
                print
                print "Processed step 2, Hillshade recalssifcation completed" # for City:" +str(cityq)
        #
        #================================.Summation of reclassified Hillshade raster on month to month bases.===================================> 
        #            
                print
                print "*********************:  Monthly Summation    :*********************"
                print
                arcpy.env.workspace = str(dPath)+str(cityq)+"/Reclass/"                                  #Line 21 
                datapath = str(dPath)+str(cityq)+"/Reclass/"
                rasters1 = arcpy.ListRasters('mar*','')
                i = 0
                # Sum of all the rasters for the Month of March
                for inRaster1 in rasters1:
                    #print "processing raster for summation (monthly): %s" %os.path.join("dataPath",inRaster1)
                    print inRaster1
                    if  i == 0:
                        outSum1 = arcpy.Raster(inRaster1)
                        i += 1
                    else:
                        outSum1 = outSum1 + inRaster1
                        i += 1
                outSum1.save(str(dPath)+str(cityq)+"/Combine/sumRec_month/"+str("Mar_sum"))
                del outSum1

                # Sum of all the rasters for the Month of June
                arcpy.env.workspace = str(dPath)+str(cityq)+"/Reclass/"                                  #Line 21 
                datapath = str(dPath)+str(cityq)+"/Reclass/"
                rasters2 = arcpy.ListRasters('jun*','')
                #print rasters2
                i = 0
                for inRaster2 in rasters2:            
                        #print "processing raster for summation (monthly): %s" %os.path.join("dataPath",inRaster2)
                        print inRaster2
                        if  i == 0:
                            outSum2 = arcpy.Raster(inRaster2)
                            i += 1
                        else:
                            outSum2 = outSum2 + inRaster2
                            i += 1
                outSum2.save(str(dPath)+str(cityq)+"/Combine/sumRec_month/"+str("Jun_sum"))
                del outSum2

                # Sum of all the rasters for the Month of September
                arcpy.env.workspace = str(dPath)+str(cityq)+"/Reclass/"                                  #Line 21 
                datapath = str(dPath)+str(cityq)+"/Reclass/"
                rasters3 = arcpy.ListRasters('sep*','')
                #print rasters3
                i = 0
                for inRaster3 in rasters3:
                        #print "processing raster for summation (monthly): %s" %os.path.join("dataPath",inRaster3)
                        print inRaster3
                        if  i == 0:
                            outSum3 = arcpy.Raster(inRaster3)
                            i += 1
                        else:
                            outSum3 = outSum3 + inRaster3
                            i += 1
                outSum3.save(str(dPath)+str(cityq)+"/Combine/sumRec_month/"+str("Sep_sum"))
                del outSum3

                # Sum of all the rasters for the Month of December
                arcpy.env.workspace = str(dPath)+str(cityq)+"/Reclass/"                                  #Line 21 
                datapath = str(dPath)+str(cityq)+"/Reclass/"  
                rasters4 = arcpy.ListRasters('dec*','')
                #print rasters4
                i = 0
                for inRaster4 in rasters4:
                    #print "processing raster for summation (monthly): %s" %os.path.join("dataPath",inRaster4)
                    print inRaster4
                    if  i == 0:
                        outSum4 = arcpy.Raster(inRaster4)
                        i += 1
                    else:
                        outSum4 = outSum4 + inRaster4
                        i += 1
                outSum4.save(str(dPath)+str(cityq)+"/Combine/sumRec_month/"+str("Dec_sum"))
                del outSum4
                print
                print "Processed step 3, Summation of Hillshade for indivual months is completed" # for the city:" +str(cityq)   
        #
        #========================================.Reclassified HILLSHADE  raster on Annual bases.===============================>
        #
                print
                print "*********************:  Annual Summation    :*********************"
                print
                arcpy.env.workspace = str(dPath)+str(cityq)+"/Combine/sumRec_month/"                     # Line 25
                datapath = str(dPath)+str(cityq)+"/Combine/sumRec_month/"  
                rasters = arcpy.ListRasters('','')
                #print rasters
                i = 0
                for inRaster in rasters:
                    #print "processing raster for summation(annual) : %s" %os.path.join("dataPath",inRaster)
                    print inRaster
                    if  i == 0:
                        outSum = arcpy.Raster(inRaster)
                        i += 1
                    else:
                        outSum = outSum + inRaster
                        i += 1
                outSum.save(str(dPath)+str(cityq)+"/Combine/sumRec_year/"+str("annual"))                  #  output,  annual   (Integer)
                del outSum
                print "Processed step 4, Summation of Hillshade for whole year is completed" # for the city:" +str(cityq)

        # SCRIPT 5
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        print "The City being analyzed:" +str(qry1)

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))
                inRaster = (str(dPath)+str(cityq)+str(dsm))

                arcpy.env.workspace  = (str(dPath)+str(cityq)+"/Buildings/")
                fcs = arcpy.ListFeatureClasses()
                for fc in fcs:
                    fc2 = fc
                    inMaskData = fc2
                #Building layer
        #
        #================================================.Selecting the data based on City Query.===============================>
        #
                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)
                lyrz2 = arcpy.MakeFeatureLayer_management(inTablez,"lyrz")
                inTablez2 = arcpy.SelectLayerByAttribute_management(lyrz2,"NEW_SELECTION",qry1)
                cnt = arcpy.GetCount_management(inTablez2)
                #print "number of selected record is:"+str(cnt)
         
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #============================================================.SLOPE CALCULATION.===============================================> 
                print
                print "*********************:   Slope Calculation :*********************"
                print
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))  
                inRaster = (str(dPath)+str(cityq)+str(dsm))
                outMeasurement = "DEGREE"                                                                  # Line 28
                zFactor = 1
                # Execute Slope           
                outSlope = Slope(inRaster, outMeasurement, zFactor)
                # Save the output 
                outSlope.save(str(dPath)+str(cityq)+"/Slope/"+str("slpraw"))                               #output,  slpraw (floating point)
                del outSlope
                print "Processed step 5,  Slope calculated for the city:" +str(cityq)
        #
        #..........................Extract by Mask..........................................................Line 33
        #
                arcpy.env.workspace  = (str(dPath)+str(cityq)+"/Buildings/")
                fcs = arcpy.ListFeatureClasses()
                for fc in fcs:
                    fc2 = fc
                inMaskData = fc2                                                                    #input, Building layer, shape file
                inRasterS2 =  (str(dPath)+str(cityq)+"/Slope/slpraw")                       #input  slpraw (floating point)
                outExtractByMask = ExtractByMask(inRasterS2, inMaskData)
                # Save the output 
                outExtractByMask.save(str(dPath)+str(cityq)+"/Slope/slpbldg")               #output, slpbldg  (floating point)
                del outExtractByMask
                #print "Processed step 6, Slope extracted with Mask for the city:" +str(cityq)
                print "Processed step 6,  Slope extracted" 
        #
        #..........................Extract with Attribute....................................................Line 37 
        #
                inRasterS3 = (str(dPath)+str(cityq)+"/Slope/slpbldg")                       #input slpbldg (floating point)
                inSQLClauseS = "VALUE < 60"
                #print "Raster is:"+str(inRasterS3)
                # Execute ExtractByAttributes
                attExtractS = ExtractByAttributes(inRasterS3, inSQLClauseS) 
                # Save the output 
                attExtractS.save(str(dPath)+str(cityq)+"/Slope/"+str("slplt60"))                    # output, slplt60 (floating point)
                del attExtractS
                #print "Processed step 7, Slope extracted by attribute for the city:" +str(cityq)
                print "Processed step 7,  Slope extracted"
        #
        #..........................HillShade Final............................................................Line 40
        #        
                inRasterS4 = (str(dPath)+str(cityq)+"/Slope/"+str("slplt60"))                        # input. slplt60  (floating point)
                inRasterH4 = (str(dPath)+str(cityq)+"/Combine/sumRec_year/"+str("annual"))           # input. annual (Integer)
                #print " Slope Raster is:"+str(inRasterS4)
                #print " Annual Hillshade Raster is:"+str(inRasterH4)
                Sval1 = Float(inRasterS4)                                 
                Hval1 = Int(inRasterH4)                                   
                outConS = Con(Sval1<= 9.5,Hval1 * 1.5, Hval1)
                outConS.save(str(dPath)+(cityq)+"/Slope/"+str("hillfinal"))                          #output, hillfinal, (floating point)
                del outConS
                #print "Processed step 8, Slope.. Hillshade final calculated for the city:" +str(cityq)
                print "Processed step 8,  Slope (Hillshade final calculated)"

        #
        #..........................Slope  focal mean............................................................Line 80
        #            
                neighborhood = NbrRectangle(3, 3, "CELL")
                outFocalStatistics = FocalStatistics(inRasterS4, neighborhood, "MEAN","")                     #Input. slplt60 (floating point)
                outFocalStatistics.save(str(dPath)+str(cityq)+"/Slope/"+str("slpfmean"))                      #Output, slpfmean (floating point)
                del outFocalStatistics
                #print "Processed step 9, Slope  focal mean for the city:" +str(cityq)
                print "Processed step 9,  Slope  (focal mean)"
        #
        #..........................Slope  focal mean 2............................................................Line 83
        #
                inRasterS5 = (str(dPath)+str(cityq)+"/Slope/"+str("slpfmean"))                              #input: slpfmean  (floating point)
                neighborhood = NbrRectangle(3, 3, "CELL")
                outFocalStatistics = FocalStatistics(inRasterS5, neighborhood, "MEAN","")                   
                outFocalStatistics.save(str(dPath)+str(cityq)+"/Slope/"+str("slpfmean2"))                   #output, slpfmean2 (floating point)
                del outFocalStatistics
                #print "Processed step 10, Slope focal mean for the city:" +str(cityq)
                print "Processed step 10, Slope (focal mean)"
        #
        #=================================================.ASPECT CALACULATION.=================================================================> 
        #
                print
                print "*********************:   Aspect Calculation :*********************"
                print
                # Execute Aspect                                                        # Line 31
                inRaster = (str(dPath)+str(cityq))+str(dsm)  #LiDAR Raster
                outAspect = Aspect(inRaster)                                                                  #Input, refsurf (Integer)
                # Save the output 
                outAspect.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspraw"))                                #Output, aspraw (floating point)
                del outAspect
                #print "Processed step 11, Aspect calculated for the city:" +str(cityq)
                print "Processed step 11, Aspect calculated"
        #
        #..........................Extract by Mask............................................................Line 35
        #       
                inRasterA2 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspraw"))                                #Input, aspraw (floating point) & buildings  (shapefile)        
                #print "In mask is:"+str(inMaskData)
                #print "Raster is:"+str(inRasterA2)
                outExtractByMaskA = ExtractByMask(inRasterA2, inMaskData)
                # Save the output 
                outExtractByMaskA.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspbldg"))                     #Output, aspbldg (floating point)
                del outExtractByMaskA
                #print "Processed step 12, Aspect extracted with Mask for the city:" +str(cityq)
                print "Processed step 12, Aspect extracted with Mask"
        #
        #..........................Flat Roof...................................................................Line 43
        #
                inRasterS4 = (str(dPath)+str(cityq)+"/Slope/"+str("slplt60"))
                Sval1 = Float(inRasterS4)
                inRasterA3 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspbldg"))                                #Input, aspbldg & slplt60 (floating points)
                Aval1 = Float(inRasterA3)                                                
                outConA = Con(Sval1<= 9.5,-1, Aval1)                                               
                outConA.save(str(dPath)+(cityq)+"/Aspect/"+str("aspflat"))                                    #Output, aspflat (floating point)
                del outConA
                #print "Processed step 13, Flat roof  calculated for the city:" +str(cityq)
                print "Processed step 13, Flat roof  calculated"
        #
        #..........................Flat Roof Reclassification..................................................Line 46
        #
                inRasterA4 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspflat"))                                 #Input, aspflat (floating point)
                reclassField = "VALUE"
                remapA1 = RemapValue([[-1,0,0],[0,22.5,1],[22.5,67.5,2] ,[67.5,112.5,3],[112.5,157.5,4],[157.5,202.5,5],[202.5,247.5,6],[247.5,292.5,7],[292.5,337.5,8],[337.5,360,1]])      #                
                outReclassifyA = Reclassify(inRasterA4, reclassField, remapA1, "NODATA")
                outReclassifyA.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspflatrc"))                          #Output, aspflatrc (Integer)
                del outReclassifyA
                #print "Processed step 14, Flat roof recalssification calculated for the city:" +str(cityq)
                print "Processed step 14, Flat roof recalssification calculated"
        #
        #..........................Focal Statistics.............................................................Line 59
        #
                inRasterA5 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspflatrc"))                                #Input, aspflatrc (Integer)
                neighborhood = NbrRectangle(3, 3, "CELL")
                # Execute FocalStatistics
                outFocalStatistics = FocalStatistics(inRasterA5, neighborhood, "VARIETY","")
                # Save the output
                outFocalStatistics.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspvar"))                          #Output, aspvar (Integer)
                del outFocalStatistics
                #print "Processed step 15, Focal Statistics calculated for the city:" +str(cityq)
                print "Processed step 15, Focal Statistics calculated"
        #
        #..........................Extract with Attribute.......................................................Line 62 
        #
                inRasterA6 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspvar"))                                     #Input, aspvar (Integer)
                inSQLClauseA = "VALUE < 4"                                                                     #KEW: changed from val<4 to include all roof aspects
                attExtractA = ExtractByAttributes(inRasterA6, inSQLClauseA) 
                # Save the output 
                attExtractA.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspvarext"))                               #Output, aspvarext (Integer)
                del attExtractA
                print "Processed step 16, Aspect extracted by attribute"
        #
        #..........................Extract by Mask 2............................................................Line 65
        #       
                inMaskDataA7 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspvarext"))                               #Input, aspvarext (Integer) & aspflatrc (Integer)  (line 46)
                outExtractByMaskAA = ExtractByMask(inRasterA5, inMaskDataA7)
                # Save the output 
                outExtractByMaskAA.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspflatmk"))                       #Output, aspflatmk (Integer)
                print "Processed step 17, Aspect for Flat Roof extracted with Mask"
                  
        #
        #..........................Focal Statistics  2.............................................................Line 68
        #
                inRasterA8 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspflatmk"))                                  #Input, aspflatmk (Integer)
                neighborhood = NbrRectangle(3, 3, "CELL")
                # Execute FocalStatistics
                outFocalStatisticsAA = FocalStatistics(inRasterA8, neighborhood, "MAJORITY","")
                # Save the output 
                outFocalStatisticsAA.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspmaj"))                         #Output, aspmaj (Integer)
                del outFocalStatisticsAA
                print "Processed step 18, Focal Statistics Majority calculated"

        #
        #..........................Extract by Mask 3............................................................Line 70
        #       
                inRasterA9 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspmaj"))                                     #Input, aspmaj (Integer) & buildings (shapefile)
                outExtractByMaskAAA = ExtractByMask(inRasterA9, inMaskData)
                # Save the output 
                outExtractByMaskAAA.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspfinal"))                        #Output, aspfinal (Integer)
                del outExtractByMaskAAA
                #print "Processed step 19, Aspect for Flat Roof extracted with Mask 3 for the city:" +str(cityq)
                print "Processed step 19, Aspect for Flat Roof extracted with Mask"

        #
        #..........................Aspect Raster to Polygon...................................................................Line 72
        #       
                inRasterA10 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspfinal"))                                  #Input, aspfinal (Integer)
                FieldA = "VALUE"
                outPolygons = (str(dPath)+str(cityq)+"/Aspect/"+str("aspfinal_poly"))                            #Output, aspfinal_poly  (shapefile)
                arcpy.RasterToPolygon_conversion(inRasterA10, outPolygons, "NO_SIMPLIFY", FieldA)
                #print "Processed step 20, Aspect, raster to polygon for the city:" +str(cityq)
                print "Processed step 20, Aspect, raster to polygon"

        #
        #..........................Aspect Feature to Raster...................................................................Line 75
        #
                inFeature = (str(dPath)+str(cityq)+"/Aspect/"+str("aspfinal_poly.shp"))                  #Input, aspfinal_poly (shapefile)
                FieldAA = "ID"
                outRaster = (str(dPath)+str(cityq)+"/Aspect/"+str("aspid"))                                          
                cellSize = 1
                # Execute PolygonToRaster
                arcpy.FeatureToRaster_conversion(inFeature, FieldAA, outRaster, cellSize)                        #Output, aspid   (Integer)    
                #print "Processed step 21, Aspect, feature to raster for the city:" +str(cityq)
                print "Processed step 21, Aspect, feature to raster"

        #
        #..........................Combine Aspect ............................................................................Line 78
        #
                inRasterA11 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspid"))                                    #Input, aspid (Integer) & aspfinal (Integer)
                # Execute PolygonToRaster
                outCombine = Combine([inRasterA11,inRasterA10])
                # Save the output 
                outCombine.save(str(dPath)+str(cityq)+"/Aspect/"+str("aspcomb"))                                 #Output, aspcomb  (Integer)
                del outCombine
                #print "Processed step 22, Combine Aspect for the city:" +str(cityq)
                print "Processed step 22, Combine Aspect"

        #
        #=================================================. SLOPE  Zonal mean.=================================================================> 
        #  
        #
        #..........................Slope zonal mean ..................................................................Line 86
        #
                print
                print "*********************:   Slope Zonal Mean  :*********************"
                print
                inValueRasterS6 = (str(dPath)+str(cityq)+"/Slope/"+str("slpfmean2"))                                    #Input,   slpfmean2
                inZoneRasterA12= (str(dPath)+str(cityq)+"/Aspect/"+str("aspcomb"))                                      #Input,   aspcomb  (line 78)
                zoneField = "VALUE"
                outZonalStatistics = ZonalStatistics(inZoneRasterA12, zoneField, inValueRasterS6,"MEAN", "NODATA") 
                outZonalStatistics.save(str(dPath)+str(cityq)+"/Combine/"+str("slpzmean"))                              #Output, slpzmean
                del outZonalStatistics
                print "Processed step 23, Slope Zonal mean"

        #
        #..........................Slope Aspect values assingment ..............................................................Line 89

                AvalA2 = Int(inRasterA10)                                                                               #Input,   aspfinal (Integer)
                inRasterS7 = (str(dPath)+str(cityq)+"/Combine/"+str("slpzmean"))                                        #Input,   slpzmean(Floating point)
                AvalS2 = Float(inRasterS7)
                outConAS = Con(AvalA2 == 0,0, AvalS2)
                outConAS.save(str(dPath)+(cityq)+"/Combine/"+str("slpfinal"))                                           #Output,  slpfinal (Floating point)
                del outConAS
                print "Processed step 24, Slope / Aspect values assinged"

        # SCRIPT 25
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        #print "The City being analyzed:" +str(qry1)

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))
                inRaster = (str(dPath)+str(cityq)+str(dsm))  
                print inRaster

        ##
                arcpy.env.workspace  = (str(dPath)+str(cityq)+"/Buildings/")
                fcs = arcpy.ListFeatureClasses()
                for fc in fcs:
                    fc2 = fc
                inMaskData = fc2               #Building layer

        #
        #================================================.Selecting the data based on City Query.===============================>
        #
                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)
                lyrz2 = arcpy.MakeFeatureLayer_management(inTablez,"lyrz")
                inTablez2 = arcpy.SelectLayerByAttribute_management(lyrz2,"NEW_SELECTION",qry1)
                cnt = arcpy.GetCount_management(inTablez2)
                #print "number of selected record is:"+str(cnt)

        #=================================================. COMBINE.=================================================================> 
         
        #
        #..........................Combine Hillshade / Slope / Aspect .........................................................Line 92
        #
                print
                print "********************:   Combine Hillshade / Slope / Aspect :********************"
                print
                inRasterA10 = (str(dPath)+str(cityq)+"/Aspect/"+str("aspfinal"))
                inRasterHfinal = (str(dPath)+(cityq)+"/Slope/"+str("hillfinal"))                                       #Input, hillfinal (Floating point)
                inRasterCon1 = (str(dPath)+(cityq)+"/Combine/"+str("slpfinal"))                                        #Input, slpfinal (Floating point)

                # Execute PolygonToRaster
                outCombine = Combine([inRasterA10,inRasterHfinal,inRasterCon1])                                  
                # Save the output 
                outCombine.save(str(dPath)+str(cityq)+"/Combine/"+str("comb"))                                         #Output, comb  (Integer)
                del outCombine
                #print "Processed step 25, Combine Hillshade / Slope / Aspectfor the city:" +str(cityq)
                print "Processed step 25, Combine Hillshade / Slope / Aspect"

        #.......................... Combine Extract by Attribute................................................................Line 94 
        #
        #
                print
                print "*********************:  Shade Value  :*********************"
                print
                ShadeTab  = str(bPath)+"/Base_map/LDR.gdb/Shade"                                          # reading attribute values from Hillfinal field
                Shadeqry    =  '"City_1"'+" ='"+str(cityq)+"'"
                print"The Shade value for the city:" +str(cityq)+ " is "+str(Shadeqry)
                Shadelyr1   = arcpy.MakeFeatureLayer_management(ShadeTab,"Shadelyr")
                ShadeTable2 = arcpy.SelectLayerByAttribute_management(Shadelyr1,"NEW_SELECTION",Shadeqry)
                print "The name of city is :"+str(cityq)
                ShadeField = "Hillfinal"
                #sVal = []
                srows = arcpy.SearchCursor(ShadeTable2)
                for row in srows:
                    sVal = row.getValue(ShadeField)
                    #sVal.append(nVal)
                    print"The Shade value for the city:" +str(cityq)+ " is "+str(sVal)
                    inRasterC3 = (str(dPath)+str(cityq)+"/Combine/"+str("comb"))                                          # Input, comb (Integer)
                    var1 = str("aspfinal")
                    var2 = str("hillfinal")
                    inSQLClauseC3 = ('("'+str(var1)+ '" = 0 OR ''"'+str(var1)+'" = 1 OR ''"'+str(var1)+'" = 2 OR ''"'+str(var1)+'" = 3 OR ''"'+str(var1)+'" = 4 OR ''"'+str(var1)+'" = 5 OR ''"'+str(var1)+'" = 6 OR ''"'+str(var1)+'" = 7 OR ''"'+str(var1)+'" = 8) AND ''"'+str(var2)+'" > '+str(sVal))                    #print inSQLClauseC3
                    attExtractC3 = ExtractByAttributes(inRasterC3, inSQLClauseC3) 
                    # Save the output 
                    attExtractC3.save(str(dPath)+str(cityq)+"/Combine/"+str("combs"))                                   #Output 1, combs (Integer)
                    del attExtractC3
                    #print "line 94, Combine 1 Extract with attribute for the city:" +str(cityq)
                    inSQLClauseC4 = ('("'+str(var1)+ '" = 0 OR ''"'+str(var1)+'" = 1 OR ''"'+str(var1)+'" = 2 OR ''"'+str(var1)+'" = 3 OR ''"'+str(var1)+'" = 4 OR ''"'+str(var1)+'" = 5 OR ''"'+str(var1)+'" = 6 OR ''"'+str(var1)+'" = 7 OR ''"'+str(var1)+'" = 8) AND ''"'+str(var2)+'" > '+str(sVal))
                    #print inSQLClauseC4
                    attExtractC4 = ExtractByAttributes(inRasterC3, inSQLClauseC4) 
                    # Save the output 
                    attExtractC4.save(str(dPath)+str(cityq)+"/Combine/"+str("combew"))                                   #Output 2,  combew (Integer)
                    del attExtractC4
                print
                print "Processed step 26 A & 26 B, Combine, Extract by attribute"
                print "Now running LiDarP27 script to process steps 27 A & 27 B"

         # SCRIPT 27
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                print "not now"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                print "now"
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        #print "The City being analyzed:" +str(qry1)

                arcpy.env.workspace  = str(dPath)+str(cityq)
                # Set Snap Raster environment
                arcpy.env.snapRaster = str(dPath)+str(cityq)+str(dsm)
                inRaster = str(dPath)+str(cityq)+str(dsm)
                #print inRaster

        ##
                arcpy.env.workspace  = (str(dPath)+str(cityq)+"/Buildings/")
                fcs = arcpy.ListFeatureClasses()
                for fc in fcs:
                    fc2 = fc
                inMaskData = fc2               #Building layer
                #print inMaskData

        #
        #================================================.Selecting the data based on City Query.===============================>
        #
                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)
                lyrz2 = arcpy.MakeFeatureLayer_management(inTablez,"lyrz")
                inTablez2 = arcpy.SelectLayerByAttribute_management(lyrz2,"NEW_SELECTION",qry1)
                cnt = arcpy.GetCount_management(inTablez2)
                #print "number of selected record is:"+str(cnt)


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #
        #.......................... Combine ................................................................Line 98 & 99
        #
                print
                print "*********************:  Combine  :*********************"
                print
                arcpy.env.overwriteOutput = True
                outFolderP1 = (str(dPath)+str(cityq)+"/Combine")
                outName1   =  "combine.gdb"
##                if os.path.exists(outFolderP1 + '/combine.gdb'):
##                        os.remove(outFolderP1 + '/combine.gdb')
                arcpy.CreateFileGDB_management(outFolderP1, outName1)
                print('created...')
                inRasterC5 = (str(dPath)+str(cityq)+"/Combine/"+str("combs"))                                           #Input, combs (Integer)
                FieldC5 = "VALUE"       
                outPolygonsC5 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_poly")                               #Output, combs_poly (Feature Class)
##                outPolygonsC5 = arcpy.MakeFeatureLayer_management(outFolderP1+"combs_poly.shp", 'combs_poly') #******************* THIS MIGHT BREAK THINGS ***********************
                arcpy.RasterToPolygon_conversion(inRasterC5, outPolygonsC5, "NO_SIMPLIFY", FieldC5)
                arcpy.FeatureClassToShapefile_conversion(outPolygonsC5, outFolderP1)                                     #To use for UTM projection in step 38
                #print "Processed step 27 A, Combine raster to polygon for the city:" +str(cityq)
                print "Processed step 27 A, Combine raster to polygon"
        #..........................................................................................................................................
                inRasterC6 = (str(dPath)+str(cityq)+"/Combine/"+str("combew"))                                          #Input, combew   (Integer)
                FieldC6 = "VALUE"
                outPolygonsC6 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_poly")                              #Output, combew_poly (shapefile)
                arcpy.RasterToPolygon_conversion(inRasterC6, outPolygonsC6, "NO_SIMPLIFY", FieldC6)
                print "Processed step 27 B, Combine raster to polygon"
                print "Please run LiDarP28 script to process steps 28 A & 28 B"
                print

        # SCRIPT 28
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        #print "The City being analyzed:" +str(qry1)

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))
                inRaster = (str(dPath)+str(cityq)+str(dsm))

        ##
                arcpy.env.workspace  = (str(dPath)+str(cityq)+"/Buildings/")
                fcs = arcpy.ListFeatureClasses()
                for fc in fcs:
                    fc2 = fc
                inMaskData = fc2               #Building layer

        #
        #================================================.Selecting the data based on City Query.===============================>
        #
                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)
                lyrz2 = arcpy.MakeFeatureLayer_management(inTablez,"lyrz")
                inTablez2 = arcpy.SelectLayerByAttribute_management(lyrz2,"NEW_SELECTION",qry1)
                cnt = arcpy.GetCount_management(inTablez2)

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #.......................... Join raster and shapefiles tables................................................................Line 102
        #   
        #         # Set local variables for combs join
                print
                print "*********************:  Join raster and shapefiles tables  :********************"
                print
                inRasterC5 = (str(dPath)+str(cityq)+"/Combine/"+str("combs"))        
                env.qualifiedFieldNames = False
                inFeatureJ1 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_poly")                    #Input, combs_poly
                layerNameJ1 = "Combs_poly"
                joinFieldJ1 = "gridcode"
                #joinFieldJ1 = "grid_code"
                #inRasterC5 # combs
                joinFieldJ2 = "VALUE"
                outFeatureJ1 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_poly2")                   #Output, combs_poly2
                arcpy.MakeFeatureLayer_management (inFeatureJ1,  layerNameJ1)        
                # Join the feature layer to a table
                arcpy.AddJoin_management(layerNameJ1, joinFieldJ1, inRasterC5, joinFieldJ2, "KEEP_ALL")  #created new layer combs_poly2 with join fields              
                # Copy the layer to a new permanent feature class
                arcpy.CopyFeatures_management(layerNameJ1, outFeatureJ1)
                fieldLength = 3        
                arcpy.AddField_management(outFeatureJ1,"SLPF", "LONG","", "",fieldLength)
                Field33B =  "vat_SLPFINAL"
                arcpy.CalculateField_management(outFeatureJ1,"SLPF","!"+str(Field33B)+"!","PYTHON_9.3","")
                dField = ["Id","gridcode","vat_Rowid","vat_VALUE","vat_COUNT","vat_ASPFINAL","vat_HILLFINAL","vat_SLPFINAL"]
                fList = arcpy.ListFields(outFeatureJ1)
                nameList = []        
                for f in fList:
                        nameList.append(f.name)
                        
##      this thing keeps breaking
##                for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(outFeatureJ1,f2)
##
                print "Processed step 28 A, Join of  raster & polygon tables (combs_poly2)"

        #.......................................................................................................................
                 # Set local variables for combew join
                inRasterC6 = (str(dPath)+str(cityq)+"/Combine/"+str("combew"))
                env.qualifiedFieldNames = False
                inFeatureJ3 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_poly")                        #Input, combew_poly
                layerNameJ2 = "Combs_poly2"
                joinFieldJ2 = "gridcode"
                #inRasterC6 # combew (_cob)
                joinFieldJ3 = "VALUE"
                outFeatureJ3 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_poly2")                      #Output, combew_poly2
                arcpy.MakeFeatureLayer_management (inFeatureJ3,  layerNameJ2)        
                # Join the feature layer to a table
                arcpy.AddJoin_management(layerNameJ2, joinFieldJ2, inRasterC6, joinFieldJ3, "KEEP_ALL")  #created new layer combew_poly2 with join fields              
                # Copy the layer to a new permanent feature class
                arcpy.CopyFeatures_management(layerNameJ2, outFeatureJ3)        
                inFeatureJ33 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_poly2")   #Input, combew_poly2
                #inFeatureJ33 = "Z:/Temp/Denver/Denver1/combine.gdb/combew_poly2" 
                fieldLength = 3               
                arcpy.AddField_management(inFeatureJ33,"SLPF", "LONG","", "",fieldLength) # (for tuple * and , )
                Field34B =  "vat_SLPFINAL"
                arcpy.CalculateField_management(inFeatureJ33,"SLPF","!"+str(Field34B)+"!","PYTHON_9.3","")
                dField = ["Id","gridcode","vat_Rowid","vat_VALUE","vat_COUNT","vat_ASPFINAL","vat_HILLFINAL","vat_SLPFINAL"]
                fList = arcpy.ListFields(inFeatureJ33)
                nameList = [f.name for f in arcpy.ListFields(inFeatureJ33)]        

##
##                        for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(inFeatureJ33,f2)
                print "Processed step 28 B, Join of  raster & polygon tables (combew_poly2)"
                print
                print "Now running LiDarP29A script to process step 29 A"
                print

        # SCRIPT 29A
        #===============d===============================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                print "step 29a: 1"
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        #print "The City being analyzed:" +str(qry1)

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))

        #..........................................................................
                # Set local variables
                print
                print "********:  Dissolve polygon by Slope Final Field of combs_poly2  :********"
                print
                inFeatureD2      = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_poly2")                          # Input,  combs_poly2
                outFeatureClass2 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_slppoly")
                arcpy.AddField_management(inFeatureD2, "SLPF_1", "SHORT", "", "", "", "", "", "", "")   #create a new SHORT integer field for dissolve field, rather than LONG integer (memory crash)-- KEW
                arcpy.CalculateField_management(inFeatureD2, "SLPF_1", "!SLPF!", "PYTHON_9.3")    #populate new SHORT int w/correct numbers
                dissolveFields = "SLPF_1"     
                # Execute Dissolve using LANDUSE and TAXCODE as Dissolve Fields
##                arcpy.Dissolve_management(inFeatureD2, outFeatureClass2, dissolveFields, "FIRST" , "SINGLE_PART", "DISSOLVE_LINES")           #not working, returns mem allocation error
                arcpy.Dissolve_management(inFeatureD2,outFeatureClass2 ,dissolve_field="SLPF_1",statistics_fields="#",multi_part="SINGLE_PART",unsplit_lines="DISSOLVE_LINES")   #Output, cs_slppoly
                print "Processed step 29 A, Dissolve by field SLPF"
                print
                print "Now running LiDarP29B script to process step 29 B"
                print
                

        # SCRIPT 29B
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        #print "The City being analyzed:" +str(qry1)

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))

        # Set local variables
                print
                print "********:  Dissolve polygon by Slope Final Field of combew_poly2  :********"
                print
                inFeatureD3      = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_poly2")                         # Input,combew_poly2
                combew_poly22 =  arcpy.MakeFeatureLayer_management(inFeatureD3, "combew_poly22")
                outFeatureClass3 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_slppoly")        
##                dissolveFields = "SLPF"     
                arcpy.AddField_management(combew_poly22, "SLPF_1", "SHORT", "", "", "", "", "", "", "")   #create a new SHORT integer field for dissolve field, rather than LONG integer (memory crash)-- KEW
                arcpy.CalculateField_management(combew_poly22, "SLPF_1", "!SLPF!", "PYTHON_9.3")    #populate new SHORT int w/correct numbers
                dissolveFields = "SLPF_1"     
                # Execute Dissolve using LANDUSE and TAXCODE as Dissolve Fields  
                arcpy.Dissolve_management(combew_poly22, outFeatureClass3, dissolve_field="SLPF_1",statistics_fields="#",multi_part="SINGLE_PART",unsplit_lines="DISSOLVE_LINES")                 #Output, cw_slppoly
                #print "Processed step 29 B, Dissolve (combew_poly2) fields for the city:" +str(cityq)
                print "Processed step 29 B, Dissolve (combew_poly2) by field SLPF"
                print
                print "Now running LiDarP30 script to process steps 30 - 45."
                print

        # SCRIPT 30
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        #print "The City being analyzed:" +str(qry1)

                
                qry1 = '"City_1"'+" ='"+str(cityq)+"'"  
                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)        
                CityName = "City"
                CityF = set()
                cities = arcpy.SearchCursor(inTable2)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq2 = Val1
                        #print "city name is :"+str(cityq)
                        qry2 =  '"City"'+" ='"+str(cityq2)+"'"
                        #print "The City being analyzed:" +str(qry2)

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))
                inRaster = (str(dPath)+str(cityq)+str(dsm))
                #print inRaster

        ##
                arcpy.env.workspace  = (str(dPath)+str(cityq)+"/Buildings/")
                fcs = arcpy.ListFeatureClasses()
                for fc in fcs:
                    fc2 = fc
                inMaskData = fc2               #Building layer

        #
        #....................................................................... Clip to buildings ....................................................Line 107, 110, 113, 117 & 120
        #
                print
                print "*********************:  Clip to buildings  :*********************"
                print
                # Set local variables        
                clip_features = inMaskData
                xy_tolerance = ""
                inFeatureCL2  = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_slppoly")             #Input: cs_slppoly
                out_feature_class2 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_slpClip")     #Output, combs_slpClip       
                # Execute Clip / adding field
                arcpy.Clip_analysis(inFeatureCL2 , clip_features, out_feature_class2, xy_tolerance)              #line 107  (clipping)  Output,& creating combs_slpClip
                #print "Processed step 30 A , Clip (cs_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 30 A, Clip (cs_slppoly)"
                arcpy.AddField_management(out_feature_class2,"flatarea",  "DOUBLE","", "","5")                   #line 110  (adding field)                                 
                geometryField = arcpy.Describe(out_feature_class2).shapeFieldName 
                cursor = arcpy.UpdateCursor(out_feature_class2)        
                for row in cursor:
                    AreaValue = row.getValue(geometryField).area
                    row.setValue("flatarea",AreaValue) #Write area value to field
                    cursor.updateRow(row)
                del row, cursor #Clean up cursor objects
                #print "Processed step 31 A, Clip (cs_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 31 A, Clip (cs_slppoly)"


                arcpy.AddField_management(out_feature_class2,"slopeconv", "DOUBLE","", "","5")                   #line 113  (adding field) 
                expression1 = "1/(math.cos((!SLPF_1!)*3.14/180))"
                arcpy.CalculateField_management(out_feature_class2, "slopeconv", expression1, "PYTHON_9.3", "")   #line 113
                #print "Processed step 32 A, Clip (cs_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 32 A, Clip (cs_slppoly)"
                arcpy.AddField_management(out_feature_class2,"slopearea", "DOUBLE","", "","5")                   #line 117  (adding field) 
                expression2 = "!flatarea!*!slopeconv!"
                arcpy.CalculateField_management(out_feature_class2, "slopearea", expression2, "PYTHON_9.3", "")   #line 117
                #print "Processed step 33 A, Clip (cs_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 33 A, Clip (cs_slppoly)"
                slopeqry1 = '"slopearea" >= 9.99999'                   ## Changed for second round
                #slopeqry1 = '"slopearea" >= 19.99999'
                slplyr1 = arcpy.MakeFeatureLayer_management(out_feature_class2,"slplyr")
                out_featclas22 = arcpy.SelectLayerByAttribute_management(slplyr1,"NEW_SELECTION",slopeqry1)       #line 120
                #slpcnt = arcpy.GetCount_management(out_featclas22)
                #print slpcnt        
                out_featclas222  = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_slpclip10")       #Output, combs_slpclip10
                arcpy.CopyFeatures_management(slplyr1, out_featclas222)                                           
                #print "Processed step 34 A, Clip / Add fields / calculations for the city:" +str(cityq)
                print "Processed step 34 A, Clip (cs_slppoly)"
                #
                #
                #
                # Set local variables
                inFeatureCL3 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_slppoly")           # input: combew_slp_poly
                out_feature_class3 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_slpClip")     # combew_slp_Clip  
                # Execute Clip / adding field
                arcpy.Clip_analysis(inFeatureCL3 , clip_features, out_feature_class3, xy_tolerance)              #line 107  (clipping)& creating combew_slp_Clip
                #print "Processed step 30 B, Clip (cw_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 30 B, Clip (cw_slppoly)"
                arcpy.AddField_management(out_feature_class3,"flatarea",  "DOUBLE","", "","5")                   #line 110  (adding field)        
                CursorFieldNames = ["SHAPE@","flatarea"]  #SHAPE@ is a shape field                               #line 110 calculate geometry
                cursor = arcpy.da.UpdateCursor(out_feature_class3,CursorFieldNames)
                for row in cursor:
                    AreaValue = row[0].area #Read area value as double
                    row[1] = AreaValue #Write area value to field
                    cursor.updateRow(row)
                del row, cursor #Clean up cursor objects
                #print "Processed step 31 B, Clip (cw_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 31 B, Clip (cw_slppoly)"
                arcpy.AddField_management(out_feature_class3,"slopeconv", "DOUBLE","", "","5")                         #line 113  (adding field)
                expression3 = "1/(math.cos((!SLPF_1!)*3.14/180))"
                arcpy.CalculateField_management(out_feature_class3, "slopeconv", expression3, "PYTHON_9.3", "")        #line 113
                #print "Processed step 32 B, Clip (cw_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 32 B, Clip (cw_slppoly)"
                arcpy.AddField_management(out_feature_class3,"slopearea", "DOUBLE","", "","5")                         #line 117  (adding field)        
                expression4 = "!flatarea!*!slopeconv!"
                arcpy.CalculateField_management(out_feature_class3, "slopearea", expression4, "PYTHON_9.3", "")        #line 117
                #print "Processed step 33 B, Clip (cs_slppoly) / Add field  for the city:" +str(cityq)
                print "Processed step 33 B, Clip (cw_slppoly)"
                slopeqry2 = '"slopearea" >= 9.99999'
                #slopeqry2 = '"slopearea" >= 19.99999'
                slplyr2 = arcpy.MakeFeatureLayer_management(out_feature_class3,"slplyr0")
                out_feature_class33 = arcpy.SelectLayerByAttribute_management(slplyr2,"NEW_SELECTION",slopeqry2)       #line 120 
                slpcnt2 = arcpy.GetCount_management(out_feature_class33)
                #print slpcnt2
                out_featclas333 = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_slpclip10")
                arcpy.CopyFeatures_management(slplyr2, out_featclas333)                                                #combew_slpclip10       
                #print "Processed step 34 B, Clip (cw_slppoly) / Add field / calculations for the city:" +str(cityq)
                print "Processed step 34 B, Clip (cw_slppoly)"
        #
        #
        #=================================================. SUMMARY.=================================================================> 

        #
        #.......................... Minimum boundary Geometry ...............................................................................Line 127, 
        #
                print
                print "*********************:  SUMMARIZATION  :*********************"
                print
                # Create variables for the input and output feature classes
                #inBld1 = ("C:/LiDAR/Base_map/"+str(cityq)+str("_2d_buildings")+str(".shp"))
                import arcpy
                outFolderP2 = (str(dPath)+str(cityq)+"/Summary")
                outName2   =  "summary.gdb"
                print "checking summary.gdb exists"
                if arcpy.Exists(outFolderP2 + "/" + outName2):
                        arcpy.Delete_management(outFolderP2 + "/" + outName2)
                        print "summary.gdb removed"
                arcpy.CreateFileGDB_management(outFolderP2, outName2)
                print "summary.gdb created"
                inBld1 = inMaskData
                inBld2 = arcpy.MakeFeatureLayer_management(inBld1, "bldg_lyr")
                inBld3 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/bldg") 
                arcpy.CopyFeatures_management(inBld2,inBld3)
                dField = ["id","AREA_M2","AVGHT_M","MINHT_M","MAXHT_M","BASE_M","LEN","WID","ORIENT8"]
                fList = arcpy.ListFields(inBld3)
                nameList = []        
                for f in fList:
                        nameList.append(f.name)
                for f in nameList:
                        for f2 in dField:
                                if f == f2:
                                   arcpy.DeleteField_management(inBld3,f2)

                #print "Processed step 35,  Minimum boundary Geometry created for city:" +str(cityq)
                print "Processed step 35, copied Feature Class for Minimum boundary Geometry creation"
                #inBld = (str(dPath)+str(cityq)+"/Combine/"+str("bldg")+str(".shp"))                                     ######## needs to creat for every city########################
                outmbg1 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/minboundgeom")                                     
                # Use MinimumBoundingGeometry function to get a convex hull area
                #for each cluster of trees which are multipoint features
                arcpy.MinimumBoundingGeometry_management(inBld3, outmbg1, "CONVEX_HULL", "ALL")                           #Output, minboundgeom
                arcpy.AddField_management(outmbg1,"area_zip", "DOUBLE","", "","5") 
                #print "Processed step 36,  Minimum boundary Geometry created for city:" +str(cityq)
                print "Processed step 36, Minimum boundary Geometry created"
        #
        #.......................... zip file ..................................................................................Line 123, 129
        #        
                inFeatureZ1 = (str(bPath)+"/Base_map/zip.shp")                                                     #Input, zip
                inFeatureZ2 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/minboundgeom")               # clipping layer, minboundgeom
                zip1 = arcpy.MakeFeatureLayer_management(inFeatureZ1, "zip_lyr")
                zip2 = arcpy.SelectLayerByLocation_management (zip1, 'intersect', inFeatureZ2)
                zip3 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/nzip")                       #Output, nzip
                arcpy.CopyFeatures_management(zip2, zip3)                                                #line 123   Zips
                deletefields = ["FIPSSTCO","STATE_FIPS"]
                arcpy.DeleteField_management(zip3,deletefields) #Delete the extra fields from output feature class
                
                #print "Processed step 37,  nzip for city:" +str(cityq)
                print "Processed step 37, nzip created"
                zip4 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zip_utm")                    # for new projection utm       
                outCS = arcpy.SpatialReference(str(dPath)+str(cityq)+"/Combine/"+str("combs_poly.prj"))   #the file use for projection
                #print out_coordinate_system
                arcpy.Project_management(zip3, zip4 ,outCS)
                #print "Processed step 38,  UTM Projection calculated for the zip file of city:" +str(cityq)
                print "Processed step 38, UTM Projection calculated for the zip layer"
                arcpy.AddField_management(zip4,"area_zip", "DOUBLE","", "","5")                          #line 129   Zips
                CursorFieldNameZ = ["SHAPE@","area_zip"]  #SHAPE@ is a shape field                       #line 129 calculate geometry
                cursor = arcpy.da.UpdateCursor(zip4,CursorFieldNameZ)
                for row in cursor:
                    AreaValue = row[0].area #Read area value as double
                    row[1] = AreaValue #Write area value to field        
                    cursor.updateRow(row)
                    del row, cursor #Clean up cursor objects
                #print "Processed step 39, Area calculated for the zip file of city:" +str(cityq)
                print "Processed step 39, Area calculated for the zip layer"
##
##        #
##        #...................................................... Intersect ......................................................................Line 132,
          #
                inFeatures = [zip4, outmbg1]                                                               #Input, zips & minboundgeom
                zipinter = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zips_intersect")           #Output, zips_intersect
                arcpy.Intersect_analysis(inFeatures, zipinter, "", "", "")                                 
                #print "Processed step 40, zips Intersect file created for city:" +str(cityq)
                print "Processed step 40, zips Intersect layer created"
        #
        #...................................................... ...... .....................................................................Line 135,138
        #       
                arcpy.AddField_management(zipinter,"Area_int", "DOUBLE","", "","5")                         #line 135   zips_intersect        
                CursorFieldNameZ = ["SHAPE@","Area_int"]  #SHAPE@ is a shape field                          #line 135 calculate geometry
                cursor = arcpy.da.UpdateCursor(zipinter,CursorFieldNameZ)
                for row in cursor:
                    AreaValue = row[0].area #Read area value as double
                    row[1] = AreaValue #Write area value to field
                    cursor.updateRow(row)
                    del row, cursor #Clean up cursor objects
                #print "Processed step 41, Area_int field added & area calculated for city:" +str(cityq)
                print "Processed step 41, Area_int field added & area calculated"
                
                arcpy.AddField_management(zipinter,"zip_pct", "DOUBLE","", "","5")                         #line 138   zips_intersect
                expression5 = "(!Area_int!/!Area_zip!)"
                arcpy.CalculateField_management(zipinter, "zip_pct", expression5, "PYTHON_9.3", "")        #line 138
                #print "Processed step 42, Percent Area calculated for zip file of city:" +str(cityq)
                print "Processed step 42, Percent Area calculated for zip layer"
        #
        #...................................................... .calculate flate area of building rooftop..........................................................Line 142,
        #
                bld = (str(dPath)+str(cityq)+"/Summary/summary.gdb/bldg")                      #Input, bldg
                arcpy.AddField_management(bld,"Bldg_Area", "DOUBLE","", "","5")                         #line 141   building layer
                arcpy.AddField_management(bld,"Bldg_FID", "LONG","", "","5")
                CursorFieldNameZ = ["OBJECTID","Bldg_FID"]  #SHAPE@ is a shape field                       #line 129 calculate geometry
                cursor = arcpy.da.UpdateCursor(bld,CursorFieldNameZ)
                for row in cursor:
                    AreaValue = row[0] 
                    row[1] = AreaValue        
                    cursor.updateRow(row)
                del row, cursor 
                print "complete"    
                CursorFieldNameZ = ["SHAPE@","Bldg_Area"]  #SHAPE@ is a shape field                     #line 141 calculate geometry
                cursor = arcpy.da.UpdateCursor(bld,CursorFieldNameZ)
                for row in cursor:
                    AreaValue = row[0].area #Read area value as double
                    row[1] = AreaValue #Write area value to field
                    cursor.updateRow(row)
                del row, cursor #Clean up cursor objects
                #print "Processed step 43, bldarea field added & area calculated for city:" +str(cityq)
                print "Processed step 43, bldarea field added & area calculated"

        #
        #..................................................Spatial join... ...... ...........................................................Line 144,      
        #
                out_feature_class = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zips_bldg")           #Output, zips_bldg
                fieldmappings = arcpy.FieldMappings() 
                fieldmappings.addTable(zipinter)   #targetFeatures
                fieldmappings.addTable(bld)        #joinFeatures
                areaField = fieldmappings.findFieldMapIndex("Bldg_Area")
                fieldmap = fieldmappings.getFieldMap(areaField)
                field = fieldmap.outputField
                field.name = "F_Area"
                field.aliasName = "Total_area"
                fieldmap.outputField = field
                fieldmap.mergeRule = "sum"
                fieldmappings.replaceFieldMap(areaField, fieldmap)      
                arcpy.SpatialJoin_analysis(zipinter,bld,out_feature_class,"", "",fieldmappings,"")
                deletefields = ["area_zip_1"]
                arcpy.DeleteField_management(out_feature_class,deletefields)
                #print "Processed step 44, spatial join between zip_intersect and city buildings for city:" +str(cityq)
                print "Processed step 44, spatial join between zip_intersect and city buildings"
        #
        #..................................................Spatial join... ...... ...........................................................Line   148     
        #
                
                combew1    = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_slpclip")    #Input, combew_slp_clip
                combs1     = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_slpclip")     #Input, combs_slp_clip
                combew2    = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combew_slpclip10")  #Input, combew_slp_clip10
                combs2     = (str(dPath)+str(cityq)+"/Combine/combine.gdb/combs_slpclip10")   #Input, combs_slp_clip10
                #output files
                combew11        = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldg")    #Output, combew_bldg     
                combs11         = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldg")    #Output, combs_bldg  
                combew22        = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldg10")    #Output, combew_bldg10  
                combs22         = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldg10.")    #Output, combs_bldg10
                arcpy.SpatialJoin_analysis(combew1,   bld, combew11,  "JOIN_ONE_TO_ONE", "KEEP_ALL","#","INTERSECT","","")
                arcpy.SpatialJoin_analysis(combs1,    bld, combs11,   "JOIN_ONE_TO_ONE", "KEEP_ALL","#","INTERSECT","","")
                arcpy.SpatialJoin_analysis(combew2,   bld, combew22,  "JOIN_ONE_TO_ONE", "KEEP_ALL","#","INTERSECT","","")
                arcpy.SpatialJoin_analysis(combs2,    bld, combs22,   "JOIN_ONE_TO_ONE", "KEEP_ALL","#","INTERSECT","","")
                print "Processed step 45, spatial join between buldings and cliped layers"
                print
                print "Now running LiDarP46 to processe steps 46 & 47"
                print

        # SCRIPT 46
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)
                
        #
        #==============================================.Query for City Name.================================================>
        #
                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"
                        #print "The City being analyzed:" +str(qry1)

                arcpy.env.workspace  = (str(dPath)+str(cityq))
                # Set Snap Raster environment
                arcpy.env.snapRaster = (str(dPath)+str(cityq)+str(dsm))
                
        #............................................................................................................

        #
        #..................................................Dissolve... ...... .............................................................Line 153    
        #
                print
                print "*********************:  Final Steps 46 - 49   :*********************"
                print
                combew11        = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldg")    #Output, combew_bldg     
                combs11         = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldg")    #Output, combs_bldg  
                combew22        = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldg10")    #Output, combew_bldg10  
                combs22         = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldg10")    #Output, combs_bldg10
                outFC1 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldgdissolve")       #Output, combew_bldg
                outFC2 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldgdissolve")       #Output, combS_bldg
                outFC3 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldgdissolve10")       #Output, combew_bldg10
                outFC4 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldgdissolve10")       #Output, combS_bldg10 
                # Execute Dissolve using LANDUSE and TAXCODE as Dissolve Fields
                arcpy.Dissolve_management(combew11, outFC1,"Bldg_FID",[["Bldg_Area","MEAN"],["SLPF_1","MEAN"],["flatarea","SUM"],["slopeconv","MEAN"],["slopearea","SUM"]],  "MULTI_PART", "DISSOLVE_LINES") #combew_bldg_dissolve
                arcpy.Dissolve_management(combs11,  outFC2,"Bldg_FID",[["Bldg_Area","MEAN"],["SLPF_1","MEAN"],["flatarea","SUM"],["slopeconv","MEAN"],["slopearea","SUM"]],  "MULTI_PART", "DISSOLVE_LINES") #combs_bldg_dissolve
                arcpy.Dissolve_management(combew22, outFC3,"Bldg_FID",[["Bldg_Area","MEAN"],["SLPF_1","MEAN"],["flatarea","SUM"],["slopeconv","MEAN"],["slopearea","SUM"]],  "MULTI_PART", "DISSOLVE_LINES") #combew_bldg_dissolve10
                arcpy.Dissolve_management(combs22,  outFC4,"Bldg_FID",[["Bldg_Area","MEAN"],["SLPF_1","MEAN"],["flatarea","SUM"],["slopeconv","MEAN"],["slopearea","SUM"]],  "MULTI_PART", "DISSOLVE_LINES") #combs_bldg_dissolve10
                #print "Processed step 46, Dissolve  fields for the city:" +str(cityq)
                print "Processed step 46, Dissolved"
                
        #......................................................................................................................................
                #Taarget Feature Class
##                zipinter = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zips_intersect")
##                dField = ["FID_zip_utm","FID_minboundgeom","area_zip_1"]
##                fList = arcpy.ListFields(zipinter)
##                nameList = []        
##                for f in fList:
##                        nameList.append(f.name)
##                for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(zipinter,f2)
##                #input feature class
##                inFC1 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldgdissolve")        #Output, combew_bldg
##                inFC2 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldgdissolve")         #Output, combS_bldg
##                inFC3 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combew_bldgdissolve10")      #Output, combew_bldg10
##                inFC4 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/combs_bldgdissolve10")       #Output, combS_bldg10
##                #Output Feature Class
##                outFCZ1 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zip_combew")                 #Output, combew_bldg
##                outFCZ2 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zip_combs")                  #Output, combS_bldg
##                outFCZ3 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zip_combew10")               #Output, combew_bldg10
##                outFCZ4 = (str(dPath)+str(cityq)+"/Summary/summary.gdb/zip_combs10")                #Output, combS_bldg10
##                inFC   = [inFC1,inFC2,inFC3,inFC4]
##                outFC  = [outFCZ1,outFCZ2,outFCZ3,outFCZ4]                     
##                for FC1,FC2 in zip (inFC,outFC):
##                        fms = arcpy.FieldMappings()
##                        fms.addTable(zipinter)  #Target Feature Class
##                        fms.addTable(FC1)
##                        #print "fc is: " +str(FC1)
##                        AF1                = fms.findFieldMapIndex("MEAN_Bldg_Area") #("Bldg_Area")  # Mean_Building_Area   
##                        fm1                = fms.getFieldMap(AF1)
##                        fmname1             = fm1.outputField     
##                        fmname1.name       = "M_Barea"
##                        fmname1.aliasName  = "M_Barea"   # Average of Mean_Building_Area
##                        fm1.outputField    = fmname1
##                        fm1.mergeRule      = "mean"
##
##                        AF2                = fms.findFieldMapIndex("MEAN_SLPF") #("Bldg_Area")  # Mean_Building_Area
##                        fm2                = fms.getFieldMap(AF2)
##                        fmname2            = fm2.outputField     
##                        fmname2.name       = "M_SlP"
##                        fmname2.aliasName  = "M_SLP"   # Average of Mean_Building_Area
##                        fm2.outputField    = fmname2
##                        fm2.mergeRule      = "mean"
##
##                        AF3                = fms.findFieldMapIndex("SUM_flatarea") #("Bldg_Area")  # Mean_Building_Area
##                        fm3                = fms.getFieldMap(AF3)
##                        fmname3            = fm3.outputField     
##                        fmname3.name       = "S_FArea"
##                        fmname3.aliasName  = "S_Flatarea"   # Average of Mean_Building_Area
##                        fm3.outputField    = fmname3
##                        fm3.mergeRule      = "sum"
##
##                        AF4                = fms.findFieldMapIndex("MEAN_slopeconv") #("Bldg_Area")  # Mean_Building_Area
##                        fm4                = fms.getFieldMap(AF4)
##                        fmname4            = fm4.outputField     
##                        fmname4.name       = "M_SCarea"
##                        fmname4.aliasName  = "M_Slopconv"   # Average of Mean_Building_Area
##                        fm4.outputField    = fmname4
##                        fm4.mergeRule      = "mean"
##
##                        AF5                = fms.findFieldMapIndex("SUM_slopearea") #("Bldg_Area")  # Mean_Building_Area
##                        fm5                = fms.getFieldMap(AF5)
##                        fmname5            = fm5.outputField     
##                        fmname5.name       = "S_Sarea"
##                        fmname5.aliasName  = "S_Sloparea"   # Average of Mean_Building_Area
##                        fm5.outputField    = fmname5
##                        fm5.mergeRule      = "sum"
##                                
##                        fms.replaceFieldMap(AF1,fm1)
##                        fms.replaceFieldMap(AF2,fm2)
##                        fms.replaceFieldMap(AF3,fm3)
##                        fms.replaceFieldMap(AF4,fm4)
##                        fms.replaceFieldMap(AF5,fm5)
##                        arcpy.SpatialJoin_analysis(zipinter,FC1,FC2,"JOIN_ONE_TO_ONE", "KEEP_ALL",fms,"INTERSECT")

                print "Processed step 47, Quad Summary for the city:" +str(cityq)
              
                print "Step 48: Repair combew geometries" 
                arcpy.RepairGeometry_management(combew11)           

                print "Step 49: Intersect combew_bldgs against aspfinal_poly"      
                arcpy.Intersect_analysis([combew11, (str(dPath)+str(cityq)+"/Aspect/aspfinal_poly.shp")], (str(dPath)+str(cityq)+"/Summary/summary.gdb/developable_planes"))

                print "Analysis completed for the city of: "+str(cityq)
                print "Creating files for final summary: "+str(cityq)

        # COPYFILESUMMARY
        #==============================================.Query for City Needed to be analyzed.================================================>
        #
                exprInTab =  "!Analyzed!+!Process!"
                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
                V1 = 'NY'
                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
                #print qryInTab
                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
                cnt = arcpy.GetCount_management(inTableA)
                #print "number of Cities selected:"+str(cnt)

                CityName = "City_1"
                CityF = set()
                #cities = arcpy.SearchCursor(inTable)
                cities = arcpy.SearchCursor(inTableA)
                for cityn in cities:
                    CityF.add(cityn.getValue(CityName))
                    #print "List of cities needs to be analyzed:" + str(CityF)
                    for Val1 in CityF:
                        cityq = Val1
                        #print "city name is :"+str(cityq)
                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"           
                        #print "The Part of City being analyzed:" +str(qry1)
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##                print
##                print "*********************:  Copying for Final Summarization    :*********************"
##                print
##
##        # Step 1: Creation of folders and sub folders
##        #       Creation of Folder "FinalSummary"
##                outfolderPath1 = str(dPath)#+str(cityq)
##                folderName1    = "FinalSummary"
##                arcpy.CreateFolder_management(outfolderPath1,folderName1) # creates folder by the name of FinalSummary
##                print "Folder created:"+str(dPath)+"/FinalSummary"
##        # Step 2: Creation of sub folders
##        # Query by city name
##                FPath = str(dPath)+"/FinalSummary/"
##                qry1 = '"City_1"'+" ='"+str(cityq)+"'"  
##                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
##                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)        
##                CityName = "City"
##                CityF = set()
##                cities = arcpy.SearchCursor(inTable2)
##                for cityn in cities:
##                    CityF.add(cityn.getValue(CityName))
##                    #print "List of cities needs to be analyzed:" + str(CityF)
##                    for Val1 in CityF:
##                        cityq2 = Val1
##                        #print "city name is :"+str(cityq)
##                        qry2 =  '"City"'+" ='"+str(cityq2)+"'"
##                        #print "The City being analyzed:" +str(qry2)
##        # Query for the state name
##                qry1 = '"City_1"'+" ='"+str(cityq)+"'"   
##                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
##                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)        
##                StateName = "STATE"
##                State = set()
##                states = arcpy.SearchCursor(inTable2)
##                for staten in states:
##                    State.add(staten.getValue(StateName))
##                    #print "List of State needs to be analyzed:" + str(staten)
##                    for Val1 in State:
##                        stateq2 = Val1
##                        #print "city name is :"+str(cityq)
##                        qry3 =  '"State"'+" ='"+str(stateq2)+"'"
##                        #print "Name of the State of the City being analyzed:" +str(qry3)
##        # Create a sub folder by City name and State (CityName_State) with in FinalSummary Folder. 
##                folderName3    = str(cityq2)+'_'+str(stateq2)
##                outfolderPath3 = str(FPath)
##                arcpy.CreateFolder_management(outfolderPath3,folderName3) 
##        #Step 4: Creation of Folder by City Name and Year
##        # Query by year
##                YearName = "Year_"
##                YearF = set()
##                Years = arcpy.SearchCursor(inTable2)
##                for yearn in Years:
##                    YearF.add(yearn.getValue(YearName))
##                    #print "List of years needs to be analyzed:" + str(YearF)
##                    for Val1 in YearF:
##                        year2 = Val1
##                        #print "city name is :"+str(cityq)
##                        qry4 =  '"Year_"'+" ='"+str(year2)+"'"
##                        #print "The Year being analyzed:" +str(qry4)     
##        # Create a sub folder by City name and year (CityName_Year) with in CityName_State        
##                folderName4    = str(cityq2)+'_'+str(year2)
##                FPath4      = str(FPath)+str(folderName3)
##                #print "Sub_Folder 1:"+str(FPath4)
##                outfolderPath4 = str(FPath4)
##                # c:/LiDAR/FinalSummary/CityName_State
##                arcpy.CreateFolder_management(outfolderPath4,folderName4)
##
##        #Step 4: Creation of a geodatabase by name of city section.
##                FPath5 = (str(outfolderPath4)+"/"+str(folderName4)+"/")
##                #print "Sub_Folder 2:"+str(FPath5)
##                outName1   =  str(cityq)
##                arcpy.CreateFileGDB_management(FPath5, outName1)
##                
##        #Step 5: Copy all the required files from the summary.gdb to the new gedatabases (the one just created).
##                FPath2 = (str(dPath)+str(cityq)+"/summary/summary.gdb/")
##                inFC1  = (str(FPath2)+"zip_combew")       
##                inFC2  = (str(FPath2)+"zip_combew10")         
##                inFC3  = (str(FPath2)+"zip_combs")      
##                inFC4  = (str(FPath2)+"zip_combs10")
##                inFC5  = (str(FPath2)+"zips_bldg")
##                FPath6 = (str(FPath5)+str(cityq)+".gdb/")
##                #print "Database Folder:"+str(FPath6)
##                outFC1 = (str(FPath6)+"zip_combew1")       
##                outFC2 = (str(FPath6)+"zip_combew101")         
##                outFC3 = (str(FPath6)+"zip_combs1")      
##                outFC4 = (str(FPath6)+"zip_combs101")
##                outFC5 = (str(FPath6)+"zips_bldg")
##        #
##                inFC   = [inFC1,inFC2,inFC3,inFC4,inFC5]
##                outFC   = [outFC1,outFC2,outFC3,outFC4,outFC5]
##                for FC1,FC2 in zip (inFC,outFC):
##                    arcpy.Copy_management(FC1, FC2)#,{data_type})
##
##                print "Features classes copied successfully for Final Summary"# to Folder."+str(FPath6)
##                print
##
##        # QUADSUMMARY
##        #==============================================.Query for City Needed to be analyzed.================================================>
##        #
##                exprInTab =  "!Analyzed!+!Process!"
##                arcpy.CalculateField_management(inTable, "AP", exprInTab, "PYTHON_9.3", "")
##                V1 = 'NY'
##                qryInTab  =  '"AP"'+" ='"+str(V1)+"'"       
##                #print qryInTab
##                InTab1 = arcpy.MakeFeatureLayer_management(inTable,"InTab")
##                inTableA = arcpy.SelectLayerByAttribute_management(InTab1,"NEW_SELECTION",qryInTab)
##                cnt = arcpy.GetCount_management(inTableA)
##                #print "number of Cities selected:"+str(cnt)
##
##                CityName = "City_1"
##                CityF = set()
##                #cities = arcpy.SearchCursor(inTable)
##                cities = arcpy.SearchCursor(inTableA)
##                for cityn in cities:
##                    CityF.add(cityn.getValue(CityName))
##                    #print "List of cities needs to be analyzed:" + str(CityF)
##                    for Val1 in CityF:
##                        cityq = Val1
##                        #print "city name is :"+str(cityq)
##                        qry1 =  '"City_1"'+" ='"+str(cityq)+"'"           
##                        #print "The Part of City being analyzed:" +str(qry1)
##        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##        # Step 1: Creation of folders and sub folders
##        #       Crearion of Folder "FinalSummary"
##                outfolderPath1 = str(dPath)#+str(cityq)
##                folderName1    = "QuadSummary"
##                arcpy.CreateFolder_management(outfolderPath1,folderName1) # creates folder by the name of FinalSummary
##                #print "Folder created:"+str(dPath)+"/FinalSummary"
##        # Step 2: Creation of sub folders
##        # Query by city name
##                FPath = str(dPath)+"QuadSummary/"
##                qry1 = '"City_1"'+" ='"+str(cityq)+"'"  
##                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
##                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)        
##                CityName = "City"
##                CityF = set()
##                cities = arcpy.SearchCursor(inTable2)
##                for cityn in cities:
##                    CityF.add(cityn.getValue(CityName))
##                    #print "List of cities needs to be analyzed:" + str(CityF)
##                    for Val1 in CityF:
##                        cityq2 = Val1
##                        #print "city name is :"+str(cityq)
##                        qry2 =  '"City"'+" ='"+str(cityq2)+"'"
##                        #print "The City being analyzed:" +str(qry2)
##        # Query for the state name
##                qry1 = '"City_1"'+" ='"+str(cityq)+"'"   
##                lyr1 = arcpy.MakeFeatureLayer_management(inTable,"lyr")
##                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry1)        
##                StateName = "STATE"
##                State = set()
##                states = arcpy.SearchCursor(inTable2)
##                for staten in states:
##                    State.add(staten.getValue(StateName))
##                    #print "List of State needs to be analyzed:" + str(staten)
##                    for Val1 in State:
##                        stateq2 = Val1
##                        #print "city name is :"+str(cityq)
##                        qry3 =  '"State"'+" ='"+str(stateq2)+"'"
##                        #print "Name of the State of the City being analyzed:" +str(qry3)
##        # Create a sub folder by City name and State (CityName_State) with in FinalSummary Folder. 
##                folderName3    = str(cityq2)+'_'+str(stateq2)
##                outfolderPath3 = str(FPath)
##                arcpy.CreateFolder_management(outfolderPath3,folderName3) 
##        #Step 4: Creation of Folder by City Name and Year
##        # Query by year
##                YearName = "Year_"
##                YearF = set()
##                Years = arcpy.SearchCursor(inTable2)
##                for yearn in Years:
##                    YearF.add(yearn.getValue(YearName))
##                    #print "List of years needs to be analyzed:" + str(YearF)
##                    for Val1 in YearF:
##                        year2 = Val1
##                        #print "city name is :"+str(cityq)
##                        qry4 =  '"Year_"'+" ='"+str(year2)+"'"
##                        #print "The Year being analyzed:" +str(qry4)     
##        # Create a sub folder by City name and year (CityName_Year) with in CityName_State        
##                folderName4    = str(cityq2)+'_'+str(year2)
##                FPath4      = str(FPath)+str(folderName3)
##                #print "Sub_Folder 1:"+str(FPath4)
##                outfolderPath4 = str(FPath4)
##                # c:/LiDAR/FinalSummary/CityName_State
##                arcpy.CreateFolder_management(outfolderPath4,folderName4) 
##
##        #Step 4: Creation of a geodatabase by name of city section.
##                FPath5 = (str(outfolderPath4)+"/"+str(folderName4)+"/")
##                #print "Sub_Folder 2:"+str(FPath5)
##                outName1   =  str(cityq)
##                arcpy.CreateFileGDB_management(FPath5, outName1)
##                print FPath5
##
##        # Quad SUMMARY *****************************************************************************
##                print
##                print "*********************:  Quad Summary    :*********************"
##                print
##        #Step 5: Creation of a geodatabase by name of city quad summary.
##                QPath7 = (str(FPath5))
##                #print FPath5
##                #print QPath7       
##                arcpy.CreateFileGDB_management(QPath7, outName1)
##        #Step 6: Copy all the required files from the summary.gdb to the new gedatabases (the one just created).
##                FPath2 = (str(dPath)+str(cityq)+"/summary/summary.gdb/")
##                inFC1  = (str(FPath2)+"zip_combew")       
##                inFC2  = (str(FPath2)+"zip_combew10")         
##                inFC3  = (str(FPath2)+"zip_combs")      
##                inFC4  = (str(FPath2)+"zip_combs10")
##                inFC5  = (str(FPath2)+"zips_bldg")
##                QPath8 = (str(QPath7)+str(cityq)+".gdb/")
##                #print "Database Folder:"+str(QPath8)
##                outFC1 = (str(QPath8)+"zip_combew1")       
##                outFC2 = (str(QPath8)+"zip_combew101")         
##                outFC3 = (str(QPath8)+"zip_combs1")      
##                outFC4 = (str(QPath8)+"zip_combs101")
##                outFC5 = (str(QPath8)+"zips_bldg")
##        #
##                inFC   = [inFC1,inFC2,inFC3,inFC4,inFC5]
##                outFC   = [outFC1,outFC2,outFC3,outFC4,outFC5]
##                for FC1,FC2 in zip (inFC,outFC):
##                    arcpy.Copy_management(FC1, FC2)#,{data_type})
##        #.............................................1
##                inZips1 = (str(QPath8)+"zip_combs1")
##                outFC2 = (str(QPath8)+"zip_combs")
##                arcpy.Dissolve_management(inZips1, outFC2, "ObjectID",[["Join_Count","SUM"],["S_FArea","SUM"]], "", "DISSOLVE_LINES")
##                fieldPrecision = 9        
##                arcpy.AddField_management(outFC2,"Count_south", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_Join_Count"
##                calcField   =  "Count_south"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")
##                #fieldPrecision = 6       
##                arcpy.AddField_management(outFC2,"Flatarea_south", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_S_FArea"  # Alias is "S_Flatarea"
##                calcField   =  "Flatarea_south"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")      
##                dField = ["SUM_Join_Count","TARGET_FID","ZIP_NAME","COUNTY","STATE","ObjectID","area_zip","Area_int","zip_pct","Bldg_FID","M_Barea","M_SlP","SUM_S_FArea","M_SCarea","S_Sarea"]
##                fList = arcpy.ListFields(outFC2)
##                nameList = []        
##                for f in fList:
##                        nameList.append(f.name)
##                for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(outFC2,f2)
##
##        #.............................................2
##                inZips1 = (str(QPath8)+"zip_combew1")
##                outFC2 = (str(QPath8)+"zip_combew")
##
##                arcpy.Dissolve_management(inZips1, outFC2, "ObjectID",[["Join_Count","SUM"],["S_FArea","SUM"]], "", "DISSOLVE_LINES")
##
##                arcpy.AddField_management(outFC2,"Count_eastwest", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_Join_Count"
##                calcField   =  "Count_eastwest"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")
##                #fieldPrecision = 6       
##                arcpy.AddField_management(outFC2,"Flatarea_eastwest", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_S_FArea"  # Alias is "S_Flatarea"
##                calcField   =  "Flatarea_eastwest"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")      
##                dField = ["SUM_Join_Count","TARGET_FID","ZIP_NAME","COUNTY","STATE","ObjectID","area_zip","Area_int","zip_pct","Bldg_FID","M_Barea","M_SlP","SUM_S_FArea","M_SCarea","S_Sarea"]
##                fList = arcpy.ListFields(outFC2)
##                nameList = []        
##                for f in fList:
##                        nameList.append(f.name)
##                for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(outFC2,f2) 
##
##        #.............................................3
##                inZips1 = (str(QPath8)+"zip_combs101")
##                outFC2 = (str(QPath8)+"zip_combs10")
##                arcpy.Dissolve_management(inZips1, outFC2, "ObjectID",[["Join_Count","SUM"],["S_FArea","SUM"]], "", "DISSOLVE_LINES")
##                #fieldPrecision = 6       
##                arcpy.AddField_management(outFC2,"Count_south10", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_Join_Count"
##                calcField   =  "Count_south10"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")
##                #fieldPrecision = 6       
##                arcpy.AddField_management(outFC2,"Flatarea_south10", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_S_FArea"  # Alias is "S_Flatarea"
##                calcField   =  "Flatarea_south10"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")      
##                dField = ["SUM_Join_Count","TARGET_FID","ZIP_NAME","COUNTY","STATE","ObjectID","area_zip","Area_int","zip_pct","Bldg_FID","M_Barea","M_SlP","SUM_S_FArea","M_SCarea","S_Sarea"]
##                fList = arcpy.ListFields(outFC2)
##                nameList = []        
##                for f in fList:
##                        nameList.append(f.name)
##                for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(outFC2,f2)
##
##        #.............................................4
##                inZips1 = (str(QPath8)+"zip_combew101")
##                outFC2 = (str(QPath8)+"zip_combew10")
##
##                arcpy.Dissolve_management(inZips1, outFC2, "ObjectID",[["Join_Count","SUM"],["S_FArea","SUM"]], "", "DISSOLVE_LINES")
##
##                arcpy.AddField_management(outFC2,"Count_eastwest10", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_Join_Count"
##                calcField   =  "Count_eastwest10"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")
##                #fieldPrecision = 6       
##                arcpy.AddField_management(outFC2,"Flatarea_eastwest10", "DOUBLE",fieldPrecision)
##                countField1 =  "SUM_S_FArea"  # Alias is "S_Flatarea"
##                calcField   =  "Flatarea_eastwest10"
##                arcpy.CalculateField_management(outFC2,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")      
##                dField = ["SUM_Join_Count","TARGET_FID","ZIP_NAME","COUNTY","STATE","ObjectID","area_zip","Area_int","zip_pct","Bldg_FID","M_Barea","M_SlP","SUM_S_FArea","M_SCarea","S_Sarea"]
##                fList = arcpy.ListFields(outFC2)
##                nameList = []        
##                for f in fList:
##                        nameList.append(f.name)
##                for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(outFC2,f2)
##
##        #........................
##                
##                inZips1 = (str(QPath8)+"zips_bldg") #################
##                fields1 = [ "Region", "ZIP_NAME2", "COUNTY2", "STATE2"]
##         
##                fieldPrecision = 50
##                for F in fields1:
##                        arcpy.AddField_management(inZips1,F, "TEXT",fieldPrecision)
##
##                countField1 =  '"'+str(cityq2)+'_'+str(stateq2)+'_'+str(year2)+'"'
##                calcField   =  "Region"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!ZIP_NAME!"
##                calcField   =  "ZIP_NAME2"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!COUNTY!"
##                calcField   =  "COUNTY2"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!STATE!"
##                calcField   =  "STATE2"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                dField1 = ["ZIP_NAME", "COUNTY", "STATE"]
##                for dF in dField1:
##                        arcpy.DeleteField_management(inZips1,dF)
##                fields1 = ["ZIP_NAME", "COUNTY", "STATE"]
##                for F in fields1:
##                        arcpy.AddField_management(inZips1,F, "TEXT",fieldPrecision)
##                countField1 =  "!ZIP_NAME2!"
##                calcField   =  "ZIP_NAME"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!COUNTY2!"
##                calcField   =  "COUNTY"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!STATE2!"
##                calcField   =  "STATE"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                dField1 = ["ZIP_NAME2", "COUNTY2", "STATE2"]
##                for dF in dField1:
##                        arcpy.DeleteField_management(inZips1,dF)
##
##                fieldPrecision = 20
##                fields1 = ["Area_zip_meters", "Area_intersect","Zip_percent","Count_total_buildings", "Area_total_buildings"]
##                for F in fields1:
##                        arcpy.AddField_management(inZips1,F, "DOUBLE",fieldPrecision)
##                countField1 =  "!area_zip!"
##                calcField   =  "Area_zip_meters"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!Area_int!"
##                calcField   =  "Area_intersect"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!zip_pct!"
##                calcField   =  "Zip_percent"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "!Join_Count!"
##                calcField   =  "Count_total_buildings"
##                arcpy.CalculateField_management(inZips1,calcField,countField1,"PYTHON_9.3","")
##                countField1 =  "F_Area"  # Alias is "Total_area"
##                calcField   =  "Area_total_buildings"
##                arcpy.CalculateField_management(inZips1,calcField,"!"+str(countField1)+"!","PYTHON_9.3","")      
##                dField = ["Id","bldgarea","area_zip", "Area_int", "zip_pct","Join_Count","TARGET_FID","FID_zip_utm","FID_minboundgeom","F_Area","BLDGID","Bldg_FID"]
##                fList = arcpy.ListFields(inZips1)
##                nameList = []        
##                for f in fList:
##                        nameList.append(f.name)
##                for f in nameList:
##                        for f2 in dField:
##                                if f == f2:
##                                   arcpy.DeleteField_management(inZips1,f2)
##
##                #print "Added the required fields"
##        # intersect
##                outZips2 = (str(QPath8)+"zip_summary2")
##                #print "Output name:"+str(outZips2)
##                arcpy.env.workspace = (str(QPath8))
##                fc = ["zips_bldg","zip_combs","zip_combew","zip_combs10","zip_combew10"]
##                arcpy.Intersect_analysis(fc, outZips2, "NO_FID", "", "INPUT") 
##        # create new layer of selected records to delete the fields with Null values
##                outZips3 = (str(QPath8)+"zip_summary")
##                inTablezs2 = (str(QPath8)+"zip_summary2")
##                qry = '"Count_south" > 0'                   ## Changed for second round
##                lyr1 = arcpy.MakeFeatureLayer_management(inTablezs2,"lyr")
##                inTable2 = arcpy.SelectLayerByAttribute_management(lyr1,"NEW_SELECTION",qry)
##                arcpy.CopyFeatures_management(lyr1, outZips3)
##                arcpy.Delete_management(outZips2, "") 
##                fieldPrecision = 9  
##                newFields = ["Pct_Count_south","Pct_Flatarea_south","Pct_Count_eastwest","Pct_Flatarea_eastwest","Pct_Count_south10"\
##                             ,"Pct_Flatarea_south10","Pct_Count_eastwest10","Pct_Flatarea_eastwest10","Check_s10_count","Check_s10_area"\
##                             ,"Check_ew10_count","Check_ew10_area","Check_south_count","Check_south_area","Check_ew_count","Check_ew_area"\
##                             ,"Check_10_count","Check_10_area"]
##                for NF in newFields:
##                        arcpy.AddField_management(outZips3,NF, "DOUBLE",fieldPrecision)
##
##                expression1 = "(float(!Count_south!)/float(!Count_total_buildings!))"
##                arcpy.CalculateField_management(outZips3, "Pct_Count_south", expression1, "PYTHON_9.3", "")
##
##                expression2 = "(!Flatarea_south!/!Area_total_buildings!)"
##                arcpy.CalculateField_management(outZips3, "Pct_Flatarea_south", expression2, "PYTHON_9.3", "")
##
##                expression3 = "(float(!Count_eastwest!)/float(!Count_total_buildings!))"
##                arcpy.CalculateField_management(outZips3, "Pct_Count_eastwest", expression3, "PYTHON_9.3", "")
##
##                expression4 = "(!Flatarea_eastwest!/!Area_total_buildings!)"
##                arcpy.CalculateField_management(outZips3, "Pct_Flatarea_eastwest", expression4, "PYTHON_9.3", "")
##
##                expression5 = "(float(!Count_south10!)/float(!Count_total_buildings!))"
##                arcpy.CalculateField_management(outZips3, "Pct_Count_south10", expression5, "PYTHON_9.3", "")
##
##                expression6 = "(!Flatarea_south10!/!Area_total_buildings!)"
##                arcpy.CalculateField_management(outZips3, "Pct_Flatarea_south10", expression6, "PYTHON_9.3", "")
##
##                expression7 = "(float(!Count_eastwest10!)/float(!Count_total_buildings!))"
##                arcpy.CalculateField_management(outZips3, "Pct_Count_eastwest10", expression7, "PYTHON_9.3", "")
##
##                expression8 = "(!Flatarea_eastwest10!/!Area_total_buildings!)"
##                arcpy.CalculateField_management(outZips3, "Pct_Flatarea_eastwest10", expression8, "PYTHON_9.3", "")
##
##                expression9 = "(!Count_south!-!Count_south10!)"
##                arcpy.CalculateField_management(outZips3, "Check_s10_count", expression9, "PYTHON_9.3", "")
##
##                expression10 = "(!Flatarea_south!-!Flatarea_south10!)"
##                arcpy.CalculateField_management(outZips3, "Check_s10_area", expression10, "PYTHON_9.3", "")
##
##                expression11 = "(!Count_eastwest!-!Count_eastwest10!)"
##                arcpy.CalculateField_management(outZips3, "Check_ew10_count", expression11, "PYTHON_9.3", "")
##
##                expression12 = "(!Flatarea_eastwest!-!Flatarea_eastwest10!)"
##                arcpy.CalculateField_management(outZips3, "Check_ew10_area", expression12, "PYTHON_9.3", "")
##
##                expression13 = "(!Count_eastwest!-!Count_south!)"
##                arcpy.CalculateField_management(outZips3, "Check_south_count", expression13, "PYTHON_9.3", "")
##                
##                expression14 = "(!Flatarea_eastwest!-!Flatarea_south!)"
##                arcpy.CalculateField_management(outZips3, "Check_south_area", expression14, "PYTHON_9.3", "")
##
##                expression15 = "(!Count_total_buildings!-!Count_eastwest!)"
##                arcpy.CalculateField_management(outZips3, "Check_ew_count", expression15, "PYTHON_9.3", "")
##
##                expression16 = "(!Area_total_buildings!-!Flatarea_eastwest!)"
##                arcpy.CalculateField_management(outZips3, "Check_ew_area", expression16, "PYTHON_9.3", "")
##
##                expression17 = "(!Count_eastwest10!-!Count_south10!)"
##                arcpy.CalculateField_management(outZips3, "Check_10_count", expression17, "PYTHON_9.3", "")
##
##                expression18 = "(!Flatarea_eastwest10!-!Flatarea_south10!)"
##                arcpy.CalculateField_management(outZips3, "Check_10_area", expression18, "PYTHON_9.3", "")
##
##                #print "Final Summary feature classes created successfully"
##
##                arcpy.env.workspace = (str(QPath7))   
##                outfolderPath1 = (str(QPath7))
##                outZips3 = (str(QPath8)+"zip_summary")
##                fc = str(outZips3)
##                rows = arcpy.SearchCursor(fc)
##                CSVFile = (str(QPath7)+"/"+str(cityq)+".csv")
##                fields = [f.name for f in arcpy.ListFields(fc) if f.type <> "Geometry" and f.name.lower() not in ['objectid','shape','shape_length','shape_area']]
##                with open(CSVFile, 'w') as f:
##                    f.write(','.join(fields)+'\n') #csv headers
##                    with arcpy.da.SearchCursor(fc, fields) as cursor:
##                        for row in cursor:
##                            f.write(','.join([str(r) for r in row])+'\n')
##                print "Quad sunmmary feature class exported as CSV file"# for the city of:"+str(folderName1)
##
##                Del1 = (str(QPath8)+"zip_combs1")
##                Del2 = (str(QPath8)+"zip_combs101")
##                Del3 = (str(QPath8)+"zip_combew1")
##                Del4 = (str(QPath8)+"zip_combew101")
##            
##                featurelist = [Del1,Del2,Del3,Del4]        
##                for feature in featurelist:
##                        arcpy.Delete_management(feature, "")
##
##                #print "Features classes copied successfully for Quad Summary to Folder."+str(QPath8)
                print
                print"******************************************************************"
                print"*                  CONGRATULATIONS                               *"
                print"******************************************************************"
                print
        ##        print "Please, run the 'LiDarPDelete' script."
##                arcpy.Delete_management(str(dPath)+str(cityq)+'/reflective_surface'
##                arcpy.Delete_management(str(dPath)+str(cityq)+'/Aspect'
##                arcpy.Delete_management(str(dPath)+str(cityq)+'/HillShade'
##                arcpy.Delete_management(str(dPath)+str(cityq)+'/Reclass'
##                arcpy.Delete_management(str(dPath)+str(cityq)+'/Slope'
##                print "DSM, aspect, hillshade, reclass, slope files deleted."
                EndTime = time.clock()
                time = ((EndTime - StartTime)/60)
                print "Time taken to process "+str(tract_fips)+" is: "+str(time)+" Minutes" 
               
        except Exception as e:
            print e.message
            arcpy.AddError(e.message)
            error_file.write(tract_fips + '------' + e.message)

print("start....")

# Set environment settings
dPath = 'D:/F_Data/data/kwaechte'
fipspath = dPath+'/tracts/' 
all_footprints = '/la_dl/building_footprints/chunks/'
all_dsms = '/la_dl/first_return_raw/chunks/'
modelpath = dPath+'/PV_Rooftop_Model/'

if not os.path.exists(fipspath):
    os.mkdir(fipspath, 0777)

print "mkdir done"

footprintpath = str(dPath)+str(all_footprints)
dsmpath = str(dPath)+str(all_dsms)

tract_fips_list = []
for file in os.listdir(footprintpath):
    if file.endswith('.shp'):
        this_fips = file.replace('.shp','').split('_')[-1]
        this_fips_path = fipspath+this_fips
        tract_fips_list.append(this_fips)
##        if not os.path.exists(this_fips_path):
##                #print(this_fips_path)
##                os.mkdir(this_fips_path, 0777)
            
#print tract_fips_list


error_file = open("D:/F_Data/data/kwaechte/tracts/c"+"_error_tracts_c.txt", 'w')
success_file = open("D:/F_Data/data/kwaechte/tracts/c"+"_success_tracts_c.txt", 'w')

tract_fips_list_c = []
for folder in os.listdir(fipspath+"/c/"):
        tract_fips_list_c.append(folder)

print "remaining c tracts to process: {0}".format(len(tract_fips_list_c))

for tract_fips in tract_fips_list_c:
        print(tract_fips)
        success_file = open("D:/F_Data/data/kwaechte/tracts/c"+"_success_tracts_c.txt", 'a')
        error_file = open("D:/F_Data/data/kwaechte/tracts/c"+"_error_tracts_c.txt", 'a')
        combine_lidar(tract_fips)
        try:
                success_file.close()
                error_file.close()
        except:
                pass
        
        gc.collect()

error_file.close()
