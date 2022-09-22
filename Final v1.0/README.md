# 函式說明

## A.讀取論文內容

### PDF相關套件
PyMuPDF

### 函式流程```dopdf(pattern,pdf_document)```
*  從路徑```pattern```及pdf檔名```pdf_document```讀取特定檔案
*  以頁為單位讀取pdf的內文文字，直至取得introduction前的文字資料(詳見注意事項)。
*  存取頁面文字與頁碼於```maintxt```，並回傳整份論文的第1/3頁```lcpage```及```maintxt```以供其他函數使用。

### 注意事項
*  為將正確資料寫入meta(作者、關鍵字、摘要等等)，若introduction在第一頁則存取整頁資料。
*  若該頁論文無introduction，則讀取下一頁，若整篇論文都沒有，會截取前三分之一的論文以供後續判斷。
---
## B.標題判斷

### PDF相關套件
PyPDF2、PyMuPDF、PDFMiner

### 判斷原理
進行EDA時，我們發現標題多為論文內字體最大的字，故以字體大小作為標題的判斷依據。

### 注意事項
1. 部分論文用PDFMiner讀取會因為編碼異常而無法正常判斷
2. 若論文標題非最大高度之文字，且```ignoretxt()```無法除錯，則會判斷錯誤

### 判斷流程```getmaxtxt()```
1. 依次讀取頁面內容
2. 依次讀取整行內容，若為空行或僅有空格則讀取下一行文字
3. 判斷文字內容，若為特殊文字則讀取下一行文字(詳見特殊判斷```ignoretxt(maintxt)```)
4. 進行字體高度判斷，若前2個文字大小不一致則讀取下一行文字，若與目前最大高度一樣則文字append進```maxtxt```內
5. 回傳文字高度 ```max``` 與文字內容```maxtxt```
6. 完成讀取整份論文前1/3之頁面文字後，將最大高度(及最大字體)之句子判斷為標題。

### 特殊判斷```ignoretxt(maintxt)```
部分論文來源的版面將造成論文標題非最大字體，故讀取到特定文字時```return False``` 以解決此問題。
*  期刊－Human Resource Management Review：```"Human Resource Management Review"```
*  出版社－Cellpress：```"Human Resource Management Review"```

### 函數說明
*  ```parse_line_layout()```:抓取頁面內的文字高度，並回傳最大的文字高度 ```max``` 與文字內容```maxtxt```
*  ```ignoretxt()```:判斷是否為特定來源之檔案(判斷方式如上所述)
---
## C.摘要判斷

### 判斷原理
進行EDA時，我們發現摘要多以abstract、summary作為摘要標題，因此以```"abstract"```及```"summary"```作為摘要的判斷依據。

### 注意事項
1. 若論文內沒有```"abstract"```與```"summary"```，則無法判斷摘要
2. 由於論文內容```maintxt```是用```"introduction"```進行分割，若無此詞且摘要後有非摘要的內容則會出錯

### 判斷流程```getab(maintxt)```
*  判斷論文內容```maintxt```內是否有摘要關鍵字```"abstract"```，若無則用```"summary"```代替
*  用條件判斷式篩去非摘要的文字
---
## D.關鍵字判斷

### 判斷原理
進行EDA時，我們發現關鍵字皆以```"keyword"```作為關鍵字標題，因此以```"keyword"```作為關鍵字的判斷依據。

### 注意事項
1. 若論文內沒有```"keyword"```，則代表該論文無關鍵字
2. 由於論文內容```maintxt```是用```"introduction"```進行分割，若無此詞且摘要後有非摘要的內容則會出錯

### 判斷流程```getkw(maintxt)```
*  判斷論文內容```maintxt```內是否有關鍵字```"keyword"```
*  用條件判斷式篩去非關鍵字的文字
*  將篩選出的內容分割成單獨關鍵字存進list
---
## E.作者判斷

### 判斷原理
進行EDA時，我們發現作者標題多以author、writer作為關鍵字，或以```,```、```;```、```and```直接列出作者，或直接標示於論文標題下方，因此以此進行相關判斷。

### 注意事項
1. 
### 判斷流程```author_maybe(maintxt,title_list)```
*  若論文標題```title_list```非```None```則先呼叫```aftertitle(maintxt,title_list)```以判斷標題後方是否有作者(詳見標題後作者判斷```aftertitle(maintxt,title_list)```)


---
## F.發佈時間判斷

### 判斷原理
進行EDA時，我們發現發佈日期多以```publish time：YYYY/MM/DD```呈現，因此以```"published online"```作為發佈時間的判斷依據。

### 判斷流程```iftime(maintxt)```
*  將論文內容```maintxt```依```\n```分割，並依次讀取整行內容
*  將每行內容依```：```分割，並判斷是否有```"publish time"```
*  若```：```後方無文字則讀取下一行文字，否則回傳```：```後方的文字
---
## G.DOI判斷

### 判斷原理
進行EDA時，我們發現關鍵字皆以```"doi"```作為doi標題，因此以```"doi"```作為關鍵字的判斷依據。
