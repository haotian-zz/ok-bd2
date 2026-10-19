"""
以 Web 模式启动 ok-bd2（无 Qt 窗口），同时开放 HTTP API 供 tools/okctl.py 远程控制。

    .venv\\Scripts\\python.exe tools\\serve_web.py            # 默认 127.0.0.1:8766
    .venv\\Scripts\\python.exe tools\\serve_web.py --port 8800
    .venv\\Scripts\\python.exe tools\\serve_web.py --debug    # 同 main_debug.py，额外加载探针/诊断任务

浏览器打开 http://127.0.0.1:8766 能看到和桌面版一样的界面。
Web 模式和桌面版（main.py / main_debug.py）不能同时运行。
需要 ok-script[web]（fastapi + uvicorn）。
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--debug", action="store_true", help="加载 main_debug.py 的调试任务")
    args = parser.parse_args()
    os.chdir(ROOT)
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from ok import run_web

    from src.config import config

    if args.debug:
        from src.debug_profile import configure_debug_profile
        from src.tasks.debug_registry import install_debug_tasks

        configure_debug_profile(config)
        install_debug_tasks(config)

    run_web(config, host=args.host, port=args.port, open_browser=False)


if __name__ == "__main__":
    main()
