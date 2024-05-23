import project, requests
import pytest

def test_init_fp():
    assert type(project.init_fp()) == eval("project.Grocer")

def test_init_cs():
    assert type(project.init_cs()) == eval("project.Grocer")

def test_searchweb():
    test=project.Grocer(baseurl= 'https://cs50.harvard.edu/python/2022/project/',
            BSselector_title=[],
            BSselector_desc=[],
            BSselector_price=[],
        name='Test')
    test.url=test.baseurl
    assert type(test.searchweb()) == eval("requests.models.Response")

def test_BS():
    fp=project.init_fp()
    text=fp.readtext('html')
    assert len(fp.BS('egg',text)) == 20
    cs=project.init_cs()
    cstext=cs.readtext('CShtml')
    assert len(cs.BS('egg',cstext)) == 20

def test_tab():
    fp=project.init_fp()
    empty=[]
    pos=(('egg','desc','$1'),('egg2','desc2','$2'))
    assert fp.tab(empty) == False
    assert fp.tab(pos) == True
def test_regex():
    fp=project.init_fp()
    string=['<span class="sc-aa673588-1 cIXEsR" color="#666666"><span class="sc-d5ac8310-0 zwfvf" data-testid="dietary-attributes-separator">•</span>Halal</span>']
    string2=['<span class="sc-aa673588-1 cIXEsR" color="#666666">30 per pack</span>','<span class="sc-aa673588-1 cIXEsR" color="#666666"><span class="sc-d5ac8310-0 zwfvf" data-testid="dietary-attributes-separator">•</span>Halal</span>']
    assert fp.regex(string) == []
    assert len(fp.regex(string2)) == 1

def main():
    test_init_fp()
    test_init_cs()
    test_searchweb()
    test_BS()
    test_tab()
    test_regex()

if __name__ == "__main__":
    main()

