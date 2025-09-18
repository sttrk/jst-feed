#!/usr/bin/env python3
"""
JSTフィード生成スクリプト（分精度）
優先順: NICT → WorldTimeAPI → ランナーのシステム時刻(JST変換)

出力: jst.json
  { "tz": "JST", "date": "YYYY-MM-DD", "time": "HH:MM" }
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone, timedelta

import requests


def try_nict():
    """NICTのJSON時刻を取得。失敗時は None。"""
    try:
        url = "https://ntp-a1.nict.go.jp/cgi-bin/json"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        for key in ("st", "it", "time"):
            if key in data and isinstance(data[key], (int, float)):
                utc = datetime.fromtimestamp(float(data[key]), tz=timezone.utc)
                return utc.astimezone(timezone(timedelta(hours=9)))
        return None
    except Exception:
        return None


def try_worldtimeapi():
    """WorldTimeAPIでAsia/Tokyoの現在時刻を取得。失敗時は None。"""
    try:
        url = "https://worldtimeapi.org/api/timezone/Asia/Tokyo"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        iso = r.json().get("datetime")
        if not iso:
            return None
        return datetime.fromisoformat(iso)
    except Exception:
        return None


def fallback_runner_clock():
    """最後の保険: ランナーのシステム時刻をJSTに変換。"""
    return datetime.now(timezone(timedelta(hours=9)))


def round_to_minute(dt: datetime):
    """datetimeを分に丸め、(YYYY-MM-DD, HH:MM) を返す。"""
    dt = dt.replace(second=0, microsecond=0)
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")


def main() -> int:
    dt = try_nict() or try_worldtimeapi() or fallback_runner_clock()
    date_str, time_str = round_to_minute(dt)
    payload = {"tz": "JST", "date": date_str, "time": time_str}
    with open("jst.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
