from openai import OpenAI
import ast
from .files import upload_files


def predict(
    history,
    file_list,
    api_key,
    model_name,
    prompt="",
    max_length=4096,
    top_p=0.7,
    temperature=0.95,
):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1",
    )
    file_messages = upload_files(ast.literal_eval(file_list), client)
    messages = [*file_messages]
    if prompt:
        messages.append({"role": "system", "content": prompt})
    for idx, (user_msg, model_msg) in enumerate(history):
        if prompt and idx == 0:
            continue
        if idx == len(history) - 1 and not model_msg:
            messages.append({"role": "user", "content": user_msg})
            break
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_length,
        top_p=top_p,
        temperature=temperature,
        stream=True,
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            history[-1][1] += chunk.choices[0].delta.content
            yield history
