# 獲取Wikidata Query ID程序
本程序為透過維基百科分類獲取其所收錄頁面之Wikidata Query ID。

## 所需設定參數
本程序之設定檔`config.py`需要設定4個參數，倘若未設定則本程序將無法運作。茲下說明之：
* `category_name`：分類名稱，如`Category:2020年台灣`...
* `language`：維基語言版本代碼，如`zh`、`en`...
* `project`：維基專案名稱，如`wikipedia`...
* `exclude`：欲排除之命名空間，如`^/wiki/(?!Wikipedia:|Special:|Category:|Help:|Portal:|Template:|User:)`表示僅需獲取主條目之Query ID。若不需排除則免填。

## 其他說明
* 程序在獲取完成後，於程序所在資料夾內輸出檔案`result.csv`，之中欄位分成2欄：qid（頁面之Qid）、page（頁面名稱）。
* 倘若該頁面無連結維基數據，則其qid欄位為空值。
