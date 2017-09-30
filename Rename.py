#coding=utf-8

import os, re, types
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import logging 
logging.Logger.propagate = False 
logging.getLogger().setLevel(logging.ERROR)
#Get file names in the folder
filenames = os.listdir(os.getcwd())
filenames_bak = []
for name in filenames:
    if re.search('pdf',name):
        filenames_bak.append(name)
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
rsrcmgr = PDFResourceManager()
#string = ['start']

#charactor = 'ﬁt'
#xxx = re.sub('ﬁ','error',charactor)
i = 0
for name in filenames_bak:
    # Open a PDF file.
    fp = open(name, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    doc = PDFDocument()
    # Connect the parser and document objects.
    parser.set_document(doc)
    # Create a PDF document object that stores the document structure.
    # Connect the parser and document objects.
    try:
        doc.set_parser(parser)
    except:
        continue
    # Supply the password for initialization.
    # (If no password is set, give an empty string.)
    doc.initialize('')
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    Text = ""
    for page in doc.get_pages():
        break
        #break
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    string = []
    try:
        for TextLine in layout:
            try:
                flag = 0
                positionh = -1
                positionw = -1
                width = 0
                size = 0
                j = 0
                for line in TextLine:
                    linetype = type(line)
                    try:
                        if isinstance(line, pdfminer.layout.LTChar) or isinstance(line, pdfminer.layout.LTAnon):
                            flag = 1
                            if (round(line.matrix[5], 2) != positionh) and (positionh > 0):
                                if not isinstance(charactor, pdfminer.layout.LTAnon):
                                    Text += '\n'
                                    string.append((Text,size))
                                    Text = ""
                                    positionw = -1
                                    size = 0
                                    j = 0
                            if (round(line.matrix[4], 2) >=  (positionw + width + 2)) and (positionw > 0): #上次的位置+上次的宽度+最小空格宽度（自己估计的值）
                                try:
                                    newText = line._text
                                except:
                                    newText = 'adsgfbgrbregtvfevsfdvsfdv'
                                if newText != ' ':
                                    Text += ' '
                            charactor = line
                            j += 1
                            positionh = round(charactor.matrix[5], 2)
                            positionw = round(charactor.matrix[4], 2)
                            width = charactor.width
                            Text = Text + charactor._text
                            if j == 2:
                                try:
                                    size = round(charactor.height, 2)
                                    #if charactor.height > 20:
                                    #    continue
                                except:
                                    j = j - 1
                                    continue
                        else:
                            size = 0
                            j = 0
                            for charactor in line:
                                j += 1
                                Text = Text + charactor._text
                                if j == 2:  #仍存在公式中带下标字母大小不对的问题，可以考虑从判断字母编码入手
                                    try:
                                        size = round(charactor.height, 2)
                                        if charactor.height > 20:
                                            continue
                                    except:
                                        continue
                            string.append((Text,size))
                            Text = ""
                    except:
                        continue
                if flag == 1:
                    string.append((Text,size))
                    Text = ""
                    flag = 0
            except:
                continue
    except:
        i = 1
    maxsize = 0
    title = []
    ScienceDirect = 0
    manuscript = 0
    flag = 0
    for line in string:
        if line[1] > maxsize:
            maxsize = line[1]      
        if re.search('Journal of The Electrochemical Society', line[0]):
            ScienceDirect = 0
            flag = 1
        if (flag == 0) and (ScienceDirect == 0):
            if re.search('ScienceDirect', line[0]):
                ScienceDirect = 1
            if re.search('Applied Energy', line[0]):
                ScienceDirect = 1
            if re.search('Renewable and Sustainable Energy Reviews', line[0]):
                ScienceDirect = 1 
            if re.search('Journal', line[0]):
                ScienceDirect = 1   
            if re.search('Accepted Manuscript', line[0]):
                ScienceDirect = 1
            if re.search('Energies', line[0]):
                ScienceDirect = 1
    for line in string:
        if line[1] == maxsize:
            title.append(line[0].replace('\n',' '))
    temp = title
    title = ''
    for line in temp:
        title = title + line
    
    data = doc.info[0].items()
    for list in data:
        if re.search('ModDate', list[0]):
            date = list[1]
            try:
                date = re.split('\:',date)[1]
                date = date[:4]
                if int(date) < 2009:
                    ScienceDirect = 0
            except:
                date = 'Invalid'
        if re.search('Title', list[0]):
            faketitle = list[1]
    if ScienceDirect == 1:
        title = faketitle
    if type(title) is type(b'1'):
        titletemp = title
        title = '' 
        for char in titletemp:
            try:
                if char <= 128:
                    title += chr(char)            
            except:
                continue
    #    continue
    #if not re.search('\:', date):
    #    continue
    title = re.sub('\:', '-', title)
    title = re.sub('\\\\', 'or', title)
    title = re.sub('\/', 'or', title)
    title = re.sub('\*', '', title)
    
    str = date + ' ' + title
    fp.close()
    try:
        print(str)
        try:
            os.rename(name, str + '.pdf')
        except:
            i = i + 1
            continue
    except:
        continue
