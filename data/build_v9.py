"""탭3 v9 빌드: 아트플렉스 공개 카탈로그(catalog+commerce), 코믹스아트 검색, 샬레 스토어 전체 목록, 굿스마일코리아(기존 X 공지 행) → 같은 제품 정리 → lib_v9.json
사용: python3 build_v9.py <raw_dir> <prev_lib.json> <out.json>"""
import json,re,sys,time,collections,os
RAW,PREV,OUT=sys.argv[1:4]
NOW=time.time();TODAY='2026-11-03';TODAY_RK=202611;REG_MIN='202511'
S_=['토키','프라나'];A_=['리오','키사키','세이아','히나','쿠루미']
B_=['세리카','이부키','이로하','카즈사','나츠','이치카','사쿠라코','마리','미카','유즈','케이','유우카','나구사','슈에린','노조미','히카리','미야코','와카모']
GR={**{c:'S' for c in S_},**{c:'A' for c in A_},**{c:'B' for c in B_}}
CHRE={'토키':r'토키','프라나':r'프라나|플라나','리오':r'(?<![나시])리오','키사키':r'키사키','세이아':r'세이아','히나':r'히나(?!타)','쿠루미':r'쿠루미(?!\s?타피)',
 '세리카':r'세리카','이부키':r'이부키','이로하':r'이로하','카즈사':r'카즈사','나츠':r'나츠(?!메|키)','이치카':r'이치카','사쿠라코':r'사쿠라코','마리':r'(?<![아])마리(?![나오아모])','미카':r'(?<![오사])미카(?![모엘사도])',
 '유즈':r'유즈(?!키|루)','케이':r'(?<![이])케이(?![스크블지팝트오])','유우카':r'유우카','나구사':r'나구사','슈에린':r'슈에린','노조미':r'노조미','히카리':r'히카리','미야코':r'미야코','와카모':r'와카모'}
GROUP={r'FOX\s?소대|SRT':['쿠루미'],r'C&C|Cleaning\s?&\s?Clearing|클리닝':['토키'],r'세미나':['유우카'],r'티파티':['세이아','미카'],r'선도부|풍기\s?위원회':['히나'],
 r'만마전|판데모니움':['이부키','이로하'],r'게임\s?개발부':['유즈'],r'방과후\s?디저트부':['카즈사','나츠'],r'하이랜더':['히카리','노조미'],r'현룡문':['키사키'],r'시스터후드':['사쿠라코','마리'],r'정의\s?실현부':['이치카'],r'RABBIT\s?소대':['미야코']}
GRP_ONLY=set()
def chars(t,extra=()):
    s=set(c for c,p in CHRE.items() if re.search(p,t))
    for e in extra:
        if e in GR:s.add(e)
    other=[n for n in BANAMES if n not in GR and n not in GRP_ONLY and len(n)>=2 and n in t] or [e for e in extra if e not in GR and e not in GRP_ONLY and e!='미분류']
    if not s and not other:
        for g,cs in GROUP.items():
            if re.search(g,t,re.I) or any(re.search(g,e,re.I) for e in extra):s|=set(cs)
    return sorted(s,key=lambda c:(['S','A','B'].index(GR[c]),list(GR).index(c)))
def grade(ch):
    gs=[GR[c] for c in ch if c in GR];return min(gs,key=['S','A','B'].index) if gs else ''
def cat(n,pt=''):
    s=n+' '+(pt or '')
    for k,v in [('피규어|넨도로이드|figma|피그마|스케일|룩업|Look Up|Trio-Try-iT|누들 스토퍼|Desktop Cute|Vivit|Aqua Float|쵸코노세|PLAMATEA|리볼텍|프라이즈|POP UP|XStellar|스태츄|스테츄|피그큐브|소프비|Coreful|Luminasta|AMP|그란디스타|맥시매틱','피규어'),('봉제|누이|인형|쿠션|쵸코푸니|초코푸니|타피누이|쿠리판|다키마쿠라','봉제·쿠션'),('캔뱃지|캔 뱃지|뱃지|배지','뱃지'),('티셔츠|자켓|후드|파우치|담요|슬로건|캐리어|안대|수건|타월|매트|태피스트리|우산|가방|의상|의류|장패드','의류·잡화')]:
        if re.search(k,s):return v
    return '기타'
