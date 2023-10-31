import nltk
from nltk.tokenize import word_tokenize

# 打开文本文件
with open('your_text_file.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 使用NLTK进行分词
nltk.download('punkt')  # 下载必要的NLTK数据（仅第一次需要）
tokens = word_tokenize(text)

# 打印分词结果
print(tokens)

# 创建并打开一个新文本文件以保存分词结果
with open('tokenized_text.txt', 'w', encoding='utf-8') as output_file:
    # 将分词结果写入文件，每个分词占据一行
    for token in tokens:
        output_file.write(token + '\n')
