import subprocess
import os
import glob


def check_fonts():
    font_path = "/usr/share/figlet/*.?lf"
    fonts = glob.glob(font_path)

    broken_fonts = []
    working_count = 0

    print(f"Checking {len(fonts)} fonts...")

    for font_file in fonts:
        font_name = os.path.basename(font_file)

        try:
            result = subprocess.run(
                ["toilet", "-f", font_name, "test"],
                capture_output=True,
                text=True,
                timeout=2,
            )

            if "could not load font" in result.stderr or result.returncode != 0:
                broken_fonts.append(font_file)
            else:
                working_count += 1

        except Exception:
            broken_fonts.append(font_file)

    print("-" * 30)
    print(f"Scan complete: {working_count} working, {len(broken_fonts)} broken.")

    if broken_fonts:
        print("\nBroken fonts found:")
        for f in broken_fonts:
            print(f"  - {f}")

        confirm = input("\nWould you like to delete these fonts? (y/N): ")
        if confirm.lower() == "y":
            for f in broken_fonts:
                try:
                    subprocess.run(["sudo", "rm", f], check=True)
                    print(f"Deleted: {f}")
                except Exception as e:
                    print(f"Failed to delete {f}: {e}")
    else:
        print("[INFO] No broken fonts detected.")


if __name__ == "__main__":
    check_fonts()
