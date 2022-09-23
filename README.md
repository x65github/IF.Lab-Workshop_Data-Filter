# PDF後設資料－檔案清洗系統(論文版)
將論文內容寫入PDF的Meta內，並移除非特定論文內的雜訊

## 環境設置
### Python3
### PyPDF2
```
pip3 install PyPDF2 #安裝PyPDF2套件
import PyPDF2 #導入PyPDF2套件
```
### PyMuPDF
```
pip3 install PyMuPDF #安裝PyMuPDF套件
import fitz #導入PyMuPDF套件
```
### 程式流程圖
![image](https://raw.githubusercontent.com/x65github/IF.Lab-Workshop_Data-Filter/main/%E5%9F%BA%E6%9C%AC%E8%AA%AA%E6%98%8E/DataFilter_ProgramFlowchart.png)
## 執行方式
執行main檔
注意事項:被此程式修改過metadata資料的pdf檔無法使用PyPDF2套件讀取，因為此套件僅能讀取官方軟體生成的pdf檔案。

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
## How To Do
> TBD
