import pandas as pd  # pip install pandas openpyxl
import plotly_express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title = "포항 아파트 실거래가 현황",
                   page_icon = ":chart_with_upwards_trend:",
                   layout = "wide",
)

# hidden hamburger menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}        
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# excel파일 불러오기
df = pd.read_excel(
    io ="포항_아파트및분양권_실거래가_현황.xlsx",
    engine = "openpyxl",
    sheet_name = "아파트 매매 실거래가",
    skiprows = 0,
    nrows = 1000,
)

# ----- 단지 선택 -----
단지명 = st.sidebar.selectbox(
    "단지명 선택",
    options = df["단지명"].unique()
)

df_selection = df.query(
    "단지명 == @단지명"
)


# ----- 선택한 단지 엑셀로 저장 -----
df_selection.to_excel(
    "real_transaction_price.xlsx",
    encoding = "openpyxl",
    sheet_name = "아파트 매매 실거래가",
)

# ----- 새로 저장한 엑셀 불러오기 -----
df = pd.read_excel(
    io ="real_transaction_price.xlsx",
    engine = "openpyxl",
    sheet_name = "아파트 매매 실거래가",
    skiprows = 0,
    nrows = 1000,
)

# ----- 전용면적 별로 정렬하기 -----
전용면적 = st.sidebar.selectbox(
    "전용면적 선택",
    options = df["전용면적"].unique()
)

df_selection = df.query(
    "전용면적 == @전용면적"
)

# st.dataframe(df_selection)

# ----- MAINPAGE -----
st.title(":chart_with_upwards_trend: 2022년 포항 주요 아파트 실거래 현황")
st.markdown("#")

# ----- 최고가 저저가 보여주기 -----
low_price = df_selection["거래금액(만원)"].min()
high_price = df_selection["거래금액(만원)"].max()
danji = df["단지명"].unique()

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("단지명:")
    st.subheader(f"{danji}")
with middle_column:
    st.subheader("최저금액:")
    st.subheader(f"{low_price}만원")
with right_column:
    st.subheader("최고금액:")
    st.subheader(f"{high_price}만원")

st.markdown("---")

# ----- 차트 그리기 -----
contract_date = df_selection["계약일"]
contract_price = df_selection["거래금액(만원)"]


fig = px.line(
    df_selection,
    x = contract_date,
    y = contract_price,
    title = '< 거래일자 별 실거래금액 추이 >',  # 그래프 타이틀 지정
    text = contract_price,
    markers = True,
)

fig.update_layout(
    width = 900,
    height = 550,
    paper_bgcolor = "#0083B8",
    plot_bgcolor = "rgb(223, 100, 200)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    title_font_size = 28,
    # font_color = "black",
    font_size = 14,
)

fig.update_traces(
    line=dict(width=3)
)

fig.update_xaxes(title_font_family="Arial")

st.plotly_chart(fig)


























