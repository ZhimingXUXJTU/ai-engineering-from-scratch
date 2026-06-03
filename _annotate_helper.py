"""
Helper script to check annotation status and identify files that need work.
"""
import os
import glob

BASE = "Z:/learn-AI_from-scratch/ai-engineering-from-scratch/phases"

phases = [
    "04-computer-vision",
    "06-speech-and-audio",
    "08-generative-ai",
    "09-reinforcement-learning",
    "10-llms-from-scratch",
    "11-llm-engineering",
    "12-multimodal-ai",
    "13-tools-and-protocols",
]

for phase in phases:
    phase_dir = os.path.join(BASE, phase)
    lessons = sorted(glob.glob(os.path.join(phase_dir, "*/docs/en.md")))
    total = len(lessons)
    need_work = []
    for lesson_path in lessons:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        cn_count = content.count("【中文") + content.count("【拓展")
        if cn_count < 4:
            lesson_name = os.path.basename(os.path.dirname(os.path.dirname(lesson_path)))
            need_work.append(f"  {lesson_name} (blocks: {cn_count})")
    print(f"\n=== {phase} ({len(need_work)}/{total} need work) ===")
    for item in need_work:
        print(item)
