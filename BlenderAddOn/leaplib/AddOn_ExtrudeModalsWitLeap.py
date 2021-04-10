import bpy, sys, os
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap
from drawingText import DrawingClass
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.normals_make_consistent(inside=False)
"""
Cette classe s'occupe de gérer l'extrusion de faces/arrêtes/sommets pré-alablement 
sélectionnés 
la hauteur de la main sera prise en compte
"""
class ModalExtrudeWithLM(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_extrude_lm"
    bl_label = "Modal Timer Operator"
    controller = Leap.Controller()
    _timer = None
    firstDist=0

    def modal(self, context, event):
        currentMSG = bpy.context.scene["msgToMod"]
        if(currentMSG=="EXITV"): #On quitte si on reçoit le signal
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            self.cancel(context)
            return {'CANCELLED'}
        if(currentMSG=="EXITC"):#On quitte si on reçoit le signal + annule
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            bpy.ops.ed.undo()
            self.cancel(context)
            return {'CANCELLED'}
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER': # on raffrachit selon le timer
            bpy.ops.ed.undo()
            frame = self.controller.frame()
            hands = frame.hands
            # ici on va vouloir appliquer la distance de la main par rapport à son ancienne position pour effectuer l'extrusion
            thisDist = abs(self.firstDist[0]-hands[0].palm_position[0])+abs(self.firstDist[1]-hands[0].palm_position[1])+abs(self.firstDist[2]-hands[0].palm_position[2])
            bpy.ops.ed.undo_push()
            bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, 
                                TRANSFORM_OT_shrink_fatten={"value":thisDist/80, "use_even_offset":True, "mirror":False, 
                                "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, 
                                "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, 
                                "snap_normal":(0, 0, 0), "release_confirm":False})

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        self.firstDist = self.controller.frame().hands[0].palm_position
        bpy.ops.object.mode_set(mode ='EDIT')
        bpy.ops.ed.undo_push()
        
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)