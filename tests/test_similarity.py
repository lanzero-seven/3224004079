"""
论文查重系统单元测试

测试:
1. 文件读取
2. 文本预处理
3. TF-IDF相似度计算
4. 文件输出
"""


import os
import tempfile

from file_io import read_text, write_answer
from processing import preprocess_text
from similarity import calc_similarity



# ==========================
# T1 文件读取正常测试
# ==========================

def test_read_text_success():

    with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False
    ) as f:

        f.write("人工智能测试文本")
        file_path = f.name


    result = read_text(file_path)

    assert result == "人工智能测试文本"

    os.remove(file_path)



# ==========================
# T2 文件不存在测试
# ==========================

def test_read_text_not_exist():

    import pytest

    with pytest.raises(FileNotFoundError):

        read_text("not_exist.txt")



# ==========================
# T3 中文分词测试
# ==========================

def test_preprocess_word_cut():

    text = "人工智能正在快速发展"

    words = preprocess_text(text)


    assert "人工智能" in words



# ==========================
# T4 停用词过滤测试
# ==========================

def test_stop_words_filter():

    text = "我是一个学生"

    words = preprocess_text(text)


    assert "我" not in words
    assert "是" not in words



# ==========================
# T5 完全相同文本
# ==========================

def test_similarity_same_text():

    text = [
        "人工智能",
        "机器学习"
    ]

    result = calc_similarity(
        text,
        text
    )


    assert result == 100



# ==========================
# T6 完全不同文本
# ==========================

def test_similarity_different_text():

    result = calc_similarity(
        [
            "人工智能"
        ],
        [
            "篮球比赛"
        ]
    )


    assert result < 50



# ==========================
# T7 增加内容测试
# ==========================

def test_similarity_add_text():

    result = calc_similarity(
        [
            "人工智能",
            "机器学习"
        ],
        [
            "人工智能",
            "机器学习",
            "计算机视觉"
        ]
    )


    assert result <= 100



# ==========================
# T8 删除内容测试
# ==========================

def test_similarity_delete_text():

    result = calc_similarity(
        [
            "人工智能",
            "机器学习",
            "深度学习"
        ],
        [
            "人工智能"
        ]
    )


    assert result <= 100



# ==========================
# T9 空文本测试
# ==========================

def test_empty_text():

    result = calc_similarity(
        [],
        []
    )


    assert result == 0



# ==========================
# T10 文件写入测试
# ==========================

def test_write_answer():

    with tempfile.NamedTemporaryFile(
            delete=False
    ) as f:

        path = f.name


    result = write_answer(
        path,
        85.126
    )


    assert result is True


    with open(
            path,
            encoding="utf-8"
    ) as f:

        content = f.read()


    assert content == "85.13"


    os.remove(path)