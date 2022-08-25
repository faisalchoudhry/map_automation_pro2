#!/usr/bin/python
# -- coding: utf-8 --
#exec(open('E:/map_automation_pro2/map_automation.py', encoding="utf8").read())

import arcpy
# import importlib
# import sys
# importlib.reload(sys)
# reload(sys)
# sys.setdefaultencoding('utf-8')
# https://stackoverflow.com/a/40346898

import sys
from importlib import reload
reload(sys)

print("Execution started")

aprx = arcpy.mp.ArcGISProject("CURRENT")
layout = aprx.listLayouts()[0]
listMap = aprx.listMaps("Layers")[0]#.listLayers("base")[0]
df = listMap.listLayers("base")[0]
extent = aprx.listMaps("Layers")[0] #Get extent

mapExtents=extent.defaultCamera.getExtent()
mapExtents.lowerLeft

level4Lyr = df.listLayers()[2]
level3Lyr = df.listLayers()[3]
level2Lyr = df.listLayers()[4]
level1Lyr = df.listLayers()[5]
level0Lyr = df.listLayers()[6]
stationLyr = df.listLayers()[7]
accessLyr = df.listLayers()[8]
returnLyr = df.listLayers()[9]
campLyr = df.listLayers()[10]

layerList = [campLyr, returnLyr, accessLyr]

fixedXMin, fixedXMax = mapExtents.XMin, mapExtents.XMax
fixedYMin, fixedYMax = mapExtents.YMin, mapExtents.YMax

print(fixedXMin, fixedYMin, fixedXMax, fixedYMax)

# get current map extent
xmin, xmax = mapExtents.XMin, mapExtents.XMax
ymin, ymax = mapExtents.YMin, mapExtents.YMax

level4Lyr.visible = False
level3Lyr.visible = False
level2Lyr.visible = False
level1Lyr.visible = False
level0Lyr.visible = False

fc = "E:/map_automation_pro/map_automation_pro.gdb/camps"
accessFeatureClass = "E:/map_automation_pro2/map_automation_pro.gdb/access"
exitFeatureClass = "E:/map_automation_pro2/map_automation_pro.gdb/return"
accessFields = ['shape_leng', 'camp__labe', 'access_pat']
exitFields = ['shape_leng', 'camp__labe', 'return_pat']

campLabel_field = "camp__labe"
jamaratLevel_field = "lev_gamart"
campNo_field = "no_camp"
streetNo_field = "no_st"
cursor = arcpy.SearchCursor(fc)

accessLength = 0
exitLength = 0
campLabelText = ''
access_path_name = ''
return_path_name = ''

