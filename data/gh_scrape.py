"""GitHub Actions용 판매처 수집 — 아트플렉스 공개 카탈로그·코믹스아트·샬레 스토어 → data/raw/ + data/raw/status.json"""
import requests,json,os,sys,time,subprocess,shutil,urllib.parse,datetime
D=os.path.dirname(os.path.abspath(__file__));RAW=os.path.join(D,'raw');os.makedirs(RAW,exist_ok=True)
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36','Accept-Language':'ko-KR,ko;q=0.9'}
ST={'started_utc':datetime.datetime.utcnow().isoformat(timespec='seconds'),'probe':{},'steps':{}}
def save():json.dump(ST,open(os.path.join(RAW,'status.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
# 0) 접속 확인
for u in ['https://storage.googleapis.com/artplex-recommender-public-artplex-automation/catalog-commerce/filter_data_version.json','https://artplex.co.kr/','https://comics-art.co.kr/','https://bluearchivestore.com/']:
    try:r=requests.get(u,headers=H,timeout=30);ST['probe'][u]=[r.status_code,len(r.content)]
    except Exception as e:ST['probe'][u]=['ERR',type(e).__name__+': '+str(e)[:160]]
save()
# 1) 아트플렉스 공개 카탈로그
t=time.time()
try:
    pu='https://storage.googleapis.com/artplex-recommender-public-artplex-automation/catalog-commerce/filter_data_version.json'
    pj=requests.get(pu,headers=H,timeout=60).json();ST['steps']['ap_pointer']=pj
    for key,fn in [('catalog_file','ap_catalog_file.json'),('commerce_file','ap_commerce_file.json'),('catalog_supplement_file','ap_catalog_supplement_file.json')]:
        v=pj.get(key)
        if not v:continue
        u=v if str(v).startswith('http') else urllib.parse.urljoin(pu,str(v))
        r=requests.get(u,headers=H,timeout=120);r.raise_for_status()
        open(os.path.join(RAW,fn),'wb').write(r.content)
    cj=json.load(open(os.path.join(RAW,'ap_catalog_file.json'),encoding='utf-8'))
    ST['steps']['artplex']=dict(ok=True,items=len(cj.get('data',[])),sec=round(time.time()-t))
except Exception as e:ST['steps']['artplex']=dict(ok=False,err=type(e).__name__+': '+str(e)[:200])
save()
# 2) 코믹스아트 검색 + 샬레 스토어 목록
t=time.time()
try:
    p=subprocess.run([sys.executable,os.path.join(D,'scrape_ca_sc.py')],cwd=D,capture_output=True,text=True,timeout=3600)
    for fn in ['ca_raw.json','sc_raw.json']:
        if os.path.exists(os.path.join(D,fn)):shutil.move(os.path.join(D,fn),os.path.join(RAW,fn))
    ca=json.load(open(os.path.join(RAW,'ca_raw.json'),encoding='utf-8'));sc=json.load(open(os.path.join(RAW,'sc_raw.json'),encoding='utf-8'))
    nos=sorted({x['no'] for arr in ca.values() for x in arr if x.get('no') and not x.get('sold')})
    json.dump(nos,open(os.path.join(D,'ca_nos.json'),'w'))
    ST['steps']['ca_sc']=dict(ok=p.returncode==0,ca_items=sum(len(v) for v in ca.values()),ca_unsold=len(nos),sc_items=len(sc),sec=round(time.time()-t),log_tail=p.stdout[-600:]+p.stderr[-600:])
except Exception as e:ST['steps']['ca_sc']=dict(ok=False,err=type(e).__name__+': '+str(e)[:200])
save()
# 3) 코믹스아트 결제 옵션
t=time.time()
try:
    p=subprocess.run([sys.executable,os.path.join(D,'scrape_ca_opts.py')],cwd=D,capture_output=True,text=True,timeout=3600)
    if os.path.exists(os.path.join(D,'ca_opts.json')):shutil.move(os.path.join(D,'ca_opts.json'),os.path.join(RAW,'ca_opts.json'))
    ST['steps']['ca_opts']=dict(ok=p.returncode==0,sec=round(time.time()-t),log_tail=p.stdout[-300:]+p.stderr[-600:])
except Exception as e:ST['steps']['ca_opts']=dict(ok=False,err=type(e).__name__+': '+str(e)[:200])
ST['finished_utc']=datetime.datetime.utcnow().isoformat(timespec='seconds');save()
