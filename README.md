# IoT Final - Your Friend, Goose

## 目錄
1. [簡介](#簡介)
2. [作品圖片及影片](#作品圖片及影片)
3. [Step1: 使用設備](#step1-使用設備)
4. [Step2: 軟體安裝](#step2-軟體安裝)
5. [Step3: 訓練模型及使用](#step3-訓練模型及使用)
6. [Step4: 語音輸入及輸出](#step4-語音輸入及輸出)
7. [Step5: 串接語言模型](#Step5-串接語言模型)
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
![成果照片](https://github.com/Eddie114114/IOT_final/blob/main/picture/IMG_1196.jpg)
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

#### opencv 安裝參考此網址
[https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA](https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA)  

1. 首先安裝CMack  
```bash
cd ~/
wget https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4.tar.gz
tar xvzf cmake-3.14.4.tar.gz
cd ~/cmake-3.14.4
./bootstrap
make -j4
sudo make install
```
2. 安裝OpenCV(需要跑一段時間)
```bash
cd ~/
sudo apt install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libatlas-base-dev python3-scipy
git clone --depth 1 --branch 4.5.2-openvino https://github.com/opencv/opencv.git
cd opencv && mkdir build && cd build
cmake –DCMAKE_BUILD_TYPE=Release –DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j4
sudo make install
``` 

#### tensorflow 安裝
tensorflow 可能無法使用 pip 安裝，從以下網址下載 python 版本對應的 wheel：
[https://github.com/lhelontra/tensorflow-on-arm/releases](https://github.com/lhelontra/tensorflow-on-arm/releases)  

python3.7、32位元使用 tensorflow-2.4.0-cp37-none-linux_armv7l.whl  

下載完成後執行以下指令：

```bash
cd /home/pi/Downloads
python3 -m pip install --upgrade pip
pip3 install tensorflow-2.4.0-cp37-none-linux_armv7l.whl
```

#### speech_recognition 問題
樹莓派執行 speech_recognition 時可能遇到錯誤，需要安裝 pyaudio：

```bash
pip3 install pyaudio
```

---

## Step3: 訓練模型及使用

### 執行 `trainEmotionModel.py` 訓練模型並測試 (不建議在樹莓派上執行，筆電跑了兩天多)
請確保資料集檔案名稱和位置正確

>#### 資料集
>使用 FER2013 資料集進行訓練：
>[https://www.kaggle.com/datasets/msambare/fer2013](https://www.kaggle.com/datasets/msambare/fer2013)
>
>FER2013中分為訓練集和測試集
>
>最終模型將可以辨識人臉的七種情緒，包括：
>- **Angry**, **Disgust**, **Fear**, **Happy**, **Neutral**, **Sad**, **Surprise**  

>#### 進行訓練
>使用 `ImageDataGenerator` 進行資料增強和多樣化
>
>模型結構包括 4 層卷積層和 2 層全連接層，並搭配使用 Dropout 防止過擬合
>
>使用優化器Adam，且訓練次數為50 Epoch  

>#### 進行測試
>使用混淆矩陣評估分類準確度
>
>隨機顯示測試圖片和預測結果  

### 執行 `convert_h5_to_tflite.py` 轉換模型
將 h5 模型轉換為 tflite 格式以提升在樹莓派上的執行效率

### 使用 `emotionDetection.py` 進行人臉檢測和情緒分類
OpenCV 提供多種預訓練的圖形辨識模型，此處使用臉部辨識模型 `data/haarcascades/haarcascade_frontalface_default.xml`   

從以下網址下載，並確保檔案儲存名稱和位置正確：
[https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml](https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml)  

用雲端或隨身碟將 tflite 格式的情緒辨識模型放進樹莓派，並確保檔案儲存名稱和位置正確

>#### 程式邏輯
>先使用 OpenCV 提供的 Haar Cascade 模型來定位影像中的人臉位置
>
>再使用剛剛訓練好的模型對人臉影像做進一步的情緒分析  
>
>鏡頭設定五秒鐘的定時關閉，大約是說一句簡單的話的時間
>
>過程中會多次收集檢測到的結果，回傳最常見的情緒

---

## Step4: 語音輸入及輸出

### 使用 `textInputOutput.py` ，確保 `gua.mp3` 檔案名稱和位置正確

>#### 語音輸出 (TTS)
>利用 gTTS 將文字轉為繁體中文的語音
>
>儲存語音檔為 MP3 格式並播放
>
>播放完自動刪除 MP3 檔案
>
>- 異常處理：當語音合成或播放過程發生錯誤，會 print 錯誤資訊

>#### 語音輸入 (STT)
>啟動麥克風，需要幾秒鐘適應環境噪音以提升辨識準確度
>
>之後播放提示音（ `gua.mp3` ），聽到此提示音後使用者有五秒鐘可以開始說話
>
>記錄使用者所說的語音，並轉換為文字
>
>最後回傳結果
>
>- 異常處理：當無法辨識語音或與 Google STT 服務的連線發生問題，會 print 錯誤資訊

---

## Step5: 串接語言模型

### 前置準備，使用 GPT-3.5
使用 `answerLLM.py`   

1. 於 OpenAI 官網申請 API key ，可在 Usage 頁面查看使用量：
[https://platform.openai.com/settings/organization/api-keys](https://platform.openai.com/settings/organization/api-keys)    

2. 在專案目錄下建立 `.env` 文件，設定剛剛申請的 OpenAI API 金鑰：

```plaintext
OPENAI_API_KEY = your_api_key
```

### 回應生成
可以在 `system role` 設定阿鵝的人設(或鵝設?)和回答方式、範圍等等  
此處設定阿鵝根據用戶提供的情緒和文字生成回應，如果超出能力範圍，阿鵝會回應 "呱呱，我是笨鵝"

>#### 使用 google gemini
>如果你的環境使用 `python3.9` ，可以使用 `google gemini` 作為語言模型
>1. 登入Google帳號並取得API
>[https://ai.google.dev/gemini-api/docs/api-key?hl=zh-tw](https://ai.google.dev/gemini-api/docs/api-key?hl=zh-tw)

>2. 安裝以下
>```bash
>pip install configparser
>pip install langchain
>pip install openai
>pip install langchain-openai
>pip install langchain-community
>pip install faiss-cpu
>pip install tiktoken
>pip install pillow
>pip install langchain-google-genai
>```
>
>3. 建立 `config.ini` 並設定
>```bash
>[Gemini]
>API_KEY = your_api_key
>```
>
>4. 更改 `answerLLM.py`
>- 在開頭加上  
>```bash
>config = ConfigParser()
>config.read("config.ini")
>
>llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=config["Gemini"]["API_KEY"])
>```
>- 更改 `gptResponse` 函式  
>```bash
>if emotion is None or user_input is None:
>        return "呱呱，我是笨鵝"
>
>    system_message = (
>        #此處設定阿鵝的人設(或鵝設?)和回答方式、範圍
>    )
>
>    try:
>        response = llm.invoke([
>            ("system", system_message),
>            ("user", user_input)
>        ])
>        return response.content
>    except Exception as e:
>        return f"抱歉，生成回應時出現錯誤：{e}"
>```

---

## Step6: 整合函式

###  `main.py` 用於整合函式並進行多執行緒處理
確保以上檔案名稱和和位置正確  

如果有更動檔案名稱或其中函式名稱，請更正  
```bash
from 檔案名稱 import 函式
```

使用 `thread` 進行多執行緒處理  
```bash
import threading
```

>#### 整合流程如下
>1. 使用語音辨識接收使用者語音
>2. 同時進行情緒偵測
>3. 將二者結果傳遞至 語言模型生成回應
>4. 將回應轉換為語音
>5. 播放語音

---

## Step7: 設定按鈕

### 使用 `button.py` 
1. 確定 `main.py` 以及 `letsPlay.mp3` 檔案名稱和和位置正確

2. 安裝RPi.GPIO
```bash
pip install RPi.GPIO
```

3. 設定樹莓派的腳位
```bash
buttonPin = 8
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # GPIO.BOARD 使用物理腳位編號；GPIO.BCM 使用 GPIO 控制器的腳位編號
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 設定按鈕為輸入並啟用上拉電阻，按下按鈕時接地
```

4. 串接按鈕  
![pin圖](https://github.com/Eddie114114/IOT_final/blob/main/picture/pi)

依照程式設定串接杜邦線，一條接到 `GPIO.BOARD` 編號8，另一條接到 `GPIO.BOARD` 編號6(接地)，兩條線的另外一端接到輕觸按鈕

---

## 可以改善的點
- FER資料集中表情明顯，因此訓練出的模型要臉部表情要夠誇張才會辨識出情緒，細微的情緒會被歸類為中性
- 語音輸出是機械化的聲音，需要改成更情緒化的聲音
- 硬體設備的延遲

---

## 參考資料
- (https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA)
- (https://www.tinkercad.com/dashboard)
- (https://www.youtube.com/watch?v=j6i4YTFlYRA&t=775s)
- (https://github.com/bnsreenu/python_for_microscopists)
- (https://ithelp.ithome.com.tw/articles/10301640)
- (https://ithelp.ithome.com.tw/articles/10302441)
- (https://boyie-chen.medium.com/%E7%94%A8raspberry-pi%E7%8E%A9%E6%B7%B1%E5%BA%A6%E5%AD%B8%E7%BF%92-1-%E6%8A%8Atensorflow2-3%E5%8F%8Akeras%E5%AE%89%E8%A3%9D%E5%88%B0pi4%E4%B8%8A%E5%90%A7-952900ef1c58)
