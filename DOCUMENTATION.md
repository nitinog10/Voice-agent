# 📖 Terminal Voice Assistant — Explained Simply

_A friendly guide you could hand to a 10th-class student. It explains **what**
this project is, **what it can do**, **how** it works inside, and the **tech
stack** — step by step, in plain language._

---

## 1. What is this project?

Imagine you could **talk to your computer** like a friend and it would **talk
back**. You say *"open YouTube"* and YouTube opens. You say *"search the latest
AI news"* and it looks it up and reads you a summary. You ask *"write a Python
function to reverse a string"* and it prints the code and explains it out loud.

That is exactly what this project is: a **voice assistant that lives in your
terminal** (the black text window on a computer). It is written **completely in
Python** — no website, no app, just Python.

---

## 2. How do you use it?

It works in simple **turns**, like a walkie-talkie:

1. You **press the Enter key** (this means "I want to talk now").
2. The assistant says **"listening…"** — you have **7 seconds to start
   speaking**.
3. You **speak your command**, then **stop/pause**. The moment you pause, it
   knows you're done.
4. It **does the task** and **speaks the answer** in a **female voice** (and also
   prints it on the screen).
5. It then **waits** — it will *not* listen again until you **come back and
   press Enter**. This stops it from accidentally hearing itself or background
   noise.

You can also just **type** a command if you don't want to talk. Say or type
**"exit"** to stop.

---

## 3. What can it do? (Its three super-powers)

<!-- APPEND -->

### 🟦 Super-power 1: Open apps & websites
Say **"open notepad"**, **"open calculator"**, **"open vs code"**,
**"open youtube"**, **"open gmail"**, **"open github"**, or **"open google"**,
and it launches them for you.

### 🟩 Super-power 2: Search the web
Say **"search latest AI news"** or **"google python tips"**. It looks the topic
up on the internet (using DuckDuckGo), then **reads you a short summary** and
prints the website links so you can read more.

### 🟪 Super-power 3: Think & answer (the AI brain)
Ask it almost anything:
- **A question:** *"What is the capital of France?"*
- **Coding help:** *"Write a Python function to check a palindrome."*
- **Brainstorming:** *"Give me three ideas for a science project."*

For this, it uses a real **Artificial Intelligence** model called **Amazon
Nova**, running on **AWS Bedrock** (Amazon's AI cloud service). Long answers and
code are **printed** on the screen, and a short version is **spoken**.

---

## 4. How does it work inside? (The pipeline)

Think of it like an **assembly line**. Your voice goes in one end, and an answer
comes out the other. Each station does one job:

```
  You speak  ➜  [Ears]  ➜  [Brain decides]  ➜  [Do the task]  ➜  [Mouth]  ➜  You hear
                STT          Router            apps/search/AI      TTS
```

1. **Ears (Speech-to-Text)** — turns your spoken words into text.
2. **Router (the decision maker)** — reads the text and figures out what you
   want: open something? search? or ask the AI?
3. **The worker** — one of the three super-powers does the actual task.
4. **Mouth (Text-to-Speech)** — turns the answer back into a female voice.

---

## 5. The files (and what each one does)

The code is split into small pieces so it's tidy and easy to understand — like
keeping different school subjects in different notebooks.

| File | Its job (in one line) |
|------|----------------------|
| `voicebot.py` | The **start button** — you run this file. |
| `bot/config.py` | Reads your **settings** from the `.env` file. |
| `bot/stt.py` | The **ears** — listens and turns speech into text. |
| `bot/tts.py` | The **mouth** — speaks answers in a female voice. |
| `bot/websearch.py` | The **web searcher** — looks things up online. |
| `bot/llm.py` | The **AI brain** — thinks using Amazon Nova. |
| `bot/apps.py` | The **launcher** — opens apps and websites. |
| `bot/router.py` | The **decision maker** — picks what to do. |
| `bot/session.py` | The **conductor** — runs the press-Enter-to-talk loop. |
| `tests/test_bot.py` | **Tests** that check the logic works. |
| `test_bedrock.py` | Checks the **AWS connection** works. |

---

## 6. The tech stack (the tools we used)

| Tool | What it is | Why we use it |
|------|-----------|---------------|
| **Python** | A programming language | Everything is written in it |
| **SpeechRecognition + PyAudio** | Listens to the microphone | Turns your voice into text |
| **pyttsx3** | A speaking library | Gives the assistant its (offline) female voice |
| **AWS Bedrock + Amazon Nova** | Amazon's AI in the cloud | The "brain" that answers questions |
| **boto3** | Amazon's Python toolkit | Lets Python talk to AWS |
| **duckduckgo-search** | A web-search library | Finds live info on the internet |
| **python-dotenv** | Reads a `.env` file | Keeps secret keys out of the code |
| **Git & GitHub** | Version control | Saves and shares the project safely |

---

## 7. Setting it up (quick recipe)

```bash
python -m venv venv                 # make a clean workspace
.\venv\Scripts\Activate.ps1         # turn it on (Windows)
pip install -r requirements.txt     # install the tools
copy .env.example .env              # make your settings file
#   ...then paste your AWS keys into .env
python voicebot.py                  # start talking!
```

If `pyaudio` refuses to install on Windows:
`pip install pipwin && pipwin install pyaudio`.

---

## 8. Staying safe

- Your **AWS keys** are secret (like a password). They live in the `.env` file,
  which is **never uploaded to GitHub** (it's in `.gitignore`).
- If your keys ever leak, **change them** in the AWS website.
- The assistant only **opens apps, searches, and asks AWS** — it does **not**
  message anyone or send your data anywhere else.

---

## 9. In one sentence

> **A fully-Python terminal assistant that listens when you press Enter, opens
> apps, searches the web, and answers questions with an AI brain — then talks
> back in a female voice.**

