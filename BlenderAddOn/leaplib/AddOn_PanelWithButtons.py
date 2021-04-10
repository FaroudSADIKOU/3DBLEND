import bpy,blf, sys ,os
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap
from bpy.props import StringProperty
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

from AddOn_SimpleTransformActiveObjectWithLeap import ModalTranslateWithLM
from AddOn_SimpleTransformActiveObjectWithLeap import ModalPETranslateWithLM
from AddOn_SimpleTransformActiveObjectWithLeap import ModalScaleWithLM
from AddOn_SimpleTransformActiveObjectWithLeap import ModalRotateWithLM

from AddOn_ExtrudeModalsWitLeap import ModalExtrudeWithLM

from AddOn_SelectToolsWithLeap import ModalSelectWithPencil

from AddOn_DeformObjectWithLeap import ModalDeformWithLM
from drawingText import DrawingClass
from AddOn_SaveAndLoad import saveDialogOperator
from AddOn_SaveAndLoad import loadDialogOperator
from AddOn_MainModalReco import ModalMainReco
"""
Cette classe est la classe principal de l'Add-on qui s'occupe de déclarer toutes les 
autres classe qui seront impliqués (indispensable pour Blender)
Elle s'occupera également en autre de disposer un panneau intégré à Blender sous le nom de
"3DBLEND" (onglet) pour pouvoir lancer les opérations 3D disponibles
elle permettra aussi de lancer le module de reconaissance (MainModalReco) avec le boutton "use Leap"

"""
class ActionsPanel3DBlend(Panel):
    bl_idname = 'TEST_PT_panel2'
    bl_label = '3DBlend'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = '3DBlend'
    
    def draw(self, context):#Gère l'affichage sur l'interface de blender
        layout = self.layout
        layout.operator('test.test_op', text='Translate').action = 'translate'
        layout.operator('test.test_op', text='Translate With Warping').action = 'translatePE'
        layout.operator('test.test_op', text='Rotate').action = 'rotate'
        layout.operator('test.test_op', text='Scale').action = 'scale'
        layout.operator('test.test_op', text='Extrude').action = 'extrude'
        layout.operator('test.test_op', text='Select With Pencil').action = 'selectwp'
        layout.operator('test.test_op', text='Twist').action = 'twist'
        layout.operator('test.test_op', text='Bend').action = 'bend'
        layout.operator('test.test_op', text='Taper').action = 'taper'
        layout.operator('test.test_op', text='Stretch').action = 'stretch'
        layout.operator('test.test_op', text='Subdivide Mesh').action = 'subdivide'
        layout.operator('test.test_op', text='save').action = 'save'
        layout.operator('test.test_op', text='load').action = 'load'
        layout.operator('test.test_op', text='use LEAP').action = 'leap'

 
 
