import bpy, sys, os
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap


class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    controller = Leap.Controller()
    _timer = None
    lastFrames=[]

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            
            frame = self.controller.frame()
            hands = frame.hands
            
            if(len(self.lastFrames)<20):
                self.lastFrames.append(frame)
            else:
                rotateX = hands[0].rotation_angle(self.lastFrames.pop(0),Leap.Vector.x_axis)
                rotateY = hands[0].rotation_angle(self.lastFrames.pop(0),Leap.Vector.y_axis)
                rotateZ = hands[0].rotation_angle(self.lastFrames.pop(0),Leap.Vector.z_axis)
                print(rotateX,rotateY,rotateZ)
                if(rotateX>0):
                    context.object.rotation_euler[1]= context.object.rotation_euler[1] - rotateX *0.20
                #context.object.rotation_euler[2]= context.object.rotation_euler[2] - rotateY *0.05
                if(rotateZ<0):
                    context.object.rotation_euler[2]= context.object.rotation_euler[2] - rotateZ *0.20
                self.lastFrames.append(frame)
            
            

            #context.object.location.x = hands[1].palm_position[2]/50
            #context.object.location.y =  hands[1].palm_position[0]/50
            #context.object.location.z =  hands[1].palm_position[1]/50

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        print("end")
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

def register():
    bpy.utils.register_class(ModalTimerOperator)

def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
