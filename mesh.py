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

# ========================================================
# Revised Animation Section with Adjusted Shoulders and Knees
# ========================================================
def set_bone_rotation(pose_bones, bone_name, frame, rotation_euler, rotation_order='XYZ'):
    bone = pose_bones.get(bone_name)
    if bone is None:
        print(f"Warning: Bone '{bone_name}' not found in rig.")
        return
    bone.rotation_mode = rotation_order
    bone.rotation_euler = rotation_euler
    bone.keyframe_insert(data_path="rotation_euler", frame=frame)

# Switch to Pose mode on the rig for animation
bpy.context.view_layer.objects.active = rig_obj
bpy.ops.object.mode_set(mode='POSE')
pose_bones = rig_obj.pose.bones

# ---------------------------------------------------
# Revised Walk Cycle (frames 1 to 25)
# The knee (thigh/shin) angles and shoulder (upper arm) rotations have been adjusted.
# ---------------------------------------------------
# Frame 1: Left leg forward (knee more bent) and right leg extended
set_bone_rotation(pose_bones, "Pelvis", 1, (math.radians(5), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 1, (math.radians(25), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 1, (math.radians(-20), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 1, (math.radians(-5), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 1, (math.radians(5), 0, 0))
# Shoulders: moderate swing
set_bone_rotation(pose_bones, "Left_Upper_Arm", 1, (math.radians(-15), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 1, (math.radians(15), 0, 0))

# Frame 13: Opposite pose: now right leg forward with more bend and left leg extended
set_bone_rotation(pose_bones, "Pelvis", 13, (math.radians(-5), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 13, (math.radians(-5), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 13, (math.radians(5), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 13, (math.radians(25), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 13, (math.radians(-20), 0, 0))
# Shoulders swap swing direction
set_bone_rotation(pose_bones, "Left_Upper_Arm", 13, (math.radians(15), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 13, (math.radians(-15), 0, 0))

# Frame 25: Return to initial pose
set_bone_rotation(pose_bones, "Pelvis", 25, (math.radians(5), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 25, (math.radians(25), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 25, (math.radians(-20), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 25, (math.radians(-5), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 25, (math.radians(5), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 25, (math.radians(-15), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 25, (math.radians(15), 0, 0))

# ---------------------------------------------------
# Revised Run Cycle (frames 30 to 48)
# More exaggerated poses with adjusted knee and shoulder rotations.
# ---------------------------------------------------
# Frame 30: Start run pose
set_bone_rotation(pose_bones, "Pelvis", 30, (math.radians(10), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 30, (math.radians(45), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 30, (math.radians(-25), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 30, (math.radians(-5), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 30, (math.radians(5), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 30, (math.radians(-35), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 30, (math.radians(35), 0, 0))

# Frame 39: Mid-run pose with legs swapping roles
set_bone_rotation(pose_bones, "Pelvis", 39, (math.radians(-10), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 39, (math.radians(-5), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 39, (math.radians(5), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 39, (math.radians(45), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 39, (math.radians(-25), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 39, (math.radians(35), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 39, (math.radians(-35), 0, 0))

# Frame 48: Loop back to the start of run pose
set_bone_rotation(pose_bones, "Pelvis", 48, (math.radians(10), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 48, (math.radians(45), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 48, (math.radians(-25), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 48, (math.radians(-5), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 48, (math.radians(5), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 48, (math.radians(-35), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 48, (math.radians(35), 0, 0))

# ---------------------------------------------------
# Revised Jump Cycle (frames 60 to 80)
# Adjusted crouch and recovery with more dynamic knee bends.
# ---------------------------------------------------
# Frame 60: Crouch before jump
set_bone_rotation(pose_bones, "Pelvis", 60, (math.radians(-15), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 60, (math.radians(-50), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 60, (math.radians(30), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 60, (math.radians(-50), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 60, (math.radians(30), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 60, (math.radians(25), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 60, (math.radians(-25), 0, 0))

# Frame 65: Takeoff – legs extend
set_bone_rotation(pose_bones, "Pelvis", 65, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 65, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 65, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 65, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 65, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 65, (math.radians(-10), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 65, (math.radians(10), 0, 0))

# Frame 70: Mid-air pose – knees slightly bent for clearance, arms raised
set_bone_rotation(pose_bones, "Pelvis", 70, (math.radians(10), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 70, (math.radians(30), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 70, (math.radians(-20), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 70, (math.radians(30), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 70, (math.radians(-20), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 70, (math.radians(40), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 70, (math.radians(40), 0, 0))

# Frame 75: Landing pose – legs bend to absorb impact
set_bone_rotation(pose_bones, "Pelvis", 75, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 75, (math.radians(-20), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 75, (math.radians(20), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 75, (math.radians(-20), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 75, (math.radians(20), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 75, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 75, (math.radians(0), 0, 0))

# Frame 80: Recovery to standing pose
set_bone_rotation(pose_bones, "Pelvis", 80, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Left_Thigh", 80, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Left_Shin", 80, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Right_Thigh", 80, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Right_Shin", 80, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Left_Upper_Arm", 80, (math.radians(0), 0, 0))
set_bone_rotation(pose_bones, "Right_Upper_Arm", 80, (math.radians(0), 0, 0))

# Return to Object mode when finished
bpy.ops.object.mode_set(mode='OBJECT')

print("Aligned human mesh created, parented to the rig, and revised animations added!")
