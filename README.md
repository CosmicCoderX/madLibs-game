# 🎩 Mad Libs Story Generator

A hilarious, feature-packed Mad Libs-style **story generator desktop app** built with Python and Tkinter. Supports themes like Funny, Spooky, Sci-Fi, and Romantic — with text-to-speech, sounds, and even silly word suggestions!

---

## ✨ Features

* 🔹 Beautiful Tkinter GUI
* 🔹 Multiple themes with dynamic styling
* 🔹 Random silly word generation with "Surprise Me!"
* 🔹 Plays theme-appropriate sound effects
* 🔹 Offline text-to-speech (TTS)
* 🔹 Saves generated stories to JSON
* 🔹 Lets users browse saved stories

---

## 📚 Demo (Sample Screenshot)

![Screenshot 2025-06-28 092522](https://github.com/user-attachments/assets/cddb001b-d97f-4440-8bb9-3b6daa5c20fe)

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.10+
* Install required packages:

```bash
pip install pyttsx3 playsound emoji
```

Ensure sound files are placed in:

```
sounds/
  general/
  themes/funny/
  themes/spooky/
  themes/scifi/
  themes/romantic/
  actions/
```

---

## 📁 Project Structure

```
MadLibs-Story-Generator/
├── madlibs.py              # Main application
├── saved_stories.json      # Generated stories (auto-saved)
├── README.md               # Project readme
├── assets/
│   └── screenshot.png      # (Add your screenshots here)
└── sounds/
    ├── general/            # e.g., drumroll.mp3, tada.mp3
    ├── themes/             # Each theme has multiple .mp3 files
    └── actions/            # For UI action sounds
```

---

## 🌈 Themes Supported

* **Funny**: Bright yellow, orange buttons, comedy sounds
* **Spooky**: Dark, horror-like visuals with creepy SFX
* **Sci-Fi**: Futuristic neon and tech SFX
* **Romantic**: Pink vibes and soft music

Each theme changes background, fonts, emoji, sounds, and button styles.

---

## 🎤 Voice Support

* Uses `pyttsx3` for offline TTS
* Speech is cleaned using regex (removes emojis, weird formatting)

---

## 🎵 Sounds Used

| Type     | Files                                 |
| -------- | ------------------------------------- |
| General  | drumroll.mp3, tada.mp3, bye.mp3       |
| Funny    | laugh.mp3, giggle.mp3                 |
| Spooky   | creepy.mp3, thunder.mp3               |
| Sci-Fi   | teleport.mp3, computer.mp3            |
| Romantic | whistle.mp3, soft\_music.mp3          |
| Actions  | surprise\_me.mp3, generate\_story.mp3 |

All sounds must be present in respective subfolders under `sounds/`.

---

## 🎨 Story Generation

Each story is generated using dynamic `f-strings` with textwrap for formatting. Templates are grouped by themes and randomly chosen.

```python
story = generate_story(inputs, theme)
```

User fills:

* Place
* Adjective
* Noun
* Verb
* Adverb
* Name

---

## 📑 Save & View Stories

* All stories saved in `saved_stories.json` with ID and timestamp
* Click "📂 View Saved" to browse your previous stories in a new scrollable window

---

## 📅 Run the App

```bash
python madlibs.py
```

---

## 🛠️ Build to .exe (Optional)

To create an executable for Windows:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed madlibs.py
```

To include sound files:

```bash
pyinstaller --onefile --windowed --add-data "sounds;./sounds" madlibs.py
```

---

## 👤 Author

**Suryakant Dwivedi**
📧 [suryakantdwivedi8493@gmail.com](mailto:suryakantdwivedi8493@gmail.com)

---

> “The only limit to your story... is your imagination.”
