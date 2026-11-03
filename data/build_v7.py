import json,re
L=json.load(open('lib/lib.json'))
for x in L: x['w']='블루아카이브'
CH={'봇치':['고토 히토리','이지치 니지카','야마다 료','키타 이쿠요','히로이 키쿠리','이지치 세이카','고토 후타리','PA씨'],
    '체인소':['덴지','레제','마키마','파워','포치타','아키','코베니','엔젤 데빌','천사의 악마','빔','폭탄의 악마'],
    '카구야':['카구야','이로하','야치요']}
WN={'봇치':'봇치 더 록','체인소':'체인소 맨','카구야':'초카구야공주'}
def rel(s):
    m=re.search(r'(\d{2})년\s*(\d{1,2})(?:~\d{1,2})?월',s)
    if m: return f"20{m.group(1)}년 {int(m.group(2))}월"
    m=re.search(r'(\d{2})년\s*(\d)분기',s)
    if m: return f"20{m.group(1)}년 {m.group(2)}분기"
    return ''
def ddl(s):
    m=re.search(r'(\d{1,2})월\s*(\d{1,2})일\s*(?:오전\s*)?마감|마감\s*:\s*(\d{1,2})월\s*(\d{1,2})일',s)
    if not m: return ''
    mo,d=(m.group(1),m.group(2)) if m.group(1) else (m.group(3),m.group(4))
    mo=int(mo);y=2026 if mo>=11 else 2027
    return f"{y}-{mo:02d}-{int(d):02d}"
def rk(r):
    m=re.match(r'(\d{4})년 (\d+)월',r)
    if m: return int(m.group(1))*100+int(m.group(2))
    m=re.match(r'(\d{4})년 (\d)분기',r)
    if m: return int(m.group(1))*100+int(m.group(2))*3-2
    return None
def cat(n):
    for k,v in [('피규어|넨도로이드|figma|피그마|스케일|PLAMATEA|리볼텍|프라이즈|POP UP|XStellar|스태츄|스테츄|피그큐브|소프비','피규어'),('봉제|누이|인형|쿠션|쵸코푸니|초코푸니|타피누이|쿠리판','봉제·쿠션'),('캔뱃지|캔 뱃지|뱃지|배지','뱃지'),('티셔츠|자켓|후드|파우치|담요|슬로건|캐리어|안대|수건|타월|매트|태피스트리|우산|가방|의상','의류·잡화')]:
        if re.search(k,n): return v
    return '기타'
for f,shop in [('lib/caA.txt','코믹스아트')]:
    for l in open(f):
        p=l.rstrip('\n').split('|')
        if len(p)<7: continue
        k,no,name,price,relt,s,img=p[:7]
        st={'S':'품절','?':'확인 필요'}.get(s,'판매중')
        if s=='A' and (re.search(r'입고예정|발매\)|잔금결제|마감 : \d',name+relt) or ((lambda r:(r or 0)>202611)(rk(rel(relt))))): st='예약'
        L.append(dict(shop=shop,no=no,t=name.replace('봇치','봇치 더 록',1) if '봇치 더 록' not in name else name,p=price,rel=rel(relt+' '+name),ddl=ddl(relt),st=st,img='https://comics-art.co.kr/web/product/medium/'+img,ch=[c for c in CH[k] if c in name],g='A',url=f'https://comics-art.co.kr/product/detail.html?product_no={no}',c=cat(name),w=WN[k]))
for l in open('lib/apA.txt'):
    p=l.rstrip('\n').split('|')
    if len(p)<6: continue
    no,name,price,relt,s,img=p[:6]
    url=img if img.startswith('http') else 'https://ecimg.cafe24img.com/pg692b46604935022/artplex/web/product/'+img[1:]
    L.append(dict(shop='아트플렉스',no=no,t='봇치 더 록 '+name,p=price,rel=rel(relt),ddl=ddl(relt),st={'R':'예약','A':'판매중','S':'품절'}[s],img=url.replace('%2C',','),ch=[c for c in CH['봇치'] if c in name],g='A',url=f'https://artplex.co.kr/product/detail.html?product_no={no}',c=cat(name),w='봇치 더 록'))

SHOPURL={'아트플렉스':'https://artplex.co.kr/product/detail.html?product_no=%s','코믹스아트':'https://comics-art.co.kr/product/detail.html?product_no=%s','샬레 스토어':'https://bluearchivestore.com/product/detail.html?product_no=%s','굿스마일코리아':'https://brand.naver.com/goodsmilekr/products/%s'}
for l in open('lib/prana.txt'):
    p=l.rstrip('\n').split('|')
    if len(p)<7: continue
    shop,no,name,price,relt,st,img=p[:7]
    d=dict(shop=shop,no=no,t=('블루 아카이브 '+name) if '블루 아카이브' not in name else name,p=price,rel=rel(relt) or relt if relt.startswith('20') else rel(relt),ddl='',st=st,img=img,ch=['프라나'],g='S',url=SHOPURL[shop]%no,c=cat(name),w='블루아카이브')
    if shop=='굿스마일코리아': d['src']='https://x.com/GoodSmile_KR/status/2063825451676790786'
    L.append(d)
