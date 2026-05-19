# LinkedIn Post Generator 📝

A streamlined, AI-powered web application built with Streamlit and LangChain that generates engaging, high-quality LinkedIn posts. The application uses few-shot prompting to learn from previously successful posts and tailor content based on the selected tone, language, and length.

## Features ✨

- **Topic Selection**: Choose from popular pre-defined tags or input your own custom topic.
- **Customizable Tone & Length**: Generate posts that are Short, Medium, or Long with tones ranging from Professional and Casual to Witty and Storytelling.
- **Bilingual Support**: Supports both English and Hinglish seamlessly.
- **Few-Shot Prompting**: Learns from a dataset of highly engaged raw posts (`data/`) to output formatted, high-quality responses.
- **Editable Output**: Provides an editable text area allowing users to tweak the generated content before downloading or copying to clipboard.

## Technologies Used 🚀

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend/LLM Integration**: [LangChain](https://python.langchain.com/)
- **LLM Provider**: [Groq](https://groq.com/) (using LLaMA 3.1)
- **Data Processing**: Pandas

## Prerequisites 🔑

To run this project, you will need a **Groq API Key**.
Create a `.env` file in the root directory and add your key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Setup & Installation 🛠️

This project uses `uv` for lightning-fast dependency management (you can also use pip).

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Atharva2026/LinkedIN_GENAI_PostGenerator.git
   cd LinkedIN_GENAI_PostGenerator
   ```

2. **Install dependencies:**
   Using `uv` (recommended):
   ```bash
   uv add -r requirements.txt
   ```
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application 🏃‍♂️

Start the Streamlit development server using `uv`:

```bash
uv run streamlit run main.py
```

*If you set up a standard virtual environment, activate it and run `streamlit run main.py`.*

Navigate to the Local URL provided in your terminal (usually `http://localhost:8501`) to start generating posts!
