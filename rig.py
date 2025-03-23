import bpy

# -------------------------------
# Step 1: Clean up the scene
# -------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# -------------------------------
# Step 2: Create a new armature and object
# -------------------------------
arm_data = bpy.data.armatures.new("BipedArmature")
armature_obj = bpy.data.objects.new("BipedRig", arm_data)
bpy.context.collection.objects.link(armature_obj)

# Set armature as active and switch to Edit mode
bpy.context.view_layer.objects.active = armature_obj
bpy.ops.object.mode_set(mode='EDIT')
edit_bones = armature_obj.data.edit_bones

# -------------------------------
# Step 3: Create the basic rig bones
# -------------------------------

# Pelvis
pelvis = edit_bones.new("Pelvis")
pelvis.head = (0, 0, 0)
pelvis.tail = (0, 0, 0.2)

# Spine
spine = edit_bones.new("Spine")
spine.head = pelvis.tail
spine.tail = (0, 0, 0.8)
spine.parent = pelvis

# Chest
chest = edit_bones.new("Chest")
chest.head = spine.tail
chest.tail = (0, 0, 1.2)
chest.parent = spine

# Neck
neck = edit_bones.new("Neck")
neck.head = chest.tail
neck.tail = (0, 0, 1.4)
neck.parent = chest

# Head
head = edit_bones.new("Head")
head.head = neck.tail
head.tail = (0, 0, 1.6)
head.parent = neck

# -------------------------------
# Left Arm
# -------------------------------
left_upper_arm = edit_bones.new("Left_Upper_Arm")
left_upper_arm.head = (0, 0, 1.15)  # approximate shoulder position
left_upper_arm.tail = (-0.3, 0, 1.0)
left_upper_arm.parent = chest

left_forearm = edit_bones.new("Left_Forearm")
left_forearm.head = left_upper_arm.tail
left_forearm.tail = (-0.5, 0, 0.8)
left_forearm.parent = left_upper_arm

left_hand = edit_bones.new("Left_Hand")
left_hand.head = left_forearm.tail
left_hand.tail = (-0.6, 0, 0.7)
left_hand.parent = left_forearm

# -------------------------------
# Right Arm
# -------------------------------
right_upper_arm = edit_bones.new("Right_Upper_Arm")
right_upper_arm.head = (0, 0, 1.15)
right_upper_arm.tail = (0.3, 0, 1.0)
right_upper_arm.parent = chest

right_forearm = edit_bones.new("Right_Forearm")
right_forearm.head = right_upper_arm.tail
right_forearm.tail = (0.5, 0, 0.8)
right_forearm.parent = right_upper_arm

right_hand = edit_bones.new("Right_Hand")
right_hand.head = right_forearm.tail
right_hand.tail = (0.6, 0, 0.7)
right_hand.parent = right_forearm

# -------------------------------
# Left Leg
# -------------------------------
left_thigh = edit_bones.new("Left_Thigh")
left_thigh.head = (0, 0, 0)  # pelvis level
left_thigh.tail = (-0.2, 0, -0.6)
left_thigh.parent = pelvis

left_shin = edit_bones.new("Left_Shin")
left_shin.head = left_thigh.tail
left_shin.tail = (-0.2, 0, -1.2)
left_shin.parent = left_thigh

left_foot = edit_bones.new("Left_Foot")
left_foot.head = left_shin.tail
left_foot.tail = (-0.2, 0.2, -1.2)
left_foot.parent = left_shin

# -------------------------------
# Right Leg
# -------------------------------
right_thigh = edit_bones.new("Right_Thigh")
right_thigh.head = (0, 0, 0)  # pelvis level
right_thigh.tail = (0.2, 0, -0.6)
right_thigh.parent = pelvis

right_shin = edit_bones.new("Right_Shin")
right_shin.head = right_thigh.tail
right_shin.tail = (0.2, 0, -1.2)
right_shin.parent = right_thigh

right_foot = edit_bones.new("Right_Foot")
right_foot.head = right_shin.tail
right_foot.tail = (0.2, 0.2, -1.2)
right_foot.parent = right_shin

# -------------------------------
# Step 4: Create IK control bones for legs
# -------------------------------
# Left Leg IK Target
left_IK_target = edit_bones.new("Left_IK_Target")
left_IK_target.head = left_foot.tail
left_IK_target.tail = (left_foot.tail[0], left_foot.tail[1], left_foot.tail[2] - 0.2)
left_IK_target.parent = pelvis  # or unparented as desired
left_IK_target.use_deform = False

# Left Knee Pole
left_knee_pole = edit_bones.new("Left_Knee_Pole")
left_knee_pole.head = (left_thigh.tail[0], left_thigh.tail[1] + 0.3, left_thigh.tail[2])
left_knee_pole.tail = (left_thigh.tail[0], left_thigh.tail[1] + 0.3, left_thigh.tail[2] + 0.1)
left_knee_pole.parent = pelvis
left_knee_pole.use_deform = False

# Right Leg IK Target
right_IK_target = edit_bones.new("Right_IK_Target")
right_IK_target.head = right_foot.tail
right_IK_target.tail = (right_foot.tail[0], right_foot.tail[1], right_foot.tail[2] - 0.2)
right_IK_target.parent = pelvis
right_IK_target.use_deform = False

