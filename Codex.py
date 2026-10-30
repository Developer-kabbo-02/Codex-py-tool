#!/usr/bin/env python3
# CODEX v4 ARGON - Elite AI Code Engine & Ethical Hacker
import os, sys, json, re, time, subprocess, difflib, shutil, random, threading, urllib.request, urllib.error

BASE  = os.path.expanduser("~/codex")
PROJ  = os.path.join(BASE, "projects")
BAK   = os.path.join(BASE, "backups")
KEYF  = os.path.join(BASE, ".apikey")
OUT   = "/sdcard/Codex"
MODEL = "gemini-1.5-pro-latest" # High Thinking Level Model
STREAM_URL = "https://generativelanguage.googleapis.com/v1beta/models/%s:streamGenerateContent?alt=sse"

# ARGON THEME COLORS
R="\033[0m"; B="\033[1m"; DIM="\033[2m"; STRIKE="\033[9m"
RED="\033[91m"; GRN="\033[92m"; YEL="\033[93m"
CYN="\033[96m"; BLU="\033[94m"; PRP="\033[95m"; GRY="\033[90m"; WHT="\033[97m"
DCYN="\033[36m" # Dark Cyan for borders
DBG_CYN="\033[48;5;23m"; DBG_GRN="\033[48;5;22m"; DBG_YEL="\033[48;5;58m"; DBG_RED="\033[48;5;52m"

def w(s): sys.stdout.write(s); sys.stdout.flush()
def cls(): os.system("clear")
def cols():
    try: return max(40, shutil.get_terminal_size().columns)
    except Exception: return 60

# UPGRADED ELITE SYSTEM PROMPT
SYSTEM = (
 "You are CODEX v4 ARGON, an Elite Senior Software Engineer, Master Web Developer, and Top-Tier Ethical Hacker. "
 "Your thinking level is exceptionally high. You write production-grade, highly secure, modular, and flawlessly optimized code. "
 "As an ethical hacker, you proactively ensure all code is hardened against vulnerabilities (XSS, SQLi, CSRF, Buffer Overflows, etc.). "
 "Output ONE complete working program. Format EXACTLY: first line 'FILENAME: name.ext', "
 "then ONE fenced code block with the full code, nothing else after it. "
 "HTML: single file, inline CSS/JS, breathtaking modern UI, fully responsive. Python: stdlib only, highly optimized. "
 "C++: C++17, secure memory management. "
 "No placeholders, no explanations, always return the COMPLETE file."
)

BANNER = r"""
  ██████╗ ██████╗ ██████╗ ███████╗██╗  ██╗
 ██╔════╝██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
 ██║     ██║   ██║██║  ██║█████╗   ╚███╔╝ 
 ██║     ██║   ██║██║  ██║██╔══╝   ██╔██╗ 
 ╚██████╗╚██████╔╝██████╔╝███████╗██╔╝ ██╗
  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
        v4 ARGON • ELITE EDITION"""

STATS = {"runs": 0, "lines": 0, "fixes": 0, "start": time.time()}

# ---------- ARGON (Cyan/Blue) shading loop effects ----------
SHADES = [27, 33, 39, 45, 51, 87, 123, 87, 51, 45, 39, 33]
def sh(n): return "\033[38;5;%dm" % n

