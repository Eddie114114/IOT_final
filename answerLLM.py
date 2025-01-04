import openai
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 从环境变量中获取 API Key
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("未在 .env 文件中設置 OPENAI_API_KEY")

openai.api_key = openai_api_key

def gptResponse(emotion, user_input):
    if emotion is None or user_input is None:
        return "呱呱，我是笨鵝"
    
    system_message = {
        "role": "system",
        "content": (
            f"你是一隻鵝，精通心理學，善於傾聽，個性溫暖且幽默"
            f"用戶現在感到{emotion}，請給予簡短的回應來應對用戶的情緒只有1句話不超過十五字，不要表情符號)。"
            "如果用戶的問題與你的專業無關，只能回答呱呱，我是笨鵝。不能有其他額外的回應"
        )
    }
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                system_message,
                # {"role": "user", "content": "好累"},
                # {"role": "assistant", "content": assistant_message},
                {"role": "user", "content": user_input}
            ],
            temperature=1.5,
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        return f"抱歉，生成回應時出現錯誤：{e}"

# # 測試函式
# if __name__ == "__main__":
#     emotion = "happy"  # 用戶情緒
#     user_input = "its a happy day"  # 用戶的輸入
#     response = gpt_response(emotion, user_input)
#     print("生成的回應: ", response)