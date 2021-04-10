import bpy, sys ,os, subprocess
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap
from bpy.props import StringProperty
from drawingText import DrawingClass
from queue import Queue, Empty
from threading  import Thread
import drawingText
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
    print("fin")
"""
Cette classe gère la logique et fais le pont entre le module de reconaissance de geste 
et active les modules 3D correspondant suivants la configuration choisies
"""
class ModalMainReco(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_mainreco"
    bl_label = "Modal recognize gesture and call other modals"
    controller = Leap.Controller()
    _timer = None
    modalInProgress="NONE"

    def modal(self, context, event):
        """
        Tout les refresh, on  :
        
        """"
        try:  line = self.q.get_nowait() #On récupère sans attendre l'item dans la queue 
        except Empty:
                pass #Si elle est vide on passe
        else: #Si on récupère un geste dans la queue alors, on le traite : 
            outil = str(line, 'utf-8')[0]
            print(outil) #Selon l'outil on va lancer tel ou tel modal (translate, select...)
            if (bpy.context.scene["modalInProgress"]=="NONE"): # Si jamais aucun outil est en cours d'utilisation
                if (outil =="1"):
                    bpy.context.scene["modalInProgress"] = "TRANSLATE" #Variable qui contient le modal en cours d'utilisation
                    print("translate mod")
                    drawingText.changeToolsName("scale, v: valid, 1 : cancel, 2 : switch transform") #On change le texte affiché pour le feedback utilisateur
                    bpy.ops.wm.modal_scale_lm() #Ligne qui lance le modal en question
                elif(outil=="2"):
                    bpy.context.scene["modalInProgress"] = "SELECT"
                    print("select mod")
                    drawingText.changeToolsName("Select with Left hand, Right hand for rotate, V for valid")
                    bpy.context.scene["nextSelect"]="Extrude"
                    bpy.ops.wm.modal_select_with_pencil()
                elif(outil=="R"): #Ici on va d'abord lancer le module select et utiliser une variable spéciale "nextSelect" (utilisé dans blender) pour indiquer au module de selection de lancer une extrusion après la fin de celui-ci
                    bpy.context.scene["modalInProgress"] = "SELECT"
                    print("select mod")
                    bpy.context.scene["nextSelect"]="Transform" #Variable spéciale post-selection
                    drawingText.changeToolsName("Select with Left hand, Right hand for rotate, V for valid")
                    bpy.ops.wm.modal_select_with_pencil()
                elif(outil=="B"):
                    bpy.context.scene["modalInProgress"] = "DEFORM"
                    print("Deform mod")
                    drawingText.changeToolsName("X TWIST Deform with Left hand, V for valid, 2 for switch method, O for switch Axe")
                    bpy.ops.wm.modal_deform_lm()
            else: #Sinon, si un outil est en cours d'usage, alors on peut décider d'envoyer des messages à ce module, à savoir : 
                if(bpy.context.scene["msgToMod"]=="NONE"):
                    if (outil =="V"): # Message général de validation (sort du module)
                        bpy.context.scene["msgToMod"] = "EXITV"
                    if (outil =="1"): # Message général d'annulation (sors du module et annule les modifications)
                        bpy.context.scene["msgToMod"] = "EXITC"
                    if (outil =="2"): # Message général de switcher une option dans le module
                        bpy.context.scene["msgToMod"] = "SWITCH"
                    if (outil =="O"): # Message général de switcher une autre option dans le module 
                        bpy.context.scene["msgToMod"] = "SWITCH2"

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        """
        à l'execution de ce modal, on va créer un sous processus (thread)
        contenant le module de reconaissance de geste dont on va piper (rediriger)
        la sortie standard sur ce module
        Le but étant ensuite de créer un thread qui va écouter les sorties du modules et de
        les stocker dans une Queue d'évenement qui sera régulièrement inspectée par le modal
        """
        self.handTrackProcess = subprocess.Popen(['python', 'C:/leaplib/handtracking/main_script.py'],stdout=subprocess.PIPE,bufsize=1,close_fds=ON_POSIX)
        self.q = Queue() #Queue contenant les inputs
        self.t = Thread(target=enqueue_output, args=(self.handTrackProcess.stdout, self.q)) #Thread qui s'occupe de récolter la sortie standard et de stocker dans la queue les nouvelles informations
        self.t.daemon = True
        self.t.start()
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self.handTrackProcess.kill()
        wm = context.window_manager
        wm.event_timer_remove(self._timer)