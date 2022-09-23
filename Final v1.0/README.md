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
6. 完成讀取整份論文前1/3之頁面文字後，將目前的```title_sure```用```colines```合併成一行```title```。

### 特殊判斷```ignoretxt(maintxt)```
部分論文來源的版面將造成論文標題非最大字體，故讀取到特定文字時```return False``` 以解決此問題。
*  期刊－Human Resource Management Review：```"Human Resource Management Review"```
*  出版社－Cellpress：```"Human Resource Management Review"```

### 函數說明
*  ```parse_line_layout(layout)```:抓取頁面內的文字高度，並回傳最大的文字高度 ```max``` 與文字內容```maxtxt```
*  ```ignoretxt(linetext)```:判斷是否為特定來源之檔案(判斷方式如上所述)
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
2. 由於論文內容```maintxt```是用```"introduction"```進行分割，若無此詞且關鍵字後有非關鍵字的內容則會出錯

### 判斷流程```getkw(maintxt)```
*  判斷論文內容```maintxt```內是否有關鍵字```"keyword"```
*  用條件判斷式篩去非關鍵字的文字
*  將篩選出的內容分割成單獨關鍵字存進list
---
## E.作者判斷

### 判斷原理
進行EDA時，我們發現作者通常直接標示於論文標題下方，或以author、writer作為關鍵字，而呈現方式多以```,```、```;```、```and```分隔各作者，因此以此進行相關判斷。

### 注意事項
1. 由於各論文版型因素，判斷之資料不一定為實際論文作者資訊
2. 部分論文作者數過多，因此原本就為完全列出相關作者資訊，而是以...呈現

### 判斷流程1```author_maybe(maintxt,title_list)```
*  若論文標題```title_list```非```None```則用特定標點符號判斷標題後方是否有作者(詳見判斷流程2```aftertitle(maintxt,title_list)```)
*  將論文內容```maintxt```依```\n```分割，並依次讀取整行內容
*  若文字包含```'author'```則判斷是否為作者區塊(詳見區分作者與內文```ifauthor(text)```)
*  呼叫```getauthor```取得作者資訊(詳見取得作者資訊```getauthor(text)```)
*  呼叫```checklen```判斷作者區塊是否結束(詳見判斷作者數量```checklen(people,target,number)

### 區分作者與內文```ifauthor(text)```
由於論文內文內可能亦有author、writer，因此用特定詞性的文字判斷是否為內文。
*  be 動詞：is、are、am
*  介係詞/其他：for、that

### 判斷流程2```aftertitle(maintxt,title)```
*  將論文內容```maintxt```依標題```title```分割，若有異常則呼叫```remaintxt```進行修正(詳見內容/標題重新判斷```remaintxt(maintxt,title)```)
*  若內容包含特定標點符號－「.」、「,」或「·」則代表有作者
*  呼叫```getauthor```取得作者資訊(詳見取得作者資訊```getauthor(text)```)
*  呼叫```checklen```判斷作者區塊是否結束(詳見判斷作者數量```checklen(people,target,number)```)

### 內容/標題重新判斷```remaintxt(maintxt,title)```
由於論文標題```titlet```是透過PDFMiner判斷的，而論文內容```maintxt```是透過PyMuPDF判斷，因此可能會有差異。
*  空格數差異：將```titlet```與```maintxt```依空格分割成list後進行比較以解決此問題。
*  文字差異：目前無法解決，直接```return False```使得```aftertitle```的回傳值為```False```以解決此問題。

### 取得作者資訊```getauthor(text)```
*  若「:」存在，則取得這一行文字```text```內「:」後方的文字
*  若特定標點符號－「,」、「;」存在，則計算特定標點符號+「and」的出現次數```num```，並將文字依特定標點符號及「and」分割
*  若無特定標點符號，且有```'author'```或```'writer'```存在，則代表該行是作者區塊的起始點，但尚未包含作者資訊
*  存取作者資訊，並移除文字右上角的註釋標號
*  回傳這一行文字內所包含的作者```people```及```num```

### 判斷作者數量```checklen(people,target,number)```
由於作者區塊可能不只一行，因此藉由判斷作者們```people```的長度與分隔符號「,」、「;」與「and」的出現次數+1```number```是否一樣，以判斷是否完成作者存取。

---
## F.發佈時間判斷

### 判斷原理
進行EDA時，我們發現發佈日期多以```publish time：YYYY/MM/DD```呈現，因此以```"published online"```...等特定字作為發佈時間的判斷依據。

### 判斷流程```iftime(maintxt)```
*  將論文內容```maintxt```依```\n```分割，並依次讀取整行內容
*  將每行內容依```：```分割，並判斷是否有```"publish time"```
*  若```：```後方無文字則讀取下一行文字，否則回傳```：```後方的文字
---
## G.DOI判斷

### 判斷原理
進行EDA時，我們發現關鍵字皆以```"doi"```作為doi標題，因此以```"doi"```作為關鍵字的判斷依據。
