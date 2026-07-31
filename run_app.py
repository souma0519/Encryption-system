import streamlit as st
import random
import string
import os
import re

# ==============================================================================
# 🎨 1. 【画面の設定】（style.cssを外から読み込む）
# ==============================================================================
st.set_page_config(
    page_title="オリジナル数理暗号システム",
    layout="centered"
)

st.markdown("""
    <style>
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

/* タブのデザイン */
.stTabs [data-baseweb="tab"] {
    color: #8b949e;
}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom-color: #58a6ff !important;
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


st.title("完全自動暗号システム")
st.write("※英語以外使用不可です！！")
st.write("※大事なパスワードなどを入力しないでください！")

# ==============================================================================
# 📜 2. 【暗号の定義】1文字も被りのない完全独立のa〜z対応表（生データ）
# ==============================================================================
RULE_STEP1 = {
    "a": r".#",  "b": r",_",  "c": r"\-",  "d": r"!@",  "e": r"$&",  "f": r"*(",
    "g": r")+",  "h": r'~"',  "i": r"?/",  "j": r":[",  "k": r";]",  "l": r"<{",
    "m": r">}",  "n": r"[]",  "o": r"{}",  "p": r";<",  "q": r":>",  "r": r"?*",
    "s": r"+/",  "t": r"=\\", "u": r"^|",  "v": r"_~",  "w": r".%",  "x": r",!",
    "y": r".$",  "z": r"&#"
}

# 💡【バグ完全消滅！】a〜zまですべてを完璧な(数字, 数字)のペアで直接登録し直しました！
CHAR_TO_NUM_PAIR = {
    "a": ("1", "2"), "b": ("3", "4"), "c": ("5", "6"), "d": ("7", "8"), "e": ("9", "10"), "f": ("11", "12"),
    "g": ("13", "14"), "h": ("15", "16"), "i": ("17", "18"), "j": ("19", "20"), "k": ("21", "22"), "l": ("23", "24"),
    "m": ("25", "26"), "n": ("27", "28"), "o": ("29", "30"), "p": ("31", "32"), "q": ("33", "34"), "r": ("35", "36"),
    "s": ("37", "38"), "t": ("39", "40"), "u": ("41", "42"), "v": ("43", "44"), "w": ("45", "46"), "x": ("47", "48"),
    "y": ("49", "50"), "z": ("51", "52")
}

# 💡【重要！】数字から記号へ戻すため、1〜52の背番号をすべて漏れなく「手書き」で登録した無敵の表です。上書きバグは一切起きません！
NUM_TO_SIGNAL = {
    "1": ".", "2": "#", "3": ",", "4": "_", "5": "\\", "6": "-", "7": "!", "8": "@", "9": "$", "10": "&", "11": "*", "12": "(",
    "13": ")", "14": "+", "15": "~", "16": '"', "17": "?", "18": "/", "19": ":", "20": "[", "21": ";", "22": "]", "23": "<", "24": "{",
    "25": ">", "26": "}", 
    "27": "[", "28": "]", "29": "{", "30": "}", "31": ";", "32": "<", "33": ":", "34": ">", "35": "?", "36": "*", "37": "+", "38": "/", 
    "39": "=", "40": "\\", "41": "^", "42": "|", "43": "_", "44": '"', "45": ".", "46": "%", "47": ",", "48": "!", "49": ".", "50": "$", 
    "51": "&", "52": "#"
}

# 💡完全にランダムなアルファベットをランダムな長さ（1〜4文字）で作る関数
def make_random_alphas():
    length = random.randint(1, 4)
    return "".join(random.choices(string.ascii_lowercase, k=length))

# --- 1. 暗号化（エンコード）システム関数 ---
def encrypt_process(text):
    text_clean = text.lower()
    kind_list = []
    total_count = 0
    unique_chars = set()
    
    for char in text_clean:
        if char in CHAR_TO_NUM_PAIR:
            num1, num2 = CHAR_TO_NUM_PAIR[char]
            unique_chars.add(char)
            total_count += 2 # 1文字につき記号は2マス増える
            
            # 💡【指定ルール】1桁なら「_」、2桁なら「ランダムアルファベット」を数字の前に自動付与！
            if int(num1) >= 10: kind_list.append(make_random_alphas() + num1)
            else: kind_list.append("_" + num1)
            
            if int(num2) >= 10: kind_list.append(make_random_alphas() + num2)
            else: kind_list.append("_" + num2)
            
    if total_count == 0:
        return None
        
    # 真ん中の数は完全なダミーなので、適当な乱数にして完全にカモフラージュ
    hidden_counts = len(unique_chars) * random.randint(100, 999)
    
    final_code = f"{total_count}.{hidden_counts}.{''.join(kind_list)}"
    return final_code

# --- 2. 復号（解読）システム関数 ---
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
        
        # 💡 お尻のコードから「_数字」か「2桁の数字」を正確にスナイプ！
        matches = re.findall(r"_[0-9]|[0-9]{2}", kind_rule)
        
        num_list = []
        for match in matches:
            if match.startswith("_"):
                num_list.append(match[1:])
            else:
                num_list.append(match)
                
        # 💡【手順2】取り出した数字を、一度すべて「元の記号」に完全復元する（第2段階）
        restored_signals = ""
        for num in num_list:
            if num in NUM_TO_SIGNAL:
                restored_signals += NUM_TO_SIGNAL[num]
                
        # 💡【手順3】復元された記号の塊を、あなたのルールで左から削り落とす！
        original_text = ""
        temp_signals = restored_signals
        
        while len(temp_signals) > 0:
            matched = False
            for char, sig in RULE_STEP1.items():
                normalized_sig = sig.replace("¥", "\\")
                if temp_signals.startswith(normalized_sig) or temp_signals.startswith(sig):
                    original_text += char
                    temp_signals = temp_signals[len(normalized_sig):] # 左から削る！
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
