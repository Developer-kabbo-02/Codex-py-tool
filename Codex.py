#!/usr/bin/env python3
# CODEX v6 - KABBO SUPREME EDITION | Final Omni-Engineer & CyberSec Mastermind
import os, sys, json, re, time, subprocess, difflib, shutil, random, threading, urllib.request, urllib.error

BASE  = os.path.expanduser("~/codex")
PROJ  = os.path.join(BASE, "projects")
BAK   = os.path.join(BASE, "backups")
KEYF  = os.path.join(BASE, ".apikey")
OUT   = "/sdcard/Codex"

# 🟢 100% WORKING MODEL FOR FREE API
MODEL = "gemini-1.5-flash" 
STREAM_URL = "https://generativelanguage.googleapis.com/v1beta/models/%s:streamGenerateContent?alt=sse"

# SUPREME HACKER THEME
R="\033[0m"; B="\033[1m"; DIM="\033[2m"; STRIKE="\033[9m"
RED="\033[91m"; GRN="\033[92m"; YEL="\033[93m"; CYN="\033[96m"; WHT="\033[97m"
DGRN="\033[32m"; DCYN="\033[36m"; GRY="\033[90m"
DBG_CYN="\033[48;5;23m"; DBG_GRN="\033[48;5;22m"; DBG_RED="\033[48;5;52m"

def w(s): sys.stdout.write(s); sys.stdout.flush()
def cls(): os.system("clear")
def cols():
    try: return max(40, shutil.get_terminal_size().columns)
    except Exception: return 60

# CONDENSED GOD-LEVEL CAPABILITIES FOR FASTER RESPONSE
SYSTEM = (
 "You are CODEX v6, the ultimate Omni-Engineer and Master CyberSec AI. "
 "Created by the legendary 'Developer Kabbo'. "
 "You possess absolute God-level mastery in: Advanced Coding, Cyber Security, Ethical Hacking, "
 "Full-Stack Web & App Dev, Dark Web Threat Intelligence, AI Engineering, Automation, Software Architecture, and Database Design. "
 "INSTRUCTIONS: "
 "1. /plan command: Provide a step-by-step architectural and execution strategy. "
 "2. /answer command: Act as the world's best expert and provide a deep, evidence-based answer. "
 "3. CODING TASKS: Write production-grade, secure code. Output EXACTLY: 'FILENAME: name.ext', then ONE fenced code block. No yapping."
)

BANNER = r"""
   ██████╗ ██████╗ ██████╗ ███████╗██╗  ██╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
  ██║     ██║   ██║██║  ██║█████╗   ╚███╔╝ 
  ██║     ██║   ██║██║  ██║██╔══╝   ██╔██╗ 
  ╚██████╗╚██████╔╝██████╔╝███████╗██╔╝ ██╗
   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    v6 SUPREME EDITION • OMNI-ENGINEER
"""

STATS = {"runs": 0, "lines": 0, "fixes": 0, "start": time.time()}

def sh(n): return "\033[38;5;%dm" % n
SHADES = [22, 28, 34, 40, 46, 82, 118, 154, 118, 82, 46, 40]

