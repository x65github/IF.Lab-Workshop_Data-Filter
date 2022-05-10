# IF.Lab Side Project Workshop-第一組 Data Filter

<h3>基本資料</h3>
<ul>
　<li>組別：第一組</li>
  <li>成員：劉語萱 09170101、陳柏尹 09170109、(組長)廖曉珺 09170131</li>
  <li>會議時間：每週五 10 點 30 分（備用時間：每週六 10 點 30 分）</li>
  <li>專案網址：https://github.com/x65github/IF.Lab-Workshop_Data-Filter.gi</li>
</ul>
<h3>專案時間</h3>
<ul>
　<li>時長：16 週</li>
  <li>開始日：4/20</li>
  <li>結束日：8/10</li>
</ul>
<h3>專案目的</h3>
匯出檔名為論文名稱&內容為僅包含該論文資訊的 PDF 檔
<table>
  <tr>
    <td>完整流程</td>
    <td>舉例</td>
  </tr>
  <tr>
    <td>匯入/選取「檔名非論文名稱」的 PDF 檔</td>
    <td>匯入/選取 123.pdf</td>
  </tr>
  <tr>
    <td>用 Python 篩選出與「主要」論文相關的論文資料</td>
    <td>第 1 頁：論文 A 的最末頁<br>第 2~16 頁：論文 B 的內容<br>第 17 頁：論文 C 的起始頁</td>
  </tr>
  <tr>
    <td>刪除其他雜訊</td>
    <td>刪除第 1 頁、第 17 頁的內容<br>保留第 2~16 頁</td>
  </tr>
  <tr>
    <td>匯出 PDF 檔案（檔名為論文名稱）</td>
    <td>匯出 B.pdf</td>
  </tr>
</table>

<h3>程式套件(開源)/h3>
PyPDF2
PyMuPDF 1.19.6 https://pymupdf.readthedocs.io/en/latest/

<h3>程式流程圖</h3>

![image](https://raw.githubusercontent.com/x65github/IF.Lab-Workshop_Data-Filter/main/%E5%9F%BA%E6%9C%AC%E8%AA%AA%E6%98%8E/DataFilter_ProgramFlowchart.png)
