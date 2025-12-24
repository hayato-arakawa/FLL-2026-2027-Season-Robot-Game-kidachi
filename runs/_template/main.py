"""
新しい run ディレクトリを作るときのテンプレート。
runXX/main.py をこのファイルからコピーして、ACTIVE_VARIANT とラベルを差し替えてください。
"""

import sys
# from importlib import import_module (MicroPython has no importlib)
# from pathlib import Path (MicroPython has no pathlib)

if __package__ is None:
    # 簡易的に sys.path に追加 (utils.runtime.ensure_project_root でやるのでここでは最小限)
    # 3つ上 (root) を追加
    import os
    # sys.path.append(os.getcwd()) # 状況によるが、runtime に任せる
    pass

from pybricks.tools import multitask, run_task, wait
from utils.control import run_with_timing
from utils.runtime import ensure_project_root

ensure_project_root(__file__)

# 同ディレクトリ内のバリアント（例: sample_variant.py）を指定
ACTIVE_VARIANT = "sample_variant"


def load_variant():
    """
    ACTIVE_VARIANT で指定したモジュールをロードして返す。
    MicroPython 互換のため __import__ を使用。
    """
    if __package__:
        module_path = "{0}.{1}".format(__package__, ACTIVE_VARIANT)
    else:
        module_path = "runs._template.{0}".format(ACTIVE_VARIANT)
        
    return __import__(module_path, None, None, ["*"])



async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    variant = load_variant()
    label = "runXX:{0}".format(ACTIVE_VARIANT)
    return await run_with_timing(
        label,
        lambda: variant.run(
            hub,
            robot,
            left_wheel,
            right_wheel,
            left_lift,
            right_lift,
        ),
    )


if __name__ == "__main__":
    from setup import initialize_robot

    hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot()
    variant = load_variant()
    label = "runXX:{0}".format(ACTIVE_VARIANT)

    async def timed_run():
        await run_with_timing(
            label,
            lambda: variant.run(
                hub,
                robot,
                left_wheel,
                right_wheel,
                left_lift,
                right_lift,
            ),
        )

    if hasattr(variant, "sensor_logger_task"):
        if hasattr(variant, "stop_logging"):

            async def wrapped_run():
                await timed_run()
                variant.stop_logging = True
                await wait(500)

            run_task(
                multitask(
                    variant.sensor_logger_task(hub, robot, left_wheel, right_wheel),
                    wrapped_run(),
                )
            )
        else:
            run_task(
                multitask(
                    variant.sensor_logger_task(hub, robot, left_wheel, right_wheel),
                    timed_run(),
                )
            )
    else:
        run_task(timed_run())
