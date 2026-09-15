"""
论文查重系统主程序。

1. 接收命令行参数
2. 调用文本处理模块
3. 输出查重结果
"""
import sys
from file_io import read_text, write_answer
from processing import preprocess_text
from similarity import calc_similarity


def print_text_preview(title: str, text: str, length: int = 300) -> None:
    """
    输出文本预览。
    """
    print(f"\n========== {title} ==========")
    if not text:
        print("（文件为空）")
        return
    if len(text) <= length:
        print(text)
    else:
        print(text[:length])
        print(f"...（仅显示前 {length} 个字符）")


def run_check(orig_path: str, copy_path: str, out_path: str) -> float:
    """
    执行完整查重业务逻辑：读取、预处理、计算、写入结果。
    :param orig_path: 原始论文文件路径
    :param copy_path: 抄袭论文文件路径
    :param out_path: 输出结果文件路径
    :return: 查重重复率浮点数
    """
    # Step1 读取文件
    orig_raw_text = read_text(orig_path)
    copy_raw_text = read_text(copy_path)

    print("✓ 原文读取成功")
    print(f"  原文字符数：{len(orig_raw_text)}")
    print("✓ 抄袭版读取成功")
    print(f"  抄袭版字符数：{len(copy_raw_text)}")

    print_text_preview("原文预览", orig_raw_text)
    print_text_preview("抄袭版预览", copy_raw_text)

    # Step2 预处理
    orig_words = preprocess_text(orig_raw_text, show_debug=True)
    copy_words = preprocess_text(copy_raw_text, show_debug=True)

    # Step3 计算相似度
    repeat_rate = calc_similarity(orig_words, copy_words, show_debug=True)

    # Step4 写入答案
    write_answer(out_path, repeat_rate)
    print("✓ 答案文件写入成功")
    print(f"✓ 输出路径：{out_path}")

    return repeat_rate


def main():
    """
    主入口函数：解析命令行参数，调用查重，处理各类异常。
    """
    print("\n")
    print("========================================")
    print("          论文查重程序 - Debug版")
    print("========================================")

    # 检查命令行参数数量
    if len(sys.argv) != 4:
        print("\n参数数量错误！")
        print("正确格式：")
        print("python main.py 原文路径 抄袭版路径 答案路径")
        sys.exit(1)

    orig_file_path = sys.argv[1]
    copy_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    print("\n========== 文件路径 ==========")
    print(f"原文文件：{orig_file_path}")
    print(f"抄袭文件：{copy_file_path}")
    print(f"答案文件：{output_file_path}")

    try:
        print("\n\n========== Step 1：读取文件 ==========")
        repeat_rate = run_check(orig_file_path, copy_file_path, output_file_path)

        print("\n")
        print("========================================")
        print(f"        最终查重率：{repeat_rate:.2f}%")
        print("========================================")
        print("\n程序运行完成！")

    except FileNotFoundError as error:
        print(f"\n❌ 文件不存在：{error}")
        sys.exit(1)
    except PermissionError as error:
        print(f"\n❌ 文件权限错误：{error}")
        sys.exit(1)
    except IsADirectoryError as error:
        print(f"\n❌ 路径错误：{error}")
        sys.exit(1)
    # pylint: disable=W0718
    except Exception as error:
        print(f"\n❌ 程序发生异常：{error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
