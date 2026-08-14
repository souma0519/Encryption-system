import html
import json
import random
import re
import string
from http.server import BaseHTTPRequestHandler

RULE_STEP1 = {
    "a": r".#", "b": r",_", "c": r"\-", "d": r"!@", "e": r"$&", "f": r"*(",
    "g": r")+", "h": r'~"', "i": r"?/", "j": r":[", "k": r";]", "l": r"<{",
    "m": r">}", "n": r"[]", "o": r"{}", "p": r";<", "q": r":>", "r": r"?*",
    "s": r"+/", "t": r"=\\", "u": r"^|", "v": r"_~", "w": r".%", "x": r",!",
    "y": r".$", "z": r"&#",
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
    ".": "49", "$": "50", "&": "51", "#": "52",
}
NUM_TO_SIGNAL = {value: key for key, value in SIGNAL_TO_NUM.items()}
NUM_TO_SIGNAL["5"] = "\\"


def make_random_alphas():
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 4)))


def encrypt_process(text):
    signal_list = []
    for char in text.lower():
        if char in RULE_STEP1:
            signal_list.append(RULE_STEP1[char].replace("¥", "\\"))
    if not signal_list:
        return None
    kind_list = []
    seen_signals = []
    for word_signal in signal_list:
        for signal in word_signal:
            if signal in SIGNAL_TO_NUM:
                number = SIGNAL_TO_NUM[signal]
                if signal not in seen_signals:
                    seen_signals.append(signal)
                if int(number) >= 10:
                    kind_list.append(make_random_alphas() + number)
                else:
                    kind_list.append("_" + number)
    combined_signals = "".join(signal_list)
    ones_number = int("1" * len(seen_signals)) if seen_signals else 1
    hidden_counts = ones_number * random.randint(100, 999)
    return f"{len(combined_signals)}.{hidden_counts}.{''.join(kind_list)}"


def decrypt_process(code):
    try:
        parts = str(code).strip().replace("¥", "\\").split(".")
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
        temporary = restored_signals
        while temporary:
            for char, signal in RULE_STEP1.items():
                normalized = signal.replace("¥", "\\")
                if temporary.startswith(normalized):
                    original_text += char
                    temporary = temporary[len(normalized):]
                    break
            else:
                temporary = temporary[1:]
        return original_text
    except Exception:
        return "解読できませんでした"


PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>オリジナル数理暗号システム</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#f0f6fc;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}main{max-width:720px;margin:0 auto;padding:48px 20px}h1{color:#58a6ff;font-weight:400;margin:0 0 12px}p{color:#8b949e}.warning{border:1px solid #9e6a03;background:#1c1708;color:#e3b341;padding:14px;border-radius:8px;margin:22px 0}.tabs{display:flex;gap:8px;margin:28px 0 16px}.tab{flex:1;padding:12px;border:1px solid #30363d;border-radius:7px;background:#161b22;color:#c9d1d9;cursor:pointer}.tab.active{border-color:#58a6ff;color:#58a6ff}section{display:none;background:#161b22;border:1px solid #30363d;border-radius:10px;padding:20px}.active-panel{display:block}label{display:block;margin:0 0 8px;color:#c9d1d9}input{width:100%;padding:12px;background:#0d1117;color:#f0f6fc;border:1px solid #30363d;border-radius:6px;font-size:16px}button.action{width:100%;margin-top:14px;padding:12px;border:0;border-radius:6px;background:#1f6feb;color:white;font-weight:600;cursor:pointer}button.action:hover{background:#388bfd}.result{margin-top:18px;padding:14px;background:#0d1117;border-radius:6px;word-break:break-all}.error{color:#f85149}
</style></head><body><main><h1>中1開発：完全自動暗号化システム</h1><p>英語のアルファベットを独自ルールで変換します。</p><div class="warning">この仕組みは学習用のオリジナル暗号です。大事なパスワードや個人情報は入力しないでください。</div>
<div class="tabs"><button class="tab active" data-target="encrypt">暗号化モード</button><button class="tab" data-target="decrypt">解読モード</button></div>
<section id="encrypt" class="active-panel"><label for="enc">暗号化したいアルファベット</label><input id="enc" value="hello" autocomplete="off"><button class="action" onclick="run('encrypt')">暗号化を計算する</button><div id="enc-result"></div></section>
<section id="decrypt"><label for="dec">暗号コード</label><input id="dec" placeholder="暗号コードをペーストしてください..." autocomplete="off"><button class="action" onclick="run('decrypt')">パズルを解読する</button><div id="dec-result"></div></section>
</main><script>
document.querySelectorAll('.tab').forEach(tab=>tab.onclick=()=>{document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.querySelectorAll('section').forEach(x=>x.classList.remove('active-panel'));tab.classList.add('active');document.getElementById(tab.dataset.target).classList.add('active-panel')});
async function run(mode){
  const value=document.getElementById(mode==='encrypt'?'enc':'dec').value;
  const box=document.getElementById(mode+'-result');
  box.textContent='処理中…';
  try {
    const response=await fetch('/api/index.py',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:mode,value:value})});
    const data=await response.json();
    box.textContent='';
    const result=document.createElement('div');
    result.className='result';
    if(data.result){
      result.textContent=(mode==='encrypt'?'完成した暗号コード: ':'解読された元の文字: ')+data.result;
    }else{
      result.className='result error';
      result.textContent=data.error||'処理に失敗しました。';
    }
    box.appendChild(result);
  } catch(error) {
    box.className='result error';
    box.textContent='通信エラーが発生しました。ページを再読み込みしてください。';
  }
}
</script></body></html>"""


class handler(BaseHTTPRequestHandler):
    def _send(self, body, status=200, content_type="text/html; charset=utf-8"):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        self._send(PAGE)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            mode, value = payload.get("mode"), payload.get("value", "")
            result = encrypt_process(value) if mode == "encrypt" else decrypt_process(value) if mode == "decrypt" else None
            response = {"result": result} if result else {"error": "入力を確認してください。"}
            self._send(json.dumps(response, ensure_ascii=False), content_type="application/json; charset=utf-8")
        except (ValueError, TypeError, json.JSONDecodeError):
            self._send(json.dumps({"error": "不正なリクエストです。"}, ensure_ascii=False), 400, "application/json; charset=utf-8")
