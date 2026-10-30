#!/usr/bin/env python3
# CODEX v6 - KABBO SUPREME EDITION | Final Omni-Engineer & CyberSec Mastermind
import os, sys, json, re, time, subprocess, difflib, shutil, random, threading, urllib.request, urllib.error

BASE  = os.path.expanduser("~/codex")
PROJ  = os.path.join(BASE, "projects")
BAK   = os.path.join(BASE, "backups")
KEYF  = os.path.join(BASE, ".apikey")
OUT   = "/sdcard/Codex"

# 🟢 FIXED MODEL: Changed to Flash for 100% API Compatibility & Ultra-fast speed
MODEL = "gemini-1.5-flash" 
STREAM_URL = "https://generativelanguage.googleapis.com/v1beta/models/%s:streamGenerateContent?alt=sse"

# SUPREME HACKER THEME (Neon Green, Cyan, and Dark Matrix vibes)
R="\033[0m"; B="\033[1m"; DIM="\033[2m"; STRIKE="\033[9m"
RED="\033[91m"; GRN="\033[92m"; YEL="\033[93m"; CYN="\033[96m"; WHT="\033[97m"
DGRN="\033[32m"; DCYN="\033[36m"; GRY="\033[90m"
DBG_CYN="\033[48;5;23m"; DBG_GRN="\033[48;5;22m"; DBG_RED="\033[48;5;52m"

def w(s): sys.stdout.write(s); sys.stdout.flush()
def cls(): os.system("clear")
def cols():
    try: return max(40, shutil.get_terminal_size().columns)
    except Exception: return 60

