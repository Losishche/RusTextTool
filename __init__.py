
bl_info = {
    "name": "RusTextTool",
    "description": "Russian text tool Addon",
    "version": (1, 1, 1),
    "category": "User",
    "author": "Stas Gorbachev",
    "warning": ""
}

import bpy


if "bpy" in locals():
    import imp
    #if "AnimateText" in locals():
        #imp.reload(AnimateText)
    #if "rustext1111" in locals():
        #imp.reload(rustext1111)

else:
    #from . import AnimateText
    from . import rustext1111

#from . import AnimateText
from . import rustext1111
from . import explode

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
