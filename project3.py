from operator import sub
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split  
from sklearn.metrics import accuracy_score 
from sklearn.metrics import confusion_matrix
from sklearn. metrics import classification_report, roc_auc_score, roc_curve
import pickle
import joblib
import streamlit as st
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns
import json

# 1. Read data
# url
url_product = 'https://drive.google.com/file/d/1ZabCyBXKPdNWK6RLg28MCa2pjW_oEmdl/view?usp=sharing'
url_review = 'https://drive.google.com/file/d/1byzbt7l36qQoCTFdwbXfVSystmSIyYN-/view?usp=sharing'
url_data_cleand = 'https://drive.google.com/file/d/10t94lNbhv0lqkijtOw8Xosc7FRSo8b25/view?usp=sharing'
url_user_recom_result = 'https://drive.google.com/file/d/1O3_f8hq0kzyXNC1bJfPBHWzWJpdBpwfK/view?usp=sharing'

# function read data
@st.cache
def read_file_from_ggdr(url):
    file_id = url.split('/')[-2]
    dwn_url = 'https://drive.google.com/uc?id=' + file_id
    data = pd.read_csv(dwn_url)
    return data

# 01. Content based filtering
@st.cache
def get_content_based_recommendation(item_name, n):
    df_item = cosine_similarities_recommend.loc[cosine_similarities_recommend['name'] == item_name, :]
    df_item.sort_values(by=['sim_score'], ascending=False, inplace=True)
    df_id = df_item[['item_id_rec']].head(n)
    result = df_id.merge(df_product, left_on='item_id_rec', right_on='item_id')
    return result

#2. Collabratiove filtering
@st.cache
def get_user_recommendation(customer_id, n):
    df_user = user_recommendation.loc[user_recommendation['customer_id'] == customer_id,:]
    df_user.sort_values(by=['rating_pred'], ascending=False, inplace=True)
    result = df_user.head(n)
    return result

#--------------
# GUI
# st.title("Data Science Project")
st.markdown("<h1 style='text-align: center; color: Red;'>Recommendation System</h1>", unsafe_allow_html=True)
# st.markdown("## **Recommendation System**")

menu = ['0. M???c ti??u kinh doanh', '1. Kh??m ph?? d??? li???u', '2. ????? xu???t d???a tr??n n???i dung', '3. ????? xu???t d???a tr??n ????nh gi?? s???n ph???m']

choice = st.sidebar.radio('Danh m???c', menu)
if choice == '0. M???c ti??u kinh doanh':
    st.markdown("<h3 style='text-align: left; color: Blue;'>0. M???c ti??u kinh doanh</h3>", unsafe_allow_html=True)
    st.image('tiki.JPG')
    st.write("""
        - Tiki l?? m???t h??? sinh th??i th????ng m???i ???all in one???, trong ???? c?? tiki.vn, l?? m???t website th????ng m???i ??i???n t??? ?????ng top 2 c???a Vi???t Nam, top 6 khu v???c ????ng Nam ??. Tr??n trang n??y ???? tri???n khai nhi???u ti???n ??ch h??? tr??? n??ng cao tr???i nghi???m ng?????i d??ng v?? h??? mu???n x??y d???ng nhi???u ti???n ??ch h??n n???a.
        """)
    st.write("""
        - C??ng ty ch??a c?? h??? th???ng Recommendation System v?? m???c ti??u l?? c?? th??? x??y d???ng ???????c h??? th???ng n??y gi??p ????? xu???t v?? g???i ?? cho ng?????i d??ng/ kh??ch h??ng'
    """)

elif choice == '1. Kh??m ph?? d??? li???u':
    # read data
    data_product = read_file_from_ggdr(url_product)
    data_review = read_file_from_ggdr(url_review)
    # header
    st.markdown("<h3 style='text-align: left; color: Blue;'>1. Kh??m ph?? d??? li???u</h3>", unsafe_allow_html=True)

    # body
    st.write("""
        - D??? li???u ???????c cung c???p s???n g???m c?? c??c t???p tin: ProductRaw.csv, ReviewRaw.csv ch???a th??ng tin s???n ph???m, review v?? rating cho c??c s???n ph???m thu???c c??c nh??m h??ng h??a nh?? Mobile_Tablet, TV_Audio, Laptop, Camera, Accessory.
        """)



    st.write('##### 1. Product Rawdata')
    st.dataframe(data_product.head(3))

    st.write('##### 2. Review Rawdata')
    st.dataframe(data_review.head(3))

    st.write('##### 3. Visualization Product Rawdata')
    st.image('01.thietbiso.JPG')
    st.image('02.hangquocte.JPG')
    st.image('03.laptop.JPG')
    st.image('04.mayanh.JPG')
    st.image('05.oto.JPG')
    st.image('06.dienthoai.JPG')
    st.image('07.nhacua.JPG')
    st.image('08.dongho.JPG')
    st.image('09.dienthoai.JPG')



