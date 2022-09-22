# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileReader, PdfFileMerger
import fitz
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTText, LTChar, LTAnno
import math,re


def writemeta(pattern_out,pattern_in,pdf_document,metaiteams):
  '''將判斷的資料放入meta內'''
  file_in = open(pattern_in+pdf_document, 'rb')
  pdf_reader = PdfFileReader(file_in)
  pdf_merger = PdfFileMerger()
  pdf_merger.append(file_in)
  for keys,values in metaiteams.items():
    key='/'+keys
    if values is None:
      pdf_merger.addMetadata({key: "None"})
    elif isinstance(values,list):
      value=','.join(values)
      pdf_merger.addMetadata({key: value})
    else:
      pdf_merger.addMetadata({key: values})

  file_out = open(pattern_out+pdf_document, 'wb')
  pdf_merger.write(file_out)
  file_in.close()
  file_out.close()

def checkdoi(target): 
  '''確認內容有doi'''
  if "https://dx.doi.org/" in target:
    word="https://dx.doi.org/"
    return word
  elif "https://doi.org/" in target:
    word="https://doi.org/"
    return word
  elif "http://dx.doi.org/" in target:
    word="http://dx.doi.org/"
    return word
  elif "http://doi.org/" in target:
    word="http://doi.org/"
    return word
  elif "doi:" in target:
    word="doi:"
    return word
  elif "d o i :" in target:
    word="d o i :"
    return word
  else:
    return False

def getdoi(target):
  '''取得doi'''
  check=checkdoi(target)
  if check != False:
    doimb=target.split(check)[1]
    doimb=doimb.split("\n")[0]
    doi=moddoi(doimb)
    return doi
  else:
    return None

def moddoi(doimb):
    '''將doi前的空格去除'''
    k=0
    for i in range(len(doimb)):
      if doimb[i]==" ":
        k+=1
        continue
      else:
        doi=doimb[k:]
        break
    return doi

def iftime(maintxt):
  '''抓取發佈日期'''
  lines=maintxt.split('\n')
  target=[]
  for line in lines:
    if "/" in line and "\n" in line:
      target.extend(re.split('/|\n',line.lower()))
    elif "/" in line:
      target.extend(line.lower().split('/'))
    else:
      target.extend(line.lower().split('\n'))

  x=['']
  for i in range(0,len(target)):
    words=target[i]
    if ":" in words:
      x=re.split(':',words)
    if "published online" in x[0] or "date" in x[0] or " read" in x[0]:
      if len(x) == 1:
        return target[i+1]
      else:
        return x[1]

def checklen(people,target,number):
  '''已確認人數是否正確'''
  if target:
    people.extend(target)
  else:
    return False
  try:
    people.remove('')
  except: 
    pass
  if len(people) == number:
    return people

def getauthor(text):
  '''移除標題，取得作者名字所在區間'''

  if ':' in text:
    text=text.split('\n')[0]
    target=text.split(':')[1]
  else:
    text=text.split('\n')[0]
    target=text

  '''取得作者們'''
  new=[]
  if ';' in target:
    num=target.count(';')+target.count('and')
    clean=re.split(';|and',target)
  elif ',' in target:
    num=target.count(',')+target.count('and')
    clean=re.split(',|and',target)
  else: 
    if 'author' in target.lower(): 
      return False,False
    elif 'writer' in target.lower():
      return False,False
    else:
      people=[]
      people.append(target.title())
      return people,0

  for i in range(0,len(clean)):
    person = re.sub('[\d_]','',clean[i]).strip()
    check = re.findall('[a-z .·,;]', person) #移除文字右上角的註釋的標號
    person = ''.join(check).lstrip()
    if person != '':
      new.append(person.title())
    else:
      if i == len(clean)-1:
        pass
      else:
        num-=1

  if len(new) >1:
    return new,num
  else:
    people=[]
    people.append(new[0].title())
    return people,num

def ifauthor(text):
  '''判斷特定字(author、writer)'''
  if 'author' in text or 'a u t h o r' in text or 'w r i t e r' in text or 'writer' in text:
    retext=text.split(' ')
    for i in range(0,len(retext),1):
      words=retext[i].strip()
      relues=re.findall('[a-z]',words) #只留下文字
      word = ''.join(relues).lstrip()
      if word == 'author' or word == 'authors' or word == 'writer' or word == 'writers':
        if 'that' in retext or 'is' in retext or'are' in retext or 'am' in retext or 'for' in retext: 
          '''在文章段落內出現作者相關字眼'''
          return False
        else:
          return True
      else:
        continue
    return False
  else:
    return False

