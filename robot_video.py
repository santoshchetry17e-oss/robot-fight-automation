
import imageio.v2 as imageio
from PIL import Image, ImageDraw
import math
import os

W, H = 480, 854
FPS = 12
FRAMES = 144

os.makedirs("videos", exist_ok=True)

writer = imageio.get_writer(
    "videos/robot_fight.mp4",
    fps=FPS,
    codec="libx264",
    pixelformat="yuv420p"
)

for frame in range(FRAMES):
    img = Image.new("RGB", (W, H), (10, 14, 35))
    d = ImageDraw.Draw(img)

    # Arena
    d.rectangle((0, 650, W, H), fill=(25, 30, 55))
    d.line((0, 650, W, 650), fill=(0, 220, 255), width=4)

    # Moving robots
    t = frame / FPS
    punch = math.sin(t * 5) * 35

    for x, color, direction in [
        (115 + punch, (0, 190, 255), 1),
        (365 - punch, (255, 55, 70), -1)
    ]:
        y = 480 + math.sin(t * 3) * 8

        # Legs
        d.rectangle((x-28, y+90, x-8, y+170), fill=color)
        d.rectangle((x+8, y+90, x+28, y+170), fill=color)

        # Body
        d.rounded_rectangle(
            (x-45, y, x+45, y+100),
            radius=12, fill=color, outline="white", width=3
        )

        # Head
        d.rounded_rectangle(
            (x-38, y-65, x+38, y-5),
            radius=12, fill=(55, 65, 90), outline=color, width=4
        )

        # Eyes
        d.ellipse((x-23, y-45, x-8, y-30), fill="yellow")
        d.ellipse((x+8, y-45, x+23, y-30), fill="yellow")

        # Punching arms
        arm_x = x + direction * (65 + abs(punch))
        d.line((x, y+20, arm_x, y+55), fill=color, width=22)
        d.ellipse((arm_x-14, y+42, arm_x+14, y+70), fill="white")

    # Fight sparks
    if frame % 12 < 5:
        for i in range(8):
            sx = 240 + math.sin(frame+i)*55
            sy = 520 + math.cos(frame+i)*40
            d.ellipse((sx-4, sy-4, sx+4, sy+4), fill="yellow")

    d.text((90, 90), "ROBOT FIGHT", fill="white")
    d.text((115, 130), "BATTLE ARENA", fill=(0, 220, 255))

    writer.append_data(imageio.asarray(img))

writer.close()
print("Robot Fight video created successfully!")

