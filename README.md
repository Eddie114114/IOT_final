# IOT-final-your friend, goose

## 目錄
1. [簡介](#簡介)
2. [作品圖片及影片](#作品圖片及影片)
3. [Step1: 使用設備](#Step1-使用設備)
4. [Step2: 軟體安裝](#Step2-軟體安裝)
5. [Step3: 訓練模型及使用](#Step3-訓練模型及使用)
6. [Step4: 語音輸入及輸出](#Step4-語音輸入及輸出)
7. [Step5: 串接語言模型](#Step5-串接語言模型)
8. [Step6: 整合函式](#Step6-整合函式)
9. [Step7: 設定按鈕](#Step7-設定按鈕)
10. [可以改善的點](#可以改善的點)
11. [參考資料](#參考資料)

---

## 簡介
現代許多人缺少可以傾訴煩惱、理解情緒的對象，此時阿鵝可以成為你的好朋友。阿鵝可以透過鏡頭辨識使用者的情緒，並以麥克風接收使用者所說的話，透過語言模型生成聊天對話並轉成語音以喇叭輸出。

---

## 作品圖片及影片
### 照片
![成果照片](https://drive.google.com/file/d/1C5Gd61JxwuGR98YHHcejBS_WONemOF2a/view)

### 影片
[![成果影片](https://img.youtube.com/vi/UhY2tnBe6VU/0.jpg)](https://youtube.com/shorts/UhY2tnBe6VU?si=Nw5qJbpsWfEdjHYD)  
點擊圖片觀看完整影片。

---

## Step1: 使用設備
- raspberry pi 4B
- 鏡頭
- 麥克風
- 喇叭
- 輕觸按鈕
- 杜邦線(母-母) * 2
- 一隻大白鵝

---

## Step2: 軟體安裝
### 1. 環境設定
- Raspberry Pi作業系統
- Python 3.7
- opencv
- openai
- tensorflow 2.4.0
- gtts
- speech_recognition

### 2. 安裝時可能遇到的問題
opencv安裝參考以下網址  
[https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA](https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA)  

tensorflow無法使用pip安裝，從以下網址下載python版本對應的wheel，python3.7、32位元使用 `tensorflow-2.4.0-cp37-none-linux_armv7l.whl`   
[https://github.com/lhelontra/tensorflow-on-arm/releases](https://github.com/lhelontra/tensorflow-on-arm/releases)  

下載完成之後直執行以下指令:  
 - cd進入wheel文件所在資料夾

<pre>
<code>
 cd /home/pi/Downloads
</code>
</pre>
 - 可能需要升級pip
<pre>
<code>
 python3 -m pip install --upgrade pip  
</code>
</pre>
 - 執行下載
<pre>
<code>
 pip3 install tensorflow-2.4.0-cp37-none-linux_armv7l.whl
</code>
</pre>

樹莓派執行speech_recognition時可能遇到錯誤，需要安裝 `pyaudio` :
<pre>
<code>
 pip3 install pyaudio
</code>
</pre>

---

## Step3: 訓練模型及使用
### 訓練(不在樹莓派上執行，會很久!!)
使用 FER2013 資料集來訓練CNN卷積神經網路，可以辨識人臉的七種情緒，包括：
- **Angry**, **Disgust**, **Fear**, **Happy**, **Neutral**, **Sad**, **Surprise**  
- 下載連結如下:  
[https://www.kaggle.com/datasets/msambare/fer2013](https://www.kaggle.com/datasets/msambare/fer2013)  

執行 `trainEmotionModel.py` 進行模型訓練、測試及查看結果  
模型訓練
- 使用 `ImageDataGenerator` 進行訓練資料增強和多樣化。
- 模型結構包括四層卷積層和兩層全連接層，並且搭配使用 `Dropout` 防止過擬合。
- 使用 `Adam` 優化器，進行 50 個 Epoch 的訓練

測試
- 使用混淆矩陣（Confusion Matrix）顯示分類準確度
- 隨機顯示測試圖片和預測結果

### 使用
使用convert_h5_to_tflite.py將模型轉換成tflite檔案，tflite在樹莓派上可以有更好的效率  
使用emotionDetection.py
人臉檢測： 使用 OpenCV 提供的 Haar Cascade 模型來檢測影像中的人臉位置。
情緒分類： 使用 TensorFlow Lite 推理模型對人臉影像進行分類。
多次檢測統計： 收集過程中多次檢測的結果，返回最常見的情緒。
設定定時關閉


---

## Step4: 語音輸入及輸出
### 1. 語音輸出 (Text-to-Speech)
透過 Google TTS 將輸入文字轉換為繁體中文語音，並透過播放設備輸出。

**功能函式**：
- `speakChinese(text)`
  - 參數：`text` (str) - 要轉換為語音的文字。
  - 流程：
    1. 利用 gTTS 將文字轉為繁體中文語音。
    2. 儲存語音檔為 MP3 格式並播放。
    3. 播放完成後自動刪除 MP3 檔案。
  - 異常處理：當語音合成或播放過程發生錯誤，會打印錯誤資訊。

### 2. 語音輸入 (Speech-to-Text)
透過 Google Speech Recognition 將使用者語音轉換為繁體中文文字，並返回辨識結果。

**功能函式**：
- `speechToText()`
  - 流程：
    1. 啟動麥克風，調整環境噪音以提升辨識準確度。
    2. 播放提示音（"呱呱"）提示使用者開始說話。
    3. 記錄使用者語音，並將其轉換為文字。
    4. 返回辨識的文字結果。
  - 異常處理：當無法辨識語音或與 Google STT 服務的連線發生問題，會打印錯誤資訊。

---

## Step5: 串接語言模型
### 1. 回應生成
根據用戶提供的情緒和輸入內容，生成不超過 15 字的簡短回應：
- 使用者提供情緒（如 "happy", "sad"）和文字輸入。
- 如果輸入內容不在阿鵝的能力範圍內，回應 "呱呱，我是笨鵝"。
### 前置準備
1. 安裝依賴：
   ```bash
   pip install openai python-dotenv
2. 在專案目錄下建立 .env 文件，並設置 OpenAI API 金鑰：OPENAI_API_KEY=your_api_key_here
### google gemini


---

## Step6: 整合函式
### 1. 多執行緒處理
- 使用 `threading` 模組讓語音輸入與情緒檢測並行執行，提升效能。
- 執行緒同步，確保在兩個功能完成後進行回應生成。
### 2. 整合了多個功能模組，包括語音輸入、情緒檢測以及基於 GPT-3.5 的對話生成。  
具體流程如下：
1. 使用語音辨識接收使用者說的話。
2. 同時啟動情緒偵測模型辨識用戶情緒。
3. 將語音與情緒傳遞給 GPT 模型生成合適的回應。
4. 將回應轉換為語音並播放。

---

## Step7: 設定按鈕
1. **按鈕事件觸發**：
   - 偵測按鈕按下時觸發執行指定程式。
   - 使用樹莓派的 GPIO 腳位監聽按鈕按下事件。

2. **音效提醒**：
   - 當程式啟動時，播放音效文件 `letsPlay.mp3` 以提醒用戶。
   - 當

3. **系統穩定性**：
   - 加入防抖處理，避免按鈕重複觸發。
---

## 可以改善的點

---

## 參考資料
