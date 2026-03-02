"""Simple retrieval layer for facts-only Mutual Fund FAQ answers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from prompts import (
    ADVICE_KEYWORDS,
    FIELD_LABELS,
    FIELD_SYNONYMS,
    REFUSAL_TEXT,
    STATEMENT_KEYWORDS,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "funds.json"
DEFAULT_SOURCE_URL = "https://www.indmoney.com/mutual-funds"
STATEMENT_SOURCE_URL = (
    "https://www.indmoney.com/learn/mutual-funds/"
    "what-is-a-mutual-fund-statement-and-how-to-download-it"
)
SOURCE_MONTH_YEAR = "March 2026"


class FundFactsRetriever:
    """Retrieves factual scheme values from local JSON data."""

    def __init__(self, data_path: Path = DATA_PATH) -> None:
        with data_path.open("r", encoding="utf-8") as f:
            self.funds: List[Dict[str, Any]] = json.load(f)

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"[^a-z0-9\s]", " ", text.lower()).strip()

    def _is_advice_query(self, query: str) -> bool:
        q = self._normalize(query)
        return any(keyword in q for keyword in ADVICE_KEYWORDS)

    def _is_statement_query(self, query: str) -> bool:
        q = self._normalize(query)
        if "statement" in q and any(x in q for x in ["download", "how", "get"]):
            return True
        return any(keyword in q for keyword in STATEMENT_KEYWORDS)

    def _detect_field(self, query: str) -> Optional[str]:
        q = self._normalize(query)

        # Resolve common ambiguity for minimum investment questions.
        if "sip" in q:
            return "minimum_sip"
        if "lump" in q or "lumpsum" in q:
            return "minimum_lump_sum"

        for field, keywords in FIELD_SYNONYMS.items():
            if any(keyword in q for keyword in keywords):
                return field
        return None

    def _find_fund(self, query: str) -> Optional[Dict[str, Any]]:
        q_norm = self._normalize(query)
        best_match: Optional[Dict[str, Any]] = None
        best_score = 0

        for fund in self.funds:
            aliases = [fund["fund_name"], *fund.get("aliases", [])]
            for alias in aliases:
                alias_norm = self._normalize(alias)
                if alias_norm and alias_norm in q_norm:
                    score = len(alias_norm)
                    if score > best_score:
                        best_match = fund
                        best_score = score

        if best_match:
            return best_match

        if "elss" in q_norm:
            for fund in self.funds:
                if "elss" in self._normalize(str(fund.get("category", ""))):
                    return fund

        # Fallback to token overlap when partial names are used.
        q_tokens = set(q_norm.split())
        stop_tokens = {
            "fund",
            "direct",
            "plan",
            "growth",
            "option",
            "of",
            "the",
            "what",
            "is",
            "minimum",
            "ratio",
            "exit",
            "load",
            "sip",
            "lump",
            "sum",
            "lock",
            "in",
            "period",
            "riskometer",
            "benchmark",
        }
        q_tokens -= stop_tokens

        for fund in self.funds:
            name_tokens = set(self._normalize(fund["fund_name"]).split()) - stop_tokens
            overlap = len(q_tokens & name_tokens)
            if overlap > best_score:
                best_score = overlap
                best_match = fund

        return best_match if best_score > 0 else None

    def _build_response(
        self,
        answer_text: str,
        source_url: str,
        last_updated_from_sources: str = SOURCE_MONTH_YEAR,
    ) -> Dict[str, str]:
        return {
            "answer_text": answer_text,
            "source_url": source_url,
            "last_updated_from_sources": last_updated_from_sources,
        }

    def answer(self, query: str) -> Dict[str, str]:
        query = (query or "").strip()
        if not query:
            return self._build_response(
                "Please ask a factual question about expense ratio, exit load, minimum SIP, "
                "minimum lump sum, lock-in period, riskometer, or benchmark.",
                DEFAULT_SOURCE_URL,
            )

        matched_fund = self._find_fund(query)

        if self._is_advice_query(query):
            source_url = matched_fund["source_url"] if matched_fund else self.funds[0]["source_url"]
            return self._build_response(REFUSAL_TEXT, source_url)

        if self._is_statement_query(query):
            return self._build_response(
                "To download a mutual fund statement, INDMoney's official guide lists methods "
                "through CAMS Online, KFintech, MF Central, and AMC portals.",
                STATEMENT_SOURCE_URL,
            )

        field = self._detect_field(query)
        if not field:
            return self._build_response(
                "I can provide factual details for fund name, AMC, category, expense ratio, "
                "exit load, minimum SIP, minimum lump sum, lock-in period, riskometer, and benchmark.",
                DEFAULT_SOURCE_URL,
            )

        if not matched_fund:
            return self._build_response(
                "I could not find that fund in the current INDMoney dataset. Please ask about one of "
                "the included schemes.",
                DEFAULT_SOURCE_URL,
            )

        value = str(matched_fund.get(field, "Not available"))
        answer_text = f"{FIELD_LABELS[field]} of {matched_fund['fund_name']} is {value}."
        return self._build_response(answer_text, matched_fund["source_url"])
