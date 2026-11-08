# Job Seeker AI Agent 🕵️‍♂️

A modular, AI-powered web application designed to assist job seekers by analyzing resumes, finding relevant job listings, scoring matches, and generating tailored application kits.

## 🚀 Features

1.  **Smart Resume Analysis**:
    *   Upload your resume (PDF/Image).
    *   Uses **Google Gemini 2.0 Flash** (Vision capabilities) to automatically extract skills, experience, and preferred roles.
    *   Auto-analyzes upon upload—no extra clicks needed.

2.  **Intelligent Job Search**:
    *   Chat interface to search for jobs using natural language (e.g., "Python Developer in Bangalore").
    *   Translates your request into a precise Google Search query targeting top job boards (LinkedIn, Naukri, Indeed).
    *   **Quality Filtering**: Automatically filters out salary articles, trends, and irrelevant pages to show only valid job listings.

3.  **AI Match Scoring**:
    *   Acts as a "Strict Recruiter" to compare your resume against each job found.
    *   Provides a **Match Score (0-100%)** and a concise reason for the score.
    *   Visual indicators: 🟢 High Match, 🟡 Medium Match, 🔴 Low Match.

4.  **Application Kit Generator**:
    *   Generates a **customized cover letter** for any selected job with one click.
    *   **Downloadable**: Save the cover letter as a Markdown (`.md`) file.

5.  **Robust State Management**:
    *   Search results and generated letters persist even if the app reruns, ensuring a smooth user experience.

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) (Python-based web framework)
*   **AI Core**: [Google Gemini 2.0 Flash](https://deepmind.google/technologies/gemini/) (via `google-generativeai`)
*   **Search**: [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview)
*   **Language**: Python 3.x

## 📂 File Structure

*   `app.py`: The main application file handling the UI, session state, and user interactions.
*   `backend.py`: Contains all logic for API calls (Gemini, Google Search), data processing, and error handling.
*   `requirements.txt`: List of Python dependencies.
*   `.streamlit/secrets.toml`: Secure storage for API keys (not committed to version control).

## ⚙️ Setup & Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Secrets**:
    Create a file named `.streamlit/secrets.toml` and add your keys:
    ```toml
    GEMINI_API_KEY = "your_gemini_api_key"
    GOOGLE_SEARCH_API_KEY = "your_google_search_api_key"
    SEARCH_ENGINE_ID = "your_search_engine_id"
    ```

3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 🐛 Troubleshooting

*   **API Key Errors**: Ensure your keys in `secrets.toml` are correct and have no extra spaces.
*   **No Jobs Found**: Try broadening your search query or checking your internet connection.
*   **JSON Errors**: The backend automatically handles markdown formatting from Gemini, but if issues persist, check the logs.
