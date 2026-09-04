import bpy
import numpy as np
import os
import math


# ============================================================
# SETTINGS
# ============================================================

PROJECT_ROOT = r"C:\Users\MGV\OneDrive\Desktop\Sign_Lang_app"

NPY_FILE = os.path.join(
    PROJECT_ROOT,
    "Dataset",
    "Words_Landmarks",
    "Greetings",
    "Hello",
    "MVI_0089.npy"       # CHANGE THIS
)

FPS = 20
FRAME_COUNT = 30


# ============================================================
# CLEAR SCENE
# ============================================================

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)


# ============================================================
# LOAD LANDMARK DATA
# ============================================================

if not os.path.exists(NPY_FILE):

    raise FileNotFoundError(
        f"\nLandmark file not found:\n{NPY_FILE}\n"
        "\nChange NPY_FILE to one of your actual .npy files."
    )


sequence = np.load(NPY_FILE)

print("Loaded:", NPY_FILE)
print("Shape:", sequence.shape)


if sequence.ndim != 2:
    raise ValueError(
        f"Expected 2D array, got {sequence.shape}"
    )


if sequence.shape[1] != 225:
    raise ValueError(
        f"Expected 225 features, got {sequence.shape[1]}"
    )


# ============================================================
# FRAME COUNT
# ============================================================

actual_frames = sequence.shape[0]

print(
    f"Frames available: {actual_frames}"
)


# ============================================================
# LANDMARK EXTRACTION
# ============================================================

def get_pose(frame):

    return frame[0:99].reshape(33, 3)


def get_left_hand(frame):

    return frame[99:162].reshape(21, 3)


def get_right_hand(frame):

    return frame[162:225].reshape(21, 3)


# ============================================================
# COORDINATE CONVERSION
# ============================================================

def convert_point(point):

    x = float(point[0])
    y = float(point[1])
    z = float(point[2])

    # MediaPipe:
    # x → horizontal
    # y → vertical
    # z → depth
    #
    # Blender:
    # X → horizontal
    # Y → depth
    # Z → vertical

    return (
        x * 3.0,
        -z * 3.0,
        -y * 3.0
    )


# ============================================================
# CREATE SPHERE
# ============================================================

def create_joint(
    name,
    location,
    radius=0.07
):

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=8,
        radius=radius,
        location=location
    )

    obj = bpy.context.object

    obj.name = name

    return obj


# ============================================================
# CREATE BONE-LIKE CYLINDER
# ============================================================

def create_bone(
    name,
    start,
    end,
    radius=0.035
):

    start = np.array(start)
    end = np.array(end)

    direction = end - start

    length = np.linalg.norm(
        direction
    )

    if length < 0.0001:

        return None


    midpoint = (
        start + end
    ) / 2


    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=radius,
        depth=length,
        location=midpoint
    )

    obj = bpy.context.object

    obj.name = name


    # Cylinder initially points along Z.
    # Rotate Z to the direction vector.

    direction = direction / length

    obj.rotation_mode = "QUATERNION"

    obj.rotation_quaternion = (
        direction.to_track_quat(
            "Z",
            "Y"
        )
    )


    return obj


# ============================================================
# CONNECTIONS
# ============================================================

POSE_CONNECTIONS = [

    (11, 12),

    (11, 13),
    (13, 15),

    (12, 14),
    (14, 16),

    (11, 23),
    (12, 24),

    (23, 24),

    (23, 25),
    (25, 27),

    (24, 26),
    (26, 28),
]


HAND_CONNECTIONS = [

    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),

    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),

    (0, 9),
    (9, 10),
    (10, 11),
    (11, 12),

    (0, 13),
    (13, 14),
    (14, 15),
    (15, 16),

    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),

    (5, 9),
    (9, 13),
    (13, 17),
]


# ============================================================
# CREATE LANDMARK OBJECTS
# ============================================================

joint_objects = []

for i in range(33):

    obj = create_joint(
        f"Pose_{i}",
        (0, 0, 0),
        0.075
    )

    joint_objects.append(obj)


left_hand_objects = []

for i in range(21):

    obj = create_joint(
        f"LeftHand_{i}",
        (0, 0, 0),
        0.045
    )

    left_hand_objects.append(obj)


right_hand_objects = []

for i in range(21):

    obj = create_joint(
        f"RightHand_{i}",
        (0, 0, 0),
        0.045
    )

    right_hand_objects.append(obj)


# ============================================================
# CREATE BONE OBJECTS
# ============================================================

pose_bones = []

for index, (a, b) in enumerate(
    POSE_CONNECTIONS
):

    obj = create_bone(
        f"PoseBone_{index}",
        (0, 0, 0),
        (0, 0, 0)
    )

    pose_bones.append(
        (obj, a, b)
    )


left_bones = []

for index, (a, b) in enumerate(
    HAND_CONNECTIONS
):

    obj = create_bone(
        f"LeftBone_{index}",
        (0, 0, 0),
        (0, 0, 0)
    )

    left_bones.append(
        (obj, a, b)
    )


right_bones = []

for index, (a, b) in enumerate(
    HAND_CONNECTIONS
):

    obj = create_bone(
        f"RightBone_{index}",
        (0, 0, 0),
        (0, 0, 0)
    )

    right_bones.append(
        (obj, a, b)
    )


# ============================================================
# UPDATE FRAME
# ============================================================

