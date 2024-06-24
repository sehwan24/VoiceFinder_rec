# VoiceFinder_rec

# 1. About Our Projects

오프라인 매장들에게 각광받고 있는 디지털 마케팅 방법 중 ‘체험단 마케팅’ 플랫폼 구축 목표.

매장 측에서 제공하는 소정의 혜택을 받고도 리뷰를 작성하지 않는 사용자들의 자발적인 참여를 증진시키고자 추천시스템 도입을 제안한다.

# 2. Stacks

- React
- pandas
- koBERT (적용 중)
- flask

# 3. File Description

**python script files**

1. app.py
    - 전체 추천 시스템의 entry point
2. collaborate_filtering.py
    - 사용자 간 유사도 계산 및 유사 사용자의 평점을 바탕으로 utility Matrix 갱신
3. content_based.py
    - 좋아하는 음식 (fav_food) vectorize 후 cosine similarity 계산
    - 못 먹는 음식 (cant_food) filtering 적용
4. hybrid_recsys.py
    - cb model (content-bassed)와 cf model (collaborate-filtering)의 조화평균을 통한 최종 추천 마켓 출력

data files

1. markets.csv
2. users.csv
3. rating.csv

# 4. System Logic

## 4.1. Content-based

## 4.2 Collaborate-Filtering

## 4.3 Hybrid System
