import streamlit as st
import random
import pandas as pd
import time

# --- 1. 頁面基本設定 ---
st.set_page_config(
    page_title="台南旅遊小幫手", 
    page_icon="🏯",
    layout="centered"
)

# --- 2. CSS 古都美感設計 (核彈級顯色修復) ---
st.markdown("""
<style>
    /* ========== 全站變數 ========== */
    :root {
        --brick-red: #8B3A3A;   /* 赤崁紅磚色 */
        --warm-beige: #FFF8F0;  /* 古樸米黃色 */
        --text-color: #2b2b2b;  /* 深灰黑色 (內文) */
    }

    /* ========== 背景設計 ========== */
    .stApp {
        background-image: linear-gradient(rgba(255, 248, 240, 0.95), rgba(255, 248, 240, 0.95)), 
                          url("https://images.unsplash.com/photo-1605211698552-144e044d895e?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* ========== 【核彈級修復】強制所有文字顏色 ========== */
    /* 使用 * 通用選擇器，強制覆蓋 Streamlit 的深色模式設定 */
    
    /* 1. 針對網頁內絕大多數的文字標籤，強制設為深色 */
    .stApp div, .stApp p, .stApp span, .stApp label, .stApp li, .stApp td, .stApp th {
        color: var(--text-color) !important;
    }

    /* 2. 特別針對標題，強制設為紅磚色 (因為上面的規則太強，要重新指定回來) */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--brick-red) !important;
        font-family: "Microsoft JhengHei", "微軟正黑體", sans-serif;
        font-weight: 800;
        text-shadow: 0px 0px 0px transparent !important; /* 移除深色模式可能有的陰影 */
    }

    /* ========== 輸入框與介面優化 ========== */
    /* 讓輸入框的背景變全白，文字變深黑，邊框變紅磚色 */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid var(--brick-red) !important;
    }
    /* 輸入框上方的標題 (如: 項目、金額) */
    .stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label {
        color: var(--brick-red) !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* 下拉選單內的選項顏色 */
    div[data-baseweb="popover"] div, div[data-baseweb="menu"] div {
        color: #000000 !important; 
        background-color: #FFFFFF !important;
    }

    /* ========== 按鈕設計 ========== */
    div.stButton > button {
        background-color: var(--warm-beige) !important;
        color: var(--brick-red) !important;
        border: 2px solid var(--brick-red) !important;
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: var(--brick-red) !important;
        color: var(--warm-beige) !important;
        border-color: var(--brick-red) !important;
    }
    div.stButton > button p {
        color: inherit !important;
    }

    /* Primary 按鈕 */
    div.stButton > button[kind="primary"] {
        background-color: var(--brick-red) !important;
        color: var(--warm-beige) !important;
        border: none !important;
    }

    /* ========== 結果卡片 ========== */
    .result-card {
        background-color: #FDF5E6;
        border: 4px double #5C3317;
        border-radius: 8px;
        padding: 25px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    /* 卡片內的文字不受全域影響，獨立設定 */
    .result-card h2, .result-card h3 {
        color: #5C3317 !important;
        margin: 0;
        font-family: "DFKai-SB", "標楷體", serif;
    }
    
    /* 分帳表格文字 */
    div[data-testid="stDataFrame"] div {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏯 台南旅遊神隊友")
st.markdown("---")

# 分頁設定
tab1, tab2, tab3, tab4 = st.tabs(["🥢 時段美食", "🐦 水雉抽籤", "💰 秒速分帳", "🛵 停車紀錄"])

# --- 功能 1: 依時段隨機推薦美食 ---
with tab1:
    st.header("🕑 餓了嗎？現在幾點？")
    
    # === 📝 你的美食名單 ===
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
        """, unsafe_allow_html=True)

        google_