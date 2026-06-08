"""Load-test anti-pattern demonstrator — stdlib Python.

Simulates how uniform prompts inflate reported throughput via prefix-cache
and request-coalescing, while realistic distribution reveals the true ceiling.

核心概念：LLM API 负载测试的反模式——统一 prompt 陷阱：所有请求使用相同 prompt
导致 prefix cache 命中率虚高(100%)，掩盖了真实的 TTFT 分布；
使用多样化的 prompt 分布(mean+stddev)才能反映生产环境的真实性能
AI 对应：LLMPerf 是 LLM 服务负载测试的参考工具，提供 --mean-input-tokens 和
--stddev-input-tokens 参数控制 prompt 多样性；GenAI-Perf (NVIDIA) 是另一个
LLM 专用基准测试工具；Locust 和 k6 是通用的 HTTP 负载测试工具；
vLLM 的 prefix caching 在统一 prompt 下表现虚高是已知的基准陷阱
"""

from __future__ import annotations

from dataclasses import dataclass
import random
import statistics


PREFIX_CACHE_HIT_TTFT_MS = 80
PREFIX_CACHE_MISS_TTFT_MS = 800
TPOT_MS = 15
BATCH_EFFICIENCY_SHARED_PREFIX = 0.8  # batch serves 1/0.8 = 1.25x fewer slots


@dataclass
class Request:
    prompt_tokens: int
    prefix_hash: str


def make_uniform_workload(n: int = 500) -> list[Request]:
    return [Request(2000, "single_prefix") for _ in range(n)]


def make_realistic_workload(n: int = 500, seed: int = 7) -> list[Request]:
    rng = random.Random(seed)
    reqs = []
    prefixes = [f"prefix_{i}" for i in range(80)]
    for _ in range(n):
        prompt = max(50, int(rng.gauss(500, 180)))
        reqs.append(Request(prompt, rng.choice(prefixes)))
    return reqs


def simulate(reqs: list[Request], concurrency: int) -> dict:
    cache: set[str] = set()
    ttft_samples: list[float] = []
    # serialize in groups of "concurrency"
    for i in range(0, len(reqs), concurrency):
        batch = reqs[i:i + concurrency]
        unique_prefixes = len({r.prefix_hash for r in batch})
        for r in batch:
            hit = r.prefix_hash in cache
            ttft = PREFIX_CACHE_HIT_TTFT_MS if hit else PREFIX_CACHE_MISS_TTFT_MS
            if not hit:
                cache.add(r.prefix_hash)
            ttft_samples.append(ttft)
    ttft_samples.sort()
    p50 = ttft_samples[len(ttft_samples) // 2]
    p99 = ttft_samples[int(len(ttft_samples) * 0.99) - 1]
    return {
        "n": len(reqs),
        "p50": p50,
        "p99": p99,
        "mean": statistics.mean(ttft_samples),
        "cache_hits": sum(1 for t in ttft_samples if t == PREFIX_CACHE_HIT_TTFT_MS),
    }


def main() -> None:
    print("=" * 95)
    print("PROMPT-UNIFORMITY TRAP — same test harness, different prompt distributions")
    print("=" * 95)

    for concurrency in (10, 50, 200):
        print(f"\nConcurrency = {concurrency}")
        header = f"{'Workload':22}  {'n':>5}  {'TTFT_P50':>9}  {'TTFT_P99':>9}  {'mean':>7}  cache_hits"
        print(header)
        print("-" * len(header))

        uniform = make_uniform_workload(500)
        u = simulate(uniform, concurrency)
        print(f"{'UNIFORM':22}  {u['n']:5}  {u['p50']:8.0f}ms  {u['p99']:8.0f}ms  {u['mean']:6.0f}ms  {u['cache_hits']:4}")

        realistic = make_realistic_workload(500)
        r = simulate(realistic, concurrency)
        print(f"{'REALISTIC':22}  {r['n']:5}  {r['p50']:8.0f}ms  {r['p99']:8.0f}ms  {r['mean']:6.0f}ms  {r['cache_hits']:4}")

    print("\nRead: uniform prompts make your endpoint look fast. Realistic prompts tell the truth.")
    print("LLMPerf: --mean-input-tokens + --stddev-input-tokens. Always.")


if __name__ == "__main__":
    main()  # 运行主函数
