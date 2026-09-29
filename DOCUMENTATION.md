# 🎙️ Voice Bot — Full Documentation

*A talking assistant that listens to your voice, thinks, and talks back — and can even open apps and text people on WhatsApp for you.*

> This guide explains **everything** in simple words. If you're in class 10 and have never coded before, you'll still understand it. No prior knowledge needed — we explain each new word the first time it appears.

---

## 📖 Table of Contents

1. [What is this thing?](#1-what-is-this-thing)
2. [What can it do?](#2-what-can-it-do)
3. [How do I talk to it? (Example commands)](#3-how-do-i-talk-to-it)
4. [The two ways to use it](#4-the-two-ways-to-use-it)
5. [How it works — the journey of your voice](#5-how-it-works--the-journey-of-your-voice)
6. [The tech stack (all the tools we use)](#6-the-tech-stack)
7. [The files in this project](#7-the-files-in-this-project)
8. [How to set it up (step by step)](#8-how-to-set-it-up)
9. [The settings file (.env) explained](#9-the-settings-file-env-explained)
10. [When things go wrong (troubleshooting)](#10-troubleshooting)
11. [Safety and privacy](#11-safety-and-privacy)
12. [Dictionary of tricky words](#12-dictionary-of-tricky-words)

---

## 1. What is this thing?

Imagine **Alexa** or **Google Assistant**, but one that *you* built and that runs on *your own* computer.

You speak to it. It understands what you said, figures out an answer (using a very smart AI brain on the internet), and then **speaks the answer back to you** in a human-like voice.

But it does more than just answer questions. It can also **do jobs for you** — like opening YouTube, opening Notepad, or sending a WhatsApp message to your mom — just because you *told it to with your voice*.

Think of it as a helpful robot assistant that lives inside your computer and listens through your microphone. 🤖

## 2. What can it do?

Here's the full list of its superpowers:

| # | Superpower | What it means in plain words |
|---|-----------|------------------------------|
| 1 | 🎧 **Hears you** | It records your voice from the microphone and turns your speech into text. |
| 2 | 🧠 **Answers questions** | It sends your question to a powerful AI brain (Amazon's "Nova" AI) and gets a smart answer. |
| 3 | 🌐 **Searches the web** | Before answering, it can quickly Google-like search the internet so its answers are fresh and correct (great for "what's the latest news?"). |
| 4 | 🗣️ **Talks back** | It reads the answer out loud in a natural **female voice**. |
| 5 | 🚀 **Opens apps & websites** | Say "open YouTube / Gmail / Notepad / LinkedIn / GitHub / Slack / VS Code" and it opens them. |
| 6 | ▶️ **Plays YouTube videos** | Say "play lofi music on YouTube" and it starts playing it. |
| 7 | 💬 **Texts people on WhatsApp** | Say "text mumma hii" and it opens WhatsApp and sends "hii" to your mom — by name, to *anyone* in your contacts. |
| 8 | 🖥️ **Two faces** | You can use it in a plain **terminal** (text screen) *or* in a pretty **web page** with a mic button you tap. |

---

## 3. How do I talk to it?

You just say (or type) natural sentences. Here are examples:

**Ask anything:**
- "What is the capital of France?"
- "Explain photosynthesis in simple words."
- "Search the latest news about ISRO."

**Open things:**
- "Open YouTube"
- "Open Gmail"
- "Open Notepad"
- "Open VS Code"

**Play music/videos:**
- "Play Shape of You on YouTube"

**Send WhatsApp messages:**
- "Text mumma hii"  → sends *hii* to the contact named **mumma**
- "Message papa I will be late"  → sends *I will be late* to **papa**

**Stop the bot:**
- "Exit" or "Quit" or "Goodbye"

## 4. The two ways to use it

### 🅰️ The Terminal way (`voicebot.py`)
The **terminal** is that black text screen where you type commands. When you run this file, the bot starts listening through your mic automatically, and keeps having a conversation with you until you say "exit". It talks back using your computer's built-in voice.

Run it like this:
```bash
venv\Scripts\python.exe voicebot.py
```

### 🅱️ The Web Page way (`app.py`)
This opens a nice **website** on your own computer (in your browser) built with a tool called **Streamlit**. It has a big **🎤 microphone button**. You **tap it once to start** talking, **tap again to stop**, and the bot transcribes what you said, answers, and speaks back *through your browser*. It also shows the whole chat like a messaging app.

Run it like this:
```bash
venv\Scripts\python.exe -m streamlit run app.py
```

Both "faces" use the **same brain** underneath — we wrote the thinking logic once and shared it, so they always behave the same way.

---

## 5. How it works — the journey of your voice

Let's follow what happens the moment you speak. Imagine your sentence is a letter traveling through a post office. ✉️

```
   YOU SPEAK
      │
      ▼
┌─────────────────┐
│ 1. MICROPHONE   │  Your voice is recorded as sound.
└─────────────────┘
      │
      ▼
┌─────────────────────────────┐
│ 2. SPEECH-TO-TEXT (STT)     │  Google's free service listens to the
│    "listen()"               │  sound and writes down the words.
└─────────────────────────────┘
      │  (now it's text, like "open youtube")
      ▼
┌─────────────────────────────┐
│ 3. THE ROUTER  "route()"    │  A traffic police 🚦 that decides:
│                             │  Is this a command or a question?
└─────────────────────────────┘
      │
      ├──► "open ___"  ──────────►  Opens the app/website
      ├──► "play ___"  ──────────►  Plays it on YouTube
      ├──► "text ___"  ──────────►  Sends a WhatsApp message
      └──► anything else ─┐
                          ▼
              ┌─────────────────────────┐
              │ 4. WEB SEARCH (optional)│  Quickly searches DuckDuckGo
              │    "web_search()"       │  for fresh facts.
              └─────────────────────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │ 5. AI BRAIN (Bedrock)   │  Amazon's Nova AI reads your
              │    "ask_llm()"          │  question + search results and
              └─────────────────────────┘  writes a short, smart answer.
                          │
                          ▼
┌─────────────────────────────┐
│ 6. TEXT-TO-SPEECH (TTS)     │  The answer text is turned back into
│    "speak()"                │  a human voice and played out loud.
└─────────────────────────────┘
      │
      ▼
   YOU HEAR THE ANSWER 🔊
```

**In one sentence:** your *voice* → becomes *text* → gets *routed* → maybe *searched* → answered by *AI* → turned back into *voice*.

## 6. The tech stack

"Tech stack" just means **the collection of tools and libraries we glued together** to build this. Think of it like the ingredients in a recipe. Here's every ingredient and *why* we chose it.

| Tool / Library | What it is | What it does in our bot |
|----------------|-----------|-------------------------|
| **Python** | A popular, easy-to-read programming language. | The whole bot is written in Python. |
| **SpeechRecognition** | A Python library that turns speech into text. | Listens to your mic and calls Google's free service to get the words. This is the "ears." |
| **PyAudio** | A helper that lets Python use your microphone. | Without it, `SpeechRecognition` can't hear the mic. |
| **pyttsx3** | An **offline** text-to-speech engine. | Speaks the answer out loud in the terminal version — works even without internet. This is one of the "mouths." |
| **gTTS** (Google Text-to-Speech) | An **online** text-to-speech that sounds very natural. | Speaks in the web page version, with a nice female voice, playing right inside your browser. |
| **AWS Bedrock** | Amazon's cloud service that gives access to powerful AI models. | This is the "brain." We use it to actually understand and answer questions. |
| **Amazon Nova (Nova Lite)** | The specific AI model we chose inside Bedrock. | Reads your question and writes the answer. It's fast and low-cost. |
| **boto3** | The official Python toolkit for talking to Amazon (AWS). | Sends your question to Bedrock and brings back the answer. |
| **DuckDuckGo Search** | A library that searches the web without needing an API key. | Fetches fresh facts from the internet so answers stay up-to-date. |
| **pywhatkit** | A fun automation library. | Can play YouTube videos and send WhatsApp messages via the web. |
| **pyautogui + pyperclip** | Tools that control the keyboard/mouse and clipboard. | Used to drive the **WhatsApp Desktop app** — typing a contact's name and message for you, like a ghost typing. |
| **Streamlit** | A tool that turns Python into a web page with almost no effort. | Builds the pretty web interface with the mic button. |
| **streamlit-mic-recorder** | An add-on for Streamlit. | Gives us the tap-to-record microphone button on the web page. |
| **python-dotenv** | Reads secret settings from a file called `.env`. | Loads your AWS keys and contacts without hard-coding them in the program. |

### A quick word on the "brain" (AWS Bedrock + Nova)

Our bot doesn't *itself* know facts. When you ask "What is the capital of France?", the bot doesn't have that memorized. Instead it **sends your question over the internet to Amazon's servers**, where a giant AI model called **Nova** reads it and writes back the answer "Paris." Our bot then just reads that answer out loud.

To use Amazon's brain, you need a **key** (like a password) called an **IAM key**. You paste yours into the `.env` file. That key proves it's really *you* using *your* Amazon account (and Amazon may charge a tiny amount for each question — usually a fraction of a rupee for Nova Lite).

## 7. The files in this project

Your project folder (`D:\voicebot`) contains these files. Here's what each one is for:

| File | What it is |
|------|-----------|
| **`voicebot.py`** | The main program (the brain + ears + mouth). Run this for the terminal version. All the real logic lives here. |
| **`app.py`** | The web page version (Streamlit). It *borrows* the logic from `voicebot.py` and wraps it in a nice interface with a mic button. |
| **`.env`** | Your **secret settings** file — AWS keys, which AI model to use, WhatsApp contacts, voice choice. **Never share this file** (it has your passwords!). |
| **`requirements.txt`** | A shopping list of all the libraries the project needs. One command installs them all. |
| **`test_bedrock.py`** | A tiny tester that checks if your AWS keys and AI model are working. |
| **`DOCUMENTATION.md`** | This file you're reading right now. 😊 |

### What's inside `voicebot.py` (the important functions)

A **function** is a named block of code that does one job. Here are the main ones:

- `listen()` — records your voice and returns the words as text (the **ears**).
- `speak()` — takes text and says it out loud (the **mouth**).
- `web_search()` — searches the internet and returns results.
- `ask_llm()` — sends your question to the AI brain and returns the answer.
- `open_target()` — opens apps and websites like YouTube or Notepad.
- `play_on_youtube()` — plays a video on YouTube.
- `send_whatsapp()` — sends a WhatsApp message.
- `route()` — the **traffic police** that decides which of the above to run.
- `main()` — the loop that keeps the conversation going until you say "exit".

---

## 8. How to set it up

Follow these steps **one line at a time** (don't paste them all at once — Windows PowerShell doesn't like the `&&` symbol).

### Step 1 — Create a private workspace ("virtual environment")
A **virtual environment** (venv) is a clean, separate box where we install this project's libraries, so they don't mess up the rest of your computer.
```bash
python -m venv venv
```

### Step 2 — Install all the libraries
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```
> 😖 **If it fails on `pyaudio`** (this is common on Windows), run these two lines:
> ```bash
> venv\Scripts\python.exe -m pip install pipwin
> ```
> ```bash
> venv\Scripts\python.exe -m pipwin install pyaudio
> ```

### Step 3 — Fill in your secrets in `.env`
Open the `.env` file and paste your **AWS access key** and **secret key** (see next section).

### Step 4 — Test the AI brain
```bash
venv\Scripts\python.exe test_bedrock.py
```
If it prints `[OK] Bedrock replied: 'OK'`, your brain is connected! 🎉

### Step 5 — Run it!
Terminal version:
```bash
venv\Scripts\python.exe voicebot.py
```
Web page version:
```bash
venv\Scripts\python.exe -m streamlit run app.py
```

## 9. The settings file (.env) explained

The `.env` file is where you keep settings **without touching the code**. Each line is `NAME=value`. Here's what every setting means:

```ini
# --- The AI brain (AWS Bedrock) ---
AWS_ACCESS_KEY_ID=your_access_key_here     # Like your username for Amazon AWS
AWS_SECRET_ACCESS_KEY=your_secret_key_here # Like your password for Amazon AWS (keep secret!)
AWS_REGION=ap-south-1                       # Which Amazon data-center to use (ap-south-1 = Mumbai)
BEDROCK_MODEL_ID=apac.amazon.nova-lite-v1:0 # Which AI model to use

# --- How it behaves ---
USE_WEB_SEARCH=true          # Search the web before answering? true/false
SPEECH_RATE=175              # How fast the voice talks (higher = faster)
VOICE_GENDER=female          # female or male voice for the terminal
WHATSAPP_WAIT_SECONDS=20     # How long to wait for WhatsApp to load

# --- WhatsApp ---
WHATSAPP_METHOD=desktop      # 'desktop' = message anyone by name using the WhatsApp app
                             # 'web'     = use pywhatkit with a saved phone number
CONTACT_MUMMA=+919999999999  # A saved contact (only needed for 'web' method)
CONTACT_PAPA=+919888888888
```

### Where do I get the AWS keys?
1. Log in to the **AWS Console** (aws.amazon.com).
2. Go to the **IAM** service → **Users** → your user → **Security credentials**.
3. Create an **access key**. You'll get an **Access Key ID** and a **Secret Access Key**.
4. Paste both into `.env`.
5. Make sure your user has permission `bedrock:InvokeModel`, and that you enabled the **Nova** model in **Bedrock → Model access** for the Mumbai region.

### The two WhatsApp methods (important!)
- **`desktop`** (default): The bot opens your installed **WhatsApp Desktop app**, searches the contact **by name**, and types the message. This lets you message *anyone* — but it works by *pretending to type on your keyboard*, so keep your hands off the mouse/keyboard while it does its thing.
- **`web`**: The bot uses WhatsApp *Web* in your browser and needs the person's **phone number** saved in `.env` as `CONTACT_NAME=+countrycode...`.

---

## 10. Troubleshooting

| Problem | Why it happens | Fix |
|---------|---------------|-----|
| `The token '&&' is not a valid statement separator` | PowerShell doesn't support `&&`. | Run each command on its **own line**. |
| `pip install` fails on **pyaudio** | PyAudio is hard to build on Windows. | Use `pipwin install pyaudio` (see Step 2). |
| `AccessDeniedException` from Bedrock | Your AWS user lacks permission. | Add the `bedrock:InvokeModel` permission to your IAM user. |
| `on-demand throughput isn't supported` | Some models need an "inference profile" in Mumbai. | Use the `apac.` model id, e.g. `apac.amazon.nova-lite-v1:0`. |
| Bot can't hear me | Microphone not working / PyAudio missing. | Check your mic, reinstall pyaudio. In the web app you can also type. |
| No voice comes out (web) | gTTS needs internet. | Check your internet connection. |
| WhatsApp sent to the wrong person | The name wasn't the top search result. | Test with a safe contact first; increase `WHATSAPP_WAIT_SECONDS`; use full, exact names. |
| `venv\Scripts\activate` gives a module error | Wrong activation command in PowerShell. | Use `.\venv\Scripts\Activate.ps1`, or just call `venv\Scripts\python.exe` directly. |

## 11. Safety and privacy

Being a responsible builder means knowing what your program does with data and the world. A few honest points:

- **Your voice goes to the internet.** The speech-to-text uses Google's free service, and answers come from Amazon's servers. Your spoken words and questions travel over the internet to these companies. Don't say secret/private things to it.
- **Your AWS keys are like passwords.** They live in `.env` in plain text. **Never** upload `.env` to GitHub or share it. If it ever leaks, go to AWS and **rotate (delete and recreate)** the key immediately. It's smart to add a file named `.gitignore` containing the line `.env` so it never gets uploaded by accident.
- **It can cost money.** Each AI answer uses your AWS account and may cost a tiny amount. Nova Lite is cheap, but it's not zero — keep an eye on your AWS billing.
- **WhatsApp automation is powerful but blind.** In `desktop` mode the bot literally types for you. If the wrong contact is on top of the search results, it could message the wrong person. Always test with a safe contact (like yourself or a close friend) first.
- **It runs on your computer only.** Nothing here is a public website. Only you, sitting at your PC, can use it.

---

## 12. Dictionary of tricky words

- **AI (Artificial Intelligence):** Computer programs that can do "smart" things like understanding language.
- **API key / IAM key:** A secret code that proves who you are to an online service (like a password).
- **AWS (Amazon Web Services):** Amazon's cloud — thousands of powerful computers you can rent over the internet.
- **Bedrock:** The part of AWS that lets you use AI models like Nova.
- **Cloud:** Someone else's powerful computers that you use over the internet.
- **Function:** A named block of code that does one specific job.
- **Library / package:** Ready-made code written by others that you can reuse instead of writing everything yourself.
- **Model (AI model):** The actual "brain" that has learned from huge amounts of text (e.g., Amazon Nova).
- **Router:** In our bot, the part that decides what kind of request you made and where to send it.
- **STT (Speech-to-Text):** Turning spoken words into written text.
- **TTS (Text-to-Speech):** Turning written text into spoken voice.
- **Terminal:** The black text screen where you type commands to the computer.
- **Streamlit:** A tool that turns Python code into a web page easily.
- **Virtual environment (venv):** A clean, private box for a project's libraries.

---

### 🎉 That's the whole thing!

You now understand **what** the bot is, **what** it can do, **how** it does it step by step, **which** tools power it, and **how** to set it up and stay safe. Go ahead — tap that mic and say *"Hello!"* 👋

*Built with Python, AWS Bedrock (Amazon Nova), and a lot of curiosity.*
