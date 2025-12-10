import streamlit as st
import random
import pandas as pd

# 設定網頁標題與圖示
st.set_page_config(page_title="台南旅遊小幫手", page_icon="🍤")

st.title("🏯 台南旅遊神隊友")
st.write("這是一個整合美食推薦、決策抽籤、分帳與置物紀錄的旅遊工具。")

# 使用 Tabs 分頁功能來區分五大需求
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🍤 隨機美食", "🎲 抽籤決定", "💰 秒速分帳", "🔐 置物櫃密碼", "🛵 停車紀錄"])

# --- 功能 1: 隨機推薦美食 ---
with tab1:
    st.header("🤤 今天吃什麼？")
    
    # 預設的美食清單 (你可以隨時在這裡擴充)
    old_shops = ["阿堂鹹粥", "六千牛肉湯", "富盛號碗粿", "阿明豬心冬粉", "葉家小卷米粉", "義豐冬瓜茶", "周氏蝦捲"]
    new_shops = ["十平 (日式丼飯)", "NINAO 蜷尾家冰淇淋", "Bar Home (特色酒吧)", "StableNice BLDG (老宅咖啡)", "糯夫米糕"]

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎲 推薦一家老字號"):
            choice = random.choice(old_shops)
            st.success(f"推薦你去吃：**{choice}**")
            
    with col2:
        if st.button("✨ 推薦一家新潮店"):
            choice = random.choice(new_shops)
            st.info(f"推薦你去試試：**{choice}**")

# --- 功能 2: 抽籤決定要吃哪家 ---
with tab2:
    st.header("🤔 選擇障礙救星")
    st.write("大家想吃的店都不一樣？輸入店名，讓命運決定！")
    
    # 讓使用者輸入店名，用換行或逗號分隔
    user_input = st.text_area("輸入想吃的店家 (每行一間)", height=150, placeholder="例如：\n文章牛肉湯\n丹丹漢堡\n阿裕牛肉鍋")
    
    if st.button("🚀 幫我們選一家！"):
        if user_input.strip():
            # 處理輸入文字，依換行切割成清單
            shop_list = [line.strip() for line in user_input.split('\n') if line.strip()]
            if shop_list:
                winner = random.choice(shop_list)
                st.balloons()  # 放氣球特效
                st.markdown(f"### 🎉 決定就是： **{winner}**")
            else:
                st.warning("請輸入有效的店家名稱")
        else:
            st.warning("還沒輸入店家喔！")

# --- 功能 3: 紀錄分攤餐點金額 ---
with tab3:
    st.header("💸 散會自動算帳")
    
    # 初始化 Session State 來暫存資料 (除非重新整理網頁，否則資料會保留)
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []

    # 輸入區塊
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            item_name = st.text_input("項目 (如: 芒果冰)", key="input_item")
        with c2:
            payer_name = st.text_input("付款人 (如: 小明)", key="input_payer")
        with c3:
            amount = st.number_input("金額", min_value=0, step=10, key="input_amount")
            
        if st.button("➕ 加入清單"):
            if item_name and payer_name and amount > 0:
                st.session_state.expenses.append({
                    "項目": item_name,
                    "付款人": payer_name,
                    "金額": amount
                })
                st.success(f"已加入: {item_name} ({payer_name} 付了 ${amount})")
            else:
                st.error("請完整填寫資訊")

    st.divider()

    # 顯示目前清單與結算
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df, use_container_width=True)
        
        # 計算邏輯
        total_cost = df["金額"].sum()
        payers = df.groupby("付款人")["金額"].sum().to_dict()
        all_people = list(payers.keys()) # 假設參與者就是有付過錢的人
        
        if len(all_people) > 0:
            avg_cost = total_cost / len(all_people)
            
            st.markdown(f"#### 💰 總金額: ${total_cost} | 平均每人: ${avg_cost:.1f}")
            st.subheader("📊 結算結果：")
            
            for person in all_people:
                paid = payers.get(person, 0)
                balance = paid - avg_cost
                
                if balance > 0:
                    st.success(f"**{person}** 先付了 ${paid}，應 **收回 ${balance:.1f}**")
                elif balance < 0:
                    st.error(f"**{person}** 先付了 ${paid}，應 **再拿出來 ${abs(balance):.1f}**")
                else:
                    st.info(f"**{person}** 不用收也不用付")
                    
        if st.button("🗑️ 清空所有帳目"):
            st.session_state.expenses = []
            st.rerun()

# --- 功能 4: 紀錄寄放行李櫃位 ---
with tab4:
    st.header("🛅 行李寄放小條")
    st.info("⚠️ 注意：網頁重新整理後資料會消失，請截圖保存！")

    col1, col2 = st.columns(2)
    with col1:
        locker_id = st.text_input("櫃位號碼", placeholder="例如：A03")
    with col2:
        door_id = st.text_input("門號/位置", placeholder="例如：下層左邊")
    
    password = st.text_input("密碼", type="password", placeholder="輸入密碼")
    
    # 增加一個顯示開關，防止朋友偷看
    show_pass = st.checkbox("顯示密碼")
    
    st.divider()
    st.subheader("您的紀錄：")
    st.markdown(f"**📦 櫃位：** {locker_id if locker_id else '---'}")
    st.markdown(f"**🚪 門號：** {door_id if door_id else '---'}")
    if show_pass:
        st.markdown(f"**🔑 密碼：** `{password}`")
    else:
        st.markdown(f"**🔑 密碼：** `******` (請勾選上方顯示)")

# --- 功能 5: 停車地點紀錄 ---
with tab5:
    st.header("🛵 我的機車停哪？")
    
    memo = st.text_area("輸入停車位置、地標或樓層", height=150, 
                       placeholder="例如：\n新光三越對面\n車牌 123-ABC\n停在 B1柱子旁")
    
    if memo:
        st.success("紀錄中...")
        st.markdown("### 👇 停車資訊預覽")
        st.info(memo)