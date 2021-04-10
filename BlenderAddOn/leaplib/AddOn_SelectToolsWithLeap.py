import bpy, sys, os, math, time
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap
from drawingText import DrawingClass
"""
Cette classe (voir plus bas) s'occupe de gérer la selection d'une partie d'un maillage
d'un objet à l'aide d'un crayon qui apparaitra à l'écran et que l'on déplacera avec la main gauche
l'idée étant au raffraichissement de vérifier la colision entre les faces (ou arêtes/sommets) avec la méthode
"check_collision" et de renvoyer toutes les faces correspondantes jusqu'à que l'utilisateur valide son choix
"""
def check_collision(object1, object2): #Renvois les faces qui sont en colisions avec l'objet 2
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="FACE")
    #bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    # Get objects world matrix
    mat1 = object1.matrix_world
    mat2 = object2.matrix_world

    # Get the geometry in world coordinates
    vert1 = [mat1 @ v.co for v in object1.data.vertices] 
    poly1 = [p.vertices for p in object1.data.polygons]

    vert2 = [mat2 @ v.co for v in object2.data.vertices] 
    poly2 = [p.vertices for p in object2.data.polygons]

    # Create the BVH trees
    bvh1 = BVHTree.FromPolygons( vert1, poly1 )
    bvh2 = BVHTree.FromPolygons( vert2, poly2 )

    # Test if overlap
    overlaping =  bvh1.overlap(bvh2)
    if(overlaping):
        facesToSelect = set(map(lambda x: x[1], overlaping))
        for face in facesToSelect:
            object2.data.polygons[face].select=True
            
    bpy.ops.object.mode_set(mode = 'EDIT')

    return overlaping

class ModalSelectWithPencil(bpy.types.Operator):
    bl_idname = "wm.modal_select_with_pencil"
    bl_label = "Modal SelectWithPencil Operator"
    controller = Leap.Controller()
    _timer = None
    itemSelected= None
    initX = -10.0
    initZ = 300.0
    initY = 64.0
    initPitch = 0
    initRoll = 90
    rotateScale = 100
    rotateScale = 100

    def modal(self, context, event):
        currentMSG = bpy.context.scene["msgToMod"]
        if(currentMSG=="EXITV"):#On quitte si on reçoit le signal
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            self.cancel(context)
            if(bpy.context.scene["nextSelect"]=="Extrude"): #On lance le modal d'extrusion si c'était ordonné
                bpy.ops.wm.modal_extrude_lm()
            else: #Sinon de translation (à voir pour ajouter d'autre modal après une selection)
                bpy.ops.wm.modal_translate_lm()
            return {'CANCELLED'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER': # On raffrachit sans cesse
            frame = self.controller.frame()
            hands = frame.hands
            pencil = bpy.data.objects["SelectPencil"]

            for hand in hands:
                if (hand.is_right): #La main droite devrait gérer la rotation mais on a préféré désactiver pour le moment
                    shiftX = self.initX - hand.palm_position[0]
                    shiftZ = self.initZ- hand.palm_position[1]
                    shiftY = self.initY - hand.palm_position[2]
                    #if(shiftX<-3):
                        #bpy.ops.transform.rotate(value=shiftX/self.rotateScale,orient_axis="X")
                    #if(shiftZ<-3):
                        #bpy.ops.transform.rotate(value=shiftZ/self.rotateScale,orient_axis="Y")

                    self.initX = self.initX-shiftX
                    self.initZ =  self.initZ-shiftZ
                    self.initY = self.initY-shiftY
                else: #Sinon la main gauche gére la position du crayon
                    pencil.location.x = hand.palm_position[2]/50
                    pencil.location.y =  hand.palm_position[0]/50
                    pencil.location.z =  hand.palm_position[1]/50
                check_collision(pencil, self.itemSelected)
                

            
        return {'PASS_THROUGH'}

    def execute(self, context):
        """
        Lors de l'execution du modal de selection, on va importer le modèle du crayon
        et le deselectionner
        """
        self.itemSelected=bpy.context.selected_objects[0]
        imported_object = bpy.ops.import_scene.obj(filepath='C:\\leaplib\\pencil.obj')
        bpy.context.selected_objects[-1].name = "SelectPencil"
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        #obj_object = bpy.context.selected_objects[0]
        #obj_object.name="SelectPencil"
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        """
        Lors du cancel de la fonction,
        on va vouloir retirer le crayon de la scene (le supprimer)
        et repasser en mode Edit de mesh pour voir le résultat obtenu
        """
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects["SelectPencil"].select_set(True)
        bpy.ops.object.delete()
        bpy.ops.object.mode_set(mode ='EDIT')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)