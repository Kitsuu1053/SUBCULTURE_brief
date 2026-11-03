# 정기 조사 절차 (1·11·21일 21:00 KST)

1. 메모리 `/areas/subculture.md`, `/topics/blue-archive.md`, `/preferences.md` 읽기 — 이 문서와 다르면 메모리 우선
2. 이 저장소 최신본 받기 → `index.html`이 작업 기준
3. 조사 (`RULES.md` 기준)
   - 탭1·탭2: 일본·한국 발매/행사/쿠지/애니 소식
   - 탭3: 샬레 스토어·아트플렉스·코믹스아트·굿스마일코리아(X 공지) 전수 조회 → `data/build_v9.py`로 같은 제품 비교
     - 아트플렉스: 검색 화면은 판매중만 보이므로 공개 상품 목록 파일 사용 — `https://storage.googleapis.com/artplex-recommender-public-artplex-automation/catalog-commerce/filter_data_version.json` 의 catalog_file·commerce_file (품절·예약·출하 예정 포함)
     - 코믹스아트·샬레 스토어: `data/scrape_ca_sc.py` (작품별 검색 / 전체 목록)
     - 작업 공간은 판매처에 접속할 수 없으므로 Chrome 또는 Kitsuu님 PC의 Python으로 실행
   - 수집 범위: 블루아카이브는 S·A·B 캐릭터 전 굿즈(C 제외), A 작품은 전 굿즈, B 작품은 피규어만, 아크릴·중고/개봉품 제외, 품절은 최근 12개월 등록분
   - 탭4: 보유품 정가·판매 상태 재확인, 하나은행 매매기준율(100엔당) 갱신
4. 이전 조사(`data/lib_v*.json` 최신본)와 비교 → 「변경」「재입고」 표시
5. `index.html` 갱신, 상단 「최근 업데이트」 날짜 변경
6. 브라우저 시험(탭 4개 표시·JS 오류 없음·이미지/로고)
7. 커밋·푸시 → Pages 반영 확인
8. PC 연결 시 `E:\Anthropic Claude Cowork\_Downloads\subculture_briefing\index.html` 에도 저장
9. SendUserMessage로 카테고리별 보고(출처 URL 포함)
