import re

CHINESE_CHAR_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
WHITESPACE_RE = re.compile(r"\s+")

SUMMARY_MIN_CHARS = 120
SUMMARY_MAX_CHARS = 180
SUMMARY_TARGET_MIN_CHARS = 140
SUMMARY_TARGET_MAX_CHARS = 170


def normalize_summary_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", (text or "")).strip()


def count_chinese_chars(text: str) -> int:
    return len(CHINESE_CHAR_RE.findall(text or ""))


def summary_needs_repair(text: str) -> bool:
    chinese_chars = count_chinese_chars(normalize_summary_text(text))
    return chinese_chars < SUMMARY_MIN_CHARS or chinese_chars > SUMMARY_MAX_CHARS
