import os
import configparser

latex_delimiters_set = [
    {"left": "$$", "right": "$$", "display": True},
    {"left": "$", "right": "$", "display": False},
    {"left": "\\(", "right": "\\)", "display": False},
    {"left": "\\[", "right": "\\]", "display": True},
    {"left": "\\begin{equation}", "right": "\\end{equation}", "display": True},
    {"left": "\\begin{align}", "right": "\\end{align}", "display": True},
    {"left": "\\begin{alignat}", "right": "\\end{alignat}", "display": True},
    {"left": "\\begin{gather}", "right": "\\end{gather}", "display": True},
    {"left": "\\begin{CD}", "right": "\\end{CD}", "display": True},
]


def get_file_content(path: str) -> str:
    if os.path.exists(path):
        with open(path, encoding="utf8") as file:
            return file.read()
    return ""


def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split("`")
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f"<br></code></pre>"
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def read_conf_file(file_path: str) -> dict:
    """
    读取 .conf 配置文件的函数。

    参数：
        file_path (str): 要读取的 .conf 配置文件的路径，包括文件名和扩展名（例如: 'config.conf'）。

    返回：
        dict: 返回配置文件内容作为嵌套字典。外层字典的键为配置文件的 section 名称，
              内层字典包含该 section 下的键值对参数。如果读取成功，返回配置内容；
              如果文件不存在或读取失败，将抛出相应的异常。

    异常处理：
        - FileNotFoundError: 如果指定的文件路径不存在，会抛出此异常。
        - 其他可能的异常：在读取文件或处理内容时发生的任何其他异常，将被捕获并抛出。

    用例：
        conf_path = 'config.conf'
        try:
            config_parameters = read_conf_file(conf_path)
            print("读取到的配置参数:", config_parameters)
        except Exception as e:
            print(f"读取配置文件时发生错误: {e}")
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")

    # 创建ConfigParser对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read(file_path)

    # 遍历配置文件中的section和它们的参数
    config_data = {}
    for section in config.sections():
        config_data[section] = {}
        for key, value in config.items(section):
            config_data[section][key] = value

    return config_data
