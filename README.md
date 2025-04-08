# OCR-Note-Transcriber

# OCR Note Transcriber

![OCR Illustration](./images/app_screen.png) <!-- Add your own image -->

A smart document processing system that combines OCR with Large Language Models (LLMs) to transform handwritten notes and documents into organized digital formats.

**Blog Post**: [Building with LLMs: How I Used LLMs to Solve My Own Problem](https://medium.com/@nolanrobbins5934/building-with-llms-how-i-used-llms-to-solve-my-own-problem-925b42b63407)
![Blog Post](./images/ocr_post.png)

## Features

- 📖 Handwritten text recognition using Tesseract OCR
- 🧠 Context-aware text processing with GPT-4
- ✅ Automatic formatting and error correction
- 🌐 Multi-language support
- 💡 Intelligent summarization and key point extraction
- 🔍 Contextual understanding of notes
- 📤 Markdown and text file export

## Installation

1. **Prerequisites**:
   - Python 3.8+
   - Tesseract OCR ([Installation guide](https://github.com/tesseract-ocr/tesseract))

2. **Install dependencies**:
```bash
pip install pytesseract opencv-python python-dotenv openai