with arcpy.da.SearchCursor(fc, field_names='*', sql_clause=(None, 'ORDER BY OBJECTID DESC')) as cursor:
    for i, row in enumerate(cursor):
        # if i % 10 == 0:
        # if row[8] == 'muzdlfa 3': #is not None:
        # if "/616" in row[11]:
        # if row[11] == '2/421' or row[11] == '2/114' or row[11] == '5/112' or row[11] == '8/528':
        xmin, xmax = fixedXMin, fixedXMax
        ymin, ymax = fixedYMin, fixedYMax

        # if camp number or street number is null then skip the loop
        if row[2] == None or row[2] == "":
            continue

        # Get camp label form the attribute table of camps
        camp_label = row[2]

        # get value of jamarat level
        level = row[7]

        # #get value of camp number
        # campNo = int(row[4])

        # #get value of street number
        # streetNo = int(row[3])
        print("camp_label",camp_label)

        # select camp layer for changing definition query to show specific camp
        campLyr.definitionQuery = "camp_label = '" + camp_label + "'"

        # select access road layer for changing definition query to show for a specific camp
        accessLyr.definitionQuery = "camp__labe = '" + camp_label + "'"

        # select return road layer for changing definition query to show for a specific camp
        returnLyr.definitionQuery = "camp__labe = '" + camp_label + "'"

        if level == 'Level 0':
            level0Lyr.visible = True
            layerList.append(level0Lyr)
        elif level == 'Level 1':
            level1Lyr.visible = True
            layerList.append(level1Lyr)
        elif level == 'Level 2':
            level2Lyr.visible = True
            layerList.append(level2Lyr)
        elif level == 'Level 3':
            level3Lyr.visible = True
            layerList.append(level3Lyr)
        else:
            level4Lyr.visible = True
            layerList.append(level4Lyr)

        # check for station value, if not null then make them visible and add them to extent list
        # if row[8] != None:
        #     if row[8] == 'Muzdalifah 3':
        #         # muzdlfa3Lyr.visible = True
        #         stationLyr.visible = True
        #         stationLyr.definitionQuery = "station IN ('Muzdalifah 3','Mina 3')"
        #         # layerList.append(muzdlfa3Lyr)
        #         if level4Lyr in layerList: layerList.remove(level4Lyr)
        #         level4Lyr.visible = False
        #         layerList.append(stationLyr)
        #     elif row[8] == 'Mina 2':
        #         # mina2Lyr.visible = True
        #         stationLyr.visible = True
        #         stationLyr.definitionQuery = "station IN ('Mina 2','Mina 3')"
        #         # layerList.append(mina2Lyr)
        #         if level4Lyr in layerList: layerList.remove(level4Lyr)
        #         level4Lyr.visible = False
        #         layerList.append(stationLyr)
        #     elif row[8] == 'Mina 1':
        #         # mina1Lyr.visible = True
        #         stationLyr.visible = True
        #         stationLyr.definitionQuery = "station IN ('Mina 1','Mina 2')"  # , 'mina3'
        #         # layerList.append(mina1Lyr)
        #         if level4Lyr in layerList: layerList.remove(level4Lyr)
        #         level4Lyr.visible = False
        #         layerList.append(stationLyr)
        # else:
        #     # muzdlfa3Lyr.visible = False
        #     # mina2Lyr.visible = False
        #     # mina1Lyr.visible = False
        #     stationLyr.visible = False

        experssion = "camp__labe = '" + camp_label + "'"

        campLabelText = camp_label

        with arcpy.da.SearchCursor(accessFeatureClass, accessFields, where_clause=experssion) as cursor:
            for row in cursor:
                accessLength = int(round(row[0]))
                print("accessLengthaccessLength " , accessLength)
                access_path_name = row[2]
                print("accessLengthaccessLength ", access_path_name)

        with arcpy.da.SearchCursor(exitFeatureClass, exitFields, where_clause=experssion) as cursor:
            for row in cursor:
                exitLength = int(round(row[0]))
                return_path_name = row[2]

        access_path_name = access_path_name #.encode('utf8')
        return_path_name = return_path_name #.encode('utf8')
        print("access_path_name ",access_path_name)
        text_access = "مسار ذهاب - " + access_path_name + " (" + str(accessLength) + " متر" + ")"
        text_return = "مسار عودة - " + return_path_name + " (" + str(exitLength) + " متر" + ")"
        # accessLyr.name = "مسار ذهاب " + str(accessLength) + " متر"
        # returnLyr.name = "مسار عودة " + str(exitLength) + " متر"
        campLyr.name = str(campLabelText)
        accessLyr.name = text_access
        returnLyr.name = text_return
        campLyr.visible = True
        accessLyr.visible = True
        returnLyr.visible = True

        for lyrr in layerList:
            extent = aprx.listMaps("Layers")[0]  # Get extent
            mapExtents = extent.defaultCamera.getExtent()
            ext = mapExtents

            if ext.XMin < xmin:
                xmin = ext.XMin
            if ext.YMin < ymin:
                ymin = ext.YMin
            if ext.XMax > xmax:
                xmax = ext.XMax
            if ext.YMax > ymax:
                ymax = ext.YMax

        df.extent = arcpy.Extent(xmin, ymin, xmax, ymax)

        campLabelFileName = camp_label
        campLabelFileName = campLabelFileName.replace('/', '_')
        # filenamePdf = "E:\ArcmapPdfE\maps_v2" + "\\" + str(1) + "{0:0=3d}".format(campLabelFileName) + "{0:0=2d}".format(campNo) + ".pdf"
        # filenamePdf = "E:\map_automation_pro2\maps_v2" + "\\" + str(campLabelFileName) + ".pdf"
        filename = "E:\map_automation_pro2\maps_v2" + "\\" + str(campLabelFileName) + ".png"
        layout.exportToPDF(filename)  # df_export_width=1654, df_export_height=2339
        layout.exportToPNG(filename, resolution=141)  # df_export_width=1654, df_export_height=2339


        # remove jamarat level, station and tracks
        # del layerList[3]
        if level0Lyr in layerList: layerList.remove(level0Lyr)
        if level1Lyr in layerList: layerList.remove(level1Lyr)
        if level2Lyr in layerList: layerList.remove(level2Lyr)
        if level3Lyr in layerList: layerList.remove(level3Lyr)
        if level4Lyr in layerList: layerList.remove(level4Lyr)
        # if muzdlfa3Lyr in layerList: layerList.remove(muzdlfa3Lyr)
        # if mina2Lyr in layerList: layerList.remove(mina2Lyr)
        # if mina1Lyr in layerList: layerList.remove(mina1Lyr)
        if stationLyr in layerList: layerList.remove(stationLyr)

        level4Lyr.visible = False
        level3Lyr.visible = False
        level2Lyr.visible = False
        level1Lyr.visible = False
        level0Lyr.visible = False
        break
        exit()

