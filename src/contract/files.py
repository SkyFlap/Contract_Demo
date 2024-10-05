from typing import *

import os
import json
from pathlib import Path


def upload_files(files: List[str], client) -> List[Dict[str, Any]]:
    """
    upload_files 会将传入的文件（路径）全部通过文件上传接口 '/v1/files' 上传，并获取上传后的
    文件内容生成文件 messages。每个文件会是一个独立的 message，这些 message 的 role 均为
    system，Kimi 大模型会正确识别这些 system messages 中的文件内容。

    :param files: 一个包含要上传文件的路径的列表，路径可以是绝对路径也可以是相对路径，请使用字符串
        的形式传递文件路径。
    :return: 一个包含了文件内容的 messages 列表，请将这些 messages 加入到 Context 中，
        即请求 `/v1/chat/completions` 接口时的 messages 参数中。
    """
    messages = []

    # 对每个文件路径，我们都会上传文件并抽取文件内容，最后生成一个 role 为 system 的 message，并加入
    # 到最终返回的 messages 列表中。
    for file in files:
        file_object = client.files.create(file=Path(file), purpose="file-extract")
        file_content = client.files.content(file_id=file_object.id).text
        messages.append(
            {
                "role": "system",
                "content": file_content,
            }
        )

    return messages
