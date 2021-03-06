# -*- coding: utf-8 -*-
"""Data_Filter_EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OaFuFje8gBt_YPOxE-3WmC5oNT4wp3Ai

將metadata匯出成dict
!pip install pymupdf
!pip install pypdf2
!pip install pandas
"""

import fitz
from glob import glob
from os import path
from PyPDF2 import PdfFileReader, PdfFileWriter

def get_meta(type,fodername,files):
    max=0
    metadata=dict()
    if type == "pymupdf":
      for pdf_document in files:
        doc = fitz.open("C:\\Users\\siao0\\Downloads\\DataFilter\\0608\\"+fodername+"\\"+pdf_document)
        meta_len=len(doc.metadata)
        if meta_len > max:
          max=meta_len
        for meta in doc.metadata:
          key=meta.split(':')[0]
          if key in metadata:
            metadata[key]+=1
          else:
            metadata[key]=1
    else:
      for pdf_document in files:
        reader = PdfFileReader("C:\\Users\\siao0\\Downloads\\DataFilter\\0608\\"+fodername+"\\"+pdf_document)
        meta = reader.getDocumentInfo()
        metadata={**metadata,**meta}
        meta_len=len(meta)
        if max < meta_len:
          max == meta_len

    return max,metadata


def trainingSet_meta_len(type):
  metadata=dict()
  pattern = "C:\\Users\\siao0\\Downloads\\DataFilter\\0608\\right\\*.pdf" 

  num,files=get_len(True,pattern)
  max,metadata=get_meta(type,"right",files)
  return num,max,metadata

def testSet_meta_len(type):
  metadata=dict()
  pattern = "C:\\Users\\siao0\\Downloads\\DataFilter\\0608\\error\\*.pdf" 

  num,files=get_len(False,pattern)
  max,metadata=get_meta(type,"error",files)
  return num,max,metadata

def get_len(rightName,pattern):
  files = [ path.basename(x) for x in glob(pattern)] #取得所有PDF的檔名
  '''
  if rightName:
    print("檔名正確的數量: ",len(files))
  else:
    print("檔名錯誤的數量: ",len(files))
  '''
  return len(files),files

def pymupdf_main():
  global metas
  num,max,metadata=trainingSet_meta_len("pymupdf")
  #print('一份PDF內，Meta最多有%d個' %max)
  #print('Meta共有%d個值' %len(metadata))
  #print('Meta資料：%s' %metadata.keys())
  metas["Pymupdf_檔名正確"]={"資料數量":num,"meta值":len(metadata)}

  num,max,metadata=testSet_meta_len("pymupdf")
  #print('一份PDF內，Meta最多有%d個' %max)
  #print('Meta共有%d個值' %len(metadata))
  #print('Meta資料：%s' %metadata.keys())
  metas["Pymupdf_檔名錯誤"]={"資料數量":num,"meta值":len(metadata)}

def pypdf2_main():
  global metas
  num,max,metadata=trainingSet_meta_len("pypdf2")
  #print('一份PDF內，Meta最多有%d個' %max)
  #print('Meta共有%d個值' %len(metadata))
  print('Meta資料：%s' %metadata.keys())
  metas["pypdf2_檔名正確"]={"資料數量":num,"meta值":len(metadata)}

  num,max,metadata=testSet_meta_len("pypdf2")
  #print('一份PDF內，Meta最多有%d個' %max)
  #print('Meta共有%d個值' %len(metadata))
  #print('Meta資料：%s' %metadata.keys())
  metas["pypdf2_檔名錯誤"]={"資料數量":num,"meta值":len(metadata)}

import pandas as pd

metas={}
pymupdf_main()
pypdf2_main()

df = pd.DataFrame(metas)
print(df)