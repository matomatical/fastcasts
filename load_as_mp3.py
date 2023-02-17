import os
import shutil
import subprocess

SRC_DIR = "/Volumes/Discworld/nexus/library/podcasts/"
DST_DIR = "/Volumes/Harmony/podcasts/"

def convert_to_mp3(src_path, dst_path):
    dst_path = os.path.splitext(dst_path)[0] + ".mp3"
    print(src_path)
    if os.path.exists(dst_path):
        print("skipping")
    else:
        ffmpeg = subprocess.run(["ffmpeg",
                "-i", src_path,
                "-filter:a",                # audio
                "atempo=2",                 # speed x2 (-vn?)
                "-vn",                      # remove video stream?
                "-acodec", "libmp3lame",    # to mp3
                # "-c:a", "libfdk_aac",     # use apple silicon?
                dst_path,
            ])

shutil.copytree(
    src=SRC_DIR,
    dst=DST_DIR,
    ignore=shutil.ignore_patterns(".DS_Store", "*.xml"),
    copy_function=convert_to_mp3,
    dirs_exist_ok=True,
)
