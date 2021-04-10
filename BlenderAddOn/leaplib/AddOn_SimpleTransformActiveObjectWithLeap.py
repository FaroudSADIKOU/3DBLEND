import bpy, sys ,os
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap
import math
from drawingText import DrawingClass
"""
Les classes suivantes vont gérer les opérations simple de transformation
à savoir respectivement la translation, la rotation, et la mise à l'échelle (scale)
On peut switch d'un à l'autre avec le message "switch"
Le scale peut également changer (restreindre) l'axe avec le message "switch2"
"""
class ModalTranslateWithLM(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_translate_lm"
    bl_label = "Modal Translate with LMC operator"
    controller = Leap.Controller()
    _timer = None
    initX = -10.0
    initZ = 300.0
    initY = 64.0
    standardScale=50


    def modal(self, context, event):
        currentMSG = bpy.context.scene["msgToMod"]
        if(currentMSG=="EXITV"):#On quitte si on reçoit le signal
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            self.cancel(context)
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            return {'CANCELLED'}
        if(currentMSG=="EXITC"):#On quitte si on reçoit le signal + annule
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            bpy.ops.ed.undo()
            self.cancel(context)
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            return {'CANCELLED'}

        if(currentMSG=="SWITCH"):#Au switch on passe au rotate
            bpy.context.scene["msgToMod"]="NONE"
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Rotate, v: valid, 1 : cancel, 2 : switch transform")
            bpy.ops.ed.undo()
            bpy.ops.wm.modal_rotate_lm() 
            self.cancel(context)
            return {'CANCELLED'}
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            self.initX = -10
            self.initZ = 300
            self.initY = 64
            return {'CANCELLED'}

        if event.type == 'TIMER': #On raffrachit
            frame = self.controller.frame()
            hands = frame.hands
            for hand in hands:#on utilisera la position de la main gauche pour déplacer l'objet
                if hand.is_left:
                    shiftX = self.initX - hand.palm_position[0]
                    shiftZ = self.initZ- hand.palm_position[1]
                    shiftY = self.initY - hand.palm_position[2]
                    bpy.ops.transform.translate(value=(shiftX/self.standardScale,-shiftY/self.standardScale,-shiftZ/self.standardScale))
                    self.initX = self.initX-shiftX
                    self.initZ =  self.initZ-shiftZ
                    self.initY = self.initY-shiftY

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self.initX = -10
        self.initZ = 300
        self.initY = 64
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


class ModalPETranslateWithLM(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_petranslate_lm"
    bl_label = "Modal Translate warping with LMC operator"
    controller = Leap.Controller()
    _timer = None
    initX = -10.0
    initZ = 300.0
    initY = 64.0
    standardScale=50


    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            self.initX = -10
            self.initZ = 300
            self.initY = 64
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            return {'CANCELLED'}

        if event.type == 'TIMER':
            bpy.ops.ed.undo()
            frame = self.controller.frame()
            hands = frame.hands
            for hand in hands: #On utilisera la position de la main gauche pour changer la position
                if hand.is_left:
                    shiftX = self.initX -hand.palm_position[0]
                    shiftZ = self.initZ- hand.palm_position[1]
                    shiftY = self.initY - hand.palm_position[2]
                    bpy.ops.ed.undo_push()
                    bpy.ops.transform.translate(proportional_size=1.0, use_proportional_edit=True, value=(shiftX/self.standardScale,-shiftY/self.standardScale,-shiftZ/self.standardScale))

        return {'PASS_THROUGH'}

    def execute(self, context):

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        bpy.ops.ed.undo_push()
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

class ModalRotateWithLM(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_rotate_lm"
    bl_label = "Modal rotate with LMC operator"
    controller = Leap.Controller()
    _timer = None
    initX = -10.0
    initZ = 300.0
    initY = 64.0
    initPitch = 0
    initRoll = 90
    rotateScale = 100


    def modal(self, context, event):
        currentMSG = bpy.context.scene["msgToMod"]
        if(currentMSG=="EXITV"):#On quitte si on reçoit le signal
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            self.cancel(context)
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            return {'CANCELLED'}
        if(currentMSG=="EXITC"):#On quitte si on reçoit le signal + annule
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            bpy.ops.ed.undo()
            self.cancel(context)
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            return {'CANCELLED'}
        if(currentMSG=="SWITCH"):# on switch de mode en passant au scale si on en recoit le signal
            bpy.context.scene["msgToMod"]="NONE"
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "All Scale, v : valid, 1 : cancel, 2 : switch transform, O : switch Axes")
            bpy.ops.ed.undo()
            bpy.ops.wm.modal_scale_lm() 
            self.cancel(context)
            return {'CANCELLED'}
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            self.cancel(context)


            return {'CANCELLED'}

        if event.type == 'TIMER':
            frame = self.controller.frame()
            hands = frame.hands
            for hand in hands: #ici on change l'orientation en fonction de la position de la main en interdisant le retour en arriere
                if hand.is_left:
                    shiftX = self.initX - hand.palm_position[0]
                    shiftZ = self.initZ- hand.palm_position[1]
                    shiftY = self.initY - hand.palm_position[2]
                    if(shiftX<-3):
                        bpy.ops.transform.rotate(value=shiftX/self.rotateScale,orient_axis="X")
                    if(shiftZ<-3):
                        bpy.ops.transform.rotate(value=shiftZ/self.rotateScale,orient_axis="Y")

                    self.initX = self.initX-shiftX
                    self.initZ =  self.initZ-shiftZ
                    self.initY = self.initY-shiftY

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

class ModalScaleWithLM(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_scale_lm"
    bl_label = "Modal scale with LMC operator"
    controller = Leap.Controller()
    _timer = None
    initScale=150
    standardScale=160
    axe = 0
    axes=["ALL","X","Y","Z"]

    def getDistance(self, h1,h2):
        return (abs(h1.palm_position[0] - h2.palm_position[0])+
                abs(h1.palm_position[1] - h2.palm_position[1])+
                abs(h1.palm_position[2] - h2.palm_position[2]))

    def modal(self, context, event):
        currentMSG = bpy.context.scene["msgToMod"]
        if(currentMSG=="EXITV"):#On quitte si on reçoit le signal
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            self.initScale=150
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            self.cancel(context)
            return {'CANCELLED'}
        if(currentMSG=="EXITC"):#On quitte si on reçoit le signal + annule
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            self.initScale=150
            bpy.ops.ed.undo()
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            self.cancel(context)
            return {'CANCELLED'}
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.context.scene["msgToMod"]="NONE"
            bpy.context.scene["modalInProgress"] = "NONE"
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Menu")
            self.initScale=150
            self.cancel(context)
            return {'CANCELLED'}
        if(currentMSG=="SWITCH"):#on repasse au translate si on reçoit le signal
            bpy.context.scene["msgToMod"]="NONE"
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            dns["dc"] = DrawingClass(bpy.context, "Translate, v: valid, 1 : cancel, 2 : switch transform")
            bpy.ops.ed.undo()
            bpy.ops.wm.modal_translate_lm()   
            self.cancel(context)
            return {'CANCELLED'}
        
        if(currentMSG=="SWITCH2"): #Si on recoit le switch2 alors on change d'axe de contrainte de scaling
            bpy.context.scene["msgToMod"]="NONE"
            self.axe=((self.axe+1)%4)
            dns = bpy.app.driver_namespace
            dns.get("dc").remove_handle()
            #bpy.ops.ed.undo()
            #bpy.ops.ed.undo_push()
            dns["dc"] = DrawingClass(bpy.context, self.axes[self.axe]+" Scale, v : valid, 1 : cancel, 2 : switch transform, O : switch Axes")

        if event.type == 'TIMER':
            frame = self.controller.frame()
            hands = frame.hands

            """for hand in hands :
                if(hand.is_left):
                    shiftS = (hand.palm_position[1]-200) - self.initScale 
                    #print(shiftS)
                    scalVal = math.exp(shiftS)
                    print(scalVal)
                    self.initScale = (hand.palm_position[1]-200)
                    if(self.axe==0):
                        bpy.ops.transform.resize(value=[scalVal,scalVal,scalVal])
                    elif(self.axe==1):
                        bpy.ops.transform.resize(value=[scalVal,0,0])
                    elif(self.axe==2):
                        bpy.ops.transform.resize(value=[0,scalVal,0])
                    elif(self.axe==3):
                        bpy.ops.transform.resize(value=[0,0,scalVal])
            """
            if(hands[0].is_valid and hands[1].is_valid): # On va vouloir utiliser la distance des deux mains pour mesurer le scale
                distance = self.getDistance(hands[0],hands[1])
                #print(distance)
                shiftS = distance - self.initScale
                scalVal = math.exp(shiftS/self.standardScale)
                if(self.axe==0):
                    bpy.ops.transform.resize(value=[scalVal,scalVal,scalVal])
                elif(self.axe==1):
                    bpy.ops.transform.resize(value=[scalVal,0,0])
                elif(self.axe==2):
                    bpy.ops.transform.resize(value=[0,scalVal,0])
                elif(self.axe==3):
                    bpy.ops.transform.resize(value=[0,0,scalVal])
                self.initScale = distance
        return {'PASS_THROUGH'}

    def execute(self, context):
        bpy.ops.ed.undo_push()
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)