class ActionsController(Operator): #Classe qui contrôle les différentes actions
    bl_idname = 'test.test_op'
    bl_label = '3DBlend'
    bl_description = 'Test'
    bl_options = {'REGISTER', 'UNDO'}
    CurrentTools="Menu"
 
    action: EnumProperty(
        items=[
            ('translate', 'translate selected', 'translate selected'),
            ('translatePE', 'translate warping selected', 'translate warping selected'),
            ('rotate', 'rotate Selected', 'rotate Selected'),
            ('scale', 'scale Selected', 'scale Selected'),
            ('extrude', 'extrude Selected', 'extrude Selected'),
            ('selectwp', 'Select With pencil', 'Select With pencil'),
            ('twist', 'Twist selected', 'Twist selected'),
            ('bend', 'bend selected', 'bend selected'),
            ('taper', 'taper selected', 'taper selected'),
            ('stretch', 'stretch selected', 'stretch selected'),
            ('subdivide', 'subdivide mesh selected', 'subdivide mesh selected'),
            ('save', 'save mesh selected', 'save mesh selected'),
            ('load', 'load mesh selected', 'load mesh selected'),
            ('leap', 'launch leap motion', 'launch leap motion')
        ]
    )
    
    def changeToolsName(self,name):#Permet de changer le nom de l'outil en cours d'usage
        dns = bpy.app.driver_namespace
        dns.get("dc").remove_handle()
        dns["dc"] = DrawingClass(bpy.context, name)
        
    def execute(self, context):#gère le lancement des outils en fonction du boutton préssé
        if self.action == 'translate':
            self.changeToolsName("Translate")
            bpy.ops.wm.modal_translate_lm()    
        elif self.action == 'translatePE':
            self.changeToolsName("Translate with warping")
            bpy.ops.wm.modal_petranslate_lm()
        elif self.action == 'rotate':
            self.changeToolsName("Rotate")
            bpy.ops.wm.modal_rotate_lm()
        elif self.action == 'scale':
            self.changeToolsName("Scale")
            bpy.ops.wm.modal_scale_lm()
        elif self.action == 'extrude':
            self.changeToolsName("Extrude")
            bpy.ops.wm.modal_extrude_lm()
        elif self.action == 'selectwp':
            self.changeToolsName("Select tools")
            bpy.ops.wm.modal_select_with_pencil()
        elif self.action == 'twist':
            bpy.context.scene["DeformMethod"] = "TWIST"
            self.changeToolsName("Twist")
            bpy.ops.wm.modal_deform_lm()
        elif self.action == 'bend':
            bpy.context.scene["DeformMethod"] = "BEND"
            self.changeToolsName("Bend")
            bpy.ops.wm.modal_deform_lm()
        elif self.action == 'taper':
            bpy.context.scene["DeformMethod"] = "TAPER"
            self.changeToolsName("Taper")
            bpy.ops.wm.modal_deform_lm()
        elif self.action == 'stretch':
            bpy.context.scene["DeformMethod"] = "STRETCH"
            self.changeToolsName("Stretch")
            bpy.ops.wm.modal_deform_lm()
        elif self.action == 'subdivide':
            bpy.ops.object.mode_set(mode = 'EDIT') 
            bpy.ops.mesh.subdivide(number_cuts=1)
        elif self.action == 'save':
            bpy.ops.object.save_dialog('INVOKE_DEFAULT')
        elif self.action == 'load':
            bpy.ops.object.load_dialog('INVOKE_DEFAULT')
        elif self.action == 'leap':
             bpy.ops.wm.modal_mainreco()
        return {'FINISHED'}
    

        
 
def register(): #Fonction d'enregistrement de blender 
    #bpy.context.scene.DeformMethod.set(StringProperty(default='BEND'))
    bpy.context.scene["modalInProgress"] = "NONE"
    bpy.context.scene["msgToMod"] = "NONE"
    bpy.context.scene["DeformMethod"] = "BEND"
    dns = bpy.app.driver_namespace
    dns["dc"] = DrawingClass(bpy.context, "Menu")
    
    register_class(ModalMainReco)
    register_class(loadDialogOperator)
    register_class(saveDialogOperator)
    register_class(ModalDeformWithLM)  
    
    register_class(ModalSelectWithPencil)
    register_class(ModalExtrudeWithLM)
    
    register_class(ModalRotateWithLM)
    register_class(ModalScaleWithLM)
    register_class(ModalPETranslateWithLM)
    register_class(ModalTranslateWithLM)
    
    register_class(ActionsController)
    register_class(ActionsPanel3DBlend)
 
 
def unregister():
    unregister_class(ModalMainReco)
    unregister_class(loadDialogOperator)
    unregister_class(saveDialogOperator)
    unregister_class(ModalDeformWithLM)  
    unregister_class(ModalSelectWithPencil)
    unregister_class(ModalExtrudeWithLM)
    unregister_class(ModalScaleWithLM)
    unregister_class(ModalTranslateWithLM)
    unregister_class(ActionsController)
    unregister_class(ActionsPanel3DBlend)
 
 
if __name__ == '__main__':
    register()