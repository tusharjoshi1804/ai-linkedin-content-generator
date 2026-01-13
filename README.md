# AI-Powered LinkedIn Content Generator

An AI-powered web application that generates professional LinkedIn posts based on topic, length and language preferences.
Built using **Streamlit**, **LangChain**, and **Groq LLM**, and deployed on **Render Cloud**.


## Live Demo

🔗 Live App: https://genai-post-generator-erv2.onrender.com


## Features

✅ Generate good-quality LinkedIn posts instantly  
✅ Select topic, length, and language  
✅ Supports English, Hinglish, French, Spanish  
✅ Cloud deployed and mobile-friendly too
✅ Live public demo available

## System Architecture

```
User Browser
     ↓
Streamlit UI
     ↓
Prompt Builder (Python)
     ↓
LangChain
     ↓
Groq LLM API
     ↓
Generated Post Output
```


## Tech Stack
  
- **Frontend:** Streamlit  
- **Backend:** Python  
- **LLM Integration:** LangChain + Groq API  
- **Deployment:** Render Cloud  
- **Version Control:** GitHub

## Local Setup

### 1. Clone repository

```bash
git clone https://github.com/tusharjoshi1804/ai-linkedin-post-generator.git
cd ai-linkedin-post-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```


### 3. Add environment variable

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### 4. Run app locally

```bash
streamlit run main.py
```

Open in browser:
```
http://localhost:8501
```

## Deployment

This project is deployed on Render using GitHub integration.

- Build Command:
```bash
pip install -r requirements.txt
```

- Start Command:
```bash
streamlit run main.py --server.port $PORT --server.address 0.0.0.0
```

## Future Improvements

- Post templates
- Hashtag suggestions
- Save history
- Download posts
- User login

## License

This project is licensed under the MIT License.
