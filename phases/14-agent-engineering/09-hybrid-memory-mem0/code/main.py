"""Mem0-shaped hybrid memory: vector + KV + graph with fusion scoring.

Stdlib only. Vector store uses token-overlap as an embedding stand-in.
Scope taxonomy: user / session / agent. Fusion: relevance + importance + recency.

核心概念：混合记忆系统 —— 向量存储（语义搜索）+ KV 存储（精确查找）+ 图存储（关系推理）
三种存储协同工作，通过融合评分（相关性 + 重要性 + 时间衰减）检索最相关的记忆。
支持 user/session/agent 三级作用域隔离，确保记忆不会跨用户泄漏。

AI 对应：Mem0 是目前最流行的 Agent 记忆层，被 LangChain、LlamaIndex 等框架集成。
其融合评分思路类似于搜索引擎的 PageRank + 新鲜度排序。
ChatGPT 的记忆功能、Claude 的项目记忆都采用了类似的向量+KV混合存储架构。
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Record:
    rid: str
    text: str
    scope: str
    user_id: str
    session_id: str
    importance: float = 0.5
    ts: float = field(default_factory=time.time)
    tags: tuple[str, ...] = ()


class VectorStore:
    """向量存储 —— 用词重叠（Jaccard 系数）模拟向量嵌入的语义搜索。"""
    def __init__(self) -> None:
        self._records: dict[str, Record] = {}

    def add(self, record: Record) -> None:
        self._records[record.rid] = record

    def search(self, query: str, top_k: int = 5) -> list[tuple[float, Record]]:
        q_tokens = set(query.lower().split())
        scored: list[tuple[float, Record]] = []
        for record in self._records.values():
            r_tokens = set(record.text.lower().split())
            if not r_tokens:
                continue
            overlap = len(q_tokens & r_tokens)
            if overlap == 0:
                continue
            score = overlap / (len(q_tokens | r_tokens))
            scored.append((score, record))
        scored.sort(key=lambda x: -x[0])
        return scored[:top_k]


@dataclass(frozen=True)
class KVKey:
    user_id: str
    fact_type: str
    entity: str


class KVStore:
    """KV 存储 —— 用于精确的键值查找，如"用户的城市是什么"。"""
    def __init__(self) -> None:
        self._map: dict[KVKey, Record] = {}

    def put(self, key: KVKey, record: Record) -> None:
        self._map[key] = record

    def get(self, key: KVKey) -> Record | None:
        return self._map.get(key)

    def by_user(self, user_id: str) -> list[Record]:
        return [r for k, r in self._map.items() if k.user_id == user_id]


@dataclass
class Edge:
    subject: str
    relation: str
    obj: str
    valid: bool = True
    ts: float = field(default_factory=time.time)


class GraphStore:
    """图存储 —— 管理实体间的关系（三元组），新关系自动使旧的相同关系失效。"""
    def __init__(self) -> None:
        self._edges: list[Edge] = []

    def add_edge(self, subject: str, relation: str, obj: str) -> None:
        """添加三元组边，自动使同主语同关系的旧边失效（保留最新关系）。"""
        for edge in self._edges:
            if edge.valid and edge.subject == subject and edge.relation == relation:
                edge.valid = False  # 旧关系失效
        self._edges.append(Edge(subject=subject, relation=relation, obj=obj))

    def neighbors(self, subject: str, valid_only: bool = True) -> list[Edge]:
        return [e for e in self._edges
                if e.subject == subject and (e.valid or not valid_only)]

    def all_edges(self) -> list[Edge]:
        return list(self._edges)


@dataclass
class Mem0Config:
    """Mem0 配置 —— 控制融合评分中相关性、重要性和时间衰减的权重。"""
    w_relevance: float = 0.6
    w_importance: float = 0.2
    w_recency: float = 0.2
    recency_halflife_s: float = 86400.0  # 时间衰减半衰期（秒），默认1天


class Mem0:
    """Mem0 混合记忆系统 —— 整合向量、KV 和图三种存储，通过融合评分检索记忆。"""
    def __init__(self, config: Mem0Config | None = None) -> None:
        self.vector = VectorStore()
        self.kv = KVStore()
        self.graph = GraphStore()
        self.config = config or Mem0Config()
        self._counter = 0

    def add(self, text: str, *, user_id: str, session_id: str = "s0",
            scope: str = "user", importance: float = 0.5,
            tags: tuple[str, ...] = (),
            kv_triples: tuple[tuple[str, str], ...] = (),
            graph_triples: tuple[tuple[str, str, str], ...] = ()) -> str:
        """添加记忆 —— 同时写入向量、KV 和图三种存储。"""
        self._counter += 1
        rid = f"m{self._counter:03d}"
        record = Record(rid=rid, text=text, scope=scope, user_id=user_id,
                        session_id=session_id, importance=importance, tags=tags)
        self.vector.add(record)
        for fact_type, entity in kv_triples:  # 写入 KV 存储
            self.kv.put(KVKey(user_id=user_id, fact_type=fact_type, entity=entity), record)
        for subject, relation, obj in graph_triples:  # 写入图存储
            self.graph.add_edge(subject, relation, obj)
        return rid

    def _recency_score(self, record: Record, now: float) -> float:
        """计算时间衰减分数 —— 使用指数衰减，半衰期由配置控制。"""
        elapsed = max(0.0, now - record.ts)
        half = self.config.recency_halflife_s
        return 0.5 ** (elapsed / half) if half > 0 else 1.0  # 指数衰减

    def search(self, query: str, *, user_id: str,
               scope: str | None = None, top_k: int = 5) -> list[tuple[float, Record]]:
        """融合搜索 —— 综合向量搜索和 KV 查找的结果，按融合评分排序返回 top_k。"""
        now = time.time()
        vector_hits = self.vector.search(query, top_k=top_k * 3)  # 向量搜索：召回候选
        fused: dict[str, tuple[float, Record]] = {}
        for rel, record in vector_hits:
            # 作用域过滤：只返回匹配用户和作用域的记录
            if scope is not None and record.scope != scope:
                continue
            if record.user_id != user_id and record.scope == "user":
                continue
            recency = self._recency_score(record, now)
            # 融合评分 = 相关性 * 权重 + 重要性 * 权重 + 时间衰减 * 权重
            score = (self.config.w_relevance * rel
                     + self.config.w_importance * record.importance
                     + self.config.w_recency * recency)
            fused[record.rid] = (score, record)
        # 补充 KV 存储中的结果（可能未被向量搜索召回）
        for record in self.kv.by_user(user_id):
            if record.rid in fused:
                continue
            recency = self._recency_score(record, now)
            score = (self.config.w_relevance * 0.4
                     + self.config.w_importance * record.importance
                     + self.config.w_recency * recency)
            fused[record.rid] = (score, record)
        ordered = sorted(fused.values(), key=lambda x: -x[0])  # 按融合评分降序排列
        return ordered[:top_k]


def main() -> None:
    print("=" * 70)
    print("MEM0 HYBRID MEMORY — Phase 14, Lesson 09")
    print("=" * 70)

    mem = Mem0()

    mem.add(
        "ava prefers citation-heavy, terse writing over tutorial style",
        user_id="ava", session_id="s001",
        importance=0.7, tags=("preference", "writing"),
        kv_triples=(("writing_style", "terse_citation_heavy"),),
    )
    mem.add(
        "ava is building a 30-lesson curriculum on agent engineering",
        user_id="ava", session_id="s001",
        importance=0.9, tags=("project",),
        kv_triples=(("project", "agent_curriculum"),),
        graph_triples=(("ava", "owns_project", "agent_curriculum"),),
    )
    mem.add(
        "ava lives in Berlin",
        user_id="ava", session_id="s001",
        importance=0.6, tags=("profile",),
        kv_triples=(("city", "Berlin"),),
        graph_triples=(("ava", "lives_in", "Berlin"),),
    )
    mem.add(
        "ava moved to Lisbon last month",
        user_id="ava", session_id="s002",
        importance=0.8, tags=("profile", "update"),
        kv_triples=(("city", "Lisbon"),),
        graph_triples=(("ava", "lives_in", "Lisbon"),),
    )
    mem.add(
        "bob requested a refund for invoice 4711",
        user_id="bob", session_id="s010",
        importance=0.9, tags=("billing",),
        kv_triples=(("refund_request", "4711"),),
    )

    print("\nvector-only recall for 'writing style preferences'")
    for score, record in mem.vector.search("writing style preferences", top_k=3):
        print(f"  {score:.3f}  {record.rid}  {record.text}")

    print("\ngraph recall for entities linked to 'ava'")
    for edge in mem.graph.neighbors("ava", valid_only=False):
        status = "VALID  " if edge.valid else "INVALID"
        print(f"  [{status}] {edge.subject} --{edge.relation}--> {edge.obj}")

    print("\nKV recall for ava all facts")
    for record in mem.kv.by_user("ava"):
        print(f"  {record.rid}  {record.text}")

    print("\nfused top-3 for ava, query 'where does ava live'")
    for score, record in mem.search("where does ava live", user_id="ava", top_k=3):
        print(f"  {score:.3f}  {record.rid}  {record.text}")

    print("\nfused top-3 for ava, query 'what is she building'")
    for score, record in mem.search("what is ava building", user_id="ava", top_k=3):
        print(f"  {score:.3f}  {record.rid}  {record.text}")

    print("\nscope isolation: bob's refund does not leak to ava's search")
    hits = mem.search("refund invoice", user_id="ava", top_k=5)
    print(f"  ava results: {len(hits)}  (expect 0 user-scoped hits from bob)")
    for score, record in hits:
        print(f"    {score:.3f}  {record.user_id}  {record.text}")

    print()
    print("fusion: relevance + importance + recency. per-product weight tuning.")


if __name__ == "__main__":
    main()  # 运行主函数
