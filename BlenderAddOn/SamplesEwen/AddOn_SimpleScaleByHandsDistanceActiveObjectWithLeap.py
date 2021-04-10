import bpy, sys, os
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap

def getDistance(h1,h2):
    return (abs(h1.palm_position[0] - h2.palm_position[0])+
            abs(h1.palm_position[1] - h2.palm_position[1])+
            abs(h1.palm_position[2] - h2.palm_position[2]))


class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    controller = Leap.Controller()
    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            frame = self.controller.frame()
            hands = frame.hands
            
            if(hands[0].is_valid):
                if(hands[1].is_valid):
                    context.object.scale.xyz=getDistance(hands[0],hands[1])/320
                    #print(getDistance(hands[0],hands[1]))

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
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
