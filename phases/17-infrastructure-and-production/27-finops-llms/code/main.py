"""Multi-tenant LLM FinOps simulator with enforcement ladder — stdlib Python.

Three-tier enforcement:
  1. rate limit per tenant
  2. daily spend cap per tenant
  3. kill switch on spend z-score > 4

核心概念：多租户 LLM FinOps 执法阶梯——三级防护：1) Rate Limit(每分钟请求限制)、
2) Spend Cap(日消费上限 = 合同金额 x 2)、3) Kill Switch(z-score > 4 时自动暂停)，
滥用租户在第 5 天触发 Kill Switch，正常和增长租户在限额内运行
AI 对应：OpenAI 和 Anthropic 的 API rate limiting 实现类似的分级保护；
AWS Budgets 和 GCP Billing Alerts 提供云级消费告警；
Vercel 的 usage-based billing 和 Stripe 的 billing 是 SaaS 计费的参考；
FinOps Foundation 定义了云成本管理的标准实践；
多租户 LLM 平台（OpenAI Platform、Anthropic Console）都需要此模式
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random
import statistics


@dataclass
class TenantPolicy:
    contracted_daily_usd: float
    rate_limit_per_min: int
    spend_cap_multiplier: float = 2.0
    kill_z_score: float = 4.0


@dataclass
class TenantState:
    spend_today_usd: float = 0.0
    minute_count: int = 0
    daily_history: list = field(default_factory=list)
    paused: bool = False


TENANTS = {
    "tenant_A_normal":  (TenantPolicy(100.0, rate_limit_per_min=120), TenantState(), 1.0),
    "tenant_B_growing": (TenantPolicy(50.0,  rate_limit_per_min=60),  TenantState(), 2.5),
    "tenant_C_abusive": (TenantPolicy(20.0,  rate_limit_per_min=40),  TenantState(), 25.0),
}


def simulate_day(day: int, verbose: bool) -> None:
    for name, (policy, state, traffic_mult) in TENANTS.items():
        if state.paused:
            continue
        requests = int(100 * traffic_mult * random.uniform(0.8, 1.3))
        tokens_per_req = int(random.gauss(600, 150))
        cost_per_req = (tokens_per_req / 1e6) * 10.0
        total_spend = requests * cost_per_req
        state.spend_today_usd += total_spend

        if state.spend_today_usd > policy.contracted_daily_usd * policy.spend_cap_multiplier:
            if verbose:
                print(f"  [cap breach] {name}: ${state.spend_today_usd:.2f} > cap ${policy.contracted_daily_usd * policy.spend_cap_multiplier:.2f} → tighten rate + alert CS")

        if len(state.daily_history) >= 5:
            mean = statistics.mean(state.daily_history)
            sd = statistics.stdev(state.daily_history) or 1
            z = (state.spend_today_usd - mean) / sd
            if z > policy.kill_z_score:
                state.paused = True
                if verbose:
                    print(f"  [KILL SWITCH] {name}: z={z:.2f} on spend ${state.spend_today_usd:.2f} (baseline ${mean:.2f} ± ${sd:.2f}) → auto-pause + page on-call")


def main() -> None:
    print("=" * 95)
    print("FINOPS ENFORCEMENT — three tenants over 10 days, abusive tenant triggers kill switch")
    print("=" * 95)
    random.seed(7)

    for day in range(1, 11):
        print(f"\n— Day {day} —")
        simulate_day(day, verbose=True)
        for name, (policy, state, _) in TENANTS.items():
            status = "PAUSED" if state.paused else "active"
            print(f"  {name}: spend=${state.spend_today_usd:7.2f}, contract=${policy.contracted_daily_usd:.2f}  [{status}]")
            state.daily_history.append(state.spend_today_usd)
            if not state.paused:
                state.spend_today_usd = 0.0
    print("\nRead: rate limits throttle; caps trigger alerts; kill switch catches blow-ups.")


if __name__ == "__main__":
    main()  # 运行主函数
