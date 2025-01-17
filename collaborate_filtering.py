# -*- coding: utf-8 -*-
"""collaborate_filtering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nGnuA_muNuqk7kCt-syzWMfijcOQEyd6
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# TO MAKE RANDOM DATA
#df_markets = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/voiceFinder/sample_data.csv')
#df_markets.head()

#random_sample = df_markets.sample(n=30, random_state=42)
#random_sample

#sample_data.to_csv('/content/drive/MyDrive/Colab Notebooks/voiceFinder/sample_data.csv', encoding='utf-8', index=False)

#sample_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/voiceFinder/sample_data.csv')
sample_data = pd.read_csv('./sample_data.csv')

sample_data['market_id'] = sample_data['market_id'].astype(int)

# 샘플 데이터: 사용자 정보
users = pd.DataFrame({
    'user_id': [1, 2, 3, 4],
    'gender': ['male', 'female', 'female', 'male'],
    'age': [25, 30, 22, 40],
    'considerations': [['음식의 맛', '가격 수준'], ['서비스 정도', '음식의 청결도'], ['음식의 맛', '분위기'], ['가격 수준', '메뉴의 다양성']]
})

users

gender_le = LabelEncoder()
users['gender_encoded'] = gender_le.fit_transform(users['gender'])

# 나이 그룹화
age_bins = [10, 20, 30, 40, 50]
age_labels = ['10대', '20대', '30대', '40대']
users['age_group'] = pd.cut(users['age'], bins=age_bins, labels=age_labels, right=False)
users['age_group_encoded'] = LabelEncoder().fit_transform(users['age_group'])

# 고려 기준 인코딩 (One-Hot Encoding)
considerations = ['기타', '할인 및 프로모션', '거리', '주차의 편리함', '부대시설', '예약의 용이함', '교통의 편리성', '메뉴의 다양성',
                  '음식의 양', '음식의 맛', '건강에 좋은 요리', '분위기', '서비스 정도', '가격 수준', '음식점의 청결도']

# 고려 기준 인코딩 (MultiLabelBinarizer 사용)
mlb = MultiLabelBinarizer(classes=considerations)
considerations_encoded = mlb.fit_transform(users['considerations'])

# 사용자 프로필 매트릭스 생성
user_profiles = pd.concat([users[['user_id', 'gender_encoded', 'age_group_encoded']], pd.DataFrame(considerations_encoded)], axis=1).set_index('user_id')
user_profiles

utility_matrix = pd.DataFrame(np.nan, index= users['user_id'], columns = sample_data['market_id'])
utility_matrix

# 유저 1 별점 부여
user_1_ratings = {
    63581: 4.5, 55402: 4.0, 65666: 3.5, 117236: 5.0, 57431: 4.0, 114791: 3.5, 367019: 4.0, 98873: 3.5, 790314: 4.5, 197230: 4.0
}
for market_id, rating in user_1_ratings.items():
    utility_matrix.at[1, market_id] = rating

# 유저 2 별점 부여
user_2_ratings = {
    178047: 4.5, 141727: 4.5, 183057: 4.0, 98873: 4.5, 543852: 4.5, 145428: 4.0, 138143: 4.0, 73916: 4.0, 13464: 4.0, 94924: 4.0
}
for market_id, rating in user_2_ratings.items():
    utility_matrix.at[2, market_id] = rating

# 유저 3 별점 부여
user_3_ratings = {
    63581: 4.5, 65666: 4.0, 117236: 5.0, 138143: 4.5, 13464: 4.0, 45790: 4.5, 189711: 4.0, 178047: 4.5, 543852: 4.0, 197230: 4.0
}
for market_id, rating in user_3_ratings.items():
    utility_matrix.at[3, market_id] = rating

# 유저 4 별점 부여
user_4_ratings = {
    63581: 4.5, 57431: 4.5, 367019: 4.0, 45790: 4.5, 189711: 4.0, 543852: 4.5, 141727: 4.0, 145428: 4.0, 39504: 3.5, 20178: 4.0
}
for market_id, rating in user_4_ratings.items():
    utility_matrix.at[4, market_id] = rating

utility_matrix

# NaN 값을 각 사용자의 평균 값으로 대체
utility_matrix_mean = utility_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

# 사용자 프로필 매트릭스와 사용자-음식점 평점 매트릭스 병합
user_profiles_ratings = pd.concat([user_profiles, utility_matrix], axis=1)
user_profiles_ratings

# 사용자 유사도 계산 (성별, 연령대, 고려 기준 기반)
profile_similarity = cosine_similarity(utility_matrix_mean)
profile_similarity_df = pd.DataFrame(profile_similarity, index=user_profiles_ratings.index, columns=user_profiles_ratings.index)

profile_similarity_df

def get_recommendations(user_id):
    # 유사한 사용자 찾기
    similar_users = profile_similarity_df[user_id].sort_values(ascending=False).index[1:]  # 첫 번째는 자기 자신이므로 제외

    # 유사한 사용자의 평점 가져오기
    similar_users_ratings = utility_matrix.loc[similar_users]

    # 음식점 평점 평균 계산 (유사한 사용자 기반)
    restaurant_recommendations = similar_users_ratings.mean(axis=0).sort_values(ascending=False)

    # 이미 평가한 음식점 제외
    rated_restaurants = utility_matrix.loc[user_id].dropna()
    unrated_restaurants = restaurant_recommendations[~restaurant_recommendations.index.isin(rated_restaurants.index)]

    return unrated_restaurants