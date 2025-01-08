# -*- coding: utf-8 -*-
__title__ = "Walls Structure"
__author__ = "Nattalie Mor"
__version__ = 'Version: 1'
__doc__ = """Version: 1
Date    = 18.08.2024
_____________________________________________________________________
Description:

Export elements from selected levels.

_____________________________________________________________________
How-to:

- Click Button
_____________________________________________________________________
Last update:
- [18.08.2024] - 1 REALESE
_____________________________________________________________________
Author: Nattalie Mor"""
from pyrevit import forms, script
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, Selection, ObjectType

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
#.NET Imports
import clr
clr.AddReference('System')
clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.UI import TaskDialog, UIApplication, RevitCommandId, PostableCommand
from Autodesk.Revit.DB import *
from rpw.ui.forms import FlexForm, ComboBox, Label, Separator, TextBox, Button
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import Pipe
from Autodesk.Revit.DB.Mechanical import Duct
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
uiapp  = DocumentManager.Instance.CurrentUIApplication
doc    = __revit__.ActiveUIDocument.Document
active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ==================================================

class ISF_box(ISelectionFilter):
    def AllowElement(self, element):
        # Check if the element is either a scope box or a section box
        if element.Category.Id.IntegerValue == int(BuiltInCategory.OST_VolumeOfInterest) or element.Category.Id.IntegerValue == int(BuiltInCategory.OST_SectionBox):
            return True
        return False
    def AllowReference(self, reference, position):
        # Not needed for this filter but must be implemented
        return True

# Apply ISelectionFilter to PickElementsByRectangle

levels = FilteredElementCollector(doc)\
                .OfCategory(BuiltInCategory.OST_Levels)\
                .WhereElementIsNotElementType()\
                .ToElements()


basic_walls_param = ParameterValueProvider(ElementId(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM))
f_rule = FilterStringRule(basic_walls_param, FilterStringEquals(), "Basic Wall")
basic_walls_filter = ElementParameterFilter(f_rule)
wall_types = FilteredElementCollector(doc).OfClass(WallType).WherePasses(basic_walls_filter).ToElements()

output = script.get_output()

# ╔╗ ╔═╗╦ ╦╔╗╔╔╦╗╦╔╗╔╔═╗  ╔╗ ╔═╗═╗ ╦  ╦╔╗╔╔╦╗╔═╗╦═╗╔═╗╔═╗╔═╗╔╦╗╔═╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ╠╩╗║ ║║ ║║║║ ║║║║║║║ ╦  ╠╩╗║ ║╔╩╦╝  ║║║║ ║ ║╣ ╠╦╝╚═╗║╣ ║   ║ ╚═╗  ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╚═╝╚═╝╝╚╝═╩╝╩╝╚╝╚═╝  ╚═╝╚═╝╩ ╚═  ╩╝╚╝ ╩ ╚═╝╩╚═╚═╝╚═╝╚═╝ ╩ ╚═╝  ╚  ╩╩═╝╩ ╚═╝╩╚═

wall_type_info = []

for wall_type in wall_types:
    wall_name = wall_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    wall_width = wall_type.Width
    wall_structure = wall_type.GetCompoundStructure()
    firstlayercore = wall_structure.GetFirstCoreLayerIndex()
    lastlayercore = wall_structure.GetLastCoreLayerIndex()
    wall_layers = wall_structure.GetLayers()

    layer_info_table = (
        "<table border='1'><tr><th>Layer</th><th>Material</th><th>Thickness (cm)</th><th>Inside Core</th></tr>"
    )
    layer_info = []
    for layer in wall_layers:
        layer_name = layer.Function.ToString()
        lay_id = int(layer.LayerId)
        if firstlayercore <= lay_id <= lastlayercore:
            iscore = "✅"
        else:
            iscore = ""
        layer_mat = doc.GetElement(layer.MaterialId)
        if layer_mat:
            mat_name = layer_mat.Name.encode('utf-8').decode('utf-8')
        else:
            mat_name = "No Material"
        layer_width_cm = UnitUtils.ConvertFromInternalUnits(layer.Width, UnitTypeId.Centimeters)

        layer_info_table += "<tr><td>" + layer_name + "</td><td>" + mat_name + "</td><td>" + str(layer_width_cm) + "</td><td>" + str(iscore) + "</td><tr>"
    layer_info_table += "</table>"
        # layer_info.append({
        #     'Layer': layer_name,
        #     'Material': mat_name,
        #     'Thickness': layer_width_cm,
        # })
    wall_width_cm = UnitUtils.ConvertFromInternalUnits(wall_width, UnitTypeId.Centimeters)
    wall_function = wall_type.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString()
    if wall_type.get_Parameter(BuiltInParameter.STRUCTURAL_MATERIAL_PARAM):
        wall_material = wall_type.get_Parameter(BuiltInParameter.STRUCTURAL_MATERIAL_PARAM).AsValueString()
    else:
        wall_material = "No Structural Material"
    linkify_wall_type = output.linkify(wall_type.Id)

    wall_type_info .append({
        'Name': wall_name,
        'Width': wall_width_cm,
        'Function': wall_function,
        'Structural Material': wall_material,
        'Layers': layer_info_table,
        'Look up': linkify_wall_type,
    })

def sort_wall_type(walls_type):
    return sorted(walls_type, key=lambda wall_name: wall_name['Name'])

# Sort the levels
sorted_walls = sort_wall_type(wall_type_info)

if not wall_type_info:
    forms.alert("There are no wall type in the project", "Wall Types", "Tool has been developed by Miss BIM.")

else:
    output = script.get_output()
    output.print_table(
        table_data=[[wall['Name'], wall['Width'], wall['Function'], wall['Structural Material'], wall['Layers'], wall['Look up']] for wall in sorted_walls],
        title="Basic Wall Types",
        columns=["Name", "Width (cm)", "Function", "Structural Material","layers", "Look up"]
    )
    print("-" * 50)
    print('Tool has been developed by Miss BIM.')