#!/usr/bin/env python
# coding: utf-8

# In[3]:


from konlpy.tag import Komoran
import pickle


# # <font color = blue> 챗봇 전처리 클래스

# In[5]:


class Preprocess:
    def __init__(self, word2index_dic = '', userdic=None):    # userdic 인자에 사용자 정의 사전 파일 경로
        # 단어 인덱스 사전 불러오기
        if(word2index_dic != ''):
            f = open(word2index_dic, "rb")
            self.word_index = pickle.load(f)
            f.close()
        else:
            self.word_index = None
            
        # 형태소 분석기 초기화
        self.komoran = Komoran(userdic=userdic)
        
        self.exclusion_tags = [    # 불용어 품사
            'JKS', 'JKC', 'JKG', 'JKO', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XSN', 'XSV', 'XSA'
        ]
        
    def pos(self, sentence):    # 형태소 분석기 POS 태거
        return self.komoran.pos(sentence)
    
    # 불용어 제거 후 필요한 품사 정보 가져오기
    def get_keywords(self, pos, without_tag = False):
        f = lambda x:x in self.exclusion_tags
        word_list = []
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list
    
    def get_wordidx_sequence(self, keywords):
        if self.word_index is None:
            return []
        w2i = []
        for word in keywords:
            try:
                w2i.append(self.word_index[word])
            except KeyError:
                # 해당 단어가 사전에 없는 경우 OOV 처리
                w2i.append(self.word_index['OOV'])
        return w2i


# In[1]:


import os


# In[2]:


os.getcwd()


# In[ ]:




