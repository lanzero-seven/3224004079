"""
文本预处理模块

1.数据清洗
2.jieba分词
3.停用词过滤
"""
import re
from typing import List

import jieba


# 暂时使用一个较小的中文停用词表
STOP_WORDS = {
    "的", "了", "是", "我", "在", "有", "和", "就", "不",
    "人", "都", "一", "他", "这", "那", "也", "很", "又",
    "或", "及", "与", "则", "而", "之", "等", "个", "把",
    "被", "让"
}


def clean_text(raw_text: str) -> str:
    """
    清洗文本。

    当前版本：
    保留中文、英文和数字；
    去除其他特殊符号。
    """
    if not isinstance(raw_text, str):
        raise TypeError("输入文本必须是字符串")

    cleaned_text = re.sub(
        r"[^\u4e00-\u9fa5a-zA-Z0-9]",
        "",
        raw_text
    )

    return cleaned_text


def tokenize_text(text: str) -> List[str]:
    """
    使用 jieba 对文本进行分词。
    """
    if not isinstance(text, str):
        raise TypeError("输入文本必须是字符串")

    return jieba.lcut(text)


def remove_stop_words(words: List[str]) -> List[str]:
    """
    删除停用词和空字符串。
    """
    return [
        word.strip()
        for word in words
        if word.strip() and word not in STOP_WORDS
    ]


def preprocess_text(raw_text: str, show_debug: bool = False) -> List[str]:
    """
    完整文本预处理流程：

    原始文本
        ↓
    文本清洗
        ↓
    jieba分词
        ↓
    停用词过滤
        ↓
    最终词语列表
    """

    # 第一步：清洗
    cleaned_text = clean_text(raw_text)

    # 第二步：jieba 分词
    words = tokenize_text(cleaned_text)

    # 第三步：过滤停用词
    filtered_words = remove_stop_words(words)

    # 调试输出
    if show_debug:
        print("\n========== 文本预处理 ==========")

        print(f"原始文本长度：{len(raw_text)}")
        print(f"清洗后长度：{len(cleaned_text)}")

        print("\n【清洗后的文本】")
        print(cleaned_text[:500])

        print("\n【jieba分词结果】")
        print(" / ".join(words[:100]))

        print("\n【过滤停用词后】")
        print(" / ".join(filtered_words[:100]))

        print(f"\n原始词语数量：{len(words)}")
        print(f"有效词语数量：{len(filtered_words)}")

        if len(words) > 100:
            print("（仅显示前100个词）")

        print("================================")

    return filtered_words
