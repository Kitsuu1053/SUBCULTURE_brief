# 정기 조사 절차 (1·11·21일 20:00 KST 시작 · 21:00 KST 알림)

0. `TZ=Asia/Seoul date` 로 조사 시작 시각 기록 (KST)

0. 시작 즉시 Kitsuu님께 「조사 시작」 메시지. 이후 각 단계 시작 때 `data/run_log.txt`에 「YYYY-MM-DD HH:MM KST 단계명」 한 줄을 추가해 커밋·푸시(실패 위치 추적용)
1. 메모리 `/areas/subculture.md`, `/topics/blue-archive.md`, `/preferences.md` 읽기 — 이 문서와 다르면 메모리 우선
2. 이 저장소 최신본 받기 → `index.html`이 작업 기준
3. 조사 (`RULES.md` 기준)
   - 탭1·탭2: 일본·한국 발매/행사/쿠지/애니 소식
   - 탭3: 샬레 스토어·아트플렉스·코믹스아트·굿스마일코리아(X 공지) 전수 조회 → `data/build_v9.py`로 같은 제품 비교
     - 아트플렉스: 검색 화면은 판매중만 보이므로 공개 상품 목록 파일 사용 — `https://storage.googleapis.com/artplex-recommender-public-artplex-automation/catalog-commerce/filter_data_version.json` 의 catalog_file·commerce_file (품절·예약·출하 예정 포함)
     - 코믹스아트·샬레 스토어: `data/scrape_ca_sc.py` (작품별 검색 / 전체 목록), 코믹스아트 결제 옵션: `data/scrape_ca_opts.py` (판매중·예약 상품 상세 페이지 → 전체결제 금액)
     - 수집 자료는 `data/raw/` — 조사 시작 직후 `data/raw/RUN` 내용을 현재 시각으로 바꿔 푸시하면 GitHub Actions(`.github/workflows/scrape.yml`)가 1분 안팎으로 수집해 올림. `git pull` 후 `data/raw/status.json`의 started_utc가 RUN 푸시 이후인지 확인(최대 15분 대기, 실패 시 이전 자료로 진행·보고). 시간 예약 수집은 GitHub 지연(11/11 7시간 반)으로 없앰
       - 아트플렉스(공개 카탈로그, gzip 보관)·샬레 스토어: GitHub에서 수집됨
       - 코믹스아트: GitHub 서버 접속은 Cafe24 보안 확인(Cloudflare Turnstile)으로 막힘 → 우회하지 않음. Kitsuu님 PC가 연결돼 있으면 PC Python으로 scrape_ca_sc.py·scrape_ca_opts.py 실행 후 ca_raw.json·ca_opts.json을 `data/raw/`에 올림. PC가 없으면 `data/raw/`의 이전 코믹스아트 자료를 그대로 쓰고, 보고에 「코믹스아트 자료 YYYY-MM-DD 기준(미갱신)」이라고 적음
       - 빌드: `python3 -I data/build_v9.py data/raw data/lib_(이전).json data/lib_(새).json`
       - 수동 재수집: `data/raw/RUN` 파일 내용을 바꿔 푸시하면 수집 작업이 다시 돎
   - 수집 범위: 블루아카이브는 S·A·B 캐릭터 전 굿즈(C 제외), A 작품은 전 굿즈, B 작품은 피규어만, 아크릴·중고/개봉품 제외, 품절은 최근 12개월 등록분
   - 탭4: 보유품 정가·판매 상태 재확인, 하나은행 매매기준율(100엔당) 갱신
4. 이전 조사(`data/lib_v*.json` 최신본)와 비교 → 「변경」「재입고」 표시
5. `index.html` 갱신, 상단 「최근 업데이트」 날짜 변경, 상단 제목 대사 교체(`RULES.md` 페이지 제목 참고)
6. 브라우저 시험(탭 4개 표시·JS 오류 없음·이미지/로고)
7. 조사 종료 시각 기록(KST, 보고용 — 페이지에는 표시하지 않음) → 커밋·푸시 → Pages 반영 확인, 게시 시각 기록(KST)
7-1. 21:00 KST 전이면 send_later로 21:00 KST 알림 예약 → 받으면 푸시 「서브컬쳐 브리핑이 갱신되었습니다 (YYYY-MM-DD)」 + 링크 / 21:00 이후면 즉시 「지연 게시」 알림 / 실패 시 즉시 실패 사유 알림
8. PC에는 저장하지 않음(GitHub Pages만 갱신). PC에서 파일·탐색기도 열지 않음
9. SendUserMessage로 카테고리별 보고(출처 URL 포함)
