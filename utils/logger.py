"""
ログ出力ユーティリティ。

目的:
- 既存の print() を活かしつつ、コンソールとファイルへ同時出力（tee）する
- ログはプロジェクトルート直下の logs/ に保存する
"""

import builtins

def logs_dir():
    """logs ディレクトリのパス文字列を返す。（作成は省略、エラーなら手動作成を促す）"""
    return "logs"


class TeeStdout:
    """
    print をフックし、コンソールとファイルに同時出力するクラス（コンテキストマネージャ）。
    contextlib 削除のためクラスで実装。
    """
    def __init__(self, run_name):
        self.run_name = run_name
        self.log_file = None
        self.original_print = builtins.print

    def __enter__(self):
        # タイムスタンプなしでファイル名を作成
        # logs ディレクトリが存在することを前提とする、または例外を無視する
        log_path = "{0}/{1}.log".format(logs_dir(), self.run_name)
        
        # Pybricksでディレクトリ作成は標準では難しい（os.mkdirなどがない場合がある）ため
        # 事前に logs ディレクトリがあることを期待する、あるいは直下に書く
        # ここでは logs/runXX.log に追記モードで開く
        try:
            self.log_file = open(log_path, "a")
        except OSError:
            # logs ディレクトリがないなどの場合、ルートに書く
            log_path = "{0}.log".format(self.run_name)
            self.log_file = open(log_path, "a")

        self.log_path = log_path

        def _print(*args, **kwargs):
            sep = kwargs.get("sep", " ")
            end = kwargs.get("end", "\n")
            message = sep.join(str(a) for a in args) + end
            
            if self.log_file:
                self.log_file.write(message)
                # flush はない場合があるが、あるなら呼ぶ
                # self.log_file.flush() 
            
            self.original_print(*args, **kwargs)

        builtins.print = _print
        return log_path

    def __exit__(self, exc_type, exc_value, traceback):
        builtins.print = self.original_print
        if self.log_file:
            self.log_file.close()


def tee_stdout(run_name):
    """(旧API互換用) TeeStdout クラスのインスタンスを返す"""
    return TeeStdout(run_name)

