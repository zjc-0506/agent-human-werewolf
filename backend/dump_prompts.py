# -*- coding: utf-8 -*-
"""
提示词契约的**只读**导出（给 §6 冻结落地用）。

用法（在仓库根执行，输出重定向到 docs/）：

    .venv\\Scripts\\python.exe backend\\dump_prompts.py > docs\\prompt-baseline-2026-10-28.json

存在的理由：冻结落地第 2 步要"按 key 逐条贴回 agents.py / summarize.py"，
手工抄 116 项必错。先把当前**生效值**导成一份基线，改完再导一次，`diff` 就是全部变化。

只读保证（三条都别破）：
  · 不调用任何写接口（本文件只 import 模块，不发 HTTP）；
  · 不碰 `_runtime.json`（不读也不写 —— 拿的是**当前进程内存里**的模块属性，
    也就等于"此刻 build_messages 会读到的值"）；
  · 不起服务。

输出：按 key 排序的 `{key: value}` JSON，`ensure_ascii=False, indent=1`。
诊断信息走 stderr，不污染 stdout 的 JSON。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import admin_api  # noqa: E402


def main() -> int:
    # stdout 固定 utf-8：prompt 正文里有 GBK 编不了的字符（发言进度段的 ✓、各类箭头），
    # 走 cp936 时一旦重定向就 UnicodeEncodeError（铁律 2）。
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                        # noqa: BLE001
        pass
    cat = admin_api._catalog()
    data = {}
    for it in cat:
        data[it["key"]] = admin_api._item_value(it)
    out = json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=1)
    sys.stdout.write(out + "\n")
    sys.stderr.write("[dump] 已导出 " + str(len(data)) + " 项（按 key 排序）\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
