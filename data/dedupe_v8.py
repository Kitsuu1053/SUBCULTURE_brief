"""탭3 중복 정리 v8: 제조사+라인+번호+캐릭터+버전 기준. 유통 구분(해외수출용/일본내수용)·재판·박스/단품은 같은 제품으로 합침.
대표 선택: 단품 우선, 그 안에서 가격 0.6·발매일 0.4 점수(품절·마감 지난 것 제외). 나머지는 alt(다른 판매처·구성)."""
import json,re,sys
TODAY=202611
L=json.load(open(sys.argv[1]))
TAG=r'\((?:해외수출용|일본내수용|재판|당일발송|입고중|예약분 입고중|추가분 입고중|입고완료|한국총판|공식 파트너샵|중국 공식|\d+월 \d주차 입고예정|\d+년 \d+(?:월|분기) 발매|\d+개입 1(?:박스|BOX)|랜덤 단품|G\.S\.C|[A-Za-z .]+)\)'
def unit(t):
    m=re.search(r'\((\d+)개입 1(?:박스|BOX)\)',t)
    return ('박스 %s개입'%m.group(1)) if m else ('랜덤 단품' if '랜덤 단품' in t else '')
def dist(t):
    a=[w for w in ['해외수출용','일본내수용','재판'] if w in t];return ' · '.join(a)
def key(x):
    t=x['t']
    t=re.sub(TAG,'',t)
    t=re.sub(r'\(G\.S\.C\)|\(Max Factory\)|\(FURYU\)|\(SEGA\)','',t)
    t=re.sub(r'블루\s?아카이브|굿즈|피규어|스케일|중국 공식|공식|BA','',t)
    t=re.sub(r'굿스마일\s?컴퍼니|굿스마일컴퍼니','GSC',t)
    t=re.sub(r'\s+','',t)
    return x['w']+'|'+t
G={}
for x in L:G.setdefault(key(x),[]).append(x)
out=[];merged=0
def ps(x):return x.get('pn')
for k,g in G.items():
    if len(g)==1:out.append(g[0]);continue
    merged+=len(g)-1
    ok=[x for x in g if x['st']!='품절']or g
    single=[x for x in ok if not unit(x['t']).startswith('박스')]or ok
    pmin=min([ps(x) for x in single if ps(x)]or[1])
    rks=[x['rk'] for x in single if x['rk']<999999];er=min(rks) if rks else None
    def sc(x):
        p=pmin/ps(x) if ps(x) else .5
        d=1-0.1*((x['rk']//100*12+x['rk']%100)-(er//100*12+er%100)) if (er and x['rk']<999999) else .5
        return round(.6*p+.4*max(d,0),3)
    rep=max(single,key=sc);rep=dict(rep);rep['score']=sc(rep)
    alts=list(rep.get('alt') or [])
    for x in g:
        if x['no']==rep['no'] and x['shop']==rep['shop']:continue
        note=' · '.join(v for v in [unit(x['t']),dist(x['t'])] if v)
        alts.append({'shop':x['shop'],'p':x['p'],'rel':x['rel'],'st':x['st'],'url':x['url'],'score':sc(x),'note':note})
        alts+=x.get('alt') or []
    rep['alt']=alts
    rep['note']=' · '.join(v for v in [unit(rep['t']),dist(rep['t'])] if v)
    out.append(rep)
print('groups merged:',sum(1 for g in G.values() if len(g)>1),'tiles removed:',merged,'→',len(out),file=sys.stderr)
for g in G.values():
    if len(g)>1:print('  ',[ (x['no'],x['p']) for x in g],'→',[x for x in out if x['no'] in [y['no'] for y in g]][0]['no'],file=sys.stderr)
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
