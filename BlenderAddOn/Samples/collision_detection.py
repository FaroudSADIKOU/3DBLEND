import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree



# %%
PENCIL_MOOVING_FORWARD = True
# %%

def get_BoundBox(object_name):
    """
    returns the corners of the bounding box of an object in world coordinates
    """
    #bpy.context.scene.update()
    ob = bpy.context.scene.objects[object_name]
    #print(ob.matrix_world)
    bbox_corners = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
 
    return bbox_corners
 

def check_collision(object1, object2):
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
    overlaping =  bvh1.overlap( bvh2 )
    if overlaping:
        print("Overlap")
    else:
        print("NO")
    return overlaping
# end check_collision
 


def moove_pencil():
    global PENCIL_MOOVING_FORWARD
    Pencil = bpy.data.objects["Pencil"]
    if(PENCIL_MOOVING_FORWARD):
        if(Pencil.location[0] < 6):
            Pencil.location[0] +=0.05
        else:
            Pencil.location[0] -=0.05
            PENCIL_MOOVING_FORWARD = False
    else:
        if(Pencil.location[0] > -11):
            Pencil.location[0] -=0.05
        else:
            Pencil.location[0] +=0.05
            PENCIL_MOOVING_FORWARD = True
# end moove_pencil

def check_collisions():
    # should ask for all object in scene except from the pencil,
    # but I will just retrieve Cube1 and Cube2.
    # First check collision with Cube2 and with Cube1 later
    Pencil = bpy.data.objects["Pencil"]
    Cube1 = bpy.data.objects["Cube1"]
    Cube2 = bpy.data.objects["Cube2"]
    if(check_collision(Pencil, Cube2)):
        bpy.ops.object.select_all(action='DESELECT')
        Cube2.select_set(True)
        bpy.context.view_layer.objects.active = Cube2
    elif(check_collision(Pencil, Cube1)):
        bpy.ops.object.select_all(action='DESELECT')
        Cube1.select_set(True)
        bpy.context.view_layer.objects.active = Cube1

# end check_collisions

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # move the pencil
            moove_pencil()
            # Check Collision of Pencil with other objects in scene
            check_collisions()
            
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
# end Modal class

def register():
    bpy.utils.register_class(ModalTimerOperator)

def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)




if __name__ == "__main__":
    register()
    # test call
    bpy.ops.wm.modal_timer_operator()
    
