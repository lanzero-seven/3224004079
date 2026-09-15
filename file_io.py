"""
文件读写模块

进行读取文本和结果写入文本
"""

import os

def read_text(file_path: str) -> str:
    """
    读取文本文件。

    支持 UTF-8、GBK、GB18030 三种常见中文编码。
    如果读取失败，直接抛出异常，由 main.py 统一处理。
    """
    if not file_path:
        raise ValueError("文件路径不能为空")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")

    if os.path.isdir(file_path):
        raise IsADirectoryError(f"路径是文件夹，不是文件：{file_path}")

    encodings = ["utf-8", "gbk", "gb18030"]

    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        f"无法识别文件编码：{file_path}"
    )


def write_answer(file_path: str, score: float) -> None:
    """
    将最终查重率写入答案文件。
    保留两位小数。
    """
    if not file_path:
        raise ValueError("答案文件路径不能为空")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{score:.2f}")
