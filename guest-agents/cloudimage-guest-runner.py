#!/usr/bin/env python3
"""Run a Cloud Image build bundle locally on the temporary guest VM."""

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


BUNDLE_DIR = Path(os.environ["GHA_BUILD_BUNDLE_DIR"])
RUNTIME_PATH = BUNDLE_DIR / "runtime.json"
MANIFEST_PATH = BUNDLE_DIR / "manifest.json"
LOG_PATH = BUNDLE_DIR / "build.log"
STATUS_PATH = BUNDLE_DIR / "status.json"
RESULT_PATH = BUNDLE_DIR / "result.json"
CANCEL_PATH = BUNDLE_DIR / "cancel.request"
PENDING_EVENTS_PATH = BUNDLE_DIR / "pending-events.jsonl"


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True) + "\n")
    temporary.replace(path)


def append_log(message: str) -> None:
    with LOG_PATH.open("a") as log:
        log.write(message)
        log.flush()


def post_event(runtime: dict, event: dict) -> bool:
    callback_url = runtime.get("callback_url")
    callback_token = runtime.get("callback_token")

    if not callback_url or not callback_token:
        return False

    request = urllib.request.Request(
        callback_url,
        data=json.dumps(event).encode(),
        headers={
            "Authorization": f"Bearer {callback_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10):
            return True
    except (urllib.error.URLError, TimeoutError):
        # The durable log/status/result files are reconciled by the manager when
        # a callback cannot be delivered.
        return False


def deliver_pending_events(runtime: dict) -> None:
    if not PENDING_EVENTS_PATH.exists():
        return

    undelivered = []
    for line in PENDING_EVENTS_PATH.read_text().splitlines():
        message = json.loads(line)
        if not post_event(runtime, message):
            undelivered.append(message)

    if undelivered:
        PENDING_EVENTS_PATH.write_text("".join(json.dumps(message) + "\n" for message in undelivered))
    else:
        PENDING_EVENTS_PATH.unlink()


def event(runtime: dict, sequence: int, event_type: str, **payload: object) -> int:
    message = {"sequence": sequence, "type": event_type, **payload}
    with PENDING_EVENTS_PATH.open("a") as pending:
        pending.write(json.dumps(message) + "\n")
    deliver_pending_events(runtime)

    return sequence + 1


def source_path(runtime: dict, upload: dict) -> Path:
    root = upload.get("source_root", "runner_images")
    if root == "catalog_root":
        base = BUNDLE_DIR / "catalog"
    elif root == "template":
        base = BUNDLE_DIR / "template"
    else:
        base = BUNDLE_DIR / "runner-images"

    return base / upload["source"]


def install_upload(runtime: dict, upload: dict) -> None:
    source = source_path(runtime, upload)
    destination = Path(upload["destination"])

    if source.is_dir():
        # The manifest destination is the directory's target root. Copy its contents to
        # match the existing per-file SFTP behavior, rather than nesting source.name below it.
        subprocess.run(["sudo", "mkdir", "-p", str(destination)], check=True)
        subprocess.run(["sudo", "cp", "-a", f"{source}/.", str(destination)], check=True)
        target = destination
    else:
        target = destination
        subprocess.run(["sudo", "mkdir", "-p", str(target.parent)], check=True)
        subprocess.run(["sudo", "cp", str(source), str(target)], check=True)

    if "mode" in upload:
        command = ["sudo", "chmod"]
        if source.is_dir():
            command.append("-R")
        subprocess.run([*command, format(upload["mode"], "o"), str(target)], check=True)


def run_stage(runtime: dict, stage: dict) -> tuple[int, str | None]:
    for upload in stage.get("uploads", []):
        install_upload(runtime, upload)

    script = stage.get("script")
    if not script:
        return 0, None

    environment = os.environ.copy()
    environment.update(runtime.get("environment", {}))
    environment.update(stage.get("environment", {}))
    process = subprocess.Popen(
        ["bash", str(BUNDLE_DIR / "template" / script)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=environment,
    )

    assert process.stdout is not None
    for line in process.stdout:
        append_log(line)

    return process.wait(), None


def main() -> int:
    runtime = json.loads(RUNTIME_PATH.read_text())
    manifest = json.loads(MANIFEST_PATH.read_text())
    sequence = 1
    started_at = int(time.time())
    atomic_json(STATUS_PATH, {"state": "running", "started_at": started_at})
    sequence = event(runtime, sequence, "started")

    for group in manifest.get("stage_groups", []):
        for stage in group.get("stages", []):
            if CANCEL_PATH.exists():
                atomic_json(RESULT_PATH, {"outcome": "cancelled", "stage_id": stage["id"], "exit_code": 130})
                event(runtime, sequence, "completed", outcome="cancelled", stage_id=stage["id"], exit_code=130)
                return 130

            append_log(stage["marker"] + "\n")
            atomic_json(STATUS_PATH, {"state": "running", "stage_id": stage["id"], "started_at": started_at})
            sequence = event(runtime, sequence, "stage_started", stage_id=stage["id"])

            try:
                exit_code, error = run_stage(runtime, stage)
            except Exception as exc:
                exit_code, error = getattr(exc, "returncode", 1), str(exc)

            if exit_code != 0:
                message = error or f"Cloud image stage failed: {stage['id']} (exit code {exit_code})."
                atomic_json(RESULT_PATH, {"outcome": "failed", "stage_id": stage["id"], "exit_code": exit_code, "error": message})
                event(runtime, sequence, "completed", outcome="failed", stage_id=stage["id"], exit_code=exit_code, error=message)
                return exit_code

            sequence = event(runtime, sequence, "stage_completed", stage_id=stage["id"])

    atomic_json(RESULT_PATH, {"outcome": "succeeded", "exit_code": 0})
    atomic_json(STATUS_PATH, {"state": "succeeded", "started_at": started_at})
    event(runtime, sequence, "completed", outcome="succeeded", exit_code=0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
