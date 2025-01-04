# IoT Final - Your Friend, Goose

## 目錄
1. [簡介](#簡介)
2. [作品圖片及影片](#作品圖片及影片)
3. [Step1: 使用設備](#step1-使用設備)
4. [Step2: 軟體安裝](#step2-軟體安裝)
5. [Step3: 訓練模型及使用](#step3-訓練模型及使用)
6. [Step4: 語音輸入及輸出](#step4-語音輸入及輸出)
7. [Step5: 串接語言模型](#step5-串接語言模型)
8. [Step6: 整合函式](#step6-整合函式)
9. [Step7: 設定按鈕](#step7-設定按鈕)
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
- Raspberry Pi 4B
- 鏡頭
- 麥克風
- 喇叭
- 輕觸按鈕
- 杜邦線(母-母) * 2
- 一隻大白鵝

---

## Step2: 軟體安裝

### 1. 環境設定
- Raspberry Pi 作業系統
- Python 3.7
- opencv
- openai
- tensorflow 2.4.0
- gtts
- speech_recognition

### 2. 安裝時可能遇到的問題

#### opencv 安裝參考
[https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA](https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA)  

#### tensorflow 安裝
從以下網址下載 python 版本對應的 wheel：
[https://github.com/lhelontra/tensorflow-on-arm/releases](https://github.com/lhelontra/tensorflow-on-arm/releases)  

下載完成後執行以下指令：

```bash
cd /home/pi/Downloads
python3 -m pip install --upgrade pip
pip3 install tensorflow-2.4.0-cp37-none-linux_armv7l.whl
```

#### speech_recognition 問題
樹莓派執行 speech_recognition 時需要安裝 pyaudio：

```bash
pip3 install pyaudio
```

---

## Step3: 訓練模型及使用

### 訓練模型 (不建議在樹莓派上執行)

#### 資料集
使用 FER2013 資料集進行訓練：
[https://www.kaggle.com/datasets/msambare/fer2013](https://www.kaggle.com/datasets/msambare/fer2013)  

#### 訓練細節
- 使用 `ImageDataGenerator` 進行資料增強
- 模型結構包括 4 層卷積層和 2 層全連接層，並搭配 Dropout 防止過擬合
- 優化器：Adam
- 訓練次數：50 Epoch

#### 測試方法
- 使用混淆矩陣評估分類準確度
- 隨機顯示測試圖片和預測結果

#### 使用 tflite 模型
將模型轉換為 tflite 格式以提升效率：
- 執行 `convert_h5_to_tflite.py` 轉換模型
- 使用 `emotionDetection.py` 進行人臉檢測和情緒分類

---

## Step4: 語音輸入及輸出

### 1. 語音輸出 (Text-to-Speech)
透過 Google TTS 將輸入文字轉為語音，並播放：

#### 功能函式
- **speakChinese(text)**
  - 將文字轉為語音並播放，播放後自動刪除音檔。

### 2. 語音輸入 (Speech-to-Text)
透過 Google Speech Recognition 將語音轉為文字：

#### 功能函式
- **speechToText()**
  - 啟動麥克風錄音，調整環境噪音，返回辨識的文字結果。

---

## Step5: 串接語言模型

### 回應生成
根據用戶提供的情緒和文字生成回應：
- 若超出能力範圍，回應 "呱呱，我是笨鵝"。

### 前置準備
1. 安裝依賴：

```bash
pip install openai python-dotenv
```

2. 在專案目錄下建立 `.env` 文件，設置 OpenAI API 金鑰：

```plaintext
OPENAI_API_KEY=your_api_key_here
```

---

## Step6: 整合函式

### 多執行緒處理
- 使用 `threading` 模組讓語音輸入與情緒檢測並行執行。
- 兩個功能完成後進行回應生成。

### 整合流程
1. 使用語音辨識接收使用者語音。
2. 同時進行情緒偵測。
3. 將結果傳遞至 GPT 模型生成回應。
4. 將回應轉換為語音並播放。

---

## Step7: 設定按鈕

### 功能設計
1. **按鈕事件觸發**
   - 偵測按鈕按下時執行指定程式。

2. **音效提醒**
   - 播放提示音 `letsPlay.mp3`。

3. **防抖處理**
   - 避免按鈕重複觸發。

---

## 可以改善的點
- 優化語音辨識準確度。
- 提升情緒分類模型的準確性。
- 減少硬體設備的延遲。

---

## 參考資料
- [opencv 安裝指引](https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA)
- [tensorflow wheel 下載](https://github.com/lhelontra/tensorflow-on-arm/releases)
- [FER2013 資料集](https://www.kaggle.com/datasets/msambare/fer2013)
