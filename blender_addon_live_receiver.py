import bpy
import threading
import socket
import json

JOINTS = [
    "Hip", "Spine", "Head",
    "LeftShoulder", "LeftElbow", "LeftWrist",
    "RightShoulder", "RightElbow", "RightWrist",
    "LeftHip", "LeftKnee", "LeftAnkle",
    "RightHip", "RightKnee", "RightAnkle",
]

PORT = 5005

def create_empties():
    for joint in JOINTS:
        name = f"EasyMocap_{joint}"
        if name not in bpy.data.objects:
            bpy.ops.object.empty_add(type='PLAIN_AXES')
            empty = bpy.context.active_object
            empty.name = name

def update_empty(joint, x, y, z):
    name = f"EasyMocap_{joint}"
    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        # Scale coordinates for Blender; origin at center
        obj.location = (x*10, y*10, z*10)

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', PORT))
    print(f"[EasyMocapLite] Listening on UDP {PORT}...")
    while True:
        data, _ = sock.recvfrom(1024)
        try:
            packet = json.loads(data.decode('utf-8'))
            joint = packet['joint']
            x, y, z = packet['x'], packet['y'], packet['z']
            bpy.app.timers.register(lambda: update_empty(joint, x, y, z), first_interval=0)
        except Exception as e:
            print("[EasyMocapLite] Error:", e)

listener_thread = None

def start_listener():
    global listener_thread
    if listener_thread is None:
        create_empties()
        listener_thread = threading.Thread(target=udp_listener, daemon=True)
        listener_thread.start()
        print("[EasyMocapLite] Listener started.")

def stop_listener():
    global listener_thread
    # No clean stop implemented; restart Blender to fully stop.

class EASYMOCAP_OT_StartListener(bpy.types.Operator):
    bl_idname = "easymocap.start_listener"
    bl_label = "Start EasyMocapLite UDP Listener"
    def execute(self, context):
        start_listener()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(EASYMOCAP_OT_StartListener)

def unregister():
    bpy.utils.unregister_class(EASYMOCAP_OT_StartListener)