ACR=re.compile(r'아크릴|acryl|케이스',re.I)
CANB=re.compile(r'캔\s?뱃지|캔\s?배지|양철\s?뱃지|틴\s?뱃지')
METAL=re.compile(r'메탈|금속')
def rel(s):
    m=re.search(r'(\d{2})년\s*(\d{1,2})(?:\s*~\s*\d{1,2})?\s*월',s)
    if m:return f"20{m.group(1)}년 {int(m.group(2))}월"
    m=re.search(r'(\d{2})년\s*(\d)\s*분기',s)
    if m:return f"20{m.group(1)}년 {m.group(2)}분기"
    m=re.search(r'발매\s*:\s*(\d{2})년\s*(\d{1,2})월',s)
    if m:return f"20{m.group(1)}년 {int(m.group(2))}월"
    return ''
def rk(r):
    m=re.match(r'(\d{4})년 (\d+)월',r or '')
    if m:return int(m.group(1))*100+int(m.group(2))
    m=re.match(r'(\d{4})년 (\d)분기',r or '')
    if m:return int(m.group(1))*100+int(m.group(2))*3-2
    return None
def ddl(s):
    m=re.search(r'(\d{1,2})월\s*(\d{1,2})일\s*(?:오전\s*|오후\s*)?(?:\d{1,2}시\s*)?마감|마감(?:일)?\s*:\s*(\d{1,2})월\s*(\d{1,2})일',s)
    if not m:return ''
    mo,d=(m.group(1),m.group(2)) if m.group(1) else (m.group(3),m.group(4));mo=int(mo);y=2026 if mo>=11 else 2027
    return f"{y}-{mo:02d}-{int(d):02d}"
def pn(p):
    try:v=int(str(p).replace(',','').replace('원',''));return v if v>1 else None
    except:return None
WORKS={'봇치 더 록':('A',r'봇치','all'),'초카구야공주':('A',r'초\s?카구야','all'),'체인소 맨':('B',r'체인소\s?맨|체인소맨','fig'),
 '어둠의 실력자가 되고 싶어서':('B',r'실력자','fig'),'무직전생':('B',r'무직전생','fig'),'Re:제로':('B',r'(?<!쓰)리제로|Re\s?:?\s?제로부터|Re 제로','fig'),
 '이 멋진 세계에 축복을!':('B',r'멋진 세계에 축복|코노스바','fig'),'노 게임 노 라이프':('B',r'노 ?게임 ?노 ?라이프','fig'),'청춘 돼지':('B',r'청춘 ?돼지','fig'),
 '유녀전기':('B',r'유녀전기','fig'),'역내청':('B',r'내 청춘 러브코메디|역내청','fig'),'시원찮은 그녀를 위한 육성방법':('B',r'시원찮은 그녀','fig'),
 '사쿠라장의 애완그녀':('B',r'사쿠라장','fig'),'에로망가 선생':('B',r'에로망가','fig'),'내 여동생이 이렇게 귀여울 리가 없어':('B',r'내 여동생이 이렇게','fig'),
 '그 비스크돌은 사랑을 한다':('B',r'비스크\s?돌','fig'),'던전에서 만남을 추구하면 안 되는 걸까':('B',r'던전에서 만남','fig'),'향기로운 꽃은 늠름하게 핀다':('B',r'향기로운 꽃','fig'),
 '중2병이라도 사랑이 하고 싶어!':('B',r'중2병이라도','fig'),'은혼':('B',r'은혼','fig'),'하이큐!!':('B',r'하이큐','fig'),'아이돌마스터 U149':('B',r'U149','fig')}
BOC=['고토 히토리','이지치 니지카','야마다 료','키타 이쿠요','히로이 키쿠리','이지치 세이카','고토 후타리','PA씨'];KAG=['카구야','이로하','야치요']
def wch(w,t):
    t=re.sub(r'초\s?카구야\s?(?:공주|히메)!?','',t)
    if w=='봇치 더 록':return [c for c in BOC if c in t or c.split()[-1] in t]
    if w=='초카구야공주':return [c for c in KAG if c in t]
    return []
