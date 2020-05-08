import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs 

def get_pdfs(_url): #find all <a> on page and put to the list all of them that ends with .pdf
    r = requests.get(_url)
    soup = bs(r.content,'html5lib')
    links = soup.findAll('a')
    pdf_links = ["https://link.springer.com" + link['href'] for link in links if link['href'].endswith('pdf')]
 
    return pdf_links

def download_pdf(_url, title, cat):
    file_name = title
    print("Downloading book: {}".format(file_name))
    r = requests.get(_url[0], stream = True) # only first link is link to full version in pdf. Other are just chapters.
    dirr = cat + "/" + title + '.pdf'
    if os.path.exists(dirr):
        pass
    else:
        with open(dirr, "wb") as pdf:
            for chunk in r.iter_content(chunk_size=10000000):
                if chunk:
                    pdf.write(chunk)

if __name__ == '__main__':
    path_ = os.getcwd()
    xlsx_path = os.path.join(path_, 'm.xlsx')
    df = pd.read_excel(xlsx_path)
    n = df.shape[0]


    names = pd.unique(df['English Package Name'])
    for name in names:
        if not os.path.exists(name):
            name_ = os.path.join(path_, name)
            os.mkdir(name_)

    for i, _url in enumerate(df['OpenURL']):
        title = df['Book Title'][i].split('/')[0] # there was an error, in x.xlsx one of the book titles tahe '/' which crashes line 22(with open(...))
        category = df['English Package Name'][i]
        print("{}/{}".format(i+1,n))
        download_pdf(get_pdfs(_url),title, category)

###############################################