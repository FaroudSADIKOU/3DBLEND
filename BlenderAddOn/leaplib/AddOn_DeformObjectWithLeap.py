import bpy, sys ,os
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap
import math
from bpy.props import StringProperty
from drawingText import DrawingClass
"""
Cette classe va gérer les déformations de l'objet actuellement selectionné (de manière global)
Un seul opérateur pour les 4 méthodes proposées : Twist, bend, taper et stretch
"""
class ModalDeformWithLM(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_deform_lm"
    bl_label = "Modal deform with LMC operator"
    controller = Leap.Controller()
    _timer = None
    transformMethod=0
    axe=0
    transMethods=["TWIST","BEND","TAPER","STRETCH"]
    axes=["X","Y","Z"]
    

    def modal(self, context, event):
        currentMSG = bpy.context.scene["msgToMod"]
        if(currentMSG=="EXITV"): #On quitte si on reçoit le signal
            self.cancel(context)
            return {'CANCELLED'}
        if(currentMSG=="EXITC"): #On quitte si on reçoit le signal + annule
            bpy.context.selected_objects[0].modifiers.clear()
            self.cancel(context)
            return {'CANCELLED'}
        if(currentMSG=="SWITCH"): #On change de méthode si on reçoit le signal du switch
            bpy.context.scene["msgToMod"]="NONE"
            self.transformMethod=((self.transformMethod+1)%4)
            bpy.context.selected_objects[0].modifiers["SimpleDeform"].deform_method=self.transMethods[self.transformMethod]
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, self.axes[self.axe]+" "+self.transMethods[self.transformMethod]+" Deform with Left hand, V for valid, 2 for switch method, O for switch Axe")
        if(currentMSG=="SWITCH2"): #On change d'axe de transformation (X/Y/Z) si on reçoit le signal switch2
            bpy.context.scene["msgToMod"]="NONE"
            self.axe=((self.axe+1)%3)
            bpy.context.selected_objects[0].modifiers["SimpleDeform"].deform_axis=self.axes[self.axe]
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, self.axes[self.axe]+" "+self.transMethods[self.transformMethod]+" Deform with Left hand, V for valid, 2 for switch method, O for switch Axe")
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER': #on raffrachit selon le timer l'écran
            frame = self.controller.frame()
            hands = frame.hands
            for hand in hands:
                if (hand.is_left):
                    bpy.context.selected_objects[0].modifiers["SimpleDeform"].factor=(hands[0].palm_position[1]-200)/100
        return {'PASS_THROUGH'}

    def execute(self, context):
        
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        bpy.ops.object.modifier_add(type="SIMPLE_DEFORM")
        bpy.context.selected_objects[0].modifiers["SimpleDeform"].deform_method=bpy.context.scene["DeformMethod"]
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        bpy.context.scene["msgToMod"]="NONE"
        bpy.context.scene["modalInProgress"] = "NONE"
        dns = bpy.app.driver_namespace
        dns.get("dc").remove_handle()
        dns["dc"] = DrawingClass(bpy.context, "Menu")
        wm = context.window_manager
        wm.event_timer_remove(self._timer)