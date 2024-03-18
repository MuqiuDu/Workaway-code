import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langdetect import detect
from nltk.tokenize import word_tokenize


def expand_contractions(text):
    contractions_mapping = {
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "can't": "cannot",
        "couldn't": "could not",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "won't": "will not",
        "wouldn't": "would not",
        "hasn't": "has not",
        "haven't": "have not",
        "hadn't": "had not",
        "mightn't": "might not",
        "mustn't": "must not",
        "shouldn't": "should not",
        "shan't": "shall not",
        "needn't": "need not",
        "oughtn't": "ought not",
        "ain't": "am not"
    }

    for contraction, expansion in contractions_mapping.items():
        text = re.sub(r'\b' + contraction + r'\b', expansion, text)

    return text

def remove_links(text):
    link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    text = re.sub(link_pattern, '', text)
    return text

# 获取文件的绝对路径
file_path = "/Users/sissismackbook2/Desktop/data_cleanning_jupyter.json"

# 使用绝对路径打开文件
with open(file_path, encoding='utf-8') as file:
    text = file.read()

# 移除链接
text = remove_links(text)

# 扩展缩写
text = expand_contractions(text)

# 转换为小写
text = text.lower()

# 分词NLTK
tokenized_word = word_tokenize(text)

# 停用词
stop_words = set(stopwords.words("english"))

# 过滤掉包含"W_Review_P"等内容
filtered_tokens = [w for w in tokenized_word if "w_review_p" not in w and "h_url" not in w and "feedback_data" not in w]

filtered_tokens = [w for w in filtered_tokens if w.lower() not in stop_words]

# 去除标点符号
filtered_tokens2 = [w for w in filtered_tokens if w.lower() not in string.punctuation]

# 词性还原
wordnet_lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [wordnet_lemmatizer.lemmatize(w) for w in filtered_tokens2]

# 删除长度小于2的单词
filtered_tokens_final = [w for w in lemmatized_tokens if len(w) >= 2]

# 将结果组合成一个字符串
cleaned_text = ' '.join(filtered_tokens_final)

# 清理文本中的空格、标点符号和 emoji 表情符号
cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # 去除多余的空格
cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # 去除标点符号
cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')  # 去除非 ASCII 字符

# 打印或保存结果
print(cleaned_text)
