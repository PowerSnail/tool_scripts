#!/usr/bin/python3

import fire
import re
import subprocess as sp
import pathlib
import requests
import json
import attr
import sys

NOPRINT_TRANS_TABLE = str.maketrans({
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable() and not chr(i).isspace()
})

def make_printable(s):
    return s.translate(NOPRINT_TRANS_TABLE)


@attr.define
class Release:
    version: str
    message: str


def get_latest_version(user: str, repo: str) -> Release:
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    with requests.get(url) as response:
        response.raise_for_status()
        data = json.loads(response.content)
        return Release(version=data["name"][1:], message=make_printable(data["body"]))


def main(specfile: str):
    with open(specfile) as file:
        content = file.read()

    name = re.search(r"Name:\s+(.+)\n", content).group(1)
    version_span = re.search(r"Version:\s+(.+)\n", content).span(1)
    cwd = pathlib.Path(".").absolute()
    repo_url = re.search(r"URL:\s+https://github.com/([^/ \n]+)/([^/ \n]+)\b", content)
    user = repo_url.group(1)
    repo = repo_url.group(2)
    
    release_info = get_latest_version(user, repo)

    if release_info.version <= content[version_span[0]:version_span[1]]:
        print("No Update")
        return
    
    existing_tar = cwd / f"{name}-{content[version_span[0]:version_span[1]]}.tar.gz"
    if existing_tar.exists():
        sp.run(["osc", "rm", existing_tar.name], check=True)
    
    tar_url = re.search(r"Source:\s+(.+)#/", content).group(1)
    tar_url = tar_url.replace("%{version}", release_info.version)

    print(f"{name=!r}")
    print(f"{release_info.version=!r}")
    print(f"{tar_url=!r}")

    tmp_d = f"/tmp/{name}-{release_info.version}/"
    sp.run(["aria2c", tar_url], check=True)
    sp.run(["tar", "xf", f"{name}-{release_info.version}.tar.gz", "--directory=/tmp/"], check=True)
    sp.run(["cargo", "vendor"], cwd=tmp_d, check=True)

    vendor_path = cwd / "vendor.tar.xz"
    vendor_path.unlink()
    sp.run(["tar", "cfj", str(vendor_path), "vendor/"], cwd=tmp_d, check=True)

    with open(specfile, "w") as in_file, open(specfile + "~", "w") as file:
        file.seek(0)
        file.write(content[:version_span[0]])
        file.write(release_info.version)
        file.write(content[version_span[1]:])
    
    pathlib.Path(specfile + "~").rename(specfile)

    sp.run(["osc", "build", "--clean"], check=True)
    sp.run(["osc", "add", f"{name}-{release_info.version}.tar.gz"], check=True)
    sp.run(["osc", "vc", "-m", f"Update to {release_info.version}\n" + release_info.message], check=True)


fire.Fire(main)
