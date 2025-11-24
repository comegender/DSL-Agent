from volcenginesdkarkruntime import Ark

# 从环境变量中读取您的方舟API Key
client = Ark(api_key="a3cfd5bd-9f7d-489b-9014-69e6ac58c51c")

def get_response(user_Input):
    userInput = user_Input
    completion = client.chat.completions.create(
        # 可按需替换为 Model ID
        model="doubao-seed-1-6-250615",
        messages=[
            {"role": "user", "content": f"现在有选项:投诉建议，使用帮助，修改密码，查询账户信息，充值，功能查询。请根据下面的输入判断一个选项：{userInput}。只需要返回选项的名称即可，不要有其他多余的文字"},
        ]
    )

    message_obj = completion.choices[0].message
    response_content = message_obj.content
    return response_content