# 체인소 맨 → B, 피규어만
for x in L:
    if x.get('w')=='체인소 맨': x['g']='B'
L=[x for x in L if not (x.get('w')=='체인소 맨' and x['c']!='피규어')]
# acrylic exclusion
L=[x for x in L if not re.search('아크릴|acryl|케이스',x['t'],re.I)]
# owned
L=[x for x in L if not (x['shop']=='코믹스아트' and x['no'] in ('126701','171861'))]
# registration ym from img path
for x in L:
    m=re.search(r'/(20\d{4})(\d{2})?/',x['img']) or re.search(r'/(20\d{4})',x['img'])
    x['reg']=m.group(1) if m else ''
    x['pn']=int(x['p'].replace(',','').replace('원','')) if re.match(r'^[\d,]+원$',x['p']) and x['p']!='1원' else None
def rk(r):
    m=re.match(r'(\d{4})년 (\d+)월',r)
    if m: return int(m.group(1))*100+int(m.group(2))
    m=re.match(r'(\d{4})년 (\d)분기',r)
    if m: return int(m.group(1))*100+int(m.group(2))*3-2
    return None
# dedupe key
VER=['빅 40cm','수영복','드레스','바니','메모리얼','파자마','재판','팝 아이돌','아이돌','체육복','라이딩','교복','사복','Live','해외수출용','일본내수용','베이직','돌','보너스','DX','무장','밴드']
def key(x):
    t=x['t']
    line=''
    m=re.search(r'넨도로이드[^\d]*(?:No\.?\s*)?(\d{3,4})',t)
    if m: line='nendo'+m.group(1)
    elif re.search(r'넨도로이드',t): line='nendo'+('doll' if '돌' in t else '')
    m2=re.search(r'(?:figma|피그마)[^\d]*(\d{3})',t,re.I)
    if m2: line='figma'+m2.group(1)
    if not line:
        if re.search(r'1/7',t): line='17'
        elif re.search(r'1/6',t): line='16'
        elif 'POP UP' in t or '팝업' in t: line='pup'
        elif re.search('쵸코푸니|초코푸니',t): line='choco'
        elif 'XStellar' in t: line='xst'
        else: return None
    vers=sorted(v for v in VER if v in t)
    return '|'.join([x['w'],line,','.join(sorted(x['ch'])),','.join(vers)])
groups={}
for i,x in enumerate(L):
    k=key(x)
    groups.setdefault(k if k else f'_{i}',[]).append(x)
PRI={'샬레 스토어':0,'굿스마일코리아':1,'아트플렉스':2,'코믹스아트':3}
out=[]
TODAY='2026-11-03'
for k,g in groups.items():
    # merge deposit duplicates within same shop: keep highest price per shop
    cand=[x for x in g if x['st']!='품절' and not (x['ddl'] and x['ddl']<TODAY)]
    pool=cand or g
    prices=[x['pn'] for x in pool if x['pn']]
    mn=min(prices) if prices else None
    rks=[rk(x['rel']) for x in pool if rk(x['rel'])]
    er=min(rks) if rks else None
    for x in pool:
        ps=(mn/x['pn']) if (mn and x['pn']) else None
        r=rk(x['rel'])
        ds=max(0,1-0.1*((r//100*12+r%100)-(er//100*12+er%100))) if (r and er) else 0.5
        x['_ps'],x['_ds']=ps,ds
    avgp=sum(x['_ps'] for x in pool if x['_ps'] is not None)/max(1,len([1 for x in pool if x['_ps'] is not None])) if any(x['_ps'] is not None for x in pool) else 0.5
    for x in pool:
        if x['_ps'] is None: x['_ps']=avgp
        x['score']=round(0.6*x['_ps']+0.4*x['_ds'],3)
    if not cand: pool=sorted(pool,key=lambda x:x['reg'],reverse=True)[:1]+[]
    best=sorted(pool,key=lambda x:(-x['score'],PRI[x['shop']]))[0]
    others=[dict(shop=o['shop'],p=o['p'],rel=o['rel'],st=o['st'],url=o['url'],score=o.get('score')) for o in g if o is not best]
    b=dict(best); b['alt']=others
    for kk in ['_ps','_ds']: b.pop(kk,None)
    out.append(b)
GO={'S':0,'A':1,'B':2,'':3}
for x in out:
    r=rk(x['rel']); x['rk']=r or 999999
out.sort(key=lambda x:(GO[x['g']],x['rk'],x['shop']))
json.dump(out,open('lib/lib_v7.json','w'),ensure_ascii=False)
from collections import Counter
print(len(L),'->',len(out),Counter(x['w'] for x in out),Counter(x['st'] for x in out),sum(1 for x in out if x['alt']))
