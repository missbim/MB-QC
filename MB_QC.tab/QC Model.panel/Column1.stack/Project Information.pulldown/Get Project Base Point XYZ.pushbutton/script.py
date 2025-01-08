# -*- coding: utf-8 -*-
__title__ = "Project Base Point"
__author__ = "Nattalie Mor"
__version__ = 'Version: 1'
__doc__ = """Version: 1
Date    = 09.05.2024
_____________________________________________________________________
Description:

Get the values of the Project Base Point for active document.

_____________________________________________________________________
How-to:

- Click Button
_____________________________________________________________________
Last update:
- [09.05.2024] - 1 REALESE
- [13.06.2024] - 2 REALESE - Linkify PBP
_____________________________________________________________________
Author: Nattalie Mor"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#====================================================================
#from Autodesk.Revit.DB import *
from pyrevit import script, forms                                       # import pyRevit modules. (Lots of useful features)

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, XYZ


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#====================================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
# Define the built-in category for Project Base Point
base_point_category = BuiltInCategory.OST_ProjectBasePoint
# Get all Project Base Points in the document
base_points = FilteredElementCollector(doc).OfCategory(base_point_category).ToElements()
output = script.get_output()

# ╔═╗╦  ╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝ CLASS
#====================================================================
# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
pbp_info = []

# Assuming there's only one Project Base Point, otherwise, adjust accordingly
if base_points:
    base_point = base_points[0]

    # Get the N/S, E/W, and elevation parameters from the Project Base Point
    north_south_param = base_point.LookupParameter("N/S")
    east_west_param = base_point.LookupParameter("E/W")
    elevation_param = base_point.LookupParameter("Elev")
    angle_param = base_point.LookupParameter("Angle to True North")


    # Extract the values
    north_south_value = north_south_param.AsValueString() if north_south_param else "Not Set"
    east_west_value = east_west_param.AsValueString() if east_west_param else "Not Set"
    elevation_value = elevation_param.AsValueString() if elevation_param else "Not Set"
    angle_value = angle_param.AsValueString() if angle_param else "Not Set"
    linkify_point = output.linkify(base_point.Id)


    output = script.get_output()
    output.print_table(
        table_data=[[north_south_value, east_west_value, elevation_value, angle_value, linkify_point]],
        title="Project Base Point",
        columns=["N/S", "E/W", "Elevation", "Angle to True North", "Look up"]
    )
else:
    print("No Project Base Point found in the document.")

print("-" * 50)
print('Tool has been developed by Miss BIM.')