def update_frame(frame_number):

    frame = sequence[
        frame_number
    ]


    pose = get_pose(frame)

    left_hand = get_left_hand(frame)

    right_hand = get_right_hand(frame)


    # --------------------------------------------------------
    # POSE JOINTS
    # --------------------------------------------------------

    pose_points = []

    for i, landmark in enumerate(pose):

        point = convert_point(
            landmark
        )

        pose_points.append(
            point
        )

        joint_objects[i].location = point


    # --------------------------------------------------------
    # LEFT HAND
    # --------------------------------------------------------

    left_points = []

    for i, landmark in enumerate(
        left_hand
    ):

        point = convert_point(
            landmark
        )

        left_points.append(
            point
        )

        left_hand_objects[i].location = point


    # --------------------------------------------------------
    # RIGHT HAND
    # --------------------------------------------------------

    right_points = []

    for i, landmark in enumerate(
        right_hand
    ):

        point = convert_point(
            landmark
        )

        right_points.append(
            point
        )

        right_hand_objects[i].location = point


    # --------------------------------------------------------
    # BODY CONNECTIONS
    # --------------------------------------------------------

    for obj, a, b in pose_bones:

        if obj is None:
            continue

        start = pose_points[a]
        end = pose_points[b]

        direction = (
            np.array(end)
            -
            np.array(start)
        )

        length = np.linalg.norm(
            direction
        )

        if length < 0.0001:
            continue

        midpoint = (
            np.array(start)
            +
            np.array(end)
        ) / 2

        obj.location = midpoint

        obj.scale.z = length / 2

        obj.rotation_mode = "QUATERNION"

        obj.rotation_quaternion = (
            direction / length
        ).astype(
            np.float64
        ).tolist()


    # --------------------------------------------------------
    # LEFT HAND CONNECTIONS
    # --------------------------------------------------------

    for obj, a, b in left_bones:

        if obj is None:
            continue

        start = left_points[a]
        end = left_points[b]

        direction = (
            np.array(end)
            -
            np.array(start)
        )

        length = np.linalg.norm(
            direction
        )

        if length < 0.0001:
            continue

        midpoint = (
            np.array(start)
            +
            np.array(end)
        ) / 2

        obj.location = midpoint

        obj.scale.z = length / 2

        obj.rotation_mode = "QUATERNION"

        obj.rotation_quaternion = (
            direction / length
        ).astype(
            np.float64
        ).tolist()


    # --------------------------------------------------------
    # RIGHT HAND CONNECTIONS
    # --------------------------------------------------------

    for obj, a, b in right_bones:

        if obj is None:
            continue

        start = right_points[a]
        end = right_points[b]

        direction = (
            np.array(end)
            -
            np.array(start)
        )

        length = np.linalg.norm(
            direction
        )

        if length < 0.0001:
            continue

        midpoint = (
            np.array(start)
            +
            np.array(end)
        ) / 2

        obj.location = midpoint

        obj.scale.z = length / 2

        obj.rotation_mode = "QUATERNION"

        obj.rotation_quaternion = (
            direction / length
        ).astype(
            np.float64
        ).tolist()


# ============================================================
# ANIMATION
# ============================================================

print()
print(
    "Creating animation..."
)


scene = bpy.context.scene

scene.render.fps = FPS

scene.frame_start = 1

scene.frame_end = actual_frames


for frame_number in range(
    actual_frames
):

    update_frame(
        frame_number
    )


    blender_frame = (
        frame_number + 1
    )


    # --------------------------------------------------------
    # Keyframe joints
    # --------------------------------------------------------

    for obj in joint_objects:

        obj.keyframe_insert(
            data_path="location",
            frame=blender_frame
        )


    for obj in left_hand_objects:

        obj.keyframe_insert(
            data_path="location",
            frame=blender_frame
        )


    for obj in right_hand_objects:

        obj.keyframe_insert(
            data_path="location",
            frame=blender_frame
        )


    # --------------------------------------------------------
    # Keyframe body bones
    # --------------------------------------------------------

    for obj, _, _ in pose_bones:

        if obj is None:
            continue

        obj.keyframe_insert(
            data_path="location",
            frame=blender_frame
        )

        obj.keyframe_insert(
            data_path="rotation_quaternion",
            frame=blender_frame
        )

        obj.keyframe_insert(
            data_path="scale",
            frame=blender_frame
        )


    for obj, _, _ in left_bones:

        if obj is None:
            continue

        obj.keyframe_insert(
            data_path="location",
            frame=blender_frame
        )

        obj.keyframe_insert(
            data_path="rotation_quaternion",
            frame=blender_frame
        )

        obj.keyframe_insert(
            data_path="scale",
            frame=blender_frame
        )


    for obj, _, _ in right_bones:

        if obj is None:
            continue

        obj.keyframe_insert(
            data_path="location",
            frame=blender_frame
        )

        obj.keyframe_insert(
            data_path="rotation_quaternion",
            frame=blender_frame
        )

        obj.keyframe_insert(
            data_path="scale",
            frame=blender_frame
        )


# ============================================================
# SMOOTH ANIMATION
# ============================================================

if scene.animation_data:

    pass


# ============================================================
# CAMERA
# ============================================================

bpy.ops.object.camera_add(
    location=(0, -12, 0)
)

camera = bpy.context.object

camera.name = "AvatarCamera"

scene.camera = camera


camera.rotation_euler = (
    math.radians(90),
    0,
    0
)


# ============================================================
# LIGHT
# ============================================================

bpy.ops.object.light_add(
    type="AREA",
    location=(0, -5, 6)
)

light = bpy.context.object

light.data.energy = 1200

light.data.shape = "DISK"

light.data.size = 5


# ============================================================
# WORLD
# ============================================================

scene.world.color = (
    0.03,
    0.03,
    0.03
)


# ============================================================
# START
# ============================================================

scene.frame_set(1)


print()
print(
    "================================================"
)

print(
    "3D LANDMARK ANIMATION READY"
)

print(
    "================================================"
)

print(
    f"Frames : {actual_frames}"
)

print(
    f"FPS    : {FPS}"
)

print(
    "Press SPACE in Blender to play."
)

print(
    "================================================"
)