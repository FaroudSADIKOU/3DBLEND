import bpy


def get_incr(self):
    return self["testprop"]


def set_incr(self, value):
    self["testprop"] = value

bpy.types.Scene.test_incr = bpy.props.FloatProperty(get=get_incr, set=set_incr)

scene = bpy.context.scene

scene.test_incr = 0

class ModalTimerOperator1(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator_1"
    bl_label = "Modal Timer Operator 1"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE'}:
            print(context.scene.test_incr)
            context.scene.test_incr=context.scene.test_incr+1.0
            bpy.ops.wm.modal_timer_operator_2()
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # This timer event gets triggered from wm.modal_timer_operator_2
            print("T1")

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
    
    
class ModalTimerOperator2(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator_2"
    bl_label = "Modal Timer Operator 2"

    _timer = None

    def modal(self, context, event):
        if event.type in {'ESC'}:
            print(context.scene.test_incr)
            bpy.ops.wm.modal_timer_operator_1()
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            print("T2")

        return {'PASS_THROUGH'}

    def execute(self, context):
        print("goooo")
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(ModalTimerOperator1)
    bpy.utils.register_class(ModalTimerOperator2)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator2)
    bpy.utils.unregister_class(ModalTimerOperator1)


if __name__ == "__main__":
    register()
    bpy.ops.wm.modal_timer_operator_1()
    