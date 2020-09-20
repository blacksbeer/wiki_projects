# 批量零編輯執行程序
本程序乃透過指定之維基百科分類獲取其收錄之頁面，並且將其進行批量零編輯（Null Edit），其目的係在調整模板或創建分類後，為更新分類而須透過零編輯以更新快取。

注意：本程序需登入維基帳戶方可正常使用，否則過濾器將限制編輯頻率而讓零編輯執行失敗。

## 所需輸入參數
本程序之設定檔`config.py`需要設定7個參數，皆為必填。倘若未設定則本程序將無法運作。茲說明之：
* `USERNAME` 使用者名稱
* `PASSWORD` 使用者密碼
* `CATEGORY_NAME` 分類名稱
* `LANGUAGE` 維基語言版本代碼
* `PROJECT` 維基專案名稱
* `CMNAMESPACE` 欲搜索之命名空間：預設值為`*`（不限）。倘若僅搜索主條目與分類，則輸入`0|14`。對於其他代碼，詳見https://www.mediawiki.org/wiki/Help:Magic_words#Namespaces_2
* `CMLIMIT` 分類搜索上限：預設值為`500`，也是一般使用者可搜索之上限。若有Bot權限則可調整至`5000`

## 程序相關資訊
* 公開日期：2020年9月20日
* 執行頻率：1 edit / 2 sec（通常），其頻率視網路情況而定