elif choice == '2. ????? xu???t d???a tr??n n???i dung':
    # read data
    data_cleaned = read_file_from_ggdr(url_data_cleand)
    df1 = data_cleaned
    cosine_similarities = pd.read_csv('cosine_similarities_10product_v2.csv', index_col=0)
    df_product = data_cleaned[['item_id', 'name', 'rating', 'price', 'brand', 'image', 'group1']]
    cosine_similarities_recommend = cosine_similarities.merge(df_product, left_on='item_id', right_on='item_id')

    # header
    st.markdown("<h3 style='text-align: left; color: Blue;'>2. ????? xu???t d???a tr??n n???i dung</h3>", unsafe_allow_html=True)

    # choose bar
    st.sidebar.markdown('***Ch???n th??ng tin***')
    item_name = st.sidebar.selectbox('T??n s???n ph???m', df1['name'])
    lst_num = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    items_num = st.sidebar.selectbox('S??? s???n ph???m mu???n ????? xu???t', lst_num)
    submit_button = st.sidebar.button(label='Summit')

    # result
    if submit_button:

        # display item name choosen:
        st.markdown('***S???n ph???m***')

        st.write('**%s**'%item_name)
        idx_prd = df1.index[df1['name'] == item_name].tolist()[0]
        col1, col2 = st.columns(2)
        col1.image(str(df1.loc[idx_prd,'image']))
        col2.write('Category: %s'%(df1['group1'].iloc[idx_prd]))
        col2.write('Brand: %s'%(df1['brand'].iloc[idx_prd]))
        col2.write('Price: %s'%(df1['price'].iloc[idx_prd]))
        col2.write('Rating: %s'%(df1['rating'].iloc[idx_prd]))    
        
        # result
        st.write('***Top %s***'%items_num, '***s???n ph???m t????ng t???***')

        results = get_content_based_recommendation(item_name, items_num)
        for i in range(0,results.shape[0]):
            st.write('**%s**'%(results['name'].iloc[i]))
            col1, col2 = st.columns(2)
            col1.image(str(results['image'].iloc[i]))
            col2.write('Category: %s'%(results['group1'].iloc[i]))
            col2.write('Brand: %s'%(results['brand'].iloc[i]))
            col2.write('Price: %s'%(results['price'].iloc[i]))
            col2.write('Rating: %s'%(results['rating'].iloc[i]))

elif choice == '3. ????? xu???t d???a tr??n ????nh gi?? s???n ph???m':
    # read data
    user_recommendation_result = read_file_from_ggdr(url_user_recom_result)
    data_cleaned = read_file_from_ggdr(url_data_cleand)
    df_product = data_cleaned[['item_id', 'name', 'rating', 'price', 'brand', 'image', 'group1']]
    user_recommendation = user_recommendation_result.merge(df_product, left_on='product_id', right_on='item_id')

    # customers list
    customers_list = user_recommendation_result[['customer_id']]
    customers_list = customers_list.drop_duplicates()

    # header
    st.markdown("<h3 style='text-align: left; color: Blue;'>2. ????? xu???t d???a tr??n ????nh gi?? s???n ph???m</h3>", unsafe_allow_html=True)

    # choose bar
    st.sidebar.markdown('***Ch???n th??ng tin***')
    customer_id = st.sidebar.selectbox('ID ng?????i d??ng', customers_list['customer_id'])
    lst_num = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    items_num = st.sidebar.selectbox('S??? s???n ph???m mu???n ????? xu???t', lst_num)
    submit_button = st.sidebar.button(label='Summit')

    # result
    if submit_button:

        # display item name choosen:
        st.markdown('***M?? kh??ch h??ng***')
        st.write('**%s**'%customer_id)  
        
        # result
        st.write('***Top %s***'%items_num, '***s???n ph???m ????? xu???t***')
        results = get_user_recommendation(customer_id, items_num)
        for i in range(0,results.shape[0]):
            st.write('**%s**'%(results['name'].iloc[i]))
            col1, col2 = st.columns(2)
            col1.image(str(results['image'].iloc[i]))
            col2.write('Category: %s'%(results['group1'].iloc[i]))
            col2.write('Brand: %s'%(results['brand'].iloc[i]))
            col2.write('Price: %s'%(results['price'].iloc[i]))
            col2.write('Rating: %s'%(results['rating'].iloc[i]))
    
