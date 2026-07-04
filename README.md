# LinkedIn Post Generator 📝

A streamlined, AI-powered web application built with Streamlit and LangChain that generates engaging LinkedIn posts with hooks, pacing, live-context grounding, and multiple ready-to-compare variants.

## Features ✨

- **Topic Selection**: Pick from curated tags or enter your own custom topic.
- **Live Context Grounding**: Uses Tavily to retrieve trending context and ground generated posts in real-time.
- **Customizable Tone & Length**: Choose Short, Medium, or Long posts, and tones like Professional, Casual, Witty, Storytelling, Motivational, and Educational.
- **Bilingual Support**: Supports both English and Hinglish.
- **Variant Comparison**: Generate 1–3 variants and choose the best draft.
- **Editable Output**: Edit the selected variant in a final draft editor, then download or copy it.

## Technologies Used 🚀

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend/LLM Integration**: [LangChain](https://python.langchain.com/)
- **LLM Provider**: [Groq](https://groq.com/)
- **Live Context Provider**: Tavily

## Prerequisites 🔑

Create a `.env` file in the root directory and add your keys:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
TAVILY_API_URL=https://api.tavily.ai/v1/trends
```

`TAVILY_API_URL` is optional if you want to use a custom endpoint.

## Setup & Installation 🛠️

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Atharva2026/LinkedIN_GENAI_PostGenerator.git
   cd LinkedIN_GENAI_PostGenerator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env`** with your API credentials.

## Running the Application 🏃‍♂️

From the project root:

```bash
streamlit run main.py
```

Open the local URL shown in the terminal (typically `http://localhost:8501`).

## How to Use 🔍

1. Select a pre-defined topic or enter a custom topic.
2. Choose length, language, tone, hook, and emoji density.
3. Click **Generate Post**.
4. Review the generated variants.
5. Select the variant you want to keep.
6. Edit the final draft, then download or copy it.

## Live Context Notes 🧠

- The app attempts to fetch Tavily context for every generation.
- If Tavily succeeds, you will see a **Grounded with live context** badge and source details.
- If Tavily cannot fetch context, the app still generates a post and shows **Generated without live context** as a fallback.

## Notes 📝

- The sidebar options allow hashtag suggestions, tone, and variant control.
- Selecting a variant updates the final draft and the live preview.
- The app uses a cached Tavily result per topic for faster repeated generation.

## License

This repository is provided as-is for experimentation and portfolio use.
