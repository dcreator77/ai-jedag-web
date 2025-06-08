import os
import json
import subprocess
import tempfile

def generate_jedag_video(video_file, preset_file):
    with tempfile.TemporaryDirectory() as tempdir:
        video_path = os.path.join(tempdir, "input.mp4")
        preset_path = os.path.join(tempdir, "preset.json")

        with open(video_path, "wb") as f:
            f.write(video_file.read())
        with open(preset_path, "wb") as f:
            f.write(preset_file.read())

        with open(preset_path) as f:
            data = json.load(f)

        cut_files = []
        for i, cut in enumerate(data["cuts"]):
            start = cut["start"]
            dur = cut["duration"]
            effect = cut["effect"]
            outname = os.path.join(tempdir, f"cut_{i}.mp4")

            if effect == "zoom":
                vf = "zoompan=z='min(zoom+0.005,1.5)':d=1"
            elif effect == "shake":
                vf = "crop=in_w-2*10:in_h-2*10:10:10"
            elif effect == "flash":
                vf = "eq=brightness=0.5"
            else:
                vf = "null"

            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-ss", str(start), "-t", str(dur),
                "-vf", vf,
                outname
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cut_files.append(outname)

        list_path = os.path.join(tempdir, "list.txt")
        with open(list_path, "w") as f:
            for fpath in cut_files:
                f.write(f"file '{fpath}'\n")

        output_file = os.path.join(tempdir, "generated_jedag.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
            "-c:v", "libx264", output_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        final_output = os.path.join(os.getcwd(), "generated_jedag.mp4")
        with open(output_file, "rb") as f_in, open(final_output, "wb") as f_out:
            f_out.write(f_in.read())

        return final_output
