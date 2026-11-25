
import os
import math
import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw

# Video settings
W, H = 480, 854
FPS = 24
FRAMES = 240

os.makedirs("videos", exist_ok=True)

output_file = "videos/robot_fight.mp4"

writer = imageio.get_writer(
    output_file,
    fps=FPS,
    codec="libx264",
    pixelformat="yuv420p"
)

try:
    for frame in range(FRAMES):
        img = Image.new("RGB", (W, H), (8, 12, 30))
        d = ImageDraw.Draw(img)

        t = frame / FPS

        # Background
        d.rectangle((0, 650, W, H), fill=(22, 28, 50))
        d.line((0, 650, W, 650), fill=(0, 220, 255), width=4)

        # Arena lights
        for i in range(6):
            lx = i * 90
            d.line(
                (lx, 0, lx + 40, 180),
                fill=(20, 45, 80),
                width=3
            )

        # Robot movement
        punch = math.sin(t * 6) * 35
        shake = math.sin(t * 18) * 5

        robots = [
            (125 + punch, (0, 190, 255), 1),
            (355 - punch, (255, 55, 70), -1)
        ]

        for x, color, direction in robots:
            y = 470 + math.sin(t * 3) * 8 + shake

            # Legs
            d.rectangle(
                (x - 28, y + 90, x - 8, y + 170),
                fill=color
            )
            d.rectangle(
                (x + 8, y + 90, x + 28, y + 170),
                fill=color
            )

            # Body
            d.rounded_rectangle(
                (x - 45, y, x + 45, y + 100),
                radius=12,
                fill=color,
                outline="white",
                width=3
            )

            # Chest light
            d.ellipse(
                (x - 12, y + 30, x + 12, y + 54),
                fill="yellow"
            )

            # Head
            d.rounded_rectangle(
                (x - 38, y - 65, x + 38, y - 5),
                radius=12,
                fill=(55, 65, 90),
                outline=color,
                width=4
            )

            # Eyes
            d.ellipse(
                (x - 23, y - 45, x - 8, y - 30),
                fill="yellow"
            )
            d.ellipse(
                (x + 8, y - 45, x + 23, y - 30),
                fill="yellow"
            )

            # Punching arm
            arm_x = x + direction * (65 + abs(punch))

            d.line(
                (x, y + 20, arm_x, y + 55),
                fill=color,
                width=22
            )

            d.ellipse(
                (arm_x - 14, y + 42, arm_x + 14, y + 70),
                fill="white"
            )

        # Fight sparks
        if frame % 12 < 6:
            for i in range(10):
                sx = 240 + math.sin(frame + i) * 55
                sy = 520 + math.cos(frame + i) * 40

                d.ellipse(
                    (sx - 5, sy - 5, sx + 5, sy + 5),
                    fill="yellow"
                )

        # Title
        d.text(
            (115, 90),
            "ROBOT FIGHT",
            fill="white",
            stroke_width=2,
            stroke_fill=(0, 150, 255)
        )

        d.text(
            (135, 130),
            "BATTLE ARENA",
            fill=(0, 220, 255)
        )

        # Convert image to video frame
        writer.append_data(np.asarray(img))

finally:
    writer.close()

print("Robot Fight video created successfully!")