def remaintxt(maintxt,title):
  '''空格數量不對'''
  titlelen=len(title) #標題的行數
  retext=[] #去除空白的標題list
  for i in title:
    text=i.lower().split(' ')
    new=[]
    for k in text:
      if not k == '':
        new.append(k)
    retext.append(new) 
  target=maintxt.split('\n')
  for line in range(0,len(target),1):
    oritext=target[line].split(' ')
    text=[]
    for i in oritext:
      if not i =='':
        text.append(i)
    if text == retext[0]: 
      remaintxt='\n'.join(target[line+titlelen:])
      return remaintxt
  #沒有讀取到標題那一行
  return False

def aftertitle(maintxt,title):
  '''判斷標題後方是否為作者'''
  text='\n'.join(title).lower()
  try:
    clean=maintxt.split(text)[1]
    clean=clean.lstrip()
  except:
    check=remaintxt(maintxt,title)
    if check:
      clean=check.lstrip()
    else:
      return False

  text=clean.split('\n') #標題後方的文字list

  if '.' in text[0] or ',' in text[0]  or '·' in text[0]: 
    people=[]
    number=1
    for i in range(0,len(text),1):
      rt=getauthor(text[i])
      target,newlen=rt[0],rt[1]
      number+=newlen
      check=checklen(people,target,number)
      if check:
        return check
  else:
    return False

def author_maybe(maintxt,title_list):
  if title_list != None:
    authors=aftertitle(maintxt,title_list)
  else:
    authors=False
  if authors: #標題後方即有作者
    return authors
  else:
    text=maintxt.split('\n')
    people=[]
    start=False
    First=True
    for i in range(0,len(text),1):
      if not start or 'author' in text[i]: #由於排版原因，author後方可能接其他非author的資料，故再次確認是否重回False
        start=ifauthor(text[i])
      if start:
        #由於author可能後方即有作者名稱，因此要拆成兩個if
        if First:
          number=1
          First=False
        rt=getauthor(text[i])
        target,newlen=rt[0],rt[1]
        number+=newlen
        finish=checklen(people,target,number)
        if finish:
          if '.' in finish:
            finish.remove('.')
            return finish

def ifkeyword(maintxt): 
  maybeabst=''
  keyword=''
  target=[]
  for line in maintxt:
    target.extend(line.lower().split('\n'))
  if "keywords:" in target:
    maybeabst,keyword=target.split('keywords:')
  elif "keyword:" in target:
    maybeabst,keyword=target.split('keyword:')
  elif "keywords" in target:
    maybeabst,keyword=target.split('keywords')
  elif "key words:" in target:
    maybeabst,keyword=target.split('key words:')
  return maybeabst,keyword

def checkab(maintxt): 
  #print("in checkab")
  '''確認內容有無abstract，若無則用summary代替或回傳False'''
  if "graphical abstract" in maintxt :
    return False
  elif "abstract" in maintxt :
    word="abstract"
    return word
  elif "a b s t r a c t" in maintxt:
    word="a b s t r a c t"
    return word
  elif "summary" in maintxt:
    word="summary"
    return word
  elif "s u m m a r y" in maintxt:
    word="s u m m a r y"
    return word
  else:
    return False

def getab(maintxt): 
  '''取得摘要'''
  abans=checkab(maintxt)
  if abans!= False:
    #print('摘要關鍵字：',abans)
    maybe=maintxt.split(abans)[1]
    if "keywords" in maybe:
      maybe=maintxt.split("keywords")[0]
    elif "k e y w o r d s" in maintxt:
      maybe=maintxt.split("k e y w o r d s")[0]
    check=checkinfo(maybe)
    if check != False:
      wordif=bfintro(maybe)
      maybe=splitinfo(maybe,wordif)
  else:
    #"此篇論文無摘要"
    return None
  clean=maybe.split('\n')
  abstract=colines(clean)
  return abstract

def checkkw(maintxt):
  if "keywords" in maintxt:
    word="keywords"
    return word
  elif "k e y w o r d s" in maintxt:
    word="k e y w o r d s"
    return word
  else:
    return False

