"""
文本相似度计算模块

词频向量+余弦相似度计算
"""
import math
from collections import Counter
from typing import List


def calculate_word_frequency(words: List[str]) -> Counter:
    """
    统计每个词语出现的次数。
    """
    return Counter(words)


def calc_similarity(
        words1: List[str],
        words2: List[str],
        show_debug: bool = False
) -> float:
    """
    使用词频向量 + 余弦相似度计算文本重复率。

    返回值范围：
        0 ~ 100

    例如：
        0.85 -> 85.00%
    """

    # 统计词频
    counter1 = calculate_word_frequency(words1)
    counter2 = calculate_word_frequency(words2)

    # 构建共同词表
    all_words = set(counter1) | set(counter2)

    # 计算向量点积
    dot_product = sum(
        counter1[word] * counter2[word]
        for word in all_words
    )

    # 计算两个向量的模
    norm1 = math.sqrt(
        sum(count ** 2 for count in counter1.values())
    )

    norm2 = math.sqrt(
        sum(count ** 2 for count in counter2.values())
    )

    # 防止除零
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # 余弦相似度
    cosine_similarity = dot_product / (norm1 * norm2)

    # 防止浮点误差造成超过100%
    cosine_similarity = max(
        0.0,
        min(1.0, cosine_similarity)
    )

    repeat_rate = cosine_similarity * 100

    # 调试输出
    if show_debug:
        print("\n========== 相似度计算 ==========")

        print(f"原文有效词数：{len(words1)}")
        print(f"抄袭版有效词数：{len(words2)}")

        print(f"原文不同词数量：{len(counter1)}")
        print(f"抄袭版不同词数量：{len(counter2)}")

        print(f"共同词数量：{len(set(counter1) & set(counter2))}")

        print(f"\n向量点积：{dot_product:.4f}")
        print(f"原文向量模：{norm1:.4f}")
        print(f"抄袭版向量模：{norm2:.4f}")

        print(f"\n余弦相似度：{cosine_similarity:.6f}")
        print(f"查重率：{repeat_rate:.2f}%")

        print("================================")

    return repeat_rate
