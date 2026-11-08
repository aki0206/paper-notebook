"""各腳本共用的設定讀取與 frontmatter 解析。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 讓 Windows 終端機正確顯示中文
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")


def load_local_config() -> dict:
    path = ROOT / "local.config.json"
    if not path.exists():
        sys.exit("缺少 local.config.json，請複製 local.config.example.json 並填入路徑。")
    return json.loads(path.read_text(encoding="utf-8"))


def load_catalog() -> dict:
    return json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))


def _scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(v) for v in value[1:-1].split(",") if v.strip()]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def split_frontmatter(text: str) -> tuple[dict, str]:
    """解析筆記用到的簡單 YAML：key: value 與 - 清單。"""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text
    meta, key = {}, None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            if not isinstance(meta.get(key), list):
                meta[key] = []
            meta[key].append(_scalar(item.group(1)))
            continue
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            key = kv.group(1)
            meta[key] = _scalar(kv.group(2)) if kv.group(2) else []
    return meta, text[m.end():]


def dump_frontmatter(meta: dict) -> str:
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(json.dumps(x, ensure_ascii=False) for x in v)}]")
        else:
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n"
