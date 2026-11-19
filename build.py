from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

ROOT = Path(__file__).resolve().parent
FILES = ("plugin.json", "main.py", "dialog.ps1", "requirements.txt", "import-lcsc.png")


def build():
    metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "plugins/plugin.json").read_text(encoding="utf-8"))
    for action in manifest["actions"]:
        for name in [action["entrypoint"], *action["icons-light"], *action["icons-dark"]]:
            if name not in FILES:
                raise ValueError(f"Missing action file in package list: {name}")

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / "lcsc-importer-pcm.zip"
    temporary = target.with_suffix(".tmp")
    with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
        archive.writestr("metadata.json", json.dumps(metadata, indent=2) + "\n")
        for name in FILES:
            archive.write(ROOT / "plugins" / name, f"plugins/{name}")
    with ZipFile(temporary) as archive:
        if archive.testzip() is not None:
            raise OSError("The plugin archive failed its integrity check.")
    temporary.replace(target)
    print(target)


if __name__ == "__main__":
    build()
