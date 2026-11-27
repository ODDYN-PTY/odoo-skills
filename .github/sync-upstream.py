#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path


repo = Path(__file__).resolve().parent.parent
upstream = Path(sys.argv[1]).resolve()
skills = upstream / "skills"
manifest = repo / ".github" / "upstream-files.txt"


def checked_path(relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or path.parts[0] == ".github":
        raise ValueError(f"Invalid managed path: {relative}")
    destination = repo / path
    if not destination.resolve().is_relative_to(repo):
        raise ValueError(f"Managed path escapes repository: {relative}")
    return destination


if not skills.is_dir():
    raise SystemExit(f"Upstream skills directory not found: {skills}")

sources = {}
for source in skills.rglob("*"):
    if source.is_symlink():
        raise SystemExit(f"Unexpected upstream symlink: {source}")
    if source.is_file():
        sources[source.relative_to(skills).as_posix()] = source
for name in ("LICENSE", "COPYRIGHT"):
    source = upstream / name
    if not source.is_file() or source.is_symlink():
        raise SystemExit(f"Missing upstream {name}")
    sources[name] = source

if not sources.get("README.md"):
    raise SystemExit("Upstream skills README is missing")

previous = set(manifest.read_text().splitlines())
for name in sorted(previous - sources.keys()):
    path = checked_path(name)
    if path.exists():
        path.unlink()
        parent = path.parent
        while parent != repo and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent

for name, source in sorted(sources.items()):
    destination = checked_path(name)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)

with (repo / "README.md").open("a") as readme:
    readme.write(
        "\n---\n\n"
        "Mirrored from https://github.com/odoo/odoo/tree/20.0/skills. "
        "See [.github/UPSTREAM_SYNC.md](.github/UPSTREAM_SYNC.md) for synchronization details.\n"
    )

manifest.write_text("".join(f"{name}\n" for name in sorted(sources)))