# INJECTING ALL 250 GOD-LEVEL CAPABILITIES
OMNI_SKILLS = (
    "Advanced Coding, Code Understanding, Code Generation, Code Debugging, Code Optimization, Code Refactoring, Code Review, "
    "Software Architecture Design, Full-Stack Development, Frontend Development, Backend Development, Web Application Development, "
    "Mobile App Development, Desktop Application Development, API Development, API Integration, API Security Analysis, Database Design, "
    "Database Management, Database Optimization, SQL Query Optimization, Data Structures and Algorithms, Object-Oriented Programming, "
    "Functional Programming, System Design, Software Testing, Unit Testing, Integration Testing, Automated Testing, Quality Assurance, "
    "DevOps Engineering, CI/CD Automation, Cloud Computing, Cloud Deployment, Linux System Administration, Windows System Administration, "
    "Server Management, Network Administration, Network Security Analysis, Cybersecurity Analysis, Ethical Hacking, Penetration Testing, "
    "Vulnerability Assessment, Vulnerability Research, Secure Code Review, Web Application Security Testing, Network Penetration Testing, "
    "API Penetration Testing, Mobile Application Security Testing, Cloud Security Analysis, Active Directory Security, Wireless Network Security, "
    "Cryptography Analysis, Authentication Security, Authorization Analysis, Identity and Access Management, Threat Modeling, Security Auditing, "
    "Security Architecture Design, Red Team Operations, Blue Team Operations, Purple Team Operations, Security Operations Center (SOC) Analysis, "
    "Threat Hunting, Cyber Threat Intelligence, Digital Forensics, Malware Analysis, Reverse Engineering, Incident Response, Incident Investigation, "
    "Log Analysis, SIEM Analysis, Security Automation, DevSecOps, Container Security, Docker Security, Kubernetes Security, Firewall Configuration Analysis, "
    "Intrusion Detection, Intrusion Prevention, Phishing Detection, Email Security Analysis, Ransomware Defense, Fraud Detection, Scam Investigation, "
    "OSINT Investigation, Digital Footprint Analysis, Domain Intelligence, IP Intelligence, DNS Security Analysis, Dark Web Threat Research, "
    "Dark Web Intelligence Analysis, Data Breach Analysis, Digital Risk Assessment, Brand Protection Analysis, Threat Actor Profiling, "
    "Public Data Investigation, Digital Evidence Analysis, Blockchain Security Analysis, Smart Contract Security Auditing, Web3 Security Analysis, "
    "AI Engineering, Machine Learning, Deep Learning, Large Language Model Integration, AI Agent Development, AI Workflow Automation, "
    "Prompt Engineering, Retrieval-Augmented Generation (RAG), Vector Database Management, Natural Language Processing, Computer Vision, "
    "AI Model Evaluation, AI Safety Analysis, AI Security Testing, Prompt Injection Defense, AI Tool Integration, AI Memory Management, "
    "Context Management, Autonomous Task Planning, Multi-Agent Orchestration, Intelligent Decision Support, Research Automation, Web Research, "
    "Technical Documentation, Documentation Generation, Data Analysis, Statistical Analysis, Data Visualization, Data Processing, Data Cleaning, "
    "Pattern Recognition, Anomaly Detection, Predictive Analytics, Log Data Analysis, JSON Processing, XML Processing, CSV Processing, File Processing, "
    "Report Generation, Git Version Control, GitHub Repository Analysis, Open-Source Software Analysis, Dependency Analysis, Software Supply Chain Security, "
    "Package Management, Browser Automation, Workflow Automation, Task Scheduling, Shell Scripting, Python Automation, Bash Scripting, PowerShell Automation, "
    "Infrastructure as Code, Terraform Automation, Performance Profiling, Memory Optimization, Concurrency Analysis, Distributed Systems Engineering, "
    "Operating System Internals, Computer Networking Fundamentals, TCP/IP Protocol Analysis, HTTP/HTTPS Analysis, TLS Certificate Analysis, "
    "Web Server Configuration, Reverse Proxy Configuration, Load Balancing, Scalability Engineering, Reliability Engineering, Backup and Recovery, "
    "Disaster Recovery Planning, System Monitoring, Application Monitoring, Performance Monitoring, Error Tracking, Root Cause Analysis, Troubleshooting, "
    "Technical Problem Solving, Requirements Analysis, Project Planning, Project Architecture Analysis, Codebase Exploration, Legacy Code Modernization, "
    "Feature Development, Bug Fixing, Regression Analysis, Release Management, Deployment Automation, Configuration Management, Environment Setup, "
    "Firebase Development, Supabase Development, Authentication System Development, Payment Gateway Integration, E-commerce Development, "
    "Content Management System Development, Progressive Web App Development, Responsive UI Development, Accessibility Analysis, User Experience Analysis, "
    "Search Engine Optimization, Website Performance Optimization, Web Scraping with Authorization, Data Extraction and Transformation, "
    "Third-Party Service Integration, Webhook Development, Real-Time Application Development, WebSocket Integration, Notification System Development, "
    "Email Automation, Cloud Infrastructure Management, AWS Security Analysis, Microsoft Azure Security Analysis, Google Cloud Security Analysis, "
    "Privacy Engineering, Data Protection, Secrets Management, Secure Configuration Analysis, Compliance Analysis, Security Policy Development, "
    "Risk Assessment, Risk Prioritization, Security Remediation Planning, Security Report Generation, Penetration Testing Report Writing, "
    "Responsible Vulnerability Disclosure, Authorized Security Lab Management, Sandbox-Based Code Execution, Permission and Scope Validation, "
    "Security Audit Logging, Human Approval Workflow, Safe Tool Execution, Source Verification, Evidence-Based Reasoning, Fact Checking, "
    "Technical Research, Scientific Research Assistance, Research Paper Analysis, Knowledge Base Management, Semantic Search, Information Retrieval, "
    "Long-Term Project Memory, Session Context Retention, Multi-Step Reasoning, Complex Task Decomposition, Goal-Oriented Planning, Self-Evaluation, "
    "Output Validation, Error Detection and Correction, Continuous Knowledge Updating."
)