L=[]
USED=re.compile(r'\[\d{8}-\d{3}\]|\[개봉\]|중고|잔금\s?결제|예약금|1차\s?결제')
def add(**d):
    if ACR.search(d['t']) or USED.search(d['t']):return
    if CANB.search(d['t']) and not METAL.search(d['t']):return
    d['pn']=pn(d['p']);d.setdefault('ddl','');d.setdefault('alt',[]);L.append(d)
# --- 아트플렉스
cj=json.load(open(os.path.join(RAW,'ap_catalog_file.json'),encoding='utf-8'));CS=cj['schema']
BANAMES=set();_gw=re.compile('|'.join(GROUP),re.I)
for r in cj['data']:
    if r[5]=='블루 아카이브':
        for c in (r[6] or []):
            (GRP_ONLY.add(c) if (_gw.search(c) or c in('밀레니엄','트리니티','게헨나','아비도스','백귀야행','산해경','발키리','레드윈터','흥신소','미분류','페로로','아리우스','SRT','샬레')) else BANAMES.add(c))
cm=json.load(open(os.path.join(RAW,'ap_commerce_file.json'),encoding='utf-8'))['products']
for r in cj['data']:
    d=dict(zip(CS,r));d.update(cm.get(str(d['id']),{}))
    nm=d['name'];ip=d['ip_name'] or '';pt=d['product_type'] or ''
    if '아크릴' in pt or '케이스' in pt:continue
    reg=time.strftime('%Y%m',time.gmtime(d['created_ts'])) if d.get('created_ts') else ''
    sold=d['availability']=='soldout'
    if sold and reg<REG_MIN:continue
    st='품절' if sold else ('예약' if d.get('is_preorder') else '판매중')
    desc=(d.get('shipping_date') or '')+' '+(d.get('simple_desc') or '')
    base=dict(shop='아트플렉스',no=str(d['id']),p=f"{d['price']:,}원" if d.get('price') else '',rel=rel(desc) or rel(nm),ddl=ddl(desc),st=st,img=d['image'],url=f"https://artplex.co.kr/product/detail.html?product_no={d['id']}",reg=reg)
    if ip=='블루 아카이브':
        ch=chars(nm,d.get('character') or []);g=grade(ch)
        if not g:continue
        add(t=('블루 아카이브 '+nm) if '블루 아카이브' not in nm else nm,w='블루아카이브',ch=ch,g=g,c=cat(nm,pt),**base)
    else:
        for w,(g,p,mode) in WORKS.items():
            if re.search(p,nm) or (w=='봇치 더 록' and ip=='봇치 더 록') or (w=='은혼' and ip=='은혼') or (w=='체인소 맨' and ip=='체인소 맨'):
                c=cat(nm,pt)
                if mode=='fig' and c!='피규어':break
                add(t=nm,w=w,ch=wch(w,nm),g=g,c=c,**base);break
# --- 코믹스아트
R=json.load(open(os.path.join(RAW,'ca_raw.json'),encoding='utf-8'));seen=set()
OPT=json.load(open(os.path.join(RAW,'ca_opts.json'),encoding='utf-8')) if os.path.exists(os.path.join(RAW,'ca_opts.json')) else {}
def ca_st(x):
    if x['sold']:return '품절'
    s=x['name']+' '+x['txt']
    r=rk(rel(s))
    if re.search(r'입고예정|잔금결제|예약|마감일?\s*:',s) or (r and r>TODAY_RK):return '예약'
    return '판매중'
def ca_base(x):
    img=x['img'];img=('https:'+img) if img.startswith('//') else img
    m=re.search(r'/(20\d{4})/',img);reg=m.group(1) if m else ''
    pm=re.search(r'판매가\s*:\s*([\d,]+원)',x['txt']);p=pm.group(1) if pm else ''
    o=OPT.get(x['no']) or {}
    split=bool(o.get('first'))
    if o.get('full'):p=f"{o['full']:,}원"
    elif split:p=''  # 1차결제만 확인되고 전체결제 금액을 못 읽으면 가격 미표기
    return dict(shop='코믹스아트',no=x['no'],p=p,split=split,rel=rel(x['name']+' '+x['txt']),ddl=ddl(x['txt']),st=ca_st(x),img=img,url=f"https://comics-art.co.kr/product/detail.html?product_no={x['no']}",reg=reg)
