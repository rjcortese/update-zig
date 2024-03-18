#!/usr/bin/env python
#
# checks the zig website for the latest master version of zig
# if that version is newer than the currently used version,
# install that version:
#   * download
#   * untar at install location
#   * update symlink in binary location

import hashlib
import json
import shutil
import ssl
import sys
from functools import partial
from pathlib import Path
from urllib.request import urlopen

# the system architecture we want to install
arc = "x86_64-linux"

# where to download the tarball
download_dir = Path("~/Downloads").expanduser()
# we will install zig by making a new directory in this dir
install_dir = Path("~/.zig/zigs").expanduser()
# this dir contains a `zig` symlink to the version of the binary want to use
# this dir should be in the PATH
binary_dir = Path("~/.local/bin").expanduser()

zig_download_index_url = "https://ziglang.org/download/index.json"
print(f"Checking\n  {zig_download_index_url}\nfor latest version of zig")

urlopenhttps = partial(urlopen, context=ssl.create_default_context())

with urlopenhttps(zig_download_index_url) as response:
    downloads_data = json.loads(response.read())

# read the metadata for the "master" (nightly version)
keys = ("version", "date", "docs", "stdDocs", arc)
master_metadata = { k: v for k, v in downloads_data["master"].items() if k in keys }
print("Current nightly version data:")
print(json.dumps(master_metadata, indent=2))

tarball_url = master_metadata[arc]["tarball"]
tarball_shasum = master_metadata[arc]["shasum"]
tarball_size = master_metadata[arc]["size"]

def remove_tarxz(path):
    # tarball ends with ".tar.xz" so we remove that with two `.with_suffix("")`
    return path.with_suffix("").with_suffix("")

tarball_name = Path(tarball_url).name
tarball_name_suffixless = remove_tarxz(Path(tarball_url)).name

download_path = download_dir.joinpath(tarball_name)
install_path = install_dir.joinpath(tarball_name_suffixless)

# download the tarball
if download_path.exists():
    if download_path.is_file():
        print(f"Tarball:\n  {download_path}\nalready exists")
    elif download_path.is_dir():
        print("Install aborted")
        sys.exit(f"Download path:\n  {download_path}\nalready exists and is a directory")
else:
    print(f"Downnloading tarball:\n  {tarball_url}\nto\n  {download_path}")
    with urlopenhttps(tarball_url) as response:
        with open(download_path, mode="xb") as tarball:
            shutil.copyfileobj(response, tarball)
    print("Done!")

# verify integrity of tarball
print(f"Verifying integrity of tarball")
if (download_size := download_path.stat().st_size) != int(tarball_size):
    print("Install aborted")
    sys.exit(f"Tarball size {download_size} does not match expected size {tarball_size}")

with open(download_path, mode='rb') as tarball:
    tarball_digest = hashlib.file_digest(tarball, "sha256")

if tarball_digest.hexdigest() != tarball_shasum:
    print("Install aborted")
    sys.exit("Tarball digest does not match expected shasum")
print("Done!")

# extract the tarball to install_path
print(f"Extracting tarball:\n  {download_path}\nto\n  {install_dir}")
shutil.unpack_archive(download_path, install_dir, "xztar", filter="data")
print("Done!")

# update softlink to binary
new_binary_path = install_path.joinpath("zig")
binary_symlink_path = binary_dir.joinpath("zig") 
binary_symlink_path.unlink(missing_ok=True)
binary_symlink_path.symlink_to(new_binary_path)
print(f"Successfully installed zig {master_metadata['version']} at\n  {install_path}")
