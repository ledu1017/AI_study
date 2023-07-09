#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os, sys
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing


# In[4]:


class IntentModel:
    def __init__(self, model_name, proprocess):
        # 의도 클래스별 레이블
        self.labels = {0:"인사", 1:'욕설', 2:'주문', 3:'예약', 4:'기타'}
        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)
        # 챗봇 Preprocess 객체
        self.p = proprocess
        
    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)
        
        # 문장 내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag = True)
        sequences = [self.p.get_wordidx_sequence(keywords)]
        

        module_paths = [
            'C:\\Users\\ledu2\\NLP\\chatbot_study\\config'
        ]

        for path in module_paths:
            abs_path = os.path.abspath(path)
            if abs_path not in sys.path:
                sys.path.append(abs_path)
                
        # 단어 스퀀스 벡터 크기
        from GlobalParams import MAX_SEQ_LEN
        
        # 패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen = MAX_SEQ_LEN, padding = 'post')
        
        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis = 1)
        return predict_class.numpy()[0]


# In[5]:


os.getcwd()


# In[ ]:




