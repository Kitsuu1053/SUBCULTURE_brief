"""코믹스아트 상세 페이지 결제방법 옵션(1차결제/전체결제) 수집 → ca_opts.json {no:{base,full,first,has_first}}"""
import requests,re,os,json,time,sys
from concurrent.futures import ThreadPoolExecutor
D=os.path.dirname(os.path.abspath(__file__))
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130'}
nos=json.load(open(os.path.join(D,'ca_nos.json')))
S=requests.Session();S.headers.update(H)
def one(n):
    for t in range(3):
        try:
            h=S.get('https://comics-art.co.kr/product/detail.html?product_no='+n,timeout=30).text;break
        except Exception:time.sleep(2)
    else:return n,None
    base=re.search(r"product_price\s*=\s*'?([\d.]+)",h);base=int(float(base.group(1))) if base else None
    m=re.search(r"option_stock_data\s*=\s*'(.*?)';",h);full=first=None
    if m:
        try:d=json.loads(json.loads('"'+m.group(1)+'"'))
        except Exception:d={}
        if not isinstance(d,dict):d={}
        for v in d.values():
            if not isinstance(v,dict):continue
            nm=str(v.get('option_name',''));val=str(v.get('option_value',''))
            if '결제' in nm:
                if '전체' in val:full=int(float(v.get('option_price') or 0))
                elif '1차' in val:first=int(float(v.get('option_price') or 0))
    return n,dict(base=base,full=full,first=first)
out={}
with ThreadPoolExecutor(4) as ex:
    for i,(n,r) in enumerate(ex.map(one,nos)):
        out[n]=r
        if i%200==0:print(i,flush=True)
json.dump(out,open(os.path.join(D,'ca_opts.json'),'w'),ensure_ascii=False)
print('done',len(out),sum(1 for v in out.values() if v and v['first']))
