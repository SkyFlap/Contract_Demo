from openai import OpenAI

client = OpenAI(
    api_key="sk-yfbUaRB9BJNqNYylK6N1GqwznhhL0uSgoIfAmWaZnNSZNotI",
    base_url="https://api.moonshot.cn/v1",
)
file_list = client.files.list()

for file in file_list.data:
    print(file)  # 查看每个文件的信息
    # client.files.delete(file_id=file.id)
