from tkinter import Tk
from tkinter.filedialog import askopenfilename,askdirectory
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from cleantext import clean
import pyttsx3
import ntpath

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

blacklist = ['[document]', 'noscript','header','html','meta','head','input','script',]

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        text = text.encode('utf-8')
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

def clean_text(text):
    text = text.replace(r"\xe2\x80\x9c","")
    text = text.replace(r"\n","")
    text = text.replace('\\',"")
    text = text.replace(r"\xe2\x80\x9d","")
    text = text.replace(r"xe2x80x94"," ")
    text = text.replace(r"b'","")
    return text

Tk().withdraw()
filename = askopenfilename()
extension = "epub"
if filename[-4:]==extension:
    new_name = ntpath.basename(filename)
    index = new_name.find(".epub")
    new_name = new_name[:index]+"_(Audiobook).mp3"

    output = epub2text(filename)
    safe_text = clean(output,fix_unicode=True,to_ascii=True,lower=True,lang="en")
    safe_text = clean_text(safe_text)

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    speech_rate = int(input("Speech Speed(Recommended 150-200): "))
    engine.setProperty('rate',speech_rate)

    gender = int(input("For Male Select 0 For Female Select 1: "))
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[gender].id)
    engine.save_to_file(safe_text,new_name)
    engine.runAndWait()
else:
    print("Select an .epub file")