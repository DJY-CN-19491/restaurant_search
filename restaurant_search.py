import pandas as pd
import streamlit as st
import plotly.express as px


fd_df = pd.read_csv('end.csv')

st.title('人気飲食店')


price_limit = st.slider('最低価格の上限', 0, 20000, 2000, 200)
score_limit = st.slider('大人気スコアの作成下限', 0.0, 1.0, 0.0, 0.1)

filtered_df = fd_df[
    (fd_df['昼価格'] <= price_limit) &
    (fd_df['pop_score'] >= score_limit)
]


fig = px.scatter(
    filtered_df,
    x = 'pop_score',
    y = '昼価格',
    hover_data = ['タイトル', '紹介', 'star', 'コメント'],
    title = '人気スコアと最低価格の散布図'
)

st.plotly_chart(fig)

selected_fd = st.selectbox('気になる飲食店を選んで詳細を確認', filtered_df['タイトル'])

if selected_fd:
    url = filtered_df[filtered_df['タイトル'] == selected_fd]['link'].values[0]
    st.markdown(f"[{selected_fd}のページへ移動]({url})", unsafe_allow_html=True)

sort_key = st.selectbox(
    "ランキング基準を選んでください",
    ("star", "pop_score", "コメント", "昼価格")
)

ascending = True if sort_key == "昼価格" else False

st.subheader(f"{sort_key}による飲食店ランキング（上位10件）")

ranking_df = filtered_df.sort_values(by=sort_key, ascending=ascending).head(10)

# 必要な列だけ表示
st.dataframe(ranking_df[["タイトル", "昼価格", "pop_score", "star", "コメント", "紹介"]])