# 榮譽假守護者

當服兵役放假的時候，新兵每天都有三個時段需要用 Line 回報目前的狀況，準時回報就有機會放 1800 榮譽假。</p>
我服兵役時正值 COVID-19 疫情猖獗，需要回報的資訊更多（ex: 096 xxx 無發燒 無感冒 無飲酒 體溫 36.0 度），而且每個人的回報訊息要整合成一個，所以就需要去複製別人的訊息，再加上自己的。很常發生有兩個以上的人同時輸入，導致互相蓋掉對方訊息的問題。</p>
因此，我寫了一個 `Linebot` 來整合弟兄們的回報訊息，命名為「榮譽假守護者」。</p>

## Table of Contents

- [Technology](#technology)
- [Features](#features)
- [Demonstration](#demonstration)
  <!-- - [Setup](#setup) -->
  <!-- - [Reference](#reference) -->

### Technology

這個專案是由 `Line Messaging API` + `AWS Lambda` + `AWS DynamoDB` 建立而成。

- `Line` 做為使用者介面
- `Lambda` 執行 `Line Messaging API` 來處理 Line 回報訊息。由於放假才需要回報，且程式邏輯單純，所以 `Lambda` 的特性很符合此專案的需求。
- `DynamoDB` 儲存新兵的回報資訊。`Lambda` 預設閒置 5 分鐘就停用（stateless），不適合將回報資訊儲存在變數中，且 NoSQL 較彈性，所以採用 `DynamoDB`。

### Features

以 `*` 做為觸發指令的關鍵字，總共有三個指令。

1. 使用預設回報 </br>
   只需輸入學號和地點，程式會自動回復預設的狀況以及自動 36.0-36.7 的體溫。

   - 指令：\*學號 地點
   - 輸入：\*096 在家
   - 回傳：\*096 xxx 無發燒 無感冒 無飲酒 體溫 36.0 度

2. 使用自訂回報 </br>
   輸入學號、地點以及自訂的狀況。

   - 指令：\*\*學號 地點 狀況
   - 輸入：\*\*096 在家 無發燒 咳嗽頭痛 已看醫生 體溫 35.8 度
   - 回傳: \*\*096 xxx 在家 無發燒 咳嗽頭痛 已看醫生 體溫 35.8 度

3. 清除回報 </br>
   只輸入學號，清除之前輸入的狀況。
   - 指令：\*學號
   - 輸入：\*096
   - 回傳：\*096

### Demonstration

<img src="https://i.imgur.com/tK4ewIO.jpg" width="350" height="400" /> &emsp;&emsp;&emsp;&emsp;
<img src="https://i.imgur.com/WcyQL2r.jpg" width="350" height="400" />