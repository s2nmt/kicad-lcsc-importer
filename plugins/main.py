"""KiCad PCB Editor action for importing LCSC parts."""
from pathlib import Path
import re
import subprocess
import sys
import ctypes
import json
import os
import tempfile


PART_NUMBER = re.compile(r"C[0-9]+")
LIBRARY_NAME = re.compile(r"[A-Za-z0-9_-]+")
RESERVED_NAME = re.compile(r"CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9]", re.IGNORECASE)
MODEL_PATH = re.compile(r'(\(model\s+")([^"\r\n]+)(")')


def valid_library_name(name):
    return LIBRARY_NAME.fullmatch(name) and not RESERVED_NAME.fullmatch(name)


def import_part(part, library, library_name, overwrite):
    model_variable = f"{library_name.upper()}_3D"
    model_prefix = "${" + model_variable + "}/"
    command = [
        sys.executable, "-m", "easyeda2kicad", "--full", "--lcsc_id", part,
        "--output", str(library / f"{library_name}.kicad_sym"),
    ]
    if overwrite:
        command.append("--overwrite")
    result = subprocess.run(
        command, capture_output=True, text=True, errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW, timeout=120,
    )
    log = "\n".join(filter(None, (result.stdout.strip(), result.stderr.strip())))
    if result.returncode:
        raise RuntimeError(log or f"Importer exited with code {result.returncode}.")

    footprint_name = re.search(r"Footprint path:\s*([^\r\n]+)", log)
    if not footprint_name:
        return log, "No newly exported footprint was reported."

    footprint_dir = (library / f"{library_name}.pretty").resolve()
    footprint = Path(footprint_name.group(1).strip()).resolve()
    if footprint.parent != footprint_dir or footprint.suffix != ".kicad_mod":
        raise RuntimeError(f"Unexpected footprint path: {footprint}")

    model_dir = library / f"{library_name}.3dshapes"
    original = footprint.read_text(encoding="utf-8")

    def replace_model(match):
        filename = Path(match.group(2)).name
        if not (model_dir / filename).is_file():
            return match.group(0)
        return f"{match.group(1)}{model_prefix}{filename}{match.group(3)}"

    updated = MODEL_PATH.sub(replace_model, original)
    if updated != original:
        temporary = footprint.with_suffix(".kicad_mod.lcsc-import.tmp")
        temporary.write_text(updated, encoding="utf-8")
        temporary.replace(footprint)
    if model_prefix in updated:
        return log, f"Set {model_variable} in KiCad Configure Paths to:\n{model_dir}"
    return log, "No matching local 3D model was available to link."



def main():
    powershell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
    dialog = Path(__file__).with_name("dialog.ps1")
    preference = Path(os.environ["LOCALAPPDATA"]) / "kicad-lcsc-importer" / "library-name.txt"
    environment = os.environ.copy()
    try:
        saved_name = preference.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError):
        saved_name = ""
    environment["LCSC_IMPORTER_LIBRARY_NAME"] = (
        saved_name if valid_library_name(saved_name) else "lcsc_importer"
    )
    try:
        result = subprocess.run(
            [str(powershell), "-NoProfile", "-NonInteractive", "-STA",
             "-ExecutionPolicy", "Bypass", "-File", str(dialog)],
            capture_output=True, encoding="utf-8", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW,
            env=environment,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or "Unable to open the import dialog.")
        if not result.stdout.strip():
            return

        selection = json.loads(result.stdout)
        number = selection["part"].strip().upper()
        library_name = selection["library_name"].strip()
        folder = Path(selection["folder"].strip()).expanduser()
        if not PART_NUMBER.fullmatch(number) or not folder.is_absolute():
            raise ValueError("Enter a valid LCSC ID and an absolute library folder.")
        if not valid_library_name(library_name):
            raise ValueError("Enter a library name using letters A–Z, digits, underscores, or hyphens. Windows device names are reserved.")

        folder.mkdir(parents=True, exist_ok=True)
        log, status = import_part(number, folder.resolve(), library_name, selection["overwrite"])
        try:
            preference.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=preference.parent, delete=False) as pending:
                temporary = Path(pending.name)
                try:
                    pending.write(library_name.encode("utf-8"))
                    pending.close()
                    temporary.replace(preference)
                finally:
                    pending.close()
                    temporary.unlink(missing_ok=True)
        except OSError:
            status += "\nKiCad LCSC Importer could not save the library name for next time."
        ctypes.windll.user32.MessageBoxW(None, f"{log}\n\n{status}", "Import LCSC", 0x40040)
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        ctypes.windll.user32.MessageBoxW(None, str(error), "Import LCSC failed", 0x40010)


if __name__ == "__main__":
    main()
