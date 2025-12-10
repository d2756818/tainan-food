import streamlit as st
import random
import pandas as pd
import time

st.set_page_config(
    page_title="台南旅遊小幫手", 
    page_icon="🏯",
    layout="centered"
)

st.markdown("""
<style>
    /* 全站主題變數 (深色系) */
    :root {
        --main-bg: #121212;
        --card-bg: #1E1E1E;
        --text-color: #E0E0E0;
        --accent-color: #B22222; /* 較亮的磚紅色 */
        --border-color: #333333;
    }

    /* 背景設定 */
    .stApp {
        background-color: var(--main-bg);
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                          url("https://images.unsplash.com/photo-1605211698552-144e044d895e?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* 文字顏色 */
    .stApp, .stMarkdown, .stText, p, div, li, span {
        color: var(--text-color) !important;
    }

    /* 標題顏色 */
    h1, h2, h3, h4 {
        color: var(--accent-color) !important;
        font-family: "Microsoft JhengHei", "微軟正黑體", sans-serif;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }

    /* 輸入框樣式 */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        border: 1px solid var(--accent-color) !important;
    }
    .stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label {
        color: var(--accent-color) !important;
        font-weight: bold;
    }
    div[data-baseweb="popover"] div, div[data-baseweb="menu"] div {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
    }

    /* 按鈕樣式 */
    div.stButton > button {
        background-color: #2D2D2D !important;
        color: var(--accent-color) !important;
        border: 2px solid var(--accent-color) !important;
        border-radius: 12px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: var(--accent-color) !important;
        color: #FFFFFF !important;
    }
    
    /* 主要按鈕 */
    div.stButton > button[kind="primary"] {
        background-color: var(--accent-color) !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* 結果卡片 */
    .result-card {
        background-color: var(--card-bg);
        border: 2px solid var(--accent-color);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .result-card h2, .result-card h3 {
        color: var(--accent-color) !important;
        margin: 0;
        text-shadow: none;
    }
    .result-card pre {
        background-color: #000;
        color: #ddd;
    }

    /* 表格樣式 */
    div[data-testid="stDataFrame"] {
        background-color: var(--card-bg);
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏯 台南旅遊神隊友")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🥢 時段美食", "🐦 水雉抽籤", "💰 秒速分帳", "🛵 停車紀錄"])

# --- 功能 1: 依時段隨機推薦美食 ---
with tab1:
    st.header("🕑 餓了嗎？現在幾點？")
    
    food_data = {
        "🌅 活力早餐 (06:00-11:00)": [
            "六千牛肉湯", "阿堂鹹粥", "富盛號碗粿", "勝利早點", 
            "阿公阿婆蛋餅", "呂 早餐", "豆奶宗"
        ],
        "☀️ 飽足午餐 (11:00-14:00)": [
            "葉家小卷米粉", "文章牛肉湯", "阿裕牛肉鍋", "丹丹漢堡", 
            "邱家小卷米粉", "集品蝦仁飯", "矮仔成蝦仁飯"
        ],
        "🍰 悠閒下午茶 (14:00-17:00)": [
            "義豐冬瓜茶", "NINAO 蜷尾家冰淇淋", "周氏蝦捲", "同記安平豆花", 
            "連得堂餅家", "深藍咖啡館 (千層蛋糕)", "双生綠豆沙牛奶"
        ],
        "🌙 晚餐與宵夜 (17:00-24:00)": [
            "阿明豬心冬粉", "十平 (日式丼飯)", "小豪洲沙茶爐", "大東夜市(需確認日期)", 
            "花園夜市(需確認日期)", "鬍鬚忠牛肉湯", "悅津鹹粥"
        ]
    }

    time_select = st.selectbox("請選擇時段：", list(food_data.keys()))
    current_list = food_data[time_select]
    st.info(f"👉 這個時段口袋名單共有 **{len(current_list)}** 家店。")

    if st.button("🎲 幫我決定吃哪家！", type="primary"):
        with st.spinner("🔍 搜尋古都美食中..."):
            time.sleep(0.5)
        
        choice = random.choice(current_list)
        
        st.markdown(f"""
        <div class="result-card">
            <h3>🎉 推薦您去吃：{choice}</h3>
        </div>
        """, unsafe_allow_html=True