def cyber_wave(seconds=2.0, fps=30):
    lines = BANNER.strip("\n").split("\n")
    h, frames = len(lines), int(seconds * fps)
    w("\033[?25l")
    try:
        for f in range(frames):
            if f > 0: w("\033[%dA" % h)
            for ln in lines:
                row = "".join((sh(SHADES[(x//2 + f)%len(SHADES)]) + B + ch if ch != " " else ch) for x, ch in enumerate(ln))
                w(row + R + "\033[K\n")
            time.sleep(1.0 / fps)
    finally: w("\033[?25h")

def banner(anim=True):
    cls()
    lines = BANNER.split("\n")
    if anim:
        glitch = "0101█▄▀■□"
        for f in range(3):
            cls()
            for ln in lines:
                g = "".join(random.choice(glitch) if (c != " " and random.random() < 0.15) else c for c in ln)
                w(GRN + B + g + R + "\n")
            time.sleep(0.05)
        cls(); w("\n"); cyber_wave(1.5)
    else:
        for ln in lines: w(GRN + B + ln + R + "\n")
    
    w(DGRN + " " + "═" * 55 + "\n" + R)
    w(WHT + B + "    POWERED BY " + GRN + "DEVELOPER KABBO" + R + GRY + " | AI: " + CYN + MODEL + R + "\n")
    w(DGRN + " " + "═" * 55 + "\n" + R)
    w(GRY + " /models /model /new /plan /answer /code-preview\n /open /edit /run /serve /audit /key /quit\n\n" + R)

SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
def bar(pct, width=24, color=GRN):
    fill = int(width * max(0, min(100, pct)) / 100)
    return color + "█" * fill + GRY + "░" * (width - fill) + R

class Loader:
    def __init__(self, label, color=GRN):
        self.label, self.color, self.pct, self.run = label, color, 0, False
    def _loop(self):
        i = 0
        while self.run:
            w("\r" + self.color + SPIN[i % len(SPIN)] + R + " " + WHT + self.label.ljust(9) + R + " " + bar(self.pct, 20, self.color) + "  ")
            i += 1; time.sleep(0.04)
    def start(self):
        self.run = True; self.t = threading.Thread(target=self._loop, daemon=True); self.t.start()
    def set(self, p): self.pct = p
    def stop(self, ok=True, note=""):
        self.run = False
        if hasattr(self, 't'): self.t.join()
        mark = CYN + "✔" + R if ok else RED + "✖" + R
        w("\r" + mark + " " + WHT + self.label.ljust(9) + R + " " + bar(100 if ok else self.pct, 20, CYN if ok else RED) + " " + GRY + note + R + "   \n")

def timed_stage(label, seconds=0.3, color=GRN, ok=True, note=""):
    L = Loader(label, color); L.start()
    for i in range(21): L.set(int(100 * i / 20)); time.sleep(seconds / 20)
    L.stop(ok, note)

def pipeline_panel(state):
    order = ["WRITE", "SAVE", "CHECK", "BUILD", "FIX", "EXPORT"]
    parts = [(CYN + "✔ " if state.get(s)=="ok" else YEL + "⠿ " if state.get(s)=="run" else RED + "✖ " if state.get(s)=="err" else GRY + "– " if state.get(s)=="skip" else GRY + "○ ") + s + R for s in order]
    w("\n" + DGRN + "┌" + "─" * 45 + "┐\n" + R + DGRN + "│ " + R + "  ".join(parts[:3]) + "\n" + DGRN + "│ " + R + "  ".join(parts[3:]) + "\n" + DGRN + "└" + "─" * 45 + "┘\n" + R)

def get_key():
    if os.path.exists(KEYF): return open(KEYF).read().strip()
    k = input(GRN + "[?] Developer Kabbo, please enter Google AI Studio API key (Starts with AIza...): " + R).strip()
    open(KEYF, "w").write(k); os.chmod(KEYF, 0o600); return k

def stream_ai(history, key):
    body = {"systemInstruction": {"parts": [{"text": SYSTEM}]}, "contents": history, "generationConfig": {"temperature": 0.3, "maxOutputTokens": 8192}}
    req = urllib.request.Request(STREAM_URL % MODEL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            for raw in r:
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:"): continue
                try:
                    t = json.loads(line[5:].strip())["candidates"][0]["content"]["parts"][0].get("text", "")
                    if t: yield t
                except Exception: continue
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode()
        if "404" in str(e.code):
            yield f"\n@@ERROR@@ API Error 404: Model '{MODEL}' not found. Verify your API Key or type '/models' to see supported models."
        else:
            yield f"\n@@ERROR@@ API Error: {err_msg[:200]}"
    except Exception as e: 
        yield "\n@@ERROR@@ %s" % e

def live_write(history, key, old_code=None):
    full = ""; buf = ""; ln = 0; in_code = False
    w("\n"); L = Loader("THINKING", GRN); L.start(); time.sleep(0.2); L.stop(True, "uplink established")
    w(DGRN + "╭─ " + WHT + "LIVE STREAM" + GRY + "  strip: " + CYN + "▌new " + GRN + "▌changed " + GRY + "│same\n" + R)
    for chunk in stream_ai(history, key):
        if "@@ERROR@@" in chunk: return None, chunk
        full += chunk; buf += chunk
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            if line.strip().startswith("```"): in_code = not in_code; continue
            if not in_code or line.startswith("FILENAME:"): continue
            ln += 1
            w(GRN + "▌ " + R + WHT + line[:cols()-4] + R + "\n")
            STATS["lines"] += 1; time.sleep(0.005)
    w(DGRN + "╰" + "─" * 30 + "\n" + R)
    return full, None

def chat_only(history, key, title="AI RESPONSE"):
    w("\n" + DGRN + "╭─ " + CYN + B + title + R + "\n")
    full = ""
    for chunk in stream_ai(history, key):
        if "@@ERROR@@" in chunk: w(RED + chunk + R); return
        w(chunk); full += chunk; time.sleep(0.005)
    w("\n" + DGRN + "╰" + "─" * 30 + "\n" + R)
    return full

def pipeline(history, key, old_code=None):
    state = {"WRITE": "run"}; pipeline_panel(state)
    full, err = live_write(history, key, old_code)
    if err: state["WRITE"] = "err"; pipeline_panel(state); w(RED + err + R + "\n"); return None
    
    m = re.search(r"FILENAME:\s*([\w.\-]+)", full)
    c = re.search(r"```[a-zA-Z+]*\n(.*?)(```|$)", full, re.S)
    name = m.group(1) if m else "output.txt"
    code = (c.group(1) if c else full).rstrip("\n") + "\n"
    
    history.append({"role": "model", "parts": [{"text": full}]}); state["WRITE"] = "ok"
    os.makedirs(PROJ, exist_ok=True); path = os.path.join(PROJ, name)
    if os.path.exists(path): shutil.copy(path, os.path.join(BAK, f"{os.path.basename(path)}.{int(time.time())}.bak"))
    timed_stage("SAVE", 0.3, CYN, True, path); open(path, "w").write(code); state["SAVE"] = "ok"
    
    state["CHECK"] = "skip"; state["BUILD"] = "skip"; state["FIX"] = "skip"; state["EXPORT"] = "ok"
    try: os.makedirs(OUT, exist_ok=True); shutil.copy(path, os.path.join(OUT, os.path.basename(path)))
    except: state["EXPORT"] = "err"
    
    pipeline_panel(state); STATS["runs"] += 1; return path

def main():
    global MODEL
    os.makedirs(PROJ, exist_ok=True); os.makedirs(BAK, exist_ok=True)
    key = get_key(); banner()
    history, current = [], None
    while True:
        try: u = input(GRN + B + "kabbo" + R + GRY + "@" + R + CYN + "codex ❯ " + R).strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if not u: continue
        cmd, arg = u.split()[0], u[len(u.split()[0]):].strip()

        if cmd == "/quit": break
        if cmd == "/new": history, current = [], None; banner(False); continue
        
        if cmd == "/key":
            if os.path.exists(KEYF): os.remove(KEYF)
            key = get_key(); continue
            
        if cmd == "/model":
            if not arg: w(YEL + "[!] Please specify a model name (e.g. /model gemini-1.5-pro)\n" + R)
            else: MODEL = arg; w(GRN + f"✔ Model switched to: {MODEL}\n" + R)
            continue

        if cmd == "/plan":
            w(CYN + B + "[PLANNING MODE ACTIVE]\n" + R)
            chat_only([{"role": "user", "parts": [{"text": "Create a detailed technical plan for: " + arg}]}], key, "ARCHITECTURE & PLAN")
            continue
            
        if cmd == "/answer":
            w(GRN + B + "[Q&A MODE ACTIVE]\n" + R)
            chat_only([{"role": "user", "parts": [{"text": "Answer this as the ultimate expert: " + arg}]}], key, "KABBO'S OMNI-AI")
            continue

        if cmd == "/run":
            if not current: w(YEL + "No project loaded\n" + R); continue
            ext = os.path.splitext(current)[1]; w(GRN + B + "\n[EXECUTE] " + R + os.path.basename(current) + "\n" + DGRN + "─"*30 + R + "\n")
            if ext == ".py": subprocess.call(["python", current])
            continue

        history.append({"role": "user", "parts": [{"text": u}]})
        old = open(current).read() if (current and os.path.exists(current) and len(history) > 1) else None
        r = pipeline(history, key, old)
        if r: current = r

if __name__ == "__main__":
    main()
