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

tensorflow無法使用pip安裝，從以下網址下載python版本對應的wheel，python3.7、32位元使用tensorflow-2.4.0-cp37-none-linux_armv7l.whl  
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

樹莓派執行speech_recognition時可能遇到錯誤，需要安裝pyaudio:
<pre>
<code>
 pip3 install pyaudio
</code>
</pre>

---

## Step3: 訓練模型及使用
### 訓練(不在樹莓派上執行，會很久!!)
使用 FER2013 資料集來訓練CNN卷積神經網路，可以辨識人臉的七種情緒：
- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad
- Surprise
下載連結如下:  
[https://www.kaggle.com/datasets/msambare/fer2013](https://www.kaggle.com/datasets/msambare/fer2013)  

使用Python 3.7 及以下套件：
- keras
- numpy
- matplotlib
- seaborn
- sklearn

參考trainEmotionModel.py

### 使用
使用convert_h5_to_tflite.py將模型轉換成tflite檔案，tflite在樹莓派上可以有更好的效率  


---

## Step4: 語音輸入及輸出

---

## Step5: 串接語言模型

---

## Step6: 整合函式

---

## Step7: 設定按鈕

---

## 可以改善的點

---

## 參考資料
