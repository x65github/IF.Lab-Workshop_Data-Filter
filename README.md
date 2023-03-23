# PDF後設資料－檔案清洗系統(論文版)
將論文內容寫入PDF的Meta內，並移除非特定論文內的雜訊

## 環境設置
### Python3
### PyPDF2
```
pip3 install PyPDF2 #安裝PyPDF2套件
from PyPDF2 import PdfFileReader, PdfFileWriter #導入PyPDF2套件，主要用以寫入meta
```
### PyMuPDF
```
pip3 install PyMuPDF #安裝PyMuPDF套件
import fitz #導入PyMuPDF套件，主要用以判斷論文內的各項目
```
### PDFMiner
```
pip install pdfminer.six #安裝PDFMiner套件，主要用以判斷標題
'''導入需要的套件'''
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTText, LTChar, LTAnno
```
### 程式流程圖
![image](https://raw.githubusercontent.com/x65github/IF.Lab-Workshop_Data-Filter/main/%E5%9F%BA%E6%9C%AC%E8%AA%AA%E6%98%8E/DataFilter_ProgramFlowchart.png)

### 範例程式
```
pattern_in = "C:\\" #pdf來源(here為現在所在路徑)
pattern_out = "C:\\" #pdf目的地(here為現在所在路徑):")
metaitems=main(pattern_in,pattern_out) 
# 注意事項：被此程式修改過metadata資料的pdf檔無法使用PyPDF2套件讀取，因為PyPDF2套件僅能讀取pdf內的特定Metadata。
```

# pdf metadata-data cleaning system(paper)
write contents into pdf meta, and delete unwanted information in unspecific  paper

## System
### Python3
### PyPDF2
```
pip3 install PyPDF2
import PyPDF2
```
### PyMuPDF
```
pip3 install PyMuPDF
import fitz
```
### Program Flowchart
![image](https://raw.githubusercontent.com/x65github/IF.Lab-Workshop_Data-Filter/main/%E5%9F%BA%E6%9C%AC%E8%AA%AA%E6%98%8E/DataFilter_En_ProgramFlowchart.png)

### Demo code
```
pattern_in = "C:\\" #pdf來源(here為現在所在路徑)
pattern_out = "C:\\" #pdf目的地(here為現在所在路徑):")
metaitems=main(pattern_in,pattern_out) 
```
# Warning！The metada of the new PDF files can't be read by PyPDF2, since PyPDF2 can only read specific metadata。
