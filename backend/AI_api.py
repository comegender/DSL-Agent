import os
from volcenginesdkarkruntime import Ark

userInput = input()


# 从环境变量中读取您的方舟API Key
client = Ark(api_key=os.environ.get("ARK_API_KEY"))
completion = client.chat.completions.create(
    # 可按需替换为 Model ID
    model="doubao-seed-1-6-250615",
    messages=[
        {"role": "user", "content": f"现在有选项:投诉，帮助，修改密码，查询，充值。请根据下面的输入判断一个选项：{userInput}。只需要返回选项的名称即可，不要有其他多余的文字"},
    ]
)
print(completion.choices[0].message)

# set ARK_API_KEY=a3cfd5bd-9f7d-489b-9014-69e6ac58c51c
