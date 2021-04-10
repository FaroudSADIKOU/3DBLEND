import bpy
from bpy.props import IntProperty, FloatProperty
from bpy import context
rtn = []
for a in context.window.screen.areas:
  if a.type == 'VIEW_3D':
    rtn.append(a)


def camera_position(matrix):
    """ From 4x4 matrix, calculate camera location """
    t = (matrix[0][3], matrix[1][3], matrix[2][3])
    r = (
      (matrix[0][0], matrix[0][1], matrix[0][2]),
      (matrix[1][0], matrix[1][1], matrix[1][2]),
      (matrix[2][0], matrix[2][1], matrix[2][2])
    )
    rp = (
      (-r[0][0], -r[1][0], -r[2][0]),
      (-r[0][1], -r[1][1], -r[2][1]),
      (-r[0][2], -r[1][2], -r[2][2])
    )
    output = (
      rp[0][0] * t[0] + rp[0][1] * t[1] + rp[0][2] * t[2],
      rp[1][0] * t[0] + rp[1][1] * t[1] + rp[1][2] * t[2],
      rp[2][0] * t[0] + rp[2][1] * t[1] + rp[2][2] * t[2],
    )
    return output

def getDistanceFrom(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])
    
def selectNearestPoint(points,mat,pos):
    nearestV=0;
    for v in range(len(points)):
        print(points[v]@mat)
        if(getDistanceFrom(pos,mat @ points[nearestV])>getDistanceFrom(pos,mat @ points[v])):
            nearestV=v
    return nearestV


class ModalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    first_mouse_x: IntProperty()
    first_mouse_y: IntProperty()
    first_value: FloatProperty()
    first_value2: FloatProperty()
    position: None
    
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            #context.object.location.x = self.first_value + delta * 0.01
            context.object.rotation_euler[1]= self.first_value + delta * 0.01
            
            delta2 = self.first_mouse_y - event.mouse_y
            #context.object.location.x = self.first_value + delta * 0.01
            context.object.rotation_euler[2]= self.first_value2 + delta2 * 0.01
    
            bpy.ops.object.mode_set(mode = 'OBJECT')
            obj = bpy.context.active_object
            bpy.ops.object.mode_set(mode = 'EDIT') 
            bpy.ops.mesh.select_mode(type="FACE")
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            #obj.data.vertices[selectNearestPoint(list(map(lambda x: x.co,obj.data.vertices)),obj.matrix_world,self.position)].select = True
            obj.data.polygons[selectNearestPoint(list(map(lambda x: x.center,obj.data.polygons)),obj.matrix_world,self.position)].select = True
            bpy.ops.object.mode_set(mode = 'EDIT')
    
        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location.x = self.first_value
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            self.position =camera_position(rtn[0].spaces[0].region_3d.view_matrix)
            self.first_mouse_x = event.mouse_x
            self.first_mouse_x = event.mouse_y
            #self.first_value = context.object.location.x
            self.first_value = context.object.rotation_euler[1]
            self.first_value2 = context.object.rotation_euler[2]

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}



def register():
    bpy.utils.register_class(ModalOperator)


def unregister():
    bpy.utils.unregister_class(ModalOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.modal_operator('INVOKE_DEFAULT')
