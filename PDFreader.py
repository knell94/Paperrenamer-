import os, re, types
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
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
#text = 'MOSBO to signiﬁcantly reduce the resulting computational effort. Three MOSBO algorithms are'
#text = 'MOSBO to signiﬁcantly reduce the resulting computational effort. Three MOSBO algorithms are'
#text = re.sub('ﬁ','error',text)
#charactor = '?t'
#xxx = re.sub('?','error',charactor)
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
    Text = []
    for page in doc.get_pages():
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        for TextLine in layout:
            if  isinstance(TextLine, LTTextBoxHorizontal): 
                for line in TextLine:
                    for charactor in line:
                        Text.append(charactor._text)
                    string = ("").join(Text)
                    try:
                        string = re.sub('?', '+', string)
                    except:
                        s = 0
                    try:
                        string = re.sub('?', '', string)
                    except:
                        s = 0
                    try:
                        string = re.sub('?','fi',string)
                        s = 1
                    except:
                        s = 0
                    try:
                        string = re.sub('\(|\)','',string)
                    except:
                        s = 0
        string = re.split('\n',string)
        for line in string:
            line = re.sub('þ', '+', line)
            line = re.sub('©', '', line)
            line = re.sub('ﬁ','fi',line)
            line = re.sub('ﬂ','fl',line)
            line = re.sub('ﬀ','ff',line)
            line = re.sub('ﬃ','ffi',line)
            line = re.sub('ﬄ','ffl',line)
            line = re.sub('ﬅ','ft',line)
            line = re.sub('\(|\)','',line)
            print(line)
        print(string)
        break