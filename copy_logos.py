import os
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_src = os.path.join(base_dir, 'Logo')
dest_dir = os.path.join(base_dir, 'static', 'images', 'logos')
os.makedirs(dest_dir, exist_ok=True)

if os.path.exists(logo_src):
    for item in os.listdir(logo_src):
        src_file = os.path.join(logo_src, item)
        if os.path.isfile(src_file):
            dest_file = os.path.join(dest_dir, item)
            shutil.copy2(src_file, dest_file)
            print(f"Copied {item} -> {dest_file}")

print("Logo copy complete! Current files in static/images/logos:", os.listdir(dest_dir))
