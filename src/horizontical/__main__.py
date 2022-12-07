import sys
import os
from typing import Tuple
from PIL import Image
from .horizontical import horizonticalize

def main() -> None:
    if len(sys.argv) < 3:
        sys.stderr.write(f"Usage: {sys.argv[0]} INPUT-DIR OUTPUT-DIR\n")
        sys.exit(1)
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    count = 0
    for child in os.listdir(in_dir):
        input_path = os.path.join(in_dir, child)
        output_path = os.path.join(out_dir, f"image-{count:04}.jpg")
        if os.path.isfile(input_path):
            try:
                im = Image.open(input_path)
            except Exception as e:
                sys.stderr.write(f"Skipping non-image {input_path}...\n")
                continue
            try:
                im = horizonticalize(im, (1280, 720))
                im.save(output_path, quality=90)
                sys.stderr.write(f"Horizonticalized {input_path} as {output_path}...\n")
                count += 1
            except Exception as e:
                sys.stderr.write(f"Error processing image {input_path}: {e}\n")


if __name__ == "__main__":
    main()