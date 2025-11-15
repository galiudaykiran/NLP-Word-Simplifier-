# Word Simplifier

A powerful NLP tool that simplifies complex sentences and words into easy-to-understand language while maintaining the original meaning. Powered by Word Simplifier AI.

## Features

- ✨ Simplifies complex text into simple, accessible language
- 🎯 Preserves the original meaning and context
- 🚀 Fast and efficient processing
- 💻 Beautiful, modern web interface
- 📋 Easy copy-to-clipboard functionality

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Open the `static/index.html` file in your browser, or serve it through the Flask app.

## How It Works

1. Enter or paste your complex text in the input box
  <img width="1365" height="683" alt="image" src="https://github.com/user-attachments/assets/f959fa4e-2aa6-4e0c-a84b-1adb8267165f" />

2. Click "Simplify Text" button
 <img width="1365" height="683" alt="Screenshot 2025-11-15 181937" src="https://github.com/user-attachments/assets/0df1b6fa-5266-4833-a9b9-f4ffc917762f" />

3. View the simplified version alongside the original
<img width="1346" height="682" alt="Screenshot 2025-11-15 182459" src="https://github.com/user-attachments/assets/369d2afb-0220-4eab-815e-5e7b07caa2d0" />

4. Copy the simplified text to use elsewhere
<img width="1346" height="682" alt="Screenshot 2025-11-15 182459" src="https://github.com/user-attachments/assets/4ce6bdc0-1f9c-4cf3-bac7-663b93e4be0b" />

## API Endpoint

The application provides a REST API endpoint:

**POST** `/simplify`

Request body:
```json
{
  "text": "Your complex text here"
}
```

Response:
```json
{
  "original": "Original text",
  "simplified": "Simplified text",
  "success": true
}
```

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: Google Gemini Pro
- **API**: Google Generative AI

## License

This project is open source and available for personal and commercial use.