def shaded_banner_frame(lines, phase):
    out = []
    for ln in lines:
        row = ""
        for x, ch in enumerate(ln):
            if ch == " ": row += ch
            else: row += sh(SHADES[(x // 2 + phase) % len(SHADES)]) + B + ch
        out.append(row + R)
    return out

def color_wave(seconds=3.0, fps=14):
    lines = BANNER.strip("\n").split("\n")
    h = len(lines)
    frames = int(seconds * fps)
    w("\033[?25l")
    try:
        for f in range(frames):
            if f > 0: w("\033[%dA" % h)
            for row in shaded_banner_frame(lines, f):
                w(row + "\033[K\n")
            time.sleep(1.0 / fps)
    finally:
        w("\033[?25h")

def banner(anim=True):
    cls()
    lines = BANNER.split("\n")
    if anim:
        glitch = "▓▒░█▄▀■□"
        for f in range(5):
            cls()
            for ln in lines:
                g = "".join(random.choice(glitch) if (c != " " and random.random() < 0.3 * (4 - f) / 4) else c for c in ln)
                w(CYN + B + g + R + "\n")
            time.sleep(0.08)
        cls()
        w("\n")
        color_wave(2.6)
    else:
        for ln in lines: w(CYN + B + ln + R + "\n")
    w(DCYN + " " + "═" * 45 + "\n" + R)
    w(GRY + "  [ ELITE AI & ETHICAL HACKER ]  " + CYN + MODEL + R + "\n")
    w(DCYN + " " + "═" * 45 + "\n" + R)
    w(GRY + " /new /paste /open /show /edit /fix /run /audit\n /serve /save /undo /list /stats /key /quit\n\n" + R)

SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
def bar(pct, width=24, color=CYN):
    pct = max(0, min(100, pct))
    fill = int(width * pct / 100)
    return color + "█" * fill + GRY + "░" * (width - fill) + R + " %3d%%" % pct

class Loader:
    def __init__(self, label, color=CYN):
        self.label, self.color, self.pct = label, color, 0
        self.run = False; self.t = None
    def _loop(self):
        i = 0
        while self.run:
            w("\r" + self.color + SPIN[i % len(SPIN)] + R + " " + WHT + self.label.ljust(9) + R + " " + bar(self.pct, 20, self.color) + "  ")
            i += 1; time.sleep(0.08)
    def start(self):
        self.run = True
        self.t = threading.Thread(target=self._loop, daemon=True); self.t.start()
    def set(self, p): self.pct = p
    def stop(self, ok=True, note=""):
        self.run = False
        if self.t: self.t.join()
        mark = GRN + "✔" + R if ok else RED + "✖" + R
        w("\r" + mark + " " + WHT + self.label.ljust(9) + R + " " + bar(100 if ok else self.pct, 20, GRN if ok else RED) + " " + GRY + note + R + "   \n")

def timed_stage(label, seconds=0.6, color=CYN, ok=True, note=""):
    L = Loader(label, color); L.start()
    for i in range(21):
        L.set(int(100 * i / 20)); time.sleep(seconds / 20)
    L.stop(ok, note)

def pipeline_panel(state):
    order = ["WRITE", "SAVE", "CHECK", "BUILD", "FIX", "EXPORT"]
    parts = []
    for s in order:
        st = state.get(s, "wait")
        if st == "ok":    parts.append(GRN + "✔ " + s + R)
        elif st == "run": parts.append(YEL + "⠿ " + s + R)
        elif st == "err": parts.append(RED + "✖ " + s + R)
        elif st == "skip":parts.append(GRY + "– " + s + R)
        else:             parts.append(GRY + "○ " + s + R)
    w("\n" + DCYN + "┌" + "─" * 40 + "┐\n" + R)
    w(DCYN + "│ " + R + "  ".join(parts[:3]) + "\n")
    w(DCYN + "│ " + R + "  ".join(parts[3:]) + "\n")
    w(DCYN + "└" + "─" * 40 + "┘\n" + R)

STRIP = {
    "new":  (GRN, DBG_GRN, "▌"),
    "mod":  (CYN, DBG_CYN, "▌"),
    "err":  (RED, DBG_RED, "▌"),
    "same": (GRY, "",      "│"),
}
def render_line(n, text, kind="same", width=None):
    fg, bg, ch = STRIP[kind]
    width = width or cols()
    body = text.replace("\t", "  ")[:max(10, width - 9)]
    pad = " " * max(0, width - 8 - len(body))
    if kind == "same":
        return fg + ch + R + GRY + "%4d " % n + R + WHT + body + R
    return fg + B + ch + R + GRY + "%4d " % n + R + bg + WHT + body + pad + R

def show_file(path, marks=None, start=1, end=None):
    marks = marks or {}
    lines = open(path, errors="ignore").read().split("\n")
    end = end or len(lines)
    w(DCYN + "╭─ " + WHT + os.path.basename(path) + GRY + "  (%d lines)\n" % len(lines) + R)
    for i in range(start, min(end, len(lines)) + 1):
        w(render_line(i, lines[i-1], marks.get(i, "same")) + "\n")
    w(DCYN + "╰" + "─" * 30 + "\n" + R)

def get_key():
    if os.path.exists(KEYF): return open(KEYF).read().strip()
    k = input(CYN + "[?] API key paste karein: " + R).strip()
    open(KEYF, "w").write(k); os.chmod(KEYF, 0o600)
    return k

def stream_ai(history, key):
    body = {"systemInstruction": {"parts": [{"text": SYSTEM}]},
            "contents": history,
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 8192}}
    req = urllib.request.Request(STREAM_URL % MODEL, data=json.dumps(body).encode(),
          headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            for raw in r:
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:"): continue
                try:
                    d = json.loads(line[5:].strip())
                    t = d["candidates"][0]["content"]["parts"][0].get("text", "")
                    if t: yield t
                except Exception: continue
    except urllib.error.HTTPError as e:
        yield "\n@@ERROR@@ %s %s" % (e.code, e.read().decode()[:300])
    except Exception as e:
        yield "\n@@ERROR@@ %s" % e

def extract(text):
    name = "output.txt"
    m = re.search(r"FILENAME:\s*([\w.\-]+)", text)
    if m: name = m.group(1)
    c = re.search(r"```[a-zA-Z+]*\n(.*?)(```|$)", text, re.S)
    code = c.group(1) if c else text
    return name, code.rstrip("\n") + "\n"

def live_write(history, key, old_code=None):
    full = ""; buf = ""; ln = 0; in_code = False
    old_lines = old_code.split("\n") if old_code else []
    w("\n")
    L = Loader("THINKING", CYN); L.start()
    time.sleep(0.4)
    L.stop(True, "stream started")
    w(DCYN + "╭─ " + WHT + "LIVE CODE" + GRY + "  strip: " + GRN + "▌new " + CYN + "▌changed " + GRY + "│same\n" + R)
    for chunk in stream_ai(history, key):
        if "@@ERROR@@" in chunk: return None, chunk
        full += chunk; buf += chunk
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            if line.strip().startswith("```"):
                in_code = not in_code; continue
            if not in_code or line.startswith("FILENAME:"): continue
            ln += 1
            if old_code is None: kind = "new"
            elif ln <= len(old_lines) and old_lines[ln-1] == line: kind = "same"
            elif line in old_lines: kind = "mod"
            else: kind = "new"
            w(render_line(ln, line, kind) + "\n")
            STATS["lines"] += 1
            time.sleep(0.01)
    w(DCYN + "╰" + "─" * 30 + "\n" + R)
    return full, None

def chat_only(history, key):
    w("\n" + DCYN + "╭─ " + CYN + B + "SECURITY AUDIT & REPORT" + R + "\n")
    full = ""
    for chunk in stream_ai(history, key):
        if "@@ERROR@@" in chunk: w(RED + chunk + R); return
        w(chunk)
        full += chunk
    w("\n" + DCYN + "╰" + "─" * 30 + "\n" + R)
    return full

def show_diff(old, new):
    o, n = old.split("\n"), new.split("\n")
    sm = difflib.SequenceMatcher(None, o, n)
    added = removed = 0
    w("\n" + DCYN + "╭─ " + WHT + "DIFF" + GRY + "  (old vs new)\n" + R)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": continue
        for k, x in enumerate(o[i1:i2]):
            w(RED + B + "▌" + R + GRY + "%4d " % (i1 + k + 1) + R + DBG_RED + RED + STRIKE + x[:cols()-9] + R + "\n"); removed += 1
        for k, x in enumerate(n[j1:j2]):
            w(GRN + B + "▌" + R + GRY + "%4d " % (j1 + k + 1) + R + DBG_GRN + WHT + x[:cols()-9] + R + "\n"); added += 1
        time.sleep(0.01)
    w(DCYN + "╰" + R + GRY + " +%d / -%d lines\n" % (added, removed) + R)

def parse_error_lines(log, path):
    base = os.path.basename(path)
    nums = set()
    for m in re.finditer(r'File "[^"]*%s", line (\d+)' % re.escape(base), log): nums.add(int(m.group(1)))
    for m in re.finditer(r"%s:(\d+):(\d+)?" % re.escape(base), log): nums.add(int(m.group(1)))
    return sorted(nums)

def debug_view(path, log):
    nums = parse_error_lines(log, path)
    lines = open(path, errors="ignore").read().split("\n")
    w("\n" + RED + B + "╭─ DEBUGGER " + R + GRY + "error lines: " + (", ".join(map(str, nums)) or "n/a") + "\n" + R)
    if nums:
        shown = set()
        for e in nums[:4]:
            for i in range(max(1, e - 2), min(len(lines), e + 2) + 1):
                if i in shown: continue
                shown.add(i)
                w(render_line(i, lines[i-1], "err" if i == e else "same") + "\n")
                if i == e:
                    msg = next((ln.strip() for ln in log.split("\n") if "error" in ln.lower()), "")
                    w(RED + " " * 6 + "└─► " + msg[:cols()-12] + R + "\n")
            w(GRY + "  ···\n" + R)
    else:
        for ln in log.strip().split("\n")[:12]:
            c = RED if ("error" in ln.lower() or "Traceback" in ln) else YEL if "warning" in ln.lower() else GRY
            w(RED + "▌" + R + " " + c + ln[:cols()-4] + R + "\n")
    w(RED + "╰" + "─" * 30 + "\n" + R)

def check_only(path):
    ext = os.path.splitext(path)[1]
    if ext == ".py":
        p = subprocess.run(["python", "-m", "py_compile", path], capture_output=True, text=True)
        return (p.returncode == 0), p.stderr
    if ext == ".cpp":
        p = subprocess.run(["clang++", "-std=c++17", "-fsyntax-only", "-Wall", path], capture_output=True, text=True)
        return (p.returncode == 0), p.stderr
    if ext in (".html", ".htm"):
        src = open(path, errors="ignore").read(); low = src.lower(); probs = []
        if "<html" not in low: probs.append("%s:1: error: <html> tag missing" % os.path.basename(path))
        for t in ("script", "style", "body", "div"):
            a, b = low.count("<" + t), low.count("</" + t + ">")
            if a != b: probs.append("%s:1: error: <%s> tags unbalanced (%d open, %d close)" % (os.path.basename(path), t, a, b))
        return (not probs), "\n".join(probs)
    return True, ""

def build(path):
    ext = os.path.splitext(path)[1]
    if ext == ".py":
        try:
            p = subprocess.run(["python", path], capture_output=True, text=True, timeout=5, input="")
            if p.returncode and "Traceback" in p.stderr: return False, p.stderr
        except subprocess.TimeoutExpired: pass
        return True, ""
    if ext == ".cpp":
        p = subprocess.run(["clang++", "-std=c++17", "-Wall", path, "-o", path[:-4]], capture_output=True, text=True)
        return (p.returncode == 0), p.stderr
    return True, ""

def backup(path):
    if os.path.exists(path):
        os.makedirs(BAK, exist_ok=True)
        dst = os.path.join(BAK, "%s.%d.bak" % (os.path.basename(path), int(time.time())))
        shutil.copy(path, dst); return dst

def export(path):
    L = Loader("EXPORT", GRN); L.start()
    try:
        os.makedirs(OUT, exist_ok=True)
        dst = os.path.join(OUT, os.path.basename(path))
        for i in range(0, 101, 10): L.set(i); time.sleep(0.03)
        shutil.copy(path, dst)
        L.stop(True, dst)
        return True
    except Exception:
        L.stop(False, "termux-setup-storage chalayein")
        return False

def pipeline(history, key, old_code=None):
    state = {"WRITE": "run"}; pipeline_panel(state)
    full, err = live_write(history, key, old_code)
    if err:
        state["WRITE"] = "err"; pipeline_panel(state); w(RED + err + R + "\n"); return None
    name, code = extract(full)
    history.append({"role": "model", "parts": [{"text": full}]})
    state["WRITE"] = "ok"
    if old_code is not None: show_diff(old_code, code)

    os.makedirs(PROJ, exist_ok=True); path = os.path.join(PROJ, name)
    backup(path); timed_stage("SAVE", 0.4, GRN, True, path)
    open(path, "w").write(code); state["SAVE"] = "ok"

    ok = False
    for attempt in range(1, 4):
        timed_stage("CHECK", 0.6, CYN, True, "syntax scan")
        ok, log = check_only(path)
        if ok:
            state["CHECK"] = "ok"; L = Loader("BUILD", CYN); L.start()
            for i in range(0, 101, 5): L.set(i); time.sleep(0.03)
            ok, log = build(path); L.stop(ok, "compile/interpret")
            if ok: state["BUILD"] = "ok"; break
            state["BUILD"] = "err"
        else: state["CHECK"] = "err"
        debug_view(path, log)
        state["FIX"] = "run"; STATS["fixes"] += 1
        w(YEL + "[FIX] AI Auto-Hacker is fixing the bug (attempt %d/3)\n" % attempt + R)
        history.append({"role": "user", "parts": [{"text": "Yeh error aaya. Poori fixed file do (same format):\n" + log[:1800]}]})
        old = code; full, err = live_write(history, key, old)
        if err: state["FIX"] = "err"; w(RED + err + R + "\n"); break
        history.append({"role": "model", "parts": [{"text": full}]})
        _, code = extract(full); show_diff(old, code)
        open(path, "w").write(code); state["FIX"] = "ok"
    
    if ok: w(GRN + B + "\n✔ PASS: All checks clear. Code is secure.\n" + R)
    else: w(YEL + "\n⚠ 3 attempts failed. Use /edit or /fix to retry.\n" + R)
    
    if not state.get("BUILD"): state["BUILD"] = "skip" if ok else "err"
    state["EXPORT"] = "ok" if export(path) else "err"
    pipeline_panel(state); STATS["runs"] += 1
    return path

def run_file(path):
    ext = os.path.splitext(path)[1]
    w(CYN + B + "\n[EXEC] " + R + os.path.basename(path) + "\n" + DCYN + "─" * 30 + R + "\n")
    try:
        if ext == ".py": subprocess.call(["python", path])
        elif ext == ".cpp":
            exe = path[:-4]
            if not os.path.exists(exe): build(path)
            subprocess.call([exe])
        elif ext in (".html", ".htm"): subprocess.call(["termux-open", path])
    except Exception as e: w(RED + str(e) + R + "\n")

def multiline(prompt):
    w(YEL + prompt + "\n(khatam karne ke liye nayi line par END)\n" + R)
    out = []
    while True:
        try: l = input()
        except EOFError: break
        if l.strip() == "END": break
        out.append(l)
    return "\n".join(out) + "\n"

def stats():
    up = int(time.time() - STATS["start"])
    w(DCYN + "╭─ " + WHT + "ELITE STATS\n" + R)
    w(GRY + "│ runs: " + WHT + str(STATS["runs"]) + GRY + "  lines written: " + WHT + str(STATS["lines"]) +
      GRY + "  auto-fixes: " + WHT + str(STATS["fixes"]) + GRY + "  uptime: " + WHT + "%ds\n" % up + R)
    w(DCYN + "╰" + "─" * 30 + "\n" + R)

def main():
    os.makedirs(PROJ, exist_ok=True); os.makedirs(BAK, exist_ok=True)
    key = get_key(); banner()
    history, current = [], None
    while True:
        try: u = input(CYN + B + "argon" + R + GRY + "@codex" + R + CYN + " ❯ " + R).strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if not u: continue
        cmd, arg = u.split()[0], u[len(u.split()[0]):].strip()

        if cmd == "/quit": break
        if cmd == "/new": history, current = [], None; banner(False); continue
        if cmd == "/stats": stats(); continue
        if cmd == "/key":
            if os.path.exists(KEYF): os.remove(KEYF)
            key = get_key(); continue
        if cmd == "/list":
            for f in sorted(os.listdir(PROJ)): w("  " + CYN + f + GRY + "  %d B\n" % os.path.getsize(os.path.join(PROJ, f)) + R)
            continue
        if cmd == "/show":
            p = current if not arg else (arg if os.path.isabs(arg) else os.path.join(PROJ, arg))
            if p and os.path.exists(p): show_file(p)
            else: w(YEL + "File nahi mili\n" + R)
            continue
        
        # --- NEW WEB DEVELOPER FEATURE ---
        if cmd == "/serve":
            if not current or not current.endswith(('.html', '.htm')):
                w(YEL + "[!] Pehle koi HTML file open karein (/open file.html)\n" + R); continue
            w(CYN + "▶ Starting Local Development Server on port 8080...\n" + R)
            subprocess.Popen(["python", "-m", "http.server", "8080", "--directory", PROJ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            w(GRN + f"✔ Server Running! Open your browser at: http://localhost:8080/{os.path.basename(current)}\n" + R)
            continue

        # --- NEW ETHICAL HACKER FEATURE ---
        if cmd == "/audit":
            if not current: w(YEL + "[!] Pehle file open karein\n" + R); continue
            code = open(current).read()
            audit_hist = [{"role": "user", "parts": [{"text": f"Act as an Elite Ethical Hacker and Senior Security Auditor. Audit the following code for vulnerabilities (XSS, SQLi, Buffer Overflows, Logic flaws). Provide a detailed professional security report. File: {os.path.basename(current)}\n\n```\n{code}\n```"}]}]
            w(PRP + B + "[AUDIT] Initiating Deep Security Scan...\n" + R)
            chat_only(audit_hist, key)
            continue

        if cmd == "/run":
            run_file(current) if current else w(YEL + "Pehle project banayein\n" + R); continue
        if cmd == "/save":
            export(current) if current else w(YEL + "Koi file nahi\n" + R); continue
        if cmd == "/open":
            p = arg if os.path.isabs(arg) else os.path.join(PROJ, arg)
            if os.path.exists(p):
                current = p; history = []
                w(GRN + "Loaded: " + p + "\n" + R); show_file(p)
            else: w(RED + "File nahi mili\n" + R)
            continue
        if cmd == "/paste":
            code = multiline("[PASTE] apna code paste karein")
            name = input(CYN + "[?] filename (jaise app.py): " + R).strip() or "pasted.py"
            current = os.path.join(PROJ, name)
            open(current, "w").write(code)
            w(GRN + "Saved: %s (%d lines)\n" % (current, code.count("\n")) + R)
            history = []; show_file(current); continue
        if cmd == "/undo":
            if not current: w(YEL + "Koi file nahi\n" + R); continue
            baks = sorted([f for f in os.listdir(BAK) if f.startswith(os.path.basename(current) + ".")])
            if not baks: w(YEL + "Koi backup nahi\n" + R); continue
            shutil.copy(os.path.join(BAK, baks[-1]), current)
            os.remove(os.path.join(BAK, baks[-1]))
            w(GRN + "Wapas restore: " + baks[-1] + "\n" + R); continue
        if cmd == "/fix":
            if not current: w(YEL + "Pehle /open ya /paste\n" + R); continue
            ok, log = check_only(current)
            if ok: ok, log = build(current)
            if ok: w(GRN + "✔ koi error nahi mila\n" + R); continue
            debug_view(current, log); old = open(current).read()
            history = [{"role": "user", "parts": [{"text": "FILENAME: %s\nCode:\n```\n%s```\nError:\n%s\nPoori fixed file do (same format)." % (os.path.basename(current), old, log[:1800])}]}]
            r = pipeline(history, key, old)
            if r: current = r
            continue
        if cmd == "/edit":
            if not current: w(YEL + "Pehle /open ya /paste\n" + R); continue
            req = arg or input(CYN + "[?] kya change karna hai: " + R)
            old = open(current).read()
            history = [{"role": "user", "parts": [{"text": "FILENAME: %s\nExisting code:\n```\n%s```\nIsme yeh change karo aur poori updated file do:\n%s" % (os.path.basename(current), old, req)}]}]
            r = pipeline(history, key, old)
            if r: current = r
            continue

        history.append({"role": "user", "parts": [{"text": u}]})
        old = open(current).read() if (current and os.path.exists(current) and len(history) > 1) else None
        r = pipeline(history, key, old)
        if r: current = r
        w(GRY + "\nTip: Try /audit for security check, or /serve to test HTML locally.\n" + R)

if __name__ == "__main__":
    main()
