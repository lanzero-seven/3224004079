"""
文本相似度计算模块

TF-IDF + 余弦相似度计算文本重复率
"""

import math
from collections import Counter
from typing import List


def calculate_tf(words: List[str]) -> dict:
    """
    计算词频 TF
    """
    counter = Counter(words)

    total_words = len(words)

    if total_words == 0:
        return {}

    return {
        word: count / total_words
        for word, count in counter.items()
    }


def calculate_idf(
        all_words: set,
        words1: List[str],
        words2: List[str]
) -> dict:
    """
    计算逆文档频率 IDF

    两篇文章作为两个文档
    """

    idf = {}

    documents = [
        set(words1),
        set(words2)
    ]

    document_count = len(documents)

    for word in all_words:

        appear_count = sum(
            1 for doc in documents
            if word in doc
        )

        # 加1避免log(0)
        idf[word] = math.log(
            document_count / (appear_count + 1)
        )

    return idf


def calculate_tfidf_vector(
        words: List[str],
        all_words: set,
        idf: dict
) -> dict:
    """
    构造TF-IDF向量
    """

    tf = calculate_tf(words)
    vector = {}
    for word in all_words:

        vector[word] = (
            tf.get(word, 0)
            *
            idf[word]
        )
    return vector


def cosine_similarity(
        vector1: dict,
        vector2: dict
) -> float:
    """
    计算两个TF-IDF向量余弦相似度
    """
    dot_product = sum(
        vector1[word] * vector2[word]
        for word in vector1
    )
    norm1 = math.sqrt(
        sum(
            value ** 2
            for value in vector1.values()
        )
    )
    norm2 = math.sqrt(
        sum(
            value ** 2
            for value in vector2.values()
        )
    )
    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)

def calc_similarity(
        words1: List[str],
        words2: List[str],
        show_debug: bool = False
) -> float:
    """
    TF-IDF + 余弦相似度

    返回:
        0~100 的重复率
    """

    # 总词表
    all_words = set(words1) | set(words2)
    # 计算IDF
    idf = calculate_idf(
        all_words,
        words1,
        words2
    )
    # TF-IDF向量
    vector1 = calculate_tfidf_vector(
        words1,
        all_words,
        idf
    )
    vector2 = calculate_tfidf_vector(
        words2,
        all_words,
        idf
    )
    # 余弦相似度
    similarity = cosine_similarity(
        vector1,
        vector2
    )
    similarity = max(
        0.0,
        min(1.0, similarity)
    )
    repeat_rate = similarity * 100

    if show_debug:
        print("\n========== TF-IDF相似度计算 ==========")
        print(f"原文词数量：{len(words1)}")
        print(f"抄袭版词数量：{len(words2)}")
        print(f"总词表数量：{len(all_words)}")
        print(f"TF-IDF向量维度：{len(vector1)}")
        print(f"余弦相似度：{similarity:.6f}")
        print(f"查重率：{repeat_rate:.2f}%")
        print("====================================")


    return repeat_rate
