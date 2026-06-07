#!/usr/bin/env python3
"""
Dictée vocale avec Whisper + PipeWire + Polish OpenRouter
- Appuie sur F9 pour commencer à dicter
- Appuie sur F9 à nouveau pour arrêter et transcrire
- Le texte s'insère automatiquement dans LibreOffice Writer
"""

import subprocess
import threading
import tempfile
import time
import os
import whisper
from openai import OpenAI
from dotenv import load_dotenv
from pynput import keyboard

# Chargement de la clé API depuis ~/.env
load_dotenv(os.path.expanduser("~/.env"))
api_key = os.getenv("MISTRAL_API_KEY")

dictation_language = os.getenv("DICTATION_LANGUAGE", "fr")
if dictation_language == "auto":
    dictation_language = None
    
    if not api_key:
    print("⚠️  Clé MISTRAL_API_KEY introuvable dans ~/.env — le script fonctionnera sans polish")

client = OpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key=api_key
)

# Chargement de Whisper sur GPU
print("Chargement de Whisper sur GPU...")
model = whisper.load_model("turbo", device="cuda")
print("✅ Whisper prêt ! Appuie sur F9 pour dicter.")

# Variables globales
is_recording = False
record_process = None
temp_file = None
lock = threading.Lock()

def polish_text(text):
    """Nettoie le texte avec Mistral"""
    if not api_key:
        return text
    response = client.chat.completions.create(
        model="mistral-medium-latest",
        messages=[
            {
                "role": "system",
                "content": """Tu es un assistant de correction de dictée vocale en français.
Remplace uniquement les mots de ponctuation dictés par leurs symboles :
- "virgule" → ,
- "point" → .
- "deux points" ou "2 points" → :
- "à la ligne" → un vrai saut de ligne
- "parenthèse" ou "ouvrir la parenthèse" → (
- "fermer la parenthèse" ou "fermé la parenthèse" → )
- "point d'interrogation" → ?
- "point d'exclamation" → !
- "tiret" → -
- "guillemet ouvrant" → «
- "guillemet fermant" → »
Ne change aucun autre mot. Ne résume pas. Ne reformule pas.
Retourne uniquement le texte corrigé, rien d'autre."""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content.strip()

def start_recording():
    global record_process, temp_file
    temp_file = tempfile.mktemp(suffix=".wav")
    print("🎤 Enregistrement démarré... (appuie sur F9 pour arrêter)")
    record_process = subprocess.Popen(
        ["pw-record", "--rate=16000", "--channels=1", temp_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def stop_and_transcribe():
    global record_process, temp_file, is_recording

    if record_process:
        record_process.terminate()
        record_process.wait()
        print("⏳ Transcription en cours...")
        time.sleep(0.5)

        try:
            result = model.transcribe(temp_file, language=dictation_language, fp16=True)
            text = result["text"].strip()
            print(f"📝 Brut : {text}")

            print("✨ Polish en cours...")
            try:
                text = polish_text(text)
                print(f"✅ Final : {text}")
            except Exception as e:
                print(f"⚠️  Polish échoué ({e}), texte brut utilisé")

            if text:
                # Focus sur LibreOffice Writer
                focus = subprocess.run(
                    ["xdotool", "search", "--onlyvisible", "--name", "LibreOffice Writer"],
                    capture_output=True, text=True
                )
                if focus.stdout.strip():
                    win_id = focus.stdout.strip().split("\n")[-1]
                    subprocess.run(["xdotool", "windowfocus", "--sync", win_id])
                    time.sleep(0.3)

                subprocess.run(["xdotool", "type", "--clearmodifiers", "--delay", "20", "--", text])

        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
            record_process = None
            temp_file = None

def on_press(key):
    global is_recording

    if key == keyboard.Key.f9:
        with lock:
            if not is_recording:
                is_recording = True
                start_recording()
            else:
                is_recording = False
                threading.Thread(target=stop_and_transcribe).start()

# Lancement du listener clavier
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
