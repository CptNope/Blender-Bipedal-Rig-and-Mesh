import bpy
import mathutils
import math

def create_cylinder_between_points(start, end, radius, name):
    """
    Creates a cylinder that spans between two 3D points.
    The cylinder is created along the Z axis by default, then rotated
    so that it aligns with the vector (end - start) and its origin is placed at the midpoint.
    """
    start_v = mathutils.Vector(start)
    end_v = mathutils.Vector(end)
    mid = (start_v + end_v) / 2.0
    length = (end_v - start_v).length

    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, location=(0,0,0))
    obj = bpy.context.active_object
    obj.name = name

    # The default cylinder is aligned along Z.
    direction = end_v - start_v
    up = mathutils.Vector((0, 0, 1))
    quat = up.rotation_difference(direction.normalized())
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = quat

    # Set the object's location to the midpoint between start and end.
    obj.location = mid
    return obj

# -------------------------------
# Ensure the rig exists and is available
# -------------------------------
rig_obj = bpy.data.objects.get("BipedRig")
if rig_obj is None:
    raise Exception("BipedRig not found! Please run the rig script first.")

# Ensure we are in Object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Access the rig’s pose bones to obtain their positions.
bones = rig_obj.pose.bones

# We'll store the created mesh parts in a list to join them later.
parts = []

# -------------------------------
# Torso: from Pelvis head to Chest tail
# -------------------------------
pelvis_head = bones["Pelvis"].head.copy()
chest_tail = bones["Chest"].tail.copy()
torso = create_cylinder_between_points(pelvis_head, chest_tail, 0.2, "Torso")
parts.append(torso)

# -------------------------------
# Head: create a sphere at the midpoint of the Head bone (using Neck tail to Head tail)
# -------------------------------
head_start = bones["Neck"].tail.copy()
head_end = bones["Head"].tail.copy()
head_mid = (head_start + head_end) / 2.0
bpy.ops.mesh.primitive_uv_sphere_add(location=head_mid, radius=0.2)
head_mesh = bpy.context.active_object
head_mesh.name = "Head"
parts.append(head_mesh)

# -------------------------------
# Left Arm: Upper Arm and Forearm
# -------------------------------
left_upper_arm = create_cylinder_between_points(bones["Left_Upper_Arm"].head, bones["Left_Upper_Arm"].tail, 0.08, "Left_Upper_Arm_Mesh")
parts.append(left_upper_arm)
left_forearm = create_cylinder_between_points(bones["Left_Forearm"].head, bones["Left_Forearm"].tail, 0.07, "Left_Forearm_Mesh")
parts.append(left_forearm)

# -------------------------------
# Right Arm: Upper Arm and Forearm
# -------------------------------
right_upper_arm = create_cylinder_between_points(bones["Right_Upper_Arm"].head, bones["Right_Upper_Arm"].tail, 0.08, "Right_Upper_Arm_Mesh")
parts.append(right_upper_arm)
right_forearm = create_cylinder_between_points(bones["Right_Forearm"].head, bones["Right_Forearm"].tail, 0.07, "Right_Forearm_Mesh")
parts.append(right_forearm)

# -------------------------------
# Left Leg: Thigh and Shin
# -------------------------------
left_thigh = create_cylinder_between_points(bones["Left_Thigh"].head, bones["Left_Thigh"].tail, 0.1, "Left_Thigh_Mesh")
parts.append(left_thigh)
left_shin = create_cylinder_between_points(bones["Left_Shin"].head, bones["Left_Shin"].tail, 0.09, "Left_Shin_Mesh")
parts.append(left_shin)

# -------------------------------
# Right Leg: Thigh and Shin
# -------------------------------
right_thigh = create_cylinder_between_points(bones["Right_Thigh"].head, bones["Right_Thigh"].tail, 0.1, "Right_Thigh_Mesh")
parts.append(right_thigh)
right_shin = create_cylinder_between_points(bones["Right_Shin"].head, bones["Right_Shin"].tail, 0.09, "Right_Shin_Mesh")
parts.append(right_shin)

# -------------------------------
# Optional: Feet (if your rig includes them)
# -------------------------------
if "Left_Foot" in bones.keys() and "Right_Foot" in bones.keys():
    left_foot = create_cylinder_between_points(bones["Left_Foot"].head, bones["Left_Foot"].tail, 0.08, "Left_Foot_Mesh")
    parts.append(left_foot)
    right_foot = create_cylinder_between_points(bones["Right_Foot"].head, bones["Right_Foot"].tail, 0.08, "Right_Foot_Mesh")
    parts.append(right_foot)

# -------------------------------
# Join all parts into one mesh
# -------------------------------
for obj in parts:
    obj.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
human_mesh = bpy.context.active_object
human_mesh.name = "AlignedHumanMesh"

# Optional: Add a Subdivision Surface modifier for smoothness
subsurf = human_mesh.modifiers.new("Subsurf", type='SUBSURF')
subsurf.levels = 2

# -------------------------------
# Parent the mesh to the rig using automatic weights
# -------------------------------
bpy.ops.object.select_all(action='DESELECT')
human_mesh.select_set(True)
rig_obj.select_set(True)
bpy.context.view_layer.objects.active = rig_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

print("Aligned human mesh created and parented to the rig!")
