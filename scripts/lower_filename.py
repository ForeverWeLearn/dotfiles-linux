#!/usr/bin/env python3

import os
import argparse
import sys
import re


def clean_name(name):
    base, ext = os.path.splitext(name)

    new_name = base.lower()
    new_name = re.sub(r"[^a-z0-9]+", "_", new_name)
    new_name = new_name.strip("_")

    return new_name + ext.lower()


def process_renaming(directory, recursive=False, force=False):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    if recursive:
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                rename_action(root, name, force)
    else:
        with os.scandir(directory) as it:
            for entry in it:
                rename_action(directory, entry.name, force)


def rename_action(parent, name, force):
    new_name = clean_name(name)

    if new_name == name:
        return

    old_path = os.path.join(parent, name)
    new_path = os.path.join(parent, new_name)

    if os.path.exists(new_path):
        if force:
            try:
                os.remove(old_path)
                print(
                    f"[ERROR] Deleted: '{name}' (Conflict with existing '{new_name}')"
                )
            except OSError as e:
                print(f"[ERROR] Error deleting '{name}': {e}")
        else:
            print(
                f"[WARN] Skipped: '{name}' -> '{new_name}' already exists. (Use -f to delete)"
            )
    else:
        try:
            os.rename(old_path, new_path)
            print(f"[INFO] Renamed: '{name}' -> '{new_name}'")
        except OSError as e:
            print(f"[ERROR] Error renaming '{name}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Professional snake_case renamer for Wayland/Linux users."
    )
    parser.add_argument("path", nargs="?", default=".", help="Target folder")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Process subdirectories"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Delete the source file if the target snake_case name already exists",
    )

    args = parser.parse_args()
    process_renaming(args.path, args.recursive, args.force)
