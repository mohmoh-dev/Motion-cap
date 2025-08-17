bl_info = {
    "name": "EasyMocapLite Live Receiver",
    "description": "Receives live mocap data over UDP and applies it to empties/bones.",
    "author": "EasyMocapLite Team",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "View3D > Tool Shelf",
    "category": "Animation"
}

import bpy
from . import live_receiver

def register():
    live_receiver.register()

def unregister():
    live_receiver.unregister()