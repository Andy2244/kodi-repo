#!/usr/bin/env python3
"""
Kodi Repository Generator

This script generates the addons.xml and addons.xml.md5 files for a Kodi repository.
It scans addon directories and zips them up, then creates the repository index files.

Usage:
    python generate_repo.py

Directory structure expected:
    kodi-repo/
    ├── repository.andy2244/
    │   └── addon.xml
    ├── zips/
    │   ├── addons.xml (generated)
    │   ├── addons.xml.md5 (generated)
    │   ├── repository.andy2244/
    │   │   └── repository.andy2244-1.0.0.zip (generated)
    │   └── service.jellyskip/
    │       └── service.jellyskip-1.1.0.zip (copied)
    └── _tools/
        └── generate_repo.py
"""

import os
import hashlib
import zipfile
import shutil
from xml.etree import ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
ZIPS_DIR = os.path.join(REPO_ROOT, "zips")

# Addons to include (directories at repo root containing addon.xml)
ADDON_DIRS = [
    "repository.andy2244",
]

# External addon zips to copy (source_path, addon_id)
EXTERNAL_ADDONS = [
    # Will be populated by checking zips/service.jellyskip/ for existing zips
]


def get_addon_xml(addon_dir):
    """Read and parse addon.xml from a directory."""
    addon_xml_path = os.path.join(addon_dir, "addon.xml")
    if not os.path.exists(addon_xml_path):
        return None

    with open(addon_xml_path, "r", encoding="utf-8") as f:
        return f.read()


def get_addon_info(addon_xml_content):
    """Extract addon id and version from addon.xml content."""
    root = ET.fromstring(addon_xml_content)
    return root.get("id"), root.get("version")


def create_addon_zip(addon_dir, output_dir):
    """Create a zip file for an addon directory."""
    addon_xml = get_addon_xml(addon_dir)
    if not addon_xml:
        return None

    addon_id, version = get_addon_info(addon_xml)
    addon_name = os.path.basename(addon_dir)

    # Create output subdirectory
    addon_output_dir = os.path.join(output_dir, addon_id)
    os.makedirs(addon_output_dir, exist_ok=True)

    zip_filename = f"{addon_id}-{version}.zip"
    zip_path = os.path.join(addon_output_dir, zip_filename)

    print(f"Creating {zip_filename}...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(addon_dir):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.join(addon_id, os.path.relpath(file_path, addon_dir))
                zf.write(file_path, arcname)

    return addon_xml


def generate_addons_xml(addon_xmls):
    """Generate the combined addons.xml file."""
    content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    content += "<addons>\n"

    for addon_xml in addon_xmls:
        # Indent and add the addon XML
        lines = addon_xml.strip().split("\n")
        # Skip XML declaration if present
        if lines[0].startswith("<?xml"):
            lines = lines[1:]
        for line in lines:
            content += "    " + line + "\n"

    content += "</addons>\n"
    return content


def generate_md5(file_path):
    """Generate MD5 checksum for a file."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def find_existing_addon_zips(zips_dir):
    """Find existing addon zips in the zips directory."""
    addon_xmls = []

    for addon_id in os.listdir(zips_dir):
        addon_dir = os.path.join(zips_dir, addon_id)
        if not os.path.isdir(addon_dir):
            continue

        # Find zip files
        for filename in os.listdir(addon_dir):
            if filename.endswith(".zip"):
                zip_path = os.path.join(addon_dir, filename)

                # Extract addon.xml from zip
                try:
                    with zipfile.ZipFile(zip_path, "r") as zf:
                        # Find addon.xml in the zip
                        for name in zf.namelist():
                            if name.endswith("addon.xml") and name.count("/") == 1:
                                addon_xml = zf.read(name).decode("utf-8")
                                addon_xmls.append(addon_xml)
                                print(f"Found existing addon: {filename}")
                                break
                except Exception as e:
                    print(f"Error reading {zip_path}: {e}")

    return addon_xmls


def main():
    print("Kodi Repository Generator")
    print("=" * 40)

    os.makedirs(ZIPS_DIR, exist_ok=True)

    addon_xmls = {}  # Use dict to avoid duplicates by addon_id

    # Process addon directories at repo root
    for addon_dir_name in ADDON_DIRS:
        addon_dir = os.path.join(REPO_ROOT, addon_dir_name)
        if os.path.exists(addon_dir):
            addon_xml = create_addon_zip(addon_dir, ZIPS_DIR)
            if addon_xml:
                addon_id, _ = get_addon_info(addon_xml)
                addon_xmls[addon_id] = addon_xml

    # Find existing addon zips (like service.jellyskip), skip ones we already processed
    existing_xmls = find_existing_addon_zips(ZIPS_DIR)
    for addon_xml in existing_xmls:
        addon_id, _ = get_addon_info(addon_xml)
        if addon_id not in addon_xmls:
            addon_xmls[addon_id] = addon_xml

    if not addon_xmls:
        print("No addons found!")
        return

    # Generate addons.xml
    addons_xml_path = os.path.join(ZIPS_DIR, "addons.xml")
    addons_xml_content = generate_addons_xml(list(addon_xmls.values()))

    with open(addons_xml_path, "w", encoding="utf-8") as f:
        f.write(addons_xml_content)
    print(f"Generated {addons_xml_path}")

    # Generate addons.xml.md5
    md5_path = os.path.join(ZIPS_DIR, "addons.xml.md5")
    md5_hash = generate_md5(addons_xml_path)

    with open(md5_path, "w", encoding="utf-8") as f:
        f.write(md5_hash)
    print(f"Generated {md5_path}")

    print("\nRepository generation complete!")
    print(f"Addons included: {len(addon_xmls)}")


if __name__ == "__main__":
    main()
