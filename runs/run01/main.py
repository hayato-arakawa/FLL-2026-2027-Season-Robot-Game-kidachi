import sys
# from importlib import import_module
# from pathlib import Path

if __package__ is None:
    # sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    pass

from utils.control import run_with_timing
from utils.runtime import ensure_project_root

ensure_project_root(__file__)

# 現在有効なバージョン（同ディレクトリのファイル名から拡張子を除いたもの）
ACTIVE_VARIANT = "m08_m06_m05"


def load_variant():
    """ACTIVE_VARIANT で指定したモジュールをロードして返す。"""
    if __package__:
        module_path = "{0}.{1}".format(__package__, ACTIVE_VARIANT)
    else:
        module_path = "runs.run01.{0}".format(ACTIVE_VARIANT)

    return __import__(module_path, None, None, ["*"])



async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    variant = load_variant()
    label = "run01:{0}".format(ACTIVE_VARIANT)
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
    from pybricks.tools import multitask, run_task
    from setup import initialize_robot

    hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot()
    variant = load_variant()
    label = "run01:{0}".format(ACTIVE_VARIANT)

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

    # センサーロガーがあれば並行実行、なければ run だけ実行
    if hasattr(variant, "sensor_logger_task"):
        run_task(
            multitask(variant.sensor_logger_task(hub, robot, left_wheel, right_wheel), timed_run())
        )
    else:
        run_task(timed_run())