for k,arr in R.items():
    for x in arr:
        if x['no'] in seen:continue
        b=ca_base(x)
        if b['st']=='품절' and b['reg']<REG_MIN:continue
        nm=x['name']
        if '블루 아카이브' in nm or '블루아카이브' in nm:
            ch=chars(nm);g=grade(ch)
            if not g:continue
            seen.add(x['no']);add(t=nm,w='블루아카이브',ch=ch,g=g,c=cat(nm),**b);continue
        for w,(g,p,mode) in WORKS.items():
            if re.search(p,nm):
                c=cat(nm)
                if mode=='fig' and c!='피규어':break
                seen.add(x['no']);add(t=nm,w=w,ch=wch(w,nm),g=g,c=c,**b);break
# --- 샬레 스토어
for x in json.load(open(os.path.join(RAW,'sc_raw.json'),encoding='utf-8')):
    nm=x['name'];img=x['img'];img=('https:'+img) if img.startswith('//') else img
    m=re.search(r'/(20\d{4})/',img);reg=m.group(1) if m else ''
    if x['sold'] and reg<REG_MIN:continue
    ch=chars(nm);g=grade(ch)
    if not g:continue
    pm=re.search(r'판매가\s*:\s*([\d,]+원)',x['txt'])
    st='품절' if x['sold'] else ('예약' if '예약' in nm else '판매중')
    add(t='블루 아카이브 '+re.sub(r'^\[[^\]]*\]\s*','',nm),w='블루아카이브',ch=ch,g=g,c=cat(nm),shop='샬레 스토어',no=x['no'],p=pm.group(1) if pm else '',rel=rel(nm),ddl=ddl(x['txt']),st=st,img=img,url=f"https://bluearchivestore.com/product/detail.html?product_no={x['no']}",reg=reg)
# --- 굿스마일코리아(기존 X 공지 행 유지)
PV=json.load(open(PREV,encoding='utf-8'))
for x in PV:
    if x['shop']=='굿스마일코리아':
        y={k:v for k,v in x.items() if k not in('alt','score','note','rk')};y['alt']=[];L.append(y)
print('listings',len(L),collections.Counter((x['shop'],x['w']=='블루아카이브') for x in L),file=sys.stderr)
# --- 같은 제품 정리
TAG=r'\((?:해외수출용|일본내수용|재판|당일발송|입고중|예약분 입고중|추가분 입고중|입고완료|한국총판|공식 파트너샵|중국 공식|\d+월 \d주차 입고예정|\d+년 \d+(?:월|분기) 발매|\d+개입 1(?:박스|BOX)|랜덤 단품|G\.S\.C|[A-Za-z .]+)\)'
def unit(t):
    m=re.search(r'\((\d+)개입 1(?:박스|BOX)\)',t);return ('박스 %s개입'%m.group(1)) if m else ('랜덤 단품' if '랜덤 단품' in t else '')
def dist(t):return ' · '.join(w for w in ['해외수출용','일본내수용','재판'] if w in t)
VER=['빅 40cm','수영복','드레스','바니','메모리얼','파자마','팝 아이돌','아이돌','체육복','라이딩','교복','사복','Live','베이직','돌','보너스','DX','무장','밴드','A버전','B버전','(A)','(B)']
def key7(x):
    t=x['t'];line=''
    m=re.search(r'넨도로이드[^\d]*(?:No\.?\s*)?(\d{3,4})',t)
    if m:line='nendo'+m.group(1)
    m2=re.search(r'(?:figma|피그마)[^\d]*(\d{3})',t,re.I)
    if m2:line='figma'+m2.group(1)
    if not line:
        if re.search(r'1/7',t):line='17'
        elif re.search(r'1/6',t):line='16'
        elif re.search(r'1/4',t):line='14'
        elif 'POP UP' in t:line='pup'
        elif re.search('쵸코푸니|초코푸니',t):line='choco'+('40' if '40cm' in t else '')
        else:return None
    if not x['ch']:return None
    return '|'.join([x['w'],line,','.join(sorted(x['ch'])),','.join(sorted(v for v in VER if v in t))])