def getkw(maintxt): #keyword處理主程式
  kwlist=[]
  part=[]
  kwmaybe=[]
  kw=takekw(maintxt)
  kw=modkw1(kw)
  kwlist=kwtolist(kw)
  kwlist=modkw2(kwlist)
  if kwlist == []:
    return None
  else:
    return kwlist

def takekw(maintxt): #取出keywords所在區間
  wordkw=checkkw(maintxt)
  if wordkw != False:
    wordab=""
    wordab=checkab(maintxt)
    if wordab != False:
      wordab=str(wordab)
      part=maintxt.split(wordab)
      if wordkw in part[0]:
        wordkw=str(wordkw)
        kwmaybe=part[0].split(wordkw)
        kw=kwmaybe[1]
      elif wordkw in part[1]:
        wordkw=str(wordkw)
        kwmaybe=part[1].split(wordkw)
        check=checkinfo(kwmaybe[1])
        if check != False:
          wordif=bfintro(kwmaybe[1])
          kw=splitinfo(kwmaybe[1],wordif)
        else:
          kw=kwmaybe[1]
      return kw
    else:
      wordkw=str(wordkw)
      kwmaybe=maintxt.split(wordkw)
      check=checkinfo(kwmaybe[1])
      if check != False:
        wordif=bfintro(kwmaybe[1])
        kw=splitinfo(kwmaybe[1],wordif)
      else:
        kw=kwmaybe[1]
      return kw
  else:
    return ""

def modkw1(kw): #篩去多餘資料
  j=0
  k=0
  #篩掉句點後的資料
  if "." in kw:
    for i in kw:
      if i !=".":
        j+=1
        continue
      else:
        kw=kw[:j+1]
        break
  #篩掉開頭符號
  for i in kw:
    if i==" " :
      k+=1
      continue
    elif i==":" or "-":
      kw=kw[k+1:]
      break
  #篩掉開頭符號
  if "[page:" in kw:
    kw.split("[page:")[0]
  return kw

def kwtolist(kw): #關鍵字分段存成list
  k=["","",""]
  k[0]=len(kw.split(";"))
  k[1]=len(kw.split(","))
  k[2]=len(kw.split("\n"))
  kk=k.index(max(k))
  if kk==0:
    kwlist=kw.split(";")
  elif kk==1:
    try:
      kw=kw.split("\n")[0]
    except:
      pass  
    kwlist=kw.split(",")
  else:
    kwlist=kw.split("\n")
  return kwlist

def modkw2(kwlist): #去除多餘資料
  #去掉\n
  for n in range(len(kwlist)):
    if "\n" in kwlist[n]:
      kwlist[n]=kwlist[n].replace("\n"," ")
  #去掉空值
  for i in kwlist:
    if i=="" or i==" " or i=="  " or i=="   " or i=="    "or i=="     " or i=="1.":
      kwlist.remove(i)
  #去掉首項開頭空格
  try:
    if kwlist[0][0]==" ":
      kwlist[0]=kwlist[0][1:]
  except:
    pass
  return kwlist

def ignoretxt(linetext):
  '''由於以下文字於特定格式內會是最大的字體，因此需要跳過'''
  splitlinetxt=linetext.split(" ")
  if splitlinetxt==['Human', 'Resource', 'Management', 'Review', '\n']:
    return True
  elif splitlinetxt==['Human', 'Resource', 'Management', 'Review\n']:
    return True
  elif splitlinetxt==['Resource\n']:
    return True
  else:
    return False

