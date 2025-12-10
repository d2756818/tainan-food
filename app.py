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
        color: var(--accent-color) !