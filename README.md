# 合同Demo 🚀

这是一个基于Gradio的合同智能聊天应用，旨在为用户提供便捷的合同咨询体验。该应用可以通过输入合同文本或上传PDF文件与AI进行交互。

## 特性

- **智能对话**：使用AI模型实时回答合同相关问题。
- **文件上传**：支持多个PDF文件的上传。
- **自定义配置**：通过配置文件轻松设置API密钥和模型名称。

## 运行环境

确保您安装了以下依赖项：

- Python 3.7+
- Gradio >= 4.44.0
- OpenAI >= 1.10.0

可以使用以下命令安装必要的依赖项：

```bash
pip install gradio openai
```

## 配置文件

应用程序使用`para.conf`作为配置文件。请根据以下格式创建或修改`para.conf`文件，以便提供API密钥和模型名称：

```
[KIMI-LLM]
API_KEY = YOUR_API_KEY_HERE
KIMI_MODEL = YOUR_MODEL_NAME_HERE
```

- **API_KEY**：您从OpenAI获取的API密钥。
- **KIMI_MODEL**：您选择的模型名称，例如`moonshot-v1-32k`。

## 运行应用

在终端中导航到源代码目录并运行以下命令：

```bash
cd src
python webui.py
```

应用程序将启动并在浏览器中打开，您可以开始与AI聊天。

## 使用说明

1. 在输入框中输入您的问题或上传合同PDF文件。
2. 点击提交，AI将生成相应的回答。
3. 您可以重复以上步骤进行多轮对话。