# if camp_label == '17/204':
#    break

# for row in cursor:
#    print(row)
#    #Get camp label form the attribute table of camps
#    camp_label = row.getValue(campLabel_field)
#    level = row.getValue(jamaratLevel_field)

#    campNo = int(row.getValue(campNo_field))
#    streetNo = int(row.getValue(streetNo_field))

#    #print(camp_label)

#    #select camp layer for changing definition query to show specific camp
#    campLyr.definitionQuery= "Camp_Label = '"+ camp_label +"'"

#    #select access road layer for changing definition query to show for a specific camp
#    accessLyr.definitionQuery= "camp__labels = '"+ camp_label +"'"

#    #select return road layer for changing definition query to show for a specific camp
#    returnLyr.definitionQuery= "camp__labels = '"+ camp_label +"'"

#    if level == 'Level 0':
#        level0Lyr.visible = True
#        layerList.append(level0Lyr)
#    elif level == 'Level 1':
#        level1Lyr.visible = True
#        layerList.append(level1Lyr)
#    elif level == 'Level 2':
#        level2Lyr.visible = True
#        layerList.append(level2Lyr)
#    elif level == 'Level 3':
#        level3Lyr.visible = True       
#        layerList.append(level3Lyr)
#    else:
#        level4Lyr.visible = True
#        layerList.append(level4Lyr)

#    print(layerList)
#    for lyr in layerList:
#        ext = lyr.getExtent()
#        print(ext.XMin, ext.YMin, ext.XMax, ext.YMax)
#        if ext.XMin < xmin:
#            xmin = ext.XMin
#        if ext.YMin < ymin:
#            ymin = ext.YMin
#        if ext.XMax > xmax:
#            xmax = ext.XMax
#        if ext.YMax > ymax:
#            ymax = ext.YMax

#    #ext = returnLyr.getExtent()
#    #df.extent = ext

#    df.extent = arcpy.Extent(xmin, ymin, xmax, ymax)

#    arcpy.RefreshTOC()
#    arcpy.RefreshActiveView()
#    filename = "D:\ArcGIS\camp_" + str(campNo) + "-" + str(streetNo) + ".pdf"
#    print(filename)
#    arcpy.mp.ExportToPDF(aprx, filename)

#    resumeExtent = returnLyr.getExtent()
#    df.extent = resumeExtent

#    del layerList[3]

#    level4Lyr.visible = False
#    level3Lyr.visible = False
#    level2Lyr.visible = False
#    level1Lyr.visible = False
#    level0Lyr.visible = False

#    if camp_label == '2/613':
#        break