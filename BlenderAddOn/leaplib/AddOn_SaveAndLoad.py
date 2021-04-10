import bpy
import mathutils as math

# This class will generate dialog and ask user the name of the scene it will save
class saveDialogOperator(bpy.types.Operator):
    bl_idname = "object.save_dialog"
    bl_label = "save mesh"

    # Here you declare everything you want to show in the dialog 
    name = bpy.props.StringProperty(name = "Objects Name : ", default = "Cube")

    # This is the method that is called when the ok button is pressed
    # which is what calls the AddCube() method 
    def execute(self, context):
        bpy.ops.wm.save_as_mainfile(filepath="C:\\leaplib\\"+self.name+".blend")   
        self.report({'INFO'}, "saved mesh")
        return {'FINISHED'}

    # This is called when the operator is called, this "shows" the dialog 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

# This class will generate dialog and ask user the name of the scene it will load
class loadDialogOperator(bpy.types.Operator):
    bl_idname = "object.load_dialog"
    bl_label = "load mesh"

    # Here you declare everything you want to show in the dialog 
    name = bpy.props.StringProperty(name = "Objects Name : ", default = "Cube")

    # This is the method that is called when the ok button is pressed
    # which is what calls the AddCube() method 
    def execute(self, context):
        bpy.ops.wm.open_mainfile(filepath="C:\\leaplib\\"+self.name+".blend")
        self.report({'INFO'}, "loaded mesh")
        return {'FINISHED'}

    # This is called when the operator is called, this "shows" the dialog 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)