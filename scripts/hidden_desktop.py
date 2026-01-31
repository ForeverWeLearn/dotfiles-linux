#!/usr/bin/env python3

import pathlib


def hide_desktop_apps():
    # Define source and destination paths
    src_dir = pathlib.Path("/usr/share/applications/")
    dest_dir = pathlib.Path.home() / ".local/share/applications/"

    # Ensure the destination directory exists
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scanning {src_dir}...")

    for desktop_file in src_dir.glob("*.desktop"):
        try:
            content = desktop_file.read_text()

            # Skip if it's already hidden or marked NoDisplay
            if "NoDisplay=true" in content:
                continue

            # Define the new file path in the local folder
            target_file = dest_dir / desktop_file.name

            # Append NoDisplay=true to the content
            # We add a newline to ensure it doesn't merge with the last line
            new_content = content.strip() + "\nNoDisplay=true\n"

            # Write the file to the local directory
            target_file.write_text(new_content)
            print(f"Hidden: {desktop_file.name}")

        except Exception as e:
            print(f"Could not process {desktop_file.name}: {e}")

    print(
        "\nDone! You may need to restart your shell or desktop environment to see changes."
    )


if __name__ == "__main__":
    hide_desktop_apps()
