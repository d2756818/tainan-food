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

# --- 2. CSS 古都美感設計 (深色主題) ---
# 這裡就是容易出錯的地方，請確保第 14 行開始，到下面 style 結束都有複製到
st.markdown("""
<style>
    /* 全站主題變數 */
    :root {
        --main-bg: #121212;
        --card-bg: #1E1E1E;
        --text-color: #E0E0E0;
        --accent-color: #B22222; /* 較亮的磚紅色 */
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

    /* 強制所有文字顏色為淺灰 (適應深色背景) */
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
    /* 下拉選單選項背景 */
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
    
    /* 主要按鈕 (Primary) */
    div.stButton > button[kind="primary"] {
        background-color: var(--accent-color) !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* 結果卡片與表格背景 */
    .result-card, div[data-testid="stDataFrame"] {
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
    /* 讓 pre 標籤 (停車紀錄) 文字清晰 */
    .result-card pre {
        background-color: #000;
        color: #ddd;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True) 
# 上面這一行 """ 就是您剛剛遺失的結束符號，這次一定要複製到它！

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
        """, unsafe_allow_html=True)

        google_url = f"https://www.google.com/search?q=台南+{choice}"
        st.link_button(f"🔍 Google 搜尋「{choice}」", google_url)

# --- 功能 2: 水雉抽籤 ---
with tab2:
    st.header("🐦 水雉大仙賜籤")
    st.write("呼喚台南市鳥「凌波仙子」，誠心祈求水雉大仙咬出籤王。")
    
    user_input = st.text_area("輸入候選店家 (每行一間)", height=150, 
                             placeholder="例如：\n阿堂鹹粥\n丹丹漢堡\n小豪洲沙茶爐")
    
    if st.button("🎋 請大仙咬籤！", type="primary"):
        if user_input.strip():
            shop_list = [line.strip() for line in user_input.split('\n') if line.strip()]
            
            if shop_list:
                animation_spot = st.empty()
                mp4_url = "https://raw.githubusercontent.com/d2756818/tainan-food/main/draw-lots.mp4"
                
                # HTML 影片區塊
                video_html = f"""
                    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                        <video width="300" autoplay muted playsinline style="border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
                            <source src="{mp4_url}" type="video/mp4">
                        </video>
                    </div>
                """
                
                animation_spot.markdown(video_html, unsafe_allow_html=True)
                time.sleep(4) 
                animation_spot.empty()
                
                winner = random.choice(shop_list)
                
                st.markdown(f"""
                    <div class="result-card">
                        <h2>🎋 籤王：{winner}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.balloons()
            else:
                st.warning("請輸入有效的店家名稱")
        else:
            st.warning("還沒輸入店家喔！")

# --- 功能 3: 秒速分帳 ---
with tab3:
    st.header("💸 散會自動算帳")
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
        
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: item_name = st.text_input("項目", key="input_item")
        with c2: payer_name = st.text_input("付款人", key="input_payer")
        with c3: amount = st.number_input("金額", min_value=0, step=10, key="input_amount")
        
        if st.button("➕ 加入清單", use_container_width=True):
            if item_name and payer_name and amount > 0:
                st.session_state.expenses.append({"項目": item_name,"付款人": payer_name,"金額": amount})
                st.success(f"已加入: {item_name}")

    st.divider()
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df, use_container_width=True)
        
        total_cost = df["金額"].sum()
        payers = df.groupby("付款人")["金額"].sum().to_dict()
        all_people = list(payers.keys())
        if len(all_people) > 0:
            avg_cost = total_cost / len(all_people)
            st.markdown(f"""
                <div class="result-card" style="padding: 15px;">
                    <h4 style="margin:0;">
                        💰 總金額: <span style="color: #ff6b6b;">${total_cost}</span> | 
                        平均每人: <span style="color: #ff6b6b;">${avg_cost:.1f}</span>
                    </h4>
                </div>
            """, unsafe_allow_html=True)
            
            st.subheader("📊 結算結果：")
            for person in all_people:
                paid = payers.get(person, 0)
                balance = paid - avg_cost
                if balance > 0: st.success(f"**{person}** 應收回 **${balance:.1f}**")
                elif balance < 0: st.error(f"**{person}** 應再付 **${abs(balance):.1f}**")
                else: st.info(f"**{person}** 結清")
        
        if st.button("🗑️ 清空帳目"):
            st.session_state.expenses = []
            st.rerun()

# --- 功能 4: 停車紀錄 ---
with tab4:
    st.header("🛵 我的機車停哪？")
    memo = st.text_area("輸入停車位置...", height=150, placeholder="例如：\n新光三越對面\n車牌 123-ABC")
    if memo: 
        st.markdown(f"""
        <div class="result-card" style="text-align: left;">
            <h4 style="margin-bottom: 10px;">📍 您的停車紀錄：</h4>
            <pre>{memo}</pre>
        </div>
        """, unsafe_allow_html=True)