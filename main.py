import threading
from textInputOutput import speechToText, speakChinese
from emotionDetection import emotionDetect
from answerLLM import gptResponse
# import keyboard

def main():
    # 初始化變數
    user_speech = None
    detected_emotion = None

    # 啟動 speechToText 作為獨立執行緒
    def getUserSpeech():
        nonlocal user_speech
        user_speech = speechToText()

    # 啟動 emotionDetect 作為獨立執行緒
    def getDetectedEmotion():
        nonlocal detected_emotion
        detected_emotion = emotionDetect()

    # 建立執行緒
    speech_thread = threading.Thread(target=getUserSpeech)
    emotion_thread = threading.Thread(target=getDetectedEmotion)

    # 啟動執行緒
    speech_thread.start()
    # time.sleep(1)
    emotion_thread.start()

    # 等待執行緒完成
    speech_thread.join()
    # keyboard.write("q")
    emotion_thread.join()

    # 呼叫 gptResponse 取得回應
    print(f"使用者說: {user_speech}")
    print(f"檢測到情緒: {detected_emotion}")

    response = gptResponse(detected_emotion, user_speech)

    # 使用 speakChinese 播放回應
    print(f"生成回應: {response}")
    speakChinese(response)

# if __name__ == "__main__":
#     main()