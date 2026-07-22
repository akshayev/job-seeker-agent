# Setup Guide for Job Seeker AI Agent

Welcome to the **Job Seeker AI Agent**! This guide will walk you through setting up the project locally.

## Prerequisites

Before you begin, ensure you have the following installed:
*   **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
*   **Git**: [Download Git](https://git-scm.com/downloads)

## 1. Get API Keys

This application relies on two main services: Google Gemini (for AI processing) and Google Custom Search (for finding jobs). You will need keys for both.

### A. Google Gemini API Key
1.  Go to Google AI Studio: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2.  Sign in with your Google Account.
3.  Click on "Create API key".
4.  Copy the generated API key. You will need this later.

### B. Google Custom Search API Key & Engine ID
To search for jobs, you need a Google Custom Search JSON API key and a Search Engine ID.

**Get the API Key:**
1.  Go to the Google Cloud Console: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2.  Create a new project (or select an existing one).
3.  Go to "APIs & Services" > "Library".
4.  Search for **Custom Search API** and click "Enable".
5.  Go to "APIs & Services" > "Credentials".
6.  Click "Create Credentials" > "API key".
7.  Copy the generated API key.

**Create a Search Engine (Engine ID):**
1.  Go to the Programmable Search Engine control panel: [https://programmablesearchengine.google.com/controlpanel/create](https://programmablesearchengine.google.com/controlpanel/create)
2.  **Name your search engine** (e.g., "Job Searcher").
3.  Under **What to search?**, select "Search specific sites or pages".
4.  Add the following URLs to search job boards (you can add more later):
    *   `linkedin.com/jobs`
    *   `naukri.com`
    *   `indeed.com`
5.  Click "Create".
6.  Once created, copy the **Search engine ID** (also called cx).

## 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    This keeps dependencies isolated.
    ```bash
    py -m venv venv
    ```
    (Note: Replace `py` with `python3` or `python` depending on your OS).

3.  **Activate the Virtual Environment:**
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 3. Configuration

Streamlit uses a `secrets.toml` file to manage sensitive information like API keys locally.

1.  Create a folder named `.streamlit` in the root of your project directory if it doesn't exist:
    ```bash
    mkdir .streamlit
    ```

2.  Create a file named `secrets.toml` inside the `.streamlit` folder:
    ```bash
    touch .streamlit/secrets.toml
    ```

3.  Open `.streamlit/secrets.toml` in your text editor and add your keys as follows:

    ```toml
    # .streamlit/secrets.toml
    GEMINI_API_KEY = "your_gemini_api_key_here"
    GOOGLE_SEARCH_API_KEY = "your_google_search_api_key_here"
    SEARCH_ENGINE_ID = "your_search_engine_id_here"
    ```
    *Replace the placeholder strings with the actual keys you obtained in Step 1.*

    **(Important: Never commit `.streamlit/secrets.toml` to version control. It is already in the `.gitignore` file, but double-check to be safe!)**

## 4. Run the Application

With your environment activated and your secrets configured, you can now run the app:

```bash
streamlit run app.py
```

This command will start a local web server and usually open your default web browser automatically. If it doesn't, navigate to the URL provided in the terminal (typically `http://localhost:8501`).
