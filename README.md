# ESYS_HW4

B07901123

## mbed_app.jason,pretty_printer.h
按講義更改

## ButtonService.h,main.cpp
在範例的server下加入IDstage(0xA002)和ledstage(0xA003)兩個characteristic，定義其資料類別及新增所需功能。

## stm_pi_BT.py
由上一個作業更改而成。
連接後打開按鈕characteristic(0xA002)的notify，並提供read/ledon/ledoff/finish功能。

* read
  * 讀取輸入的characteristic
* ledon
  * 打開LED2
* ledoff
  * 關閉LED2
* finish
  * 結束main thread

有另外用一個thread來做接收訊息的功能(在main thread 沒有任何操作下)。
