"""Prompt and policy constants for the Mutual Fund Facts Assistant."""

SYSTEM_RULES = """
You are a facts-only Mutual Fund FAQ assistant for INDMoney scheme pages.
Answer only factual scheme details from the local dataset and provide exactly one official source link.
Do not provide investment advice, recommendations, buy/sell calls, allocation suggestions, return comparisons, or performance claims.
Keep responses concise and factual.
""".strip()

REFUSAL_TEXT = (
    "I can only provide factual information about mutual fund schemes, not investment advice "
    "or recommendations. You can review the official fund details here."
)

FIELD_SYNONYMS = {
    "expense_ratio": ["expense ratio", "expense", "ter"],
    "exit_load": ["exit load"],
    "minimum_sip": ["minimum sip", "min sip", "sip amount", "sip"],
    "minimum_lump_sum": [
        "minimum lump sum",
        "minimum lumpsum",
        "min lump sum",
        "lump sum",
        "lumpsum",
        "minimum investment",
    ],
    "lock_in_period": ["lock-in", "lock in", "lockin", "lock-in period"],
    "riskometer": ["riskometer", "risk level", "risk"],
    "benchmark_index": ["benchmark", "benchmark index", "index"],
    "category": ["category"],
    "amc": ["amc", "asset management company"],
    "fund_name": ["fund name", "scheme name"],
}

FIELD_LABELS = {
    "expense_ratio": "Expense ratio",
    "exit_load": "Exit load",
    "minimum_sip": "Minimum SIP",
    "minimum_lump_sum": "Minimum lump sum",
    "lock_in_period": "Lock-in period",
    "riskometer": "Riskometer",
    "benchmark_index": "Benchmark index",
    "category": "Category",
    "amc": "AMC",
    "fund_name": "Fund name",
}

ADVICE_KEYWORDS = [
    "advice",
    "recommend",
    "recommendation",
    "best fund",
    "best mutual fund",
    "which fund should",
    "should i",
    "buy",
    "sell",
    "compare",
    "portfolio",
    "allocation",
    "compare returns",
    "returns comparison",
    "higher return",
    "outperform",
    "invest in",
]

STATEMENT_KEYWORDS = [
    "statement",
    "download statement",
    "mutual fund statement",
    "cas statement",
]
