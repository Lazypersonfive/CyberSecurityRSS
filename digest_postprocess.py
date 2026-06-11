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


# Technical elements a vulnerability summary should cover (Direction 3 in
# tasks/current_state_2026-06-11.md). Patterns are intentionally loose: they
# detect that the *topic* is addressed, not that it is well written.
VULN_TECH_ELEMENT_RES = {
    "vuln_type": re.compile(
        r"注入|溢出|越权|绕过|反序列化|路径穿越|路径遍历|UAF|释放后使用|RCE|远程代码"
        r"|权限提升|提权|XSS|跨站|SSRF|CSRF|逻辑缺陷|配置错误|后门|内存损坏|条件竞争"
        r"|身份验证|认证缺陷|目录遍历|代码执行|拒绝服务|信息泄露",
        re.IGNORECASE,
    ),
    "trigger": re.compile(
        r"触发|需要|前提|无需|未经身份|经过身份|本地访问|远程攻击者|构造|发送|诱导|交互|默认配置",
    ),
    "scope": re.compile(
        r"版本|v\d|\d+\.\d|影响.{0,8}(组件|系统|产品|用户|实例)|受影响|波及",
        re.IGNORECASE,
    ),
    "remediation": re.compile(
        r"修复|补丁|升级|缓解|尚未|已发布|建议|临时方案|官方未",
    ),
}

VULN_MIN_TECH_ELEMENTS = 2


def vuln_tech_element_count(text: str) -> int:
    """How many of the four vuln-summary elements the text touches."""
    normalized = normalize_summary_text(text)
    return sum(1 for pattern in VULN_TECH_ELEMENT_RES.values() if pattern.search(normalized))


def vuln_summary_needs_repair(text: str) -> bool:
    return vuln_tech_element_count(text) < VULN_MIN_TECH_ELEMENTS
