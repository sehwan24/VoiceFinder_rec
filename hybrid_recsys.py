#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

# 업로드된 파일을 경로에 추가
#sys.path.append('/content/drive/MyDrive/Colab Notebooks/voiceFinder/hybird')

# 파일에서 함수 불러오기
import content_based 
import collaborate_filtering


# In[8]:


#sample_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/voiceFinder/sample_data.csv')
sample_data = pd.read_csv('./sample_data.csv')
sample_data['market_id'] = sample_data['market_id'].astype(int)


# In[21]:


# 하이브리드 추천 시스템
def get_recommendations(user_profile, alpha=0.5):
    user_id = user_profile['user_id']
    
    print(f"user id is {user_id}")
    
    cb_recommendation = content_based.get_recommendations(user_profile, 3)
    print(f"cb result: {cb_recommendation}")
          
    cf_recommendation = collaborate_filtering.get_recommendations(user_id)
    print(f"cb result: {cb_recommendation}")

    combined_recommendation = alpha * cb_recommendation + (1 - alpha) * cf_recommendation

    top_recommendations = combined_recommendation.sort_values(ascending=False).head(3)
    print(f"total result: {top_recommendations}")

    return sample_data[sample_data['market_id'].isin(top_recommendations.index)]['market_id']

