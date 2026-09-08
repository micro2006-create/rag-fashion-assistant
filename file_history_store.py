import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, chat_id, storage_path):
        self.chat_id = chat_id           # 会话id
        self.storage_path = storage_path       # 不同会话id对应的文件夹路径

        self.file_path = os.path.join(self.storage_path, self.chat_id) # 完整文件路径

        # 确保文件夹存在，如果不存在，会自动创建
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # 功能：把传给的messages追加到已有的消息列表里面，type(messages): Sequence[BaseMessage], 是一个BaseMessage序列
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # self.messages 这个属性来自于父类(BaseChatMessageHistory)
        all_messages = list(self.messages)   # 已有的消息列表
        all_messages.extend(messages)        # 新的和已有的融合成一个list

        # 讲数据同步写入本地文件中
        # 类对象写入文件会得到一堆二进制
        # 为了方便查看，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        # 官方提供的message_to_dict：BaseMessage消息 -> 字典
        # 将[BaseMessage, BaseMessage, ....] -> [字典, 字典, ....]
        new_messages = []
        for message in all_messages:
            d = message_to_dict(message)
            new_messages.append(d)
        # 相同写法如下：
        # new_messages = [message_to_dict(message) for message in new_messages]

        # 将数据写入文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            #将[字典, 字典, ....]写入文件中
            json.dump(new_messages, f)

    @property # 装饰器：将messages方法变成类的成员属性，方便以后创建实例的时用实例.messages
    # 这个函数的 -> 含义时返回值注解，说明messages这个方法返回类型是list[BaseMessage]
    # 功能：打开文件，把里面的内容转变成list[BaseMessage]返回出来
    def messages(self) -> list[BaseMessage]:
        # 从json文件中读取内容，json存放的内容是[字典, 字典, ....]
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                message_data = json.load(f)    # 读到的内容是[字典, 字典, ....]
                # 通过message_from_dict把[字典、字典...] -> [消息、消息]
                return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