def key8(x):
    t=re.sub(TAG,'',x['t']);t=re.sub(r'\(G\.S\.C\)|\(Max Factory\)|\(FURYU\)|\(SEGA\)','',t)
    t=re.sub(r'블루\s?아카이브|굿즈|피규어|스케일|중국 공식|공식|BA|◈[^◈]*◈','',t);t=re.sub(r'굿스마일\s?컴퍼니|굿스마일컴퍼니','GSC',t)
    return x['w']+'|'+re.sub(r'\s+','',t)
# union-find over key7 / key8
par=list(range(len(L)))
def f(i):
    while par[i]!=i:par[i]=par[par[i]];i=par[i]
    return i
for kf in (key7,key8):
    first={}
    for i,x in enumerate(L):
        k=kf(x)
        if not k:continue
        if k in first:par[f(i)]=f(first[k])
        else:first[k]=i
G=collections.defaultdict(list)
for i,x in enumerate(L):G[f(i)].append(x)
PRI={'샬레 스토어':0,'굿스마일코리아':1,'아트플렉스':2,'코믹스아트':3}
out=[]
for g in G.values():
    # 코믹스아트 1차결제(예약금) 페이지 제거: 같은 제품의 코믹스아트 최고가 30% 미만 가격 행
    mc=max([x['pn'] for x in g if x['shop']=='코믹스아트' and x['pn']] or [0])
    g=[x for x in g if not (x['shop']=='코믹스아트' and x['pn'] and mc and x['pn']<0.3*mc)] or g
    ok=[x for x in g if x['st']!='품절' and not (x['ddl'] and x['ddl']<TODAY)] or g
    single=[x for x in ok if not unit(x['t']).startswith('박스')] or ok
    prices=[x['pn'] for x in single if x['pn']];mn=min(prices) if prices else None
    rks=[rk(x['rel']) for x in single if rk(x['rel'])];er=min(rks) if rks else None
    def sc(x):
        p=(mn/x['pn']) if (mn and x['pn']) else .5;r=rk(x['rel'])
        d=max(0,1-0.1*((r//100*12+r%100)-(er//100*12+er%100))) if (r and er) else .5
        return round(.6*p+.4*d,3)
    rep=dict(sorted(single,key=lambda x:(-sc(x),bool(x.get('split')),PRI[x['shop']]))[0]);rep['score']=sc(rep)
    if any(x.get('split') for x in g if x['shop']==rep['shop']):rep['split']=True
    rep['alt']=[dict(shop=x['shop'],p=x['p'],rel=x['rel'],st=x['st'],url=x['url'],score=sc(x),note=' · '.join(v for v in [unit(x['t']),dist(x['t'])] if v)) for x in g if x is not None and not (x['shop']==rep['shop'] and x['no']==rep['no'])]
    rep['note']=' · '.join(v for v in [unit(rep['t']),dist(rep['t'])] if v)
    rep['rk']=rk(rep['rel']) or 999999
    out.append(rep)
# --- 이전 회차와 비교: 판매처 변경·재입고
pv={}
for x in PV:
    pv[(x['shop'],x['no'])]=x
    for a in x.get('alt') or []:
        m=re.search(r'product_no=(\d+)',a.get('url',''))
        if m:pv.setdefault((a['shop'],m.group(1)),dict(st=a['st'],shop=x['shop'],no=x['no']))
for x in out:
    keys=[(x['shop'],x['no'])]+[(a['shop'],(re.search(r'product_no=(\d+)',a['url']) or [None,''])[1]) for a in x['alt']]
    old=[pv[k] for k in keys if k in pv]
    if old:
        o=pv.get((x['shop'],x['no']))
        if o and o.get('st')=='품절' and x['st'] in('판매중','예약'):x['flag']='재입고'
        prevrep=[k for k in keys if k in pv and 't' in pv[k]]
        if prevrep and prevrep[0]!=(x['shop'],x['no']):x['flag']=x.get('flag') or '변경'
    else:x['new']=True
out.sort(key=lambda x:(-(x['rk'] if x['rk']<999999 else 0),x['shop']))
json.dump(out,open(OUT,'w',encoding='utf-8'),ensure_ascii=False)
c=collections.Counter
print('out',len(out),c(x['w'] for x in out).most_common(),c(x['st'] for x in out),c(x['g'] for x in out),c(x['shop'] for x in out),'merged',sum(1 for x in out if x['alt']),'flags',c(x.get('flag') for x in out),'new',sum(1 for x in out if x.get('new')),file=sys.stderr)
