"""Letta-shaped memory blocks with a sleep-time consolidation agent.

Primary agent writes raw facts during turns. Sleep-time agent runs between
turns, off the critical path, and consolidates blocks. Scripted so it runs
offline.

核心概念：记忆块（Memory Blocks）+ 睡眠时间计算（Sleep-Time Compute）—— 将记忆整理工作
从用户交互的关键路径上移出。主 Agent 在对话轮次中快速写入原始事实，
睡眠时间 Agent 在轮次之间（离线）运行，合并接近上限的记忆块、
使失效的归档记录标记为无效，不影响用户感知的延迟。

AI 对应：Letta 的 sleep-time compute 模式让 Agent 可以在用户不活跃时
用更强的模型做记忆整理。类似于人类睡眠期间大脑巩固记忆的过程。
OpenAI 的 ChatGPT 记忆管理也采用类似的异步整理策略。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Block:
    """记忆块 —— 固定大小的文本容器，支持追加、替换和重写操作，并维护版本历史。"""
    label: str
    value: str = ""
    limit: int = 300
    description: str = ""
    version: int = 0
    history: list[str] = field(default_factory=list)

    def append(self, text: str) -> str:
        """追加文本到记忆块，记录版本历史。"""
        old = self.value
        self.value = (self.value + " " + text).strip() if self.value else text
        self.version += 1
        self.history.append(old)  # 保存旧版本，支持回滚
        return f"{self.label} v{self.version} ({len(self.value)}/{self.limit})"

    def replace(self, old: str, new: str) -> str:
        if old not in self.value:
            return f"error: {old!r} not in {self.label}"
        prev = self.value
        self.value = self.value.replace(old, new)
        self.version += 1
        self.history.append(prev)
        return f"{self.label} v{self.version} replaced"

    def rewrite(self, new: str) -> str:
        prev = self.value
        self.value = new
        self.version += 1
        self.history.append(prev)
        return f"{self.label} v{self.version} rewritten ({len(self.value)}/{self.limit})"

    def near_limit(self, threshold: float = 0.8) -> bool:
        """检查记忆块是否接近容量上限（默认 80%），用于触发合并。"""
        return len(self.value) >= int(self.limit * threshold)


class BlockStore:
    """记忆块存储 —— 管理多个命名记忆块，支持创建、查询和渲染。"""
    def __init__(self) -> None:
        self._blocks: dict[str, Block] = {}

    def create(self, label: str, description: str, limit: int = 300) -> Block:
        block = Block(label=label, description=description, limit=limit)
        self._blocks[label] = block
        return block

    def get(self, label: str) -> Block | None:
        return self._blocks.get(label)

    def labels(self) -> list[str]:
        return sorted(self._blocks)

    def render(self) -> str:
        lines: list[str] = []
        for label in self.labels():
            block = self._blocks[label]
            lines.append(f"[{block.label} v{block.version} "
                         f"{len(block.value)}/{block.limit}]")
            lines.append(f"  {block.value}")
        return "\n".join(lines)


@dataclass
class ArchivalRecord:
    rid: str
    text: str
    valid: bool = True


class Archival:
    def __init__(self) -> None:
        self._records: list[ArchivalRecord] = []
        self._counter = 0

    def insert(self, text: str) -> str:
        self._counter += 1
        rid = f"a{self._counter:03d}"
        self._records.append(ArchivalRecord(rid=rid, text=text))
        return rid

    def invalidate(self, rid: str) -> bool:
        for record in self._records:
            if record.rid == rid:
                record.valid = False
                return True
        return False

    def valid_records(self) -> list[ArchivalRecord]:
        return [r for r in self._records if r.valid]

    def all_records(self) -> list[ArchivalRecord]:
        return list(self._records)


class PrimaryAgent:
    """主 Agent —— 处理用户对话轮次，快速写入原始事实到记忆块和归档，不做整理。"""

    def __init__(self, blocks: BlockStore, archival: Archival) -> None:
        self.blocks = blocks
        self.archival = archival
        self.trace: list[str] = []

    def turn(self, user_text: str, writes: list[tuple[str, str, str]]) -> str:
        self.trace.append(f"user: {user_text}")
        for kind, label_or_text, payload in writes:
            if kind == "block_append":
                block = self.blocks.get(label_or_text)
                if block is not None:
                    self.trace.append(f"  block_append -> {block.append(payload)}")
            elif kind == "archival_insert":
                rid = self.archival.insert(payload)
                self.trace.append(f"  archival_insert -> {rid}")
        response = f"response to: {user_text}"
        self.trace.append(f"assistant: {response}")
        return response


class SleepTimeAgent:
    """睡眠时间 Agent —— 在关键路径之外运行，合并接近上限的记忆块，
    使失效的归档记录标记为无效，不影响用户感知的延迟。
    """

    def __init__(self, blocks: BlockStore, archival: Archival) -> None:
        self.blocks = blocks
        self.archival = archival
        self.trace: list[str] = []

    def run(self, contradictions: list[tuple[str, str]]) -> None:
        """执行睡眠时间整理：合并接近上限的记忆块，使矛盾的归档记录失效。"""
        self.trace.append("sleep-time pass start")
        for label in self.blocks.labels():
            block = self.blocks.get(label)
            if block is None:
                continue
            if block.near_limit():  # 记忆块接近上限，需要合并
                summary = _summarize(block.value, block.limit // 2)
                result = block.rewrite(summary)  # 用摘要替换原始内容
                self.trace.append(f"  consolidate {label}: {result}")
        for claim, reason in contradictions:  # 处理矛盾的归档记录
            for record in self.archival.all_records():
                if record.valid and claim.lower() in record.text.lower():
                    self.archival.invalidate(record.rid)  # 标记为失效
                    self.trace.append(
                        f"  invalidate {record.rid} ({reason}): {record.text[:50]}..."
                    )
        self.trace.append("sleep-time pass end")


def _summarize(text: str, target_len: int) -> str:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if not sentences:
        return text[:target_len]
    picked: list[str] = []
    total = 0
    for sentence in sentences:
        if total + len(sentence) + 1 > target_len:
            break
        picked.append(sentence)
        total += len(sentence) + 2
    return ". ".join(picked) + "."


def main() -> None:
    print("=" * 70)
    print("LETTA MEMORY BLOCKS + SLEEP-TIME COMPUTE — Phase 14, Lesson 08")
    print("=" * 70)

    blocks = BlockStore()
    blocks.create("human", "facts about the user", limit=180)
    blocks.create("persona", "the agent's self-concept", limit=160)
    blocks.create("task", "the current task scope", limit=220)
    archival = Archival()

    primary = PrimaryAgent(blocks, archival)
    sleep = SleepTimeAgent(blocks, archival)

    primary.turn(
        "my name is ava, I ship agents for a living, I live in Berlin",
        [("block_append", "human", "name=ava role=ships_agents city=Berlin")],
    )
    primary.turn(
        "today help me plan a 30-lesson curriculum on agent engineering",
        [
            ("block_append", "task", "plan 30-lesson agent curriculum, target senior eng"),
            ("archival_insert", "",
             "ava prefers concise, citation-heavy writing over tutorial-style"),
        ],
    )
    primary.turn(
        "I moved to Lisbon last month; update your notes",
        [
            ("block_append", "human", "city=Lisbon (updated from Berlin)"),
            ("archival_insert", "",
             "ava lives in Berlin - old address, outdated"),
        ],
    )
    primary.turn(
        "also the curriculum target is senior and staff engineers, not junior",
        [("block_append", "task",
          "audience=senior+staff eng, cite arXiv and first-party framework docs")],
    )

    print("\nprimary turns (writes are fast and raw)")
    for line in primary.trace:
        print(f"  {line}")

    print("\nblocks after primary phase (pre-consolidation)")
    print(blocks.render())

    sleep.run(contradictions=[
        ("ava lives in Berlin",
         "human block updated city to Lisbon; Berlin archival claim is stale"),
    ])

    print("\nsleep-time trace")
    for line in sleep.trace:
        print(f"  {line}")

    print("\nblocks after sleep-time (consolidated)")
    print(blocks.render())

    print("\narchival state")
    for record in archival.all_records():
        status = "VALID  " if record.valid else "INVALID"
        print(f"  {record.rid} [{status}] {record.text}")

    print()
    print("key property: primary-turn latency is unchanged by consolidation.")
    print("sleep-time can run a stronger, slower model — it is off the path.")


if __name__ == "__main__":
    main()  # 运行主函数
