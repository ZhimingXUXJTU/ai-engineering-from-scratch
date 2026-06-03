#!/usr/bin/env python3
"""Personal learning progress tracker for AI Engineering from Scratch.

Tracks which lessons you've studied, quiz scores, time spent, and notes.
Data stored in MY_PROGRESS.json at repo root.

Usage:
    python scripts/track_progress.py start  <phase>/<lesson>   # mark lesson started
    python scripts/track_progress.py done   <phase>/<lesson>   # mark lesson completed
    python scripts/track_progress.py skip   <phase>/<lesson>   # skip a lesson
    python scripts/track_progress.py undo   <phase>/<lesson>   # reset to not_started
    python scripts/track_progress.py note   <phase>/<lesson> "some note"
    python scripts/track_progress.py time   <phase>/<lesson> <minutes>  # log time
    python scripts/track_progress.py quiz   <phase>/<lesson>   # run interactive quiz
    python scripts/track_progress.py status [phase_num]        # show progress overview
    python scripts/track_progress.py report                    # detailed report
    python scripts/track_progress.py next                      # suggest next lesson

Lesson path format: phase-dir/lesson-dir (relative to phases/)
    e.g. 01-math-foundations/01-linear-algebra-intuition
    or just the number: 1/1  (shortcut for phase 01, lesson 01)
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PHASES_DIR = REPO_ROOT / "phases"
DATA_FILE = REPO_ROOT / "MY_PROGRESS.json"

STATUS_ORDER = ["not_started", "in_progress", "completed", "skipped"]

STATUS_ICONS = {
    "not_started": "  ",
    "in_progress": "..",
    "completed":   "OK",
    "skipped":     "--",
}


# ── Data management ──────────────────────────────────────────────

def load_data() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {"created": now_iso(), "lessons": {}}


def save_data(data: dict) -> None:
    data["last_updated"] = now_iso()
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ── Path resolution ──────────────────────────────────────────────

def resolve_lesson(path: str) -> tuple[str, Path]:
    """Accept 'phase/lesson', 'NN/NN', or full path. Return (key, Path)."""
    # Shortcut: "1/1" -> "01-math-foundations/01-linear-algebra-intuition"
    if "/" in path and path.replace("/", "").isdigit():
        phase_num = int(path.split("/")[0])
        lesson_num = int(path.split("/")[1])
        return resolve_by_numbers(phase_num, lesson_num)

    # Already a phase-dir/lesson-dir
    parts = path.strip("/").split("/")
    if len(parts) == 2:
        phase_dir = parts[0]
        lesson_dir = parts[1]
        full = PHASES_DIR / phase_dir / lesson_dir
        if full.exists():
            return f"{phase_dir}/{lesson_dir}", full

    # Try partial match on lesson name
    if len(parts) == 1:
        for phase_dir in sorted(PHASES_DIR.iterdir()):
            if not phase_dir.is_dir():
                continue
            for lesson_dir in sorted(phase_dir.iterdir()):
                if lesson_dir.is_dir() and lesson_dir.name.startswith(parts[0]):
                    key = f"{phase_dir.name}/{lesson_dir.name}"
                    return key, lesson_dir

    print(f"Error: lesson not found: {path}")
    print("Use format: phase-dir/lesson-dir  e.g. 01-math-foundations/01-linear-algebra-intuition")
    print("Or shortcut: phase_num/lesson_num  e.g. 1/1")
    sys.exit(1)


def resolve_by_numbers(phase_num: int, lesson_num: int) -> tuple[str, Path]:
    """Resolve '1/1' to the actual directory path."""
    phase_dirs = sorted(d for d in PHASES_DIR.iterdir()
                        if d.is_dir() and d.name.startswith(f"{phase_num:02d}"))
    if not phase_dirs:
        print(f"Error: phase {phase_num} not found")
        sys.exit(1)
    phase_dir = phase_dirs[0]

    lesson_dirs = sorted(d for d in phase_dir.iterdir()
                         if d.is_dir() and d.name.startswith(f"{lesson_num:02d}"))
    if not lesson_dirs:
        print(f"Error: lesson {lesson_num} not found in phase {phase_num}")
        sys.exit(1)
    lesson_dir = lesson_dirs[0]

    return f"{phase_dir.name}/{lesson_dir.name}", lesson_dir


def get_phase_name(phase_dir: str) -> str:
    """Extract human-readable name from directory like '01-math-foundations'."""
    parts = phase_dir.split("-", 1)
    if len(parts) == 2:
        return parts[1].replace("-", " ").title()
    return phase_dir


# ── Lesson commands ──────────────────────────────────────────────

def cmd_start(data: dict, path: str) -> None:
    key, _ = resolve_lesson(path)
    lesson = data["lessons"].setdefault(key, {"status": "not_started"})
    if lesson["status"] == "completed":
        print(f"Already completed: {key}")
        return
    lesson["status"] = "in_progress"
    if "started_at" not in lesson:
        lesson["started_at"] = now_iso()
    save_data(data)
    print(f"Started: {key}")


def cmd_done(data: dict, path: str) -> None:
    key, _ = resolve_lesson(path)
    lesson = data["lessons"].setdefault(key, {"status": "not_started"})
    lesson["status"] = "completed"
    lesson["completed_at"] = now_iso()
    save_data(data)
    print(f"Completed: {key}")


def cmd_skip(data: dict, path: str) -> None:
    key, _ = resolve_lesson(path)
    lesson = data["lessons"].setdefault(key, {"status": "not_started"})
    lesson["status"] = "skipped"
    save_data(data)
    print(f"Skipped: {key}")


def cmd_undo(data: dict, path: str) -> None:
    key, _ = resolve_lesson(path)
    if key in data["lessons"]:
        data["lessons"][key]["status"] = "not_started"
        save_data(data)
    print(f"Reset: {key}")


def cmd_note(data: dict, path: str, text: str) -> None:
    key, _ = resolve_lesson(path)
    lesson = data["lessons"].setdefault(key, {"status": "not_started"})
    notes = lesson.setdefault("notes", [])
    notes.append({"text": text, "at": now_iso()})
    save_data(data)
    print(f"Note added to {key}")


def cmd_time(data: dict, path: str, minutes: int) -> None:
    key, _ = resolve_lesson(path)
    lesson = data["lessons"].setdefault(key, {"status": "not_started"})
    lesson["time_minutes"] = lesson.get("time_minutes", 0) + minutes
    save_data(data)
    print(f"Logged {minutes} min for {key} (total: {lesson['time_minutes']} min)")


# ── Quiz ─────────────────────────────────────────────────────────

def cmd_quiz(data: dict, path: str) -> None:
    key, lesson_path = resolve_lesson(path)
    quiz_file = lesson_path / "quiz.json"
    if not quiz_file.exists():
        print(f"No quiz found for {key}")
        return

    quiz = json.loads(quiz_file.read_text(encoding="utf-8"))
    questions = quiz.get("questions", [])
    if not questions:
        print(f"Quiz is empty for {key}")
        return

    print(f"\n=== Quiz: {key} ===\n")

    # Run pre-quiz first, then post
    for stage in ["pre", "post"]:
        stage_qs = [q for q in questions if q.get("stage") == stage]
        if not stage_qs:
            continue

        stage_label = "PRE-LESSON" if stage == "pre" else "POST-LESSON"
        print(f"--- {stage_label} ({len(stage_qs)} questions) ---\n")

        correct = 0
        for i, q in enumerate(stage_qs, 1):
            print(f"Q{i}: {q['question']}")
            for j, opt in enumerate(q["options"]):
                print(f"  {chr(65+j)}) {opt}")

            while True:
                ans = input("\nYour answer (A/B/C/D or number 1-4): ").strip().upper()
                if ans in ("A", "B", "C", "D"):
                    ans_idx = ord(ans) - ord("A")
                    break
                elif ans in ("1", "2", "3", "4"):
                    ans_idx = int(ans) - 1
                    break
                elif ans == "":
                    ans_idx = -1
                    break
                print("Enter A-D or 1-4 (or Enter to skip)")

            is_correct = ans_idx == q["correct"]
            if is_correct:
                correct += 1
                print("  >> Correct!")
            elif ans_idx >= 0:
                print(f"  >> Wrong. Correct: {chr(65 + q['correct'])}) {q['options'][q['correct']]}")
            else:
                print(f"  >> Skipped. Answer: {chr(65 + q['correct'])}) {q['options'][q['correct']]}")
            print(f"  {q.get('explanation', '')}\n")

        score = f"{correct}/{len(stage_qs)}"
        pct = correct / len(stage_qs) * 100 if stage_qs else 0
        print(f"  {stage_label} score: {score} ({pct:.0f}%)\n")

        lesson = data["lessons"].setdefault(key, {"status": "not_started"})
        lesson[f"quiz_{stage}"] = {"score": score, "pct": round(pct, 1), "at": now_iso()}

    save_data(data)


# ── Status & Report ──────────────────────────────────────────────

def scan_all_lessons() -> dict[str, list[str]]:
    """Return {phase_dir: [lesson_dir, ...]} for all phases."""
    result = {}
    for phase_dir in sorted(PHASES_DIR.iterdir()):
        if not phase_dir.is_dir() or phase_dir.name.startswith("."):
            continue
        lessons = sorted(
            d.name for d in phase_dir.iterdir()
            if d.is_dir() and d.name[0:2].isdigit()
        )
        if lessons:
            result[phase_dir.name] = lessons
    return result


def cmd_status(data: dict, phase_filter: str | None = None) -> None:
    all_lessons = scan_all_lessons()
    lessons_data = data.get("lessons", {})

    total_lessons = sum(len(v) for v in all_lessons.values())
    done = sum(1 for v in lessons_data.values() if v.get("status") == "completed")
    skipped = sum(1 for v in lessons_data.values() if v.get("status") == "skipped")
    in_prog = sum(1 for v in lessons_data.values() if v.get("status") == "in_progress")
    total_time = sum(v.get("time_minutes", 0) for v in lessons_data.values())

    print(f"\n{'='*60}")
    print(f"  AI Learning Progress — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*60}")
    print(f"  Total: {total_lessons} lessons")
    print(f"  Done: {done}  In Progress: {in_prog}  Skipped: {skipped}  Remaining: {total_lessons - done - skipped - in_prog}")
    if total_time > 0:
        print(f"  Time logged: {total_time // 60}h {total_time % 60}m")
    if done + skipped > 0:
        pct = (done + skipped) / total_lessons * 100
        print(f"  Coverage: {pct:.1f}%")
    print()

    for phase_dir, lesson_dirs in all_lessons.items():
        # Filter by phase number if requested
        if phase_filter and not phase_dir.startswith(f"{int(phase_filter):02d}"):
            continue

        phase_num = phase_dir.split("-")[0]
        phase_name = get_phase_name(phase_dir)

        # Count statuses
        p_done = sum(1 for l in lesson_dirs
                     if lessons_data.get(f"{phase_dir}/{l}", {}).get("status") == "completed")
        p_skip = sum(1 for l in lesson_dirs
                     if lessons_data.get(f"{phase_dir}/{l}", {}).get("status") == "skipped")
        p_prog = sum(1 for l in lesson_dirs
                     if lessons_data.get(f"{phase_dir}/{l}", {}).get("status") == "in_progress")

        bar_len = 20
        filled = int((p_done + p_skip) / len(lesson_dirs) * bar_len) if lesson_dirs else 0
        bar = "#" * filled + "-" * (bar_len - filled)

        status_parts = []
        if p_done: status_parts.append(f"done:{p_done}")
        if p_prog: status_parts.append(f"wip:{p_prog}")
        if p_skip: status_parts.append(f"skip:{p_skip}")
        status_str = " ".join(status_parts) if status_parts else "not started"

        print(f"  P{phase_num} {phase_name:35s} [{bar}] {p_done + p_skip}/{len(lesson_dirs)}  {status_str}")

        # Show lesson-level detail for active phases
        if p_prog > 0 or (phase_filter and int(phase_filter) == int(phase_num)):
            for ldir in lesson_dirs:
                key = f"{phase_dir}/{ldir}"
                st = lessons_data.get(key, {}).get("status", "not_started")
                icon = STATUS_ICONS.get(st, "??")
                lesson_name = ldir.split("-", 1)[1] if "-" in ldir else ldir
                print(f"    [{icon}] {ldir}")

    print()


def cmd_report(data: dict) -> None:
    lessons_data = data.get("lessons", {})
    if not lessons_data:
        print("No progress recorded yet.")
        return

    print(f"\n{'='*60}")
    print(f"  Detailed Learning Report — {data.get('last_updated', 'N/A')}")
    print(f"{'='*60}\n")

    by_phase: dict[str, list] = {}
    for key, info in sorted(lessons_data.items()):
        phase = key.split("/")[0]
        by_phase.setdefault(phase, []).append((key, info))

    total_time = 0
    for phase, items in sorted(by_phase.items()):
        phase_name = get_phase_name(phase)
        print(f"--- Phase {phase} ({phase_name}) ---")
        for key, info in items:
            status = info.get("status", "unknown")
            icon = STATUS_ICONS.get(status, "??")
            t = info.get("time_minutes", 0)
            total_time += t
            time_str = f"{t}min" if t else ""

            # Quiz scores
            quiz_str = ""
            for qtype in ["quiz_pre", "quiz_post"]:
                if qtype in info:
                    q = info[qtype]
                    label = "pre" if "pre" in qtype else "post"
                    quiz_str += f" {label}:{q['score']}"

            notes_count = len(info.get("notes", []))

            lesson_short = key.split("/", 1)[1] if "/" in key else key
            parts = []
            if time_str: parts.append(time_str)
            if quiz_str: parts.append(quiz_str.strip())
            if notes_count: parts.append(f"notes:{notes_count}")
            extra = " | ".join(parts) if parts else ""

            print(f"  [{icon}] {lesson_short:50s} {extra}")

        print()

    print(f"Total time: {total_time // 60}h {total_time % 60}m")
    print()


def cmd_next(data: dict) -> None:
    """Suggest the next lesson to study based on current progress."""
    all_lessons = scan_all_lessons()
    lessons_data = data.get("lessons", {})

    # Find first non-completed, non-skipped lesson in order
    for phase_dir, lesson_dirs in all_lessons.items():
        for ldir in lesson_dirs:
            key = f"{phase_dir}/{ldir}"
            status = lessons_data.get(key, {}).get("status", "not_started")
            if status == "in_progress":
                phase_name = get_phase_name(phase_dir)
                print(f"\n  Resume (in progress):")
                print(f"  {key}")
                print(f"  Phase: {phase_name}")
                print(f"  Command: python scripts/track_progress.py done {key}")
                print()
                return

    # No in-progress, find first not_started
    for phase_dir, lesson_dirs in all_lessons.items():
        for ldir in lesson_dirs:
            key = f"{phase_dir}/{ldir}"
            status = lessons_data.get(key, {}).get("status", "not_started")
            if status == "not_started":
                phase_name = get_phase_name(phase_dir)
                lesson_name = ldir.split("-", 1)[1].replace("-", " ") if "-" in ldir else ldir
                print(f"\n  Next lesson:")
                print(f"  {key}")
                print(f"  Phase: {phase_name} — {lesson_name}")
                print(f"  Start:  python scripts/track_progress.py start {key}")
                print()
                return

    print("\n  All lessons completed or skipped!\n")


# ── Main ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    data = load_data()

    if cmd in ("start", "done", "skip", "undo", "quiz"):
        if len(sys.argv) < 3:
            print(f"Usage: track_progress.py {cmd} <phase>/<lesson>")
            sys.exit(1)
        path = sys.argv[2]

        if cmd == "start":
            cmd_start(data, path)
        elif cmd == "done":
            cmd_done(data, path)
        elif cmd == "skip":
            cmd_skip(data, path)
        elif cmd == "undo":
            cmd_undo(data, path)
        elif cmd == "quiz":
            cmd_quiz(data, path)

    elif cmd == "note":
        if len(sys.argv) < 4:
            print('Usage: track_progress.py note <phase>/<lesson> "your note"')
            sys.exit(1)
        cmd_note(data, sys.argv[2], " ".join(sys.argv[3:]))

    elif cmd == "time":
        if len(sys.argv) < 4:
            print("Usage: track_progress.py time <phase>/<lesson> <minutes>")
            sys.exit(1)
        try:
            minutes = int(sys.argv[3])
        except ValueError:
            print("Error: minutes must be a number")
            sys.exit(1)
        cmd_time(data, sys.argv[2], minutes)

    elif cmd == "status":
        phase_filter = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_status(data, phase_filter)

    elif cmd == "report":
        cmd_report(data)

    elif cmd == "next":
        cmd_next(data)

    else:
        print(f"Unknown command: {cmd}")
        print("Commands: start done skip undo quiz note time status report next")
        sys.exit(1)


if __name__ == "__main__":
    main()
