from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.lite.python.interpreter import Interpreter
import cv2
import numpy as np
import time
from collections import Counter

# 載入模型
face_classifier = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')

emotion_interpreter = Interpreter(model_path="model/emotion_detection_model_100epochs_no_opt.tflite")
emotion_interpreter.allocate_tensors()

# 獲取輸入和輸出張量
emotion_input_details = emotion_interpreter.get_input_details()
emotion_output_details = emotion_interpreter.get_output_details()

# 定義情緒標籤
class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def emotionDetect():
    # 統計情緒次數
    emotion_counter = Counter()

    # 啟動鏡頭
    cap = cv2.VideoCapture(0)

    # 記錄開始時間
    start_time = time.time()

    # 設置持續時間，單位為秒
    duration = 8

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法獲取鏡頭畫面。")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            # 準備圖片進行預測
            roi = roi_gray.astype('float') / 255.0  # 比例化
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)  # 擴展維度 (1, 48, 48, 1)

            emotion_interpreter.set_tensor(emotion_input_details[0]['index'], roi)
            emotion_interpreter.invoke()
            emotion_preds = emotion_interpreter.get_tensor(emotion_output_details[0]['index'])

            # 獲取情緒標籤
            emotion_label = class_labels[emotion_preds.argmax()]
            emotion_counter[emotion_label] += 1  # 統計此情緒次數

            emotion_label_position = (x, y)
            cv2.putText(frame, emotion_label, emotion_label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Emotion Detector', frame)

        # 檢查時間是否超過設定的持續時間
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            print("時間到")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 手動退出
            break

    cap.release()
    cv2.destroyAllWindows()

    # 回傳最常見的情緒
    most_common_emotion = emotion_counter.most_common(1)
    if most_common_emotion:
        return most_common_emotion[0][0]
    else:
        return None

# if __name__ == "__main__":
#     result = emotionDetect()
#     print("\n===== 最常見的情緒 =====")
#     print(f"最常見的情緒: {result}")