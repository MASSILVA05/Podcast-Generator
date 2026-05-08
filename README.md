# 🎙️ Podcast Generator

An AI-powered podcast generation app that transforms any topic, webpage, YouTube video, or document into a full audio episode — complete with AI-generated script, voiceover, and intro music.

Built with a **FastAPI** backend, a **React + Vite** frontend, and packaged as a **desktop app with Electron**.

---

## ✨ Features

- 🧠 AI-generated podcast scripts from multiple input types (text, URL, YouTube, slides)
- 🔊 Dual TTS engine — **Fish Audio** and **Coqui XTTS**
- 🎭 Multiple voice profiles (EN & FR, male & female)
- 🎵 Intro music selection
- 📄 Script editor before audio generation
- 🗂️ Archives page to replay past episodes
- 🖥️ Desktop app via Electron
- 🐳 Fully containerized with Docker Compose
- ✅ Full test suite across all modules

---

## 🗂️ Project Structure
Podcast-Generator/
├── back/
│   ├── api.py                  # FastAPI routes
│   ├── main_backend.py         # App entry point
│   ├── TTs/                    # TTS engines (Fish Audio, Coqui)
│   │   └── Voices_wav/         # Voice reference samples (EN/FR)
│   ├── segmentation/           # Input parsers (web, YouTube, PDF, text)
│   ├── extraction/             # Content extraction
│   └── scenario/               # Script generation
├── frontend/
│   ├── src/
│   │   ├── pages/              # BuilderPage, ScriptPage, PlayerPage, ArchivesPage
│   │   └── services/           # Supabase client
│   ├── electron/               # Desktop app wrapper
│   └── public/audios/          # Voice preview samples
├── intros/                     # Intro music files
├── voix.json                   # Voice configuration
├── Dockerfile
├── Dockerfile.tts
├── docker-compose.yml
└── requirements.txt
---

## ▶️ How to Run

### With Docker
```bash
git clone https://github.com/MASSILVA05/Podcast-Generator.git
cd Podcast-Generator
docker-compose up --build
```
Then open: `http://localhost:5173`

### Without Docker
```bash
# Backend
pip install -r requirements.txt
uvicorn back.main_backend:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## 🧩 Input Sources Supported

| Source | Module |
|---|---|
| Raw text | `SegmentationTxt` |
| Web page / URL | `SegmentationWeb` |
| YouTube video | `SegmentationYT` |
| PDF / slides | `SegDiapo` |
| Fallback | `SegmentationFallback` |

---

## 🎤 Available Voices

| Language | Gender | Voices |
|---|---|---|
| 🇫🇷 French | Female | Léa, Marie, + 2 more |
| 🇫🇷 French | Male | Marc, Paul, + 3 more |
| 🇬🇧 English | Female | Eva, Jessy, + 3 more |
| 🇬🇧 English | Male | Adam, John, + 2 more |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Electron |
| Backend | FastAPI, Python |
| TTS | Fish Audio, Coqui XTTS |
| Database | Supabase |
| Infra | Docker, Docker Compose |
| CI/CD | GitHub Actions |

---

## 👩‍💻 Author

**Massilva** — [@MASSILVA05](https://github.com/MASSILVA05)

---

## 📄 License

Personal project — all rights reserved.