def parse_line_layout(layout):
  '''取得頁面內最大字體的文字&文字高度'''
  max=0
  maxtxt=[]
  for textbox in layout:
      if isinstance(textbox, LTText):
        for line in textbox:
          firstchar=True
          if line.get_text() == ' ' or line.get_text() == '':
            break
          linetext=line.get_text()
          ifignore=ignoretxt(linetext)
          if ifignore:
            continue
          else:
            try:
              for char in line:
                if isinstance(char, LTAnno) or char.get_text() == ' ':
                  pass
                elif isinstance(char, LTChar):
                  y0=char.bbox[1] #print("從頁面底部到文字下邊緣的距離:",y0,"|||",char.get_text())
                  y1=char.bbox[3] #print("從页面底部到文字上邊缘的距離:",y1,"|||",char.get_text())
                  height=round(y1-y0, 12) #print(char.get_text(),'文字高度',height)
                  if firstchar : #取得每行的第一個字
                    fheight=height 
                    firstchar=False
                    continue
                  else: 
                    if fheight==height: #首字與第二個字高度一樣
                      if height>max: 
                        max=height
                        maxtxt.clear()
                        clean=linetext.replace("\n","")
                        maxtxt.append(clean)
                      elif height==max: #有和標題一樣高的字(應該是換行的標題)
                        clean=linetext.replace("\n","")
                        maxtxt.append(clean)
                      break
                    else:
                        continue #內文的第一行(第一個字特大)，跳過此行
              #print(line.get_text(),'整句高度',height)
            except:
              #print('Warning！此論文包含錯誤編碼')
              continue #編碼有誤，跳過此行
  return max,maxtxt

def colines(lines):
  '''將分行的list合併到一段內'''
  line=""
  for i in lines:
    sentence=i.strip()
    if sentence == '\n' or sentence == "":
      continue
    if sentence[-1:]=='-':
      clean=sentence[:-1]
    else:
      clean=sentence+" "
    line+=clean
  return line

def getmaxtxt(pattern,lcpage):
  pdf_document = open(pattern, 'rb')
  rsrcmgr = PDFResourceManager()
  laparams = LAParams()
  device = PDFPageAggregator(rsrcmgr, laparams=laparams)
  interpreter = PDFPageInterpreter(rsrcmgr, device)
  nowpage=0
  maxhigh=0
  title_sure=[]
  title=""
  for page in PDFPage.get_pages(pdf_document):
    if not nowpage > lcpage :
      interpreter.process_page(page)
      layout = device.get_result()
      max,title_maybe=parse_line_layout(layout)
      if maxhigh<max:
        title_sure=title_maybe
        maxhigh=max
      nowpage+=1
    else:
      break 
  title=colines(title_sure)
  if title =="":
    return None
  else:
    return title_sure,title

def splitinfo(target,word): 
  '''分割字串內容'''
  aftersplit = target.split(word)[0]
  return aftersplit

def bfintro(target): 
  '''確認introduction的呈現方式'''
  if "1. introduction" in target:
    word="1. introduction"
    return word
  elif "1.introduction" in target:
    word="1.introduction"
    return word
  elif "1 introduction" in target:
    word="1 introduction"
    return word
  elif "i. introduction" in target:
    word="i. introduction"
    return word
  elif "introduction" in target:
    word="introduction"
    return word
  elif "i n t r o d u c t i o n" in target:
    word="i n t r o d u c t i o n"
    return word
  else:
    return False

def checkinfo(target): 
  '''確認內容有introduction'''
  if "introduction" in target:
    return True
  elif "i n t r o d u c t i o n" in target:
    return True
  else:
    return False

def dopdf(pattern,pdf_document): 
  '''抓introduction前的資料，若無再抓result或前1/3頁的資料'''
  maintxt=""
  doc = fitz.open(pattern+pdf_document)
  pages=doc.page_count #總頁數
  lcpage=math.ceil(pages/3) #lastcheckpage，第三分之一頁
  ofttext="" #若整份資料查無introduction或result，將先暫存三分之一的內容
  for j in range(0,pages):
    nowpage=j+1
    page = doc.load_page(j)
    origin = page.get_text("text")
    target=origin.lower()
    ans=checkinfo(target) #print(str(j),'頁是否有introduction 或 result:',ans)
    if ans != False:
      text=bfintro(target)
      if j==0:
        maybe=target #若introduction或result在第1頁，將先暫存第1頁的內容
      else:
        maybe=splitinfo(target,text)
    else:
      maybe=""
    if maybe =="":
      if nowpage==pages:
        '''若有result則取result前的字眼'''
        if "result" in ofttext:
          ofttext=splitinfo(ofttext,"result")
        elif "r e s u l t" in target:
          ofttext=splitinfo(ofttext,"r e s u l t")
        maintxt=ofttext #將前1/3的內容取代txt的現有內容(無頁碼)
        break
      else:
        maintxt+=target+"page[:"+str(nowpage)+"]"
        if nowpage==lcpage:
          ofttext=maintxt
    else:
      maintxt+=maybe
      break
  return pages,lcpage,maintxt