# Right Knee Pole
right_knee_pole = edit_bones.new("Right_Knee_Pole")
right_knee_pole.head = (right_thigh.tail[0], right_thigh.tail[1] + 0.3, right_thigh.tail[2])
right_knee_pole.tail = (right_thigh.tail[0], right_thigh.tail[1] + 0.3, right_thigh.tail[2] + 0.1)
right_knee_pole.parent = pelvis
right_knee_pole.use_deform = False

# -------------------------------
# Step 5: Create IK control bones for arms
# -------------------------------
# Left Arm IK Target
left_IK_arm = edit_bones.new("Left_IK_Arm")
left_IK_arm.head = left_hand.tail
left_IK_arm.tail = (left_hand.tail[0] - 0.1, left_hand.tail[1] - 0.1, left_hand.tail[2])
left_IK_arm.parent = chest
left_IK_arm.use_deform = False

# Left Elbow Pole
left_elbow_pole = edit_bones.new("Left_Elbow_Pole")
left_elbow_pole.head = (left_forearm.head[0], left_forearm.head[1] + 0.3, left_forearm.head[2])
left_elbow_pole.tail = (left_forearm.head[0], left_forearm.head[1] + 0.3, left_forearm.head[2] + 0.1)
left_elbow_pole.parent = chest
left_elbow_pole.use_deform = False

# Right Arm IK Target
right_IK_arm = edit_bones.new("Right_IK_Arm")
right_IK_arm.head = right_hand.tail
right_IK_arm.tail = (right_hand.tail[0] + 0.1, right_hand.tail[1] - 0.1, right_hand.tail[2])
right_IK_arm.parent = chest
right_IK_arm.use_deform = False

# Right Elbow Pole
right_elbow_pole = edit_bones.new("Right_Elbow_Pole")
right_elbow_pole.head = (right_forearm.head[0], right_forearm.head[1] + 0.3, right_forearm.head[2])
right_elbow_pole.tail = (right_forearm.head[0], right_forearm.head[1] + 0.3, right_forearm.head[2] + 0.1)
right_elbow_pole.parent = chest
right_elbow_pole.use_deform = False

# Exit Edit mode
bpy.ops.object.mode_set(mode='OBJECT')

# -------------------------------
# Step 6: Add IK constraints in Pose mode
# -------------------------------
bpy.ops.object.mode_set(mode='POSE')
pose_bones = armature_obj.pose.bones

# --- Leg IK Constraints ---
# Left Leg: Apply IK to the Left_Shin
left_shin_pose = pose_bones["Left_Shin"]
left_leg_ik = left_shin_pose.constraints.new('IK')
left_leg_ik.name = "LeftLeg_IK"
left_leg_ik.target = armature_obj
left_leg_ik.subtarget = "Left_IK_Target"
left_leg_ik.chain_count = 2  # Affects Left_Thigh and Left_Shin
left_leg_ik.pole_target = armature_obj
left_leg_ik.pole_subtarget = "Left_Knee_Pole"
left_leg_ik.pole_angle = 0

# Right Leg: Apply IK to the Right_Shin
right_shin_pose = pose_bones["Right_Shin"]
right_leg_ik = right_shin_pose.constraints.new('IK')
right_leg_ik.name = "RightLeg_IK"
right_leg_ik.target = armature_obj
right_leg_ik.subtarget = "Right_IK_Target"
right_leg_ik.chain_count = 2  # Affects Right_Thigh and Right_Shin
right_leg_ik.pole_target = armature_obj
right_leg_ik.pole_subtarget = "Right_Knee_Pole"
right_leg_ik.pole_angle = 0

# --- Arm IK Constraints ---
# Left Arm: Apply IK to the Left_Forearm
left_forearm_pose = pose_bones["Left_Forearm"]
left_arm_ik = left_forearm_pose.constraints.new('IK')
left_arm_ik.name = "LeftArm_IK"
left_arm_ik.target = armature_obj
left_arm_ik.subtarget = "Left_IK_Arm"
left_arm_ik.chain_count = 2  # Affects Left_Upper_Arm and Left_Forearm
left_arm_ik.pole_target = armature_obj
left_arm_ik.pole_subtarget = "Left_Elbow_Pole"
left_arm_ik.pole_angle = 0

# Right Arm: Apply IK to the Right_Forearm
right_forearm_pose = pose_bones["Right_Forearm"]
right_arm_ik = right_forearm_pose.constraints.new('IK')
right_arm_ik.name = "RightArm_IK"
right_arm_ik.target = armature_obj
right_arm_ik.subtarget = "Right_IK_Arm"
right_arm_ik.chain_count = 2  # Affects Right_Upper_Arm and Right_Forearm
right_arm_ik.pole_target = armature_obj
right_arm_ik.pole_subtarget = "Right_Elbow_Pole"
right_arm_ik.pole_angle = 0

# Return to Object mode
bpy.ops.object.mode_set(mode='OBJECT')

print("Biped rig with leg and arm IK controls has been created!")
