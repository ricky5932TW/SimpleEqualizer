import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


STATUS_FILE = Path("static/status.txt")
INSTRUCTION_FILE = Path("instruction.txt")
RUN_ID_FILE = Path("static/run_id.txt")
IMAGE_DIR = Path("static/temp_img")
RUNTIME_IMAGES = ("full.png", "Spectrum.png", "separated_spectrum.png")


def _atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(data)
    os.replace(tmp_path, path)


def write_status(data):
    _atomic_write(STATUS_FILE, data)


def read_status():
    try:
        return STATUS_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def write_instruction(data):
    _atomic_write(INSTRUCTION_FILE, data)


def read_instruction():
    try:
        return INSTRUCTION_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def current_run_id():
    try:
        return RUN_ID_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""


def clear_runtime_outputs():
    if IMAGE_DIR.exists():
        for file_name in RUNTIME_IMAGES:
            image_path = IMAGE_DIR / file_name
            try:
                image_path.unlink()
            except (FileNotFoundError, OSError):
                pass
    write_instruction(" ")


def start_run():
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S") + "-" + uuid4().hex[:8]
    clear_runtime_outputs()
    _atomic_write(RUN_ID_FILE, run_id)
    write_status("Starting...")
    return run_id
