import bpy,blf
"""
Cette classe gére l'affichage du texte sur l'interface de blender
afin d'avoir un retour visuel pour l'utilisateur
"""
class DrawingClass:
    def __init__(self, context, prop):
        self.prop = prop
        self.handle = bpy.types.SpaceView3D.draw_handler_add(
                   self.draw_text_callback,(context,),
                   'WINDOW', 'POST_PIXEL')

    def draw_text_callback(self, context):
        font_id = 0  # XXX, need to find out how best to get this.

        # draw some text
        blf.position(font_id, 15, 50, 0)
        blf.size(font_id, 20, 72)
        #blf.draw(font_id, "%s %s" % (context.scene.name, self.prop))
        blf.draw(font_id,self.prop)

    def remove_handle(self):
         bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')

def changeToolsName(name):
        dns = bpy.app.driver_namespace
        dns.get("dc").remove_handle()
        dns["dc"] = DrawingClass(bpy.context, name)