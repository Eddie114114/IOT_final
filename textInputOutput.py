from gtts import gTTS
import os
import speech_recognition as sr


# 使用 Google TTS 播放語音
def speakChinese(text):
    try:
        print(f"語音輸出內容：{text}")
        tts = gTTS(text, lang='zh-TW')  # 使用繁體中文
        tts.save("output.mp3")  # 將語音保存到 MP3 文件
        os.system("mpg321 output.mp3")  # 播放音頻文件
        os.remove("output.mp3")  # 播放完畢後刪除文件
    except Exception as e:
        print(f"語音轉換或播放過程中發生錯誤：{e}")

# # 測試函式
# if __name__ == "__main__":
#     test_text = "呱呱"
#     speak_chinese(test_text)
    


# 使用 Google STT 將語音轉換為文字
def speechToText():
    recognizer = sr.Recognizer()

    # 使用默認麥克風作為音頻輸入
    with sr.Microphone() as source:
        try:
            print("調整環境噪音...")
            recognizer.adjust_for_ambient_noise(source, duration=2)  # 適應環境噪聲
            
            print("呱呱...")
            os.system("mpg321 gua.mp3")  # 播放音頻文件
            audio = recognizer.listen(source, timeout = 5)  # 設定最大等待時間 5 秒
            
            print("辨識中...")
            # 使用 Google Speech Recognition 將音頻轉換為文字
            text = recognizer.recognize_google(audio, language="zh-TW")  # 語言設為繁體中文
            print("你: ", text)
            return text

        except sr.UnknownValueError:
            print("笨鵝無法理解。")
            return None
        except sr.RequestError as e:
            print(f"笨鵝無法向 Google STT 發出請求；錯誤訊息：{e}")
            return None
        except sr.WaitTimeoutError:
            print("笨鵝沒聽到")
            return None
        
# # 測試函式
# if __name__ == "__main__":
#     text = speech_to_text()
#     print(text)
    
