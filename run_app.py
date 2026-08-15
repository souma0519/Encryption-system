import streamlit as st
import random
import string
import os
import re

st.set_page_config(
    page_title="オリジナル暗号化システム",
    layout="centered"
)


st.markdown("""
    <style>
    /* 全体の背景：高級感のある深いダークグレー */
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }

    /* タイトル：細めでスマートな鮮やかブルー */
    h1 {
        color: #58a6ff !important;
        font-weight: 300 !important;
        letter-spacing: -0.5px !important;
    }

    /* 💡【ここに入っています！】普段のタブの文字色（選んでいないほう） */
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important; /* 👈 今は薄いグレー。好きな色に変えられます！ */
    }

    /* 💡【ここに入っています！】カチッと選んでいるほうのタブの文字色と、その下線の色 */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #58a6ff !important;          /* 👈 タブの文字色（今は上品なブルー） */
        border-bottom-color: #58a6ff !important; /* 👈 タブの下線の色（今は上品なブルー） */
    }

    /* 入力欄：選択したときだけ上品にブルーに光る */
    .stTextInput input {
        background-color: #161b22 !important;
        color: #f0f6fc !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        transition: border-color 0.2s;
    }
    .stTextInput input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15) !important;
    }

    /* 実行ボタン：シンプルで押し心地の良いブルーのボタン */
    .stButton button {
        background-color: #1f6feb !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        border: none !important;
        border-radius: 6px !important;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton button:hover {
        background-color: #388bfd !important;
    }

    /* コピーボタン：シンプルに枠線の中に溶け込む形に */
    [data-testid="stCopyButton"] button {
        background-color: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("完全自動暗号化システム")
st.write("※英語以外使用不可です！！！")
st.write("※大事なパスワードなどを入力しないでください！")


RULE_STEP1 = {
    "a": r".#",  "b": r",_",  "c": r"\-",  "d": r"!@",  "e": r"$&",  "f": r"*(",
    "g": r")+",  "h": r'~"',  "i": r"?/",  "j": r":[",  "k": r";]",  "l": r"<{",
    "m": r">}",  "n": r"[]",  "o": r"{}",  "p": r";<",  "q": r":>",  "r": r"?*",
    "s": r"+/",  "t": r"=\\", "u": r"^|",  "v": r"_~",  "w": r".%",  "x": r",!",
    "y": r".$",  "z": r"&#"
}


SIGNAL_TO_NUM = {
    ".": "1", "#": "2", ",": "3", "_": "4", "\\": "5", "¥": "5", "-": "6",
    "!": "7", "@": "8", "$": "9", "&": "10", "*": "11", "(": "12",
    ")": "13", "+": "14", "~": "15", '"': "16", "?": "17", "/": "18",
    ":": "19", "[": "20", ";": "21", "]": "22", "<": "23", "{": "24",
    ">": "25", "}": "26", "[": "27", "]": "28", "{": "29", "}": "30",
    ";": "31", "<": "32", ":": "33", ">": "34", "?": "35", "*": "36",
    "+": "37", "/": "38", "=": "39", "\\": "40", "^": "41", "|": "42",
    "_": "43", "~": "44", ".": "45", "%": "46", ",": "47", "!": "48",
    ".": "49", "$": "50", "&": "51", "#": "52"
}

# 💡数字から記号へ戻す対応表
NUM_TO_SIGNAL = {v: k for k, v in SIGNAL_TO_NUM.items()}
NUM_TO_SIGNAL["5"] = "\\" 

# 💡完全にランダムなアルファベットをランダムな長さ（1〜4文字）で作る関数
def make_random_alphas():
    length = random.randint(1, 4)
    return "".join(random.choices(string.ascii_lowercase, k=length))

# --- 1. 暗号化（エンコード）システム関数 ---
def encrypt_process(text):
    signal_list = []
    for char in text.lower():
        if char in RULE_STEP1:
            normalized_raw_sig = RULE_STEP1[char].replace("¥", "\\")
            signal_list.append(normalized_raw_sig)
            
    if not signal_list:
        return None
        
    kind_list = []
    seen_signals = []
    
    for word_signal in signal_list:
        for s in word_signal:
            if s in SIGNAL_TO_NUM:
                num_str = SIGNAL_TO_NUM[s]
                if s not in seen_signals:
                    seen_signals.append(s)
                
                if int(num_str) >= 10:
                    kind_list.append(make_random_alphas() + num_str)
                else:
                    kind_list.append("_" + num_str)
                    
    combined_signals = "".join(signal_list)
    total_count = len(combined_signals)
    
    ones_string = "1" * len(seen_signals)
    ones_number = int(ones_string) if ones_string else 1
    
    hidden_counts = ones_number * random.randint(100, 999)
    
    final_code = f"{total_count}.{hidden_counts}.{''.join(kind_list)}"
    return final_code

# --- 2. 復号（解読）システム ---
def decrypt_process(code):
    try:
        cleaned_code = str(code).strip()
        cleaned_code = cleaned_code.replace("¥", "\\")
        
        parts = cleaned_code.split(".")
        if len(parts) != 3:
            return "コードの形式が違います"
            
        total_count = int(parts[0])
        hidden_counts = parts[1]
        kind_rule = parts[2]
        
        matches = re.findall(r"_[0-9]|[0-9]{2}", kind_rule)
        
        num_list = []
        for match in matches:
            if match.startswith("_"):
                num_list.append(match[1:])
            else:
                num_list.append(match)
                
        restored_signals = ""
        for num in num_list:
            if num in NUM_TO_SIGNAL:
                restored_signals += NUM_TO_SIGNAL[num]
                
        original_text = ""
        temp_signals = restored_signals
        
        while len(temp_signals) > 0:
            matched = False
            for char, sig in RULE_STEP1.items():
                normalized_sig = sig.replace("¥", "\\")
                if temp_signals.startswith(normalized_sig) or temp_signals.startswith(sig):
                    original_text += char
                    temp_signals = temp_signals[len(normalized_sig):]
                    matched = True
                    break
            if not matched:
                temp_signals = temp_signals[1:]
                
        return original_text
    except Exception as e:
        return "解読できませんでした"

# --- 画面のレイアウト ---
tab1, tab2 = st.tabs(["🔒 暗号化モード", "🔓 解読モード"])

with tab1:
    user_input = st.text_input("暗号化したいアルファベットを入力：", value="hello", key="enc_input_field")
    if st.button("暗号化を計算する"):
        final_code = encrypt_process(user_input)
        if final_code:
            st.write("🎉 [完成] 暗号コード:")
            st.code(final_code, language="text")

with tab2:
    st.write("暗号化モードで生成されたコードをここに貼り付け、解読ボタンを押してください。")
    code_input = st.text_input(
        "解読コード入力欄", 
        key="dec_input_field",
        placeholder="ここに暗号コードをペーストしてください...",
        label_visibility="collapsed"
    )
    
    if st.button("パズルを解読する"):
        if code_input:
            decrypted_text = decrypt_process(code_input)
            st.success(f"🎉 解読された元の文字 ➔ **`{decrypted_text}`**")
        else:
            st.warning("コードを入力してください。")
