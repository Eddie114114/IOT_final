import RPi.GPIO as GPIO
from time import sleep
import main
import os

buttonPin = 8
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 設定按鈕為輸入並啟用上拉電阻，按下按鈕時接地

def buttonCallback(channel):
    print("按鈕被按下，執行主函式...")
    main.main()

# 偵測按鈕事件
GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=buttonCallback, bouncetime=300)

try:
    print("準備就緒，等待按鈕...")
    os.system("mpg321 letsPlay.mp3")
    while True:
        sleep(0.1)  # 主迴圈保持運行，但不佔用過多 CPU 資源

except KeyboardInterrupt:
    print("程式中止。")

finally:
    GPIO.cleanup()
    
    
    
    
