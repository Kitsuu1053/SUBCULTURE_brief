import requests,os,json,re,time,urllib.parse
from bs4 import BeautifulSoup as B
D=os.path.dirname(os.path.abspath(__file__))
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36','Accept-Language':'ko-KR,ko;q=0.9'}
S=requests.Session();S.headers.update(H)
def items(html,base):
    s=B(html,'html.parser');out=[]
    for li in s.select('ul.prdList > li'):
        no=re.sub(r'\D','',li.get('id') or '')
        if not no:
            a=li.select_one('a[href*="product_no="]');m=re.search(r'product_no=(\d+)',a['href']) if a else None;no=m.group(1) if m else ''
        nm=li.select_one('.name');name=nm.get_text(' ',strip=True).replace('상품명 :','').strip() if nm else ''
        alts=[i.get('alt') or '' for i in li.select('img')]
        img=''
        for i in li.select('img'):
            src=i.get('ec-data-src') or i.get('src') or ''
            if '/web/product/' in src:img=src;break
        txt=li.get_text(' ',strip=True)
        out.append(dict(no=no,name=name,img=img,sold=any('품절' in a for a in alts),txt=txt[:600]))
    return out,s
R={}
KW=['블루 아카이브','봇치 더 록','초 카구야','체인소 맨','체인소맨','어둠의 실력자','무직전생','리제로','Re:제로','이 멋진 세계에 축복','코노스바','노 게임 노 라이프','청춘 돼지','유녀전기','역시 내 청춘','시원찮은 그녀','사쿠라장','에로망가','내 여동생이 이렇게','비스크 돌','비스크돌','던전에서 만남','향기로운 꽃','카오루하나','중2병','U149']
for k in KW:
    allit=[];p=1
    while p<=40:
        u='https://comics-art.co.kr/product/search.html?keyword='+urllib.parse.quote_plus(k)+'&page=%d'%p
        try:r=S.get(u,timeout=40)
        except Exception as e:print('ERR',k,p,e);break
        it,s=items(r.text,'ca')
        if not it:break
        new=[x for x in it if x['no'] not in {y['no'] for y in allit}]
        if not new:break
        allit+=new;p+=1;time.sleep(0.4)
    R[k]=allit;print('ca',k,len(allit),'pages',p-1,flush=True)
json.dump(R,open(os.path.join(D,'ca_raw.json'),'w',encoding='utf-8'),ensure_ascii=False)
SC=[];p=1
while p<=30:
    r=S.get('https://bluearchivestore.com/product/list.html?cate_no=95&page=%d'%p,timeout=40)
    it,s=items(r.text,'sc')
    new=[x for x in it if x['no'] not in {y['no'] for y in SC}]
    if not new:break
    SC+=new;p+=1;time.sleep(0.4)
print('sc',len(SC))
json.dump(SC,open(os.path.join(D,'sc_raw.json'),'w',encoding='utf-8'),ensure_ascii=False)
