import requests,os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'raw')
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36','Accept-Language':'ko-KR,ko;q=0.9','Accept':'text/html,application/xhtml+xml'}
for n,u in [('home','https://comics-art.co.kr/'),('search','https://comics-art.co.kr/product/search.html?keyword=%EB%B4%87%EC%B9%98&page=1'),('m','https://m.comics-art.co.kr/')]:
    try:
        r=requests.get(u,headers=H,timeout=30);open(os.path.join(D,f'probe_ca_{n}.html'),'w',encoding='utf-8').write(f'<!-- {r.status_code} {r.url} {dict(r.headers)} -->\n'+r.text[:20000])
    except Exception as e:open(os.path.join(D,f'probe_ca_{n}.html'),'w').write('ERR '+repr(e))
