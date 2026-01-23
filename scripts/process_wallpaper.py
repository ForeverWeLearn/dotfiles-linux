from PIL.Image import Resampling
import argparse
from pathlib import Path
from PIL import Image, ImageOps

RESOLUTIONS = {
    "1080p": (1920, 1080),
    "2k": (2560, 1440),
    "4k": (3840, 2160),
}


def process_images(input_dir, preset, output_ext):
    output_ext = output_ext.lower().lstrip(".")
    if output_ext not in ["jpg", "jpeg", "png", "webp"]:
        print(f"Error: Format '{output_ext}' is not supported. Use jpg, png, or webp.")
        return

    target_size = RESOLUTIONS.get(preset.lower())
    if not target_size:
        print(
            f"Error: Preset {preset} not recognized. Choose from: {list(RESOLUTIONS.keys())}"
        )
        return

    input_path = Path(input_dir).expanduser().resolve()
    output_path = input_path.with_name(f"{input_path.name}_{output_ext}_output")

    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

    output_path.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Processing: {input_path} -> {output_path}")
    print(f"[INFO] Target: {target_size[0]}x{target_size[1]} ({output_ext.upper()})")

    for img_file in input_path.rglob("*"):
        if img_file.suffix.lower() in valid_extensions:
            try:
                relative_path = img_file.relative_to(input_path)
                target_file = output_path / relative_path.with_suffix(f".{output_ext}")

                target_file.parent.mkdir(parents=True, exist_ok=True)

                with Image.open(img_file) as img:
                    processed_img = ImageOps.fit(
                        img, target_size, method=Resampling.LANCZOS
                    )

                    save_format = (
                        "JPEG" if output_ext in ["jpg", "jpeg"] else output_ext.upper()
                    )

                    if save_format == "JPEG" and processed_img.mode in ("RGBA", "P"):
                        processed_img = processed_img.convert("RGB")

                    processed_img.save(target_file, save_format, quality=100)
                    print(f"[INFO] Saved: {target_file.name}")

            except Exception as e:
                print(f"[ERROR] Error processing {img_file.name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch resize and convert wallpapers.")
    parser.add_argument("-i", "--input", required=True, help="Input directory path")
    parser.add_argument(
        "-p", "--preset", required=True, help="Resolution preset (1080p, 2k, 4k)"
    )
    parser.add_argument(
        "-e",
        "--extension",
        default="webp",
        help="Output format (jpg, png, webp). Default: webp",
    )

    args = parser.parse_args()
    process_images(args.input, args.preset, args.extension)
