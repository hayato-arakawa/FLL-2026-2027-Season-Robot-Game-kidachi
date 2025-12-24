"""
実行時のブートストラップ用ユーティリティ。

主に次の目的で使用します:
- `runs/` 配下のスクリプトを単体実行する際にプロジェクトルートを sys.path に追加する
- プロジェクトルート Path を取得する
"""

import sys


def ensure_project_root(current_file):
    """
    スクリプトの位置からプロジェクトルートを探索し、sys.path に追加して返す。
    Pybricks MicroPython 互換のため pathlib や複雑な探索は削除。
    3階層上 (runs/runXX/main.py から見たルート) をルートと仮定する。
    """
    # 簡易的なパス操作: 文字列として扱う
    # current_file は __file__ (例: "runs/run01/main.py")
    
    # パス区切り文字の正規化（念のため）
    path_str = str(current_file).replace("\\", "/")
    
    # 簡易的に "../.." 相当のパスを追加
    # 注: Pybricksでは絶対パス取得が難しいため、相対パスで sys.path に追加する
    # runs/runXX/main.py -> ルートは 2階層上だが、
    # 念のため sys.path に "." も追加しておく
    
    if "." not in sys.path:
        sys.path.append(".")
        
    return "."

