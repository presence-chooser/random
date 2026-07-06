import cv2
import random
import math

# ==========================================
# Settings
# ==========================================

INPUT_VIDEO = "VID_20240329_021151_HSR_120.mp4"
OUTPUT_VIDEO = "probability.mp4"

MODE = "probability"

# Available modes:
#
# random
# nearby
# reverse
# pingpong
# freeze
# jumpcut
# reverse_blocks
# random_walk
# sine
# saw
# random_blocks
# circular
# probability
# skip
# reverse_skip

SEED = 123456789
random.seed(SEED)

# ==========================================
# Global Variables
# ==========================================

last_frame = 0
jump_offset = 0
walk_position = 0
block_start = 0

# ==========================================
# Frame Selection Algorithms
# ==========================================

def get_frame(i, total):

    global last_frame
    global jump_offset
    global walk_position
    global block_start

    # -------------------------
    # Complete Random
    # -------------------------
    if MODE == "random":
        return random.randint(0, total - 1)

    # -------------------------
    # Nearby Random
    # -------------------------
    elif MODE == "nearby":

        radius = 30

        start = max(0, i - radius)
        end = min(total - 1, i + radius)

        return random.randint(start, end)

    # -------------------------
    # Reverse
    # -------------------------
    elif MODE == "reverse":
        return total - i - 1

    # -------------------------
    # Ping Pong
    # -------------------------
    elif MODE == "pingpong":

        cycle = total * 2

        x = i % cycle

        if x < total:
            return x

        return cycle - x - 1

    # -------------------------
    # Freeze
    # -------------------------
    elif MODE == "freeze":

        if random.random() < 0.10:
            return last_frame

        last_frame = i

        return i

    # -------------------------
    # Jump Cut
    # -------------------------
    elif MODE == "jumpcut":

        if random.random() < 0.02:
            jump_offset = random.randint(0, total - 1)

        return (jump_offset + i) % total

    # -------------------------
    # Reverse Blocks
    # -------------------------
    elif MODE == "reverse_blocks":

        block = 30

        start = (i // block) * block

        end = min(start + block - 1, total - 1)

        return end - (i - start)

    # -------------------------
    # Random Walk
    # -------------------------
    elif MODE == "random_walk":

        walk_position += random.randint(-3, 3)

        walk_position = max(
            0,
            min(total - 1, walk_position)
        )

        return walk_position

    # -------------------------
    # Sine Wave
    # -------------------------
    elif MODE == "sine":

        return int(
            ((math.sin(i / 25) + 1) / 2)
            * (total - 1)
        )

    # -------------------------
    # Saw Wave
    # -------------------------
    elif MODE == "saw":

        return (i * 5) % total

    # -------------------------
    # Random Blocks
    # -------------------------
    elif MODE == "random_blocks":

        if i % 20 == 0:
            block_start = random.randint(
                0,
                max(0, total - 21)
            )

        return block_start + (i % 20)

    # -------------------------
    # Circular Buffer
    # -------------------------
    elif MODE == "circular":

        buffer_size = 200

        start = max(0, i - buffer_size)

        return random.randint(start, i)

    # -------------------------
    # Probability Mix
    # -------------------------
    elif MODE == "probability":

        r = random.random()

        if r < 0.10:
            return i

        if r < 0.80:
            return max(0, i - 1)

        if r < 0.95:
            return min(total - 1, i + 1)

        return random.randint(0, total - 1)

    # -------------------------
    # Skip
    # -------------------------
    elif MODE == "skip":

        return (i * 3) % total

    # -------------------------
    # Reverse Skip
    # -------------------------
    elif MODE == "reverse_skip":

        return total - 1 - ((i * 3) % total)

    return i

# ==========================================
# Open Video
# ==========================================

cap = cv2.VideoCapture(INPUT_VIDEO)

if not cap.isOpened():
    print("Cannot open video.")
    quit()

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Frames :", frame_count)
print("FPS    :", fps)
print("Mode   :", MODE)

# ==========================================
# Output
# ==========================================

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    fps,
    (width, height)
)

# ==========================================
# Process
# ==========================================

for i in range(frame_count):

    source_frame = get_frame(i, frame_count)

    source_frame = max(
        0,
        min(frame_count - 1, source_frame)
    )

    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        source_frame
    )

    ret, frame = cap.read()

    if ret:
        writer.write(frame)

    if i % 100 == 0:
        print(
            f"{i}/{frame_count} "
            f"-> {source_frame}"
        )

# ==========================================
# Finish
# ==========================================

writer.release()
cap.release()

print("Done!")
print("Saved:", OUTPUT_VIDEO)
