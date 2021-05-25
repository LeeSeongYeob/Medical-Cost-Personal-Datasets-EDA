import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache()
def load_data():
    return pd.read_csv('./data/insurance.csv')

medical_df = load_data()
st.title('Medical Cost Personal Datasets')
st.write('각각의 col 정보와 보험료와의 상관관계를 분석해보기')
st.header('1. 전체적인 Dataset 확인')
st.write("""
        - AGE : 나이 데이터
        - SEX : 성별 정보
        - BMI : 신체 Bmi 지수
        - Children : 자녀 수
        - Smoker : 흡연 여부
        - Region : 거주 지역
        - Charges : 지출하는 보험료
        """)
st.dataframe(medical_df.head())

st.header("2. 개별 데이터 확인")
st.write('1. 성별과 요금과의 관계')
st.write('성별과 요금의 관계는 남성이 조금 더 많이 지불하는 경향이 있어보이지만, 거의 비슷하다')
s = sns.catplot(x='sex', y='charges',data=medical_df, kind='violin')
s.fig.set_size_inches(6,4)
st.pyplot(s)


age1= medical_df[medical_df["age"].between(18,28, inclusive = True)]["charges"].mean()
age2 = medical_df[medical_df["age"].between(29,39, inclusive = True)]["charges"].mean()
age3 = medical_df[medical_df["age"].between(40,50, inclusive = True)]["charges"].mean()
age4 = medical_df[medical_df["age"].between(51,64, inclusive = True)]["charges"].mean()
average_age = [age1, age2, age3,age4]
st.write('2.나이와 요금과의 관계')
st.write('대체적으로 나이가 많아질수록 보험료가 증가하는 경향이 있다.')
fig = plt.figure(figsize=(6,4))
sns.barplot(x=["18-28 Age","29-39 Age","40-50 Age","51-64 Age"], y=average_age, palette="crest")
plt.title('Charges by Age')
plt.xlabel('Age Range')
plt.ylabel('Charges')
st.pyplot(fig)


st.write('3.bmi 지수와 요금의 관계')
st.write('BMI가 높을 수록 보험료를 더 많이 내는 경향이 있어보인다. 그렇다면 BMI 와 흡연 유무와의 관계를 비교해 보자.')
fig = plt.figure(figsize=(6,4))
plt.scatter(medical_df['bmi'], medical_df['charges'])
plt.grid()
st.pyplot(fig)

fig = plt.figure(figsize=(6,4))
sns.scatterplot(x='bmi', y='charges', hue='smoker', data=medical_df)
st.write('BMI와 Charges 와의 양의 관계가 사실 대부분 smoker의 지표이다. 따라서 BMI 와 Charges와의 관계가 거의 없고, smoker의 영향으로 이런 그래프가 나왔다고 생각할 수 있다.')
st.pyplot(fig)

st.write('4. children 과 요금과의 관계')
st.write('아이수가 2, 3명일 때 요금을 좀 더 많이 내는 경향이 있다.')
new_df = medical_df.groupby('children')['charges'].mean().reset_index()
fig = plt.figure(figsize=(6,4))
sns.barplot(x='children',y='charges',data=new_df)
st.pyplot(fig)

st.write('5. 흡연과 요금')
st.write('흡연을 하는 사람이 보험료를 더 많이 낸다')
new_df = medical_df.groupby(['smoker'])['charges'].mean().reset_index()
fig = plt.figure(figsize=(6,4))
sns.barplot(x='smoker',y='charges',data=new_df)
st.pyplot(fig)


st.write('6. 지역과 요금')
st.write('southest 비용의 charges가 가장 높다')
new_df = medical_df.groupby('region')[['charges']].mean().sort_values(by='charges', ascending=False)
st.dataframe(new_df)