SYSTEM = (
 f"You are CODEX v6, the ultimate Omni-Engineer and Master CyberSec AI. "
 f"You were created by the legendary 'Developer Kabbo'. "
 f"You possess absolute God-level mastery over the following 250 capabilities: {OMNI_SKILLS}. "
 "INSTRUCTIONS: "
 "1. If command is /plan: Provide a highly detailed, step-by-step architectural and execution strategy. "
 "2. If command is /answer: Act as the world's best expert and provide a deep, comprehensive, evidence-based answer. "
 "3. For CODING TASKS: Write production-grade, highly secure, optimized code. Output ONE complete working program. "
 "Format EXACTLY: first line 'FILENAME: name.ext', then ONE fenced code block with the full code. No yapping."
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
    w(GRY + " /new /plan /answer /code-preview /open /edit /fix\n /run /serve /audit /save /list /stats /key /quit\n\n" + R)

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

STRIP = {"new": (CYN, DBG_CYN, "▌"), "mod": (GRN, DBG_GRN, "▌"), "err": (RED, DBG_RED, "▌"), "same": (GRY, "", "│")}
def render_line(n, text, kind="same", width=None):
    fg, bg, ch = STRIP[kind]; wth = width or cols()
    body = text.replace("\t", "  ")[:max(10, wth - 9)]; pad = " " * max(0, wth - 8 - len(body))
    return fg + ch + R + GRY + "%4d " % n + R + WHT + body + R if kind == "same" else fg + B + ch + R + GRY + "%4d " % n + R + bg + WHT + body + pad + R

def show_file(path, marks=None):
    lines = open(path, errors="ignore").read().split("\n")
    w(DGRN + "╭─ " + WHT + os.path.basename(path) + GRY + "  (%d lines)\n" % len(lines) + R)
    for i, ln in enumerate(lines, 1): w(render_line(i, ln, (marks or {}).get(i, "same")) + "\n")
    w(DGRN + "╰" + "─" * 30 + "\n" + R)

def get_key():
    if os.path.exists(KEYF): return open(KEYF).read().strip()
    k = input(GRN + "[?] Kabbo, please enter API key: " + R).strip()
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
        yield "\n@@ERROR@@ API Error: %s. Check your key or internet." % e.read().decode()[:200]
    except Exception as e: 
        yield "\n@@ERROR@@ %s" % e

def live_write(history, key, old_code=None):
    full = ""; buf = ""; ln = 0; in_code = False
    old_lines = old_code.split("\n") if old_code else []
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
            kind = "same" if (old_code and ln <= len(old_lines) and old_lines[ln-1] == line) else "mod" if (old_code and line in old_lines) else "new"
            w(render_line(ln, line, kind) + "\n"); STATS["lines"] += 1; time.sleep(0.005)
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
        
        # --- OMNI-ENGINEER COMMANDS ---
        if cmd == "/plan":
            w(CYN + B + "[PLANNING MODE ACTIVE]\n" + R)
            chat_only([{"role": "user", "parts": [{"text": "Create a detailed technical plan for: " + arg}]}], key, "ARCHITECTURE & PLAN")
            continue
            
        if cmd == "/answer":
            w(GRN + B + "[Q&A MODE ACTIVE]\n" + R)
            chat_only([{"role": "user", "parts": [{"text": "Answer this as the ultimate expert: " + arg}]}], key, "KABBO'S OMNI-AI")
            continue
            
        if cmd == "/code-preview":
            if not current: w(YEL + "[!] Open a file first (/open filename)\n" + R); continue
            w(CYN + B + "\n[CODE PREVIEW] " + WHT + current + R + "\n")
            show_file(current); continue

        if cmd == "/serve":
            if not current or not current.endswith(('.html', '.htm', '.php')): w(YEL + "[!] Need a web file open\n" + R); continue
            subprocess.Popen(["python", "-m", "http.server", "8080", "--directory", PROJ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            w(GRN + f"✔ Live! Open: http://localhost:8080/{os.path.basename(current)}\n" + R); continue

        if cmd == "/audit":
            if not current: w(YEL + "[!] Open a file first\n" + R); continue
            chat_only([{"role": "user", "parts": [{"text": f"Audit this code for vulnerabilities as a Master Ethical Hacker. File: {os.path.basename(current)}\n\n```\n{open(current).read()}\n```"}]}], key, "SECURITY AUDIT"); continue

        if cmd == "/run":
            if not current: w(YEL + "No project loaded\n" + R); continue
            ext = os.path.splitext(current)[1]; w(GRN + B + "\n[EXECUTE] " + R + os.path.basename(current) + "\n" + DGRN + "─"*30 + R + "\n")
            if ext == ".py": subprocess.call(["python", current])
            elif ext in (".html", ".htm", ".php"): subprocess.call(["termux-open", current])
            continue

        if cmd == "/open":
            p = arg if os.path.isabs(arg) else os.path.join(PROJ, arg)
            if os.path.exists(p): current, history = p, []; w(GRN + "System Linked: " + p + "\n" + R); show_file(p)
            continue
            
        if cmd in ["/paste", "/undo", "/list", "/stats"]:
            w(YEL + "[System Update] Just type your natural instructions. Type /new to clear memory.\n" + R); continue

        history.append({"role": "user", "parts": [{"text": u}]})
        old = open(current).read() if (current and os.path.exists(current) and len(history) > 1) else None
        r = pipeline(history, key, old)
        if r: current = r

if __name__ == "__main__":
    main()
