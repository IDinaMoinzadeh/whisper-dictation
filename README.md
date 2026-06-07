# 🎤 Whisper Dictation — Dictée vocale sur Linux

Un outil de dictée vocale pour Linux utilisant [Whisper](https://github.com/openai/whisper) d'OpenAI, conçu pour remplacer Dragon NaturallySpeaking sur Ubuntu. Développé dans le cadre d'un master en humanités numériques pour faciliter la rédaction avec un handicap moteur.

## ✨ Fonctionnalités

- Appui sur F9 pour dicter, F9 à nouveau pour arrêter
- Transcription en français (et autres langues) avec Whisper turbo sur GPU
- Polish automatique de la ponctuation via API Mistral *(optionnel)*
- Injection du texte directement dans n'importe quelle application (LibreOffice, VS Code, etc.)
- 100% local pour la transcription — aucune donnée envoyée sans accord

## 🖥️ Prérequis

- Ubuntu 22.04 ou supérieur
- Python 3.10+
- Une carte graphique NVIDIA (recommandé) ou CPU
- Système audio PipeWire

## 📦 Installation

### 1. Installer les dépendances système

```bash
sudo apt install xdotool ffmpeg git
```

### 2. Installer les dépendances Python

```bash
pip install openai-whisper sounddevice pynput python-dotenv openai
```

### 3. Cloner le dépôt

```bash
git clone https://github.com/IDinaMoinzadeh/whisper-dictation.git
cd whisper-dictation
```

### 4. Configurer la clé API *(optionnel — pour le polish)*

Créer un fichier `~/.env` :

```bash
nano ~/.env
```

Et ajouter une clé Mistral :

```
MISTRAL_API_KEY=clé_ici
```

> Sans clé API, le script fonctionne quand même — la transcription brute de Whisper s'affiche sans correction de ponctuation.

## 🚀 Utilisation

```bash
python3 whisper_dictation.py
```

Puis :
1. Cliquer dans l'application où dicter (LibreOffice, VS Code...)
2. Appuyer sur **F9** pour commencer
3. Parler en français
4. Appuyer sur **F9** pour arrêter — le texte apparaît automatiquement

### Commandes vocales de ponctuation

| Mot dicté | Symbole obtenu |
|-----------|-----------|
| "virgule" | , |
| "point" | . |
| "deux points" | : |
| "à la ligne" | ↵ |
| "ouvrir la parenthèse" | ( |
| "fermer la parenthèse" | ) |
| "point d'interrogation" | ? |
| "point d'exclamation" | ! |
| "guillemet ouvrant" | « |
| "guillemet fermant" | » |

## 📝 Notes

- Le premier lancement télécharge le modèle Whisper (~1.5 GB)
- Le modèle se charge en ~10 secondes au démarrage
- Fonctionne avec PipeWire (Ubuntu 22.04+)

## 🤝 Contribution

Les contributions sont les bienvenues — n'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

MIT
