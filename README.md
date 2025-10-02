<!-- ASCII Banner -->
Of course\! Here is the word "ASTRA" in the same large block ASCII art style.

```
       .
      /^\
      |-|      █████╗  ██████╗████████╗██████╗    █████╗
      |A|     ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗  ██╔══██╗
      |S|     ███████║███████╗   ██║   ██████╔╝  ███████║
      |T|     ██╔══██║╚════██║   ██║   ██╔═██╗   ██╔══██║
      |R|     ██║  ██║███████║   ██║   ██║  ██╗  ██║  ██║
      |A|     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝  ╚═╝  ╚═╝
     /| |\               🚀 Wake-Word Voice Agent for Pi
    /_|_|_\              
      /_\
``` 

---

# Astra Assistant

> **A privacy-first, open-source, *local* voice assistant for Raspberry Pi and Linux.**
> 
> Modular. Event-driven. Hackable. Yours.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%204%2B%20%7C%20Linux-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Status](https://img.shields.io/badge/status-alpha-orange)

---

## 🚀 Project Vision

**Astra** is an always-on, offline-first voice assistant designed for real-world use on Raspberry Pi and Linux edge devices. It uses wake-word detection to listen only when called, then passes control to an extensible agent pipeline for natural conversation, tool use, and automation—*with no cloud dependencies by default*.

If you want Mycroft-style skills, but with full transparency, privacy, and hackability, Astra is your playground.

---

## 🌱 Current Status

- [x] **Wake-word detection**: Works (Porcupine, custom-trained “Astra”)
- [x] **Simple audio notification**: Plays `ding.wav` on wakeword hit
- [ ] **Voice pipeline**: [Next up] Integrate ASR (Automatic Speech Recognition) via Whisper or Vosk
- [ ] **LLM agent**: [Planned] Trigger agent to interpret, plan, call APIs/tools, respond
- [ ] **Text-to-speech (TTS)**: [Planned] Modular TTS (Coqui, Piper, etc.)
- [ ] **Skills/Tools**: [Planned] Pluggable “skills” (system control, home automation, search…)

The project is in **early alpha**. Only the wake-word system and demo notification are implemented.

---

## 🧑‍💻 Quickstart (Dev Install)

**Requirements:**
- Python 3.10+
- Raspberry Pi 4+ (or any modern Linux box)
- ALSA drivers & microphone
- Porcupine wake-word engine (see below for setup)

```bash
git clone https://github.com/yourname/astra-assistant.git
cd astra-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Download Porcupine model and copy your keyword file
python wakeword.py
```

This will run Astra in “wakeword mode”: it listens for the wakeword, then plays a sound. This is a confirmation that mic + voice activation + Speaker is working.

---

## 🏗️ Architecture

Astra is built to be *deeply modular*. Each part is a plug-and-play module:

* **Wake-word engine** (Porcupine, open to others)
* **Audio recorder** (ALSA, async)
* **ASR** (Planned: Whisper, Vosk, etc.)
* **Agent core** (Planned: LLM, tool/skill system, intent parser)
* **TTS** (Planned: local, swappable)
* **Skill plugins** (Planned: drop in your own automations, scripts, etc.)

All events flow through a realtime pipeline.

---

## 🗺️ Roadmap

* **Phase 1**:

  * [x] Wake-word trigger (done)
  * [x] Async/efficient audio capture (done)
  * [ ] Build event-driven pipeline (in progress)

* **Phase 2**:

  * [ ] Integrate open-source ASR (Whisper, Vosk)
  * [ ] Implement agent logic (LLM, context, tool-call, prompt chaining)
  * [ ] Modular TTS

* **Phase 3**:

  * [ ] Plugin system: user scripts, system commands, API tools
  * [ ] Local web dashboard/config UI
  * [ ] Skill library & documentation

* **Phase 4**:

  * [ ] Hardware support (LED ring, speaker integration)
  * [ ] Edge model optimizations, on-device LLM

---

## 🤔 FAQ

**Why another voice assistant?**
Because privacy matters, and none of the open options today are fully modular, agent-driven, and easy to hack on.

**Why local only?**
Cloud is optional. The goal is to *never* require it.

**Will it support other hardware?**
Yes, Pi is just the reference. Runs anywhere Linux + Python + mic.

**How is it different from Mycroft or Jasper?**
Focus on modern, agent-based architecture, explicit privacy, and modular skill chaining. All processing, all tools, your choice.

---

## 🤝 Contributing

**Still in solo dev alpha!**
If you want to follow or suggest features, open an issue or star the repo to watch progress.
Major PRs welcome once the pipeline is live.

---

## 📂 Repo Structure

* `wakeword.py` – Wake-word detection loop
* `alsa_recorder.py` – ALSA PCM audio input abstraction
* `requirements.txt` – Python dependencies
* `ding.wav` – Example notification sound
* `.github/` – Issue templates, actions (WIP)
* `docs/` – Architecture and dev notes
