#Project Title: Grocery price finder
#Name: Tsai Chun Yuan
#GitHub: ChunYuanTsai
#EdX: CY1966
#Country & City: Singapore
#Date: 13 April 2024
'''
Accept user input via CLI for product names
Get top 20 search results from 2 grocery stores in Singapore (Fairprice and Cold Storage)
Ouput a table in CLI of the search results with col Grocer, Product, Price
'''
import argparse,sys,requests,re,html,logging
from tabulate import tabulate
from bs4 import BeautifulSoup

class Grocer:
    def __init__(self,name,baseurl,BSselector_title,BSselector_desc,BSselector_price):
        #self.searchterms=searchterms
        self.name=name
        self.baseurl= baseurl
        self.BSselector_title= BSselector_title
        self.BSselector_desc=BSselector_desc
        self.BSselector_price=BSselector_price
        self.url=''

    def searchweb(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        headers = {"User-Agent": user_agent}
        logging.info(f'Downloading webpage {self.url}')
        req=requests.get(self.url, headers=headers)
        try:
            req.raise_for_status()
        except:
            sys.exit('Fail to download result')
        return req

    def BS(self,word,text):
        text=html.unescape(text)
        logging.info(f'Parsing downloaded webpage for {word}')
        bs=BeautifulSoup(text,'html.parser')
        title=bs.find_all(*self.BSselector_title)
        desc=bs.find_all(*self.BSselector_desc)
        price=bs.find_all(*self.BSselector_price)
        logging.debug(f'{len(title)}----{len(desc)}----{len(price)}')
        logging.debug(f'title\n\n{title}')
        logging.debug(f'desc\n\n{desc}')
        logging.debug(f'price\n\n{price}')
        if not title or not desc or not price:
            print('No result found')
            return False
        if len(title)==len(desc)==len(price):
            logging.info(f'Getting sequence of title,desc,price for {word} by getText')
            title=map(lambda x: x.getText(),title)
            desc=map(lambda x: x.getText(),desc)
            price=map(lambda x: x.getText(),price)
            comb=zip(title,desc,price)
        else:
            logging.info(f'Getting sequence of title,desc,price for {word} by regex')
            comb=zip(self.regex(title),self.regex(desc),self.regex(price))
        comb=list(comb)
        if len(comb) > 20:
            comb=comb[:20]
        return tuple(comb)

    def tab(self,i):
        if i:
            logging.info(f'Tabulating first 20 results...')
            print(self.name)
            print(tabulate(i, tablefmt="grid",headers=["Product","Description","Price"]))
            return True
        else:
            print('Nothing to tabulate')
            return False

    def savetofile(self,filename,respobj):
        with open(f'{filename}.txt','wb') as file:
            for chunk in respobj.iter_content(100000):
                    file.write(chunk)

    def readtext(self,filename):
        with open(f'{filename}.txt','r') as file:
            text=file.read()
            return text

    def regex(self,list):
        t=[]
        regex=re.compile(r'\">([^<•].+)</span>')
        for i in list:
            match=regex.search(str(i))
            if match != None:
                t.append(match.group(1))
        return t

    @property
    def baseurl(self):
        return self._baseurl
    @property
    def BSselector_title(self):
        return self._BSselector_title
    @property
    def BSselector_desc(self):
        return self._BSselector_desc
    @property
    def BSselector_price(self):
        return self._BSselector_price
    @property
    def name(self):
        return self._name
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, url):
        self._url = url
    @name.setter
    def name(self, name):
        self._name = name
    @baseurl.setter
    def baseurl(self, baseurl):
        self._baseurl = baseurl
    @BSselector_title.setter
    def BSselector_title(self, BSselector_title):
        self._BSselector_title = BSselector_title
    @BSselector_desc.setter
    def BSselector_desc(self, BSselector_desc):
        self._BSselector_desc = BSselector_desc
    @BSselector_price.setter
    def BSselector_price(self, BSselector_price):
        self._BSselector_price = BSselector_price

def main():
    plist, grocer = getinput()
    logging.debug(f'plist, grocer: {plist} --- {grocer}')
    if grocer == None:
        for word in plist:
            searchcs(word)
            searchfp(word)
    elif grocer[0] =='fp':
        for word in plist:
            searchfp(word)
    elif grocer[0] =='cs':
        for word in plist:
            searchcs(word)
    else:
        raise ValueError

def searchcs(word):
    cs=init_cs()
    cs.url=cs.baseurl+word
    csreq=cs.searchweb()
    if csres:=cs.BS(word,csreq.text):
        cs.tab(csres)
        return True
    else:
        return False

def searchfp(word):
    fp=init_fp()
    fp.url=fp.baseurl+word
    fpreq=fp.searchweb()
    if fpres:=fp.BS(word,fpreq.text):
        fp.tab(fpres)
        return True
    else:
        return False

def getinput():
    parser = argparse.ArgumentParser(description='Input search string to output tabular search result')
    parser.add_argument('-n', type=int, nargs=1, required=True, dest='pdtnos', help='Enter the number of products')
    parser.add_argument(nargs='+', dest='pdt', help='Enter the product name(s). Separate two products by a space. For a product with multiple words, delimit by comma')
    parser.add_argument('-g', nargs=1, dest='grocer',choices=['fp','cs'], help='Option to output result from selected grocer only. Enter either \'fp\' or \'cs\'.',required=False)
    args=parser.parse_args()
    logging.info(f'args.pdtnos, args.prd, args.grocer: {args.pdtnos},{args.pdt}, {args.grocer}')
    if args.pdtnos[0] != len(args.pdt):
        sys.exit('Number of products entered does not match up.')
    else:
        inp=list(map(lambda x:x.replace(',',' '),args.pdt))
        if args.grocer == None:
            logging.debug(f'Return value: {inp}, {args.grocer}')
            return inp,args.grocer
        elif args.grocer[0] =='fp':
            logging.debug(f'Return value: {inp}, {args.grocer}')
            return inp,args.grocer
        elif args.grocer[0] =='cs':
            logging.debug(f'Return value: {inp}, {args.grocer}')
            return inp, args.grocer
        else:
            raise ValueError
def init_fp():
    fp=Grocer(baseurl= 'https://www.fairprice.com.sg/search?query=',
              BSselector_title=("span",{"class":"sc-aa673588-1 iCYFVg","weight":"normal"}),
              BSselector_desc=("span", {"class": "sc-aa673588-1 cIXEsR"}),
              BSselector_price=("span",{"class":"sc-aa673588-1 sc-65bf849-1 kdTuLI cXCGWM"}),
              name='FairPrice')
    return fp

def init_cs():
    cs=Grocer(baseurl= 'https://coldstorage.com.sg/search?q=',
              BSselector_title=("div",{"class":"product_category_name"}),
              BSselector_desc=("div",{"class":"product_desc"}),
              BSselector_price=("div",{"class":"content_price"}),
              name='Cold Storage')
    return cs

def log():
    #logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    logging.disable()

if __name__=="__main__":
    main()
