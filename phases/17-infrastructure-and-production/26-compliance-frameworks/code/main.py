"""Cross-framework compliance mapping — stdlib Python.

Given a control, print the frameworks it satisfies. Given a customer profile
(geography + segment), print the required frameworks.

核心概念：跨框架合规映射——一个安全控制(如 access logging、encryption in transit、
PII redaction)对应多个合规框架(ISO 27001、GDPR、HIPAA、SOC 2、PCI-DSS、EU AI Act)，
以及按客户画像(地理区域+行业)确定所需合规框架
AI 对应：EU AI Act (2026 年 8 月 2 日高风险系统强制执行，罚款高达 3500 万欧元或
全球营收 7%)是 AI 系统最重要的新法规；SOC 2 Type II 是 B2B SaaS 的标准合规要求；
ISO 42001 是 AI 管理体系的新标准；Colorado AI Act SB24-205 是美国最早的 AI 法规之一；
HIPAA BAA 是医疗 AI 的必要前提
"""

from __future__ import annotations


CONTROL_MAP = {
    "access logging": ["ISO 27001 A.5.15-5.18", "GDPR Art. 32", "HIPAA §164.312(a)", "SOC 2 CC6"],
    "change management": ["ISO 27001 A.8.32", "PCI DSS Req. 6", "HIPAA breach-notification", "SOC 2 CC8"],
    "encryption in transit": ["ISO 27001 A.8.24", "GDPR Art. 32", "HIPAA §164.312(e)", "PCI DSS Req. 4"],
    "secrets management": ["ISO 27001 A.8.19", "PCI DSS Req. 8", "SOC 2 CC6.1"],
    "PII redaction (inference-time)": ["GDPR Art. 25", "EU AI Act Art. 10", "HIPAA §164.514"],
    "audit log retention": ["SOC 2 CC7", "HIPAA §164.312(b)", "ISO 27001 A.8.15"],
    "conformity assessment": ["EU AI Act Art. 43 (high-risk)"],
    "impact assessment": ["Colorado AI Act SB24-205", "EU AI Act Art. 27"],
    "data subject rights": ["GDPR Ch. III", "CCPA"],
    "BAA signed": ["HIPAA §164.504(e)"],
}


PROFILE_MAP = {
    ("US", "B2B SaaS"):             ["SOC 2 Type II", "ISO 27001", "ISO 42001"],
    ("US", "healthcare"):           ["SOC 2 Type II", "HIPAA", "ISO 27001"],
    ("US", "fintech"):              ["SOC 2 Type II", "PCI-DSS", "ISO 27001"],
    ("EU", "B2B SaaS"):             ["GDPR", "SOC 2 Type II", "ISO 27001", "EU AI Act"],
    ("EU", "healthcare"):           ["GDPR", "SOC 2 Type II", "HIPAA (global)", "EU AI Act"],
    ("Global", "enterprise"):       ["SOC 2 Type II", "ISO 27001", "ISO 42001", "GDPR", "HIPAA", "EU AI Act"],
    ("US-CO", "B2B SaaS"):          ["SOC 2 Type II", "Colorado AI Act", "ISO 27001"],
}


def main() -> None:
    print("=" * 80)
    print("COMPLIANCE CONTROL MAP — one control, many frameworks")
    print("=" * 80)
    for control, frameworks in CONTROL_MAP.items():
        print(f"\n{control}")
        for f in frameworks:
            print(f"  → {f}")

    print("\n" + "=" * 80)
    print("CUSTOMER PROFILE MAP — required frameworks per geography + segment")
    print("=" * 80)
    for (geo, segment), frameworks in PROFILE_MAP.items():
        print(f"\n{geo} · {segment}")
        for f in frameworks:
            print(f"  · {f}")

    print("\nNote: EU AI Act high-risk enforcement August 2, 2026.")
    print("Fines up to €35M or 7% global annual turnover.")


if __name__ == "__main__":
    main()  # 运行主函数
