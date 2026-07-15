# SmartCampusAI 🎓

SmartCampusAI is a production-ready, premium Python-based student workspace app built on Streamlit. It integrates a custom-designed sidebar, interactive charts/metrics, local JSON databases, and OpenAI API capabilities. Students can register, log in securely, customize preferences, chat with an academic AI bot across multiple subjects, and manage their conversation logs.

---

## 🚀 Key Features

* **Secure Authentication**: Hashed password checks (SHA-256 with static salt), dynamic session states, email format validation, and automated path authorization redirects.
* **Unified Sidebar Menu**: Sidebar navigation via `streamlit-option-menu` with custom styles (Light/Dark themes).
* **Modern Dashboard**: Custom HSL-tailored visual cards (Total Users, AI Requests count, saved history, activity status) and Quick Actions.
* **Interactive AI Chatbot**: Prompts categories (Programming, Career, Assignments, exam study guidelines, campus FAQs) targeting OpenAI's `gpt-4o-mini` client.
* **Student Profile Editor**: View registration credentials and modify credentials dynamically.
* **Searchable logs**: Search past interactions, delete individual logs, or clean history caches.
* **API Key Management**: Override env vars inside active settings dynamically and test validity against models list endpoints.
* **JSON Local Database**: Dependency-free JSON template operations with auto-corruption backups and self-healing loaders.

---

## 📁 Folder Structure

```text
SmartCampusAI/
│
├── .streamlit/
│      └── config.toml         # Disables default sidebar page navigation list
│
├── assets/
│      ├── style.css           # Premium gradients, layout custom rules, cards
│      └── logo.png            # Generated digital university logo
│
├── components/
│      ├── cards.py            # Dashboard metrics grid and quick action buttons
│      ├── navbar.py           # Top user details and API connection indicators
│      └── sidebar.py          # Unified option-menu navigation controls
│
├── database/
│      ├── users.json          # Persistent user register list
│      └── history.json        # Persistent chat history database
│
├── pages/
│      ├── ai_assistant.py     # AI Chatbot interface with prompts selectors
│      ├── dashboard.py        # Statistics workspace and activity feeds
│      ├── history.py          # Keyword logs filter and deletion controls
│      ├── login.py            # Secure authentication form
│      ├── profile.py          # Student detail cards and editor form
│      ├── register.py         # Sign up form with fields checks
│      └── settings.py         # Theme selection and connection status tests
│
├── utils/
│      ├── ai.py               # OpenAI client calls and system prompt routing
│      ├── auth.py             # User signup, matching, and passwords hashing
│      ├── database.py         # JSON file reading, writing, and backup recovery
│      └── helpers.py          # Styles injects, greetings, and timestamps
│
├── .env                       # Environment credentials keys configuration
├── .gitignore                 # Excluded elements listing
├── app.py                     # Main workspace execution router
├── requirements.txt           # Deployment dependencies manifest
└── README.md                  # System instruction handbook
```

---

## 🛠️ Local Installation

Follow these steps to configure and run SmartCampusAI on your local machine:

### 1. Prerequisite Checks
Ensure you have **Python 3.11 or higher** installed.

### 2. Set Up a Virtual Environment (Recommended)
Open your terminal in the project folder and run:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Run the installation script to import libraries:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Keys
Open the `.env` file in the project root and add your OpenAI API key:

```text
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```

*Note: If the key is unset, you can still register, log in, browse the dashboard, and manage profiles. You can also paste your API key temporarily inside the settings page during runtime.*

---

## 🏃 Run Project

Once installation is complete, start the application:

```bash
streamlit run app.py
```

Streamlit will launch a server and open the app in your browser (usually at `http://localhost:8501`).

---

## ☁️ Deployment Steps (Streamlit Cloud)

To host your app online for free using Streamlit Cloud:

1. **Push your code to GitHub**: Create a repository containing all files (except the local `.env` and `venv` directory).
2. **Access Streamlit Share**: Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. **Deploy App**:
   * Choose your repository, branch (usually `main`), and the main file path (`app.py`).
4. **Set Up Secrets**:
   * Open the **Advanced Settings** dialog in the deployment workflow.
   * Under the **Secrets** text area, paste your environment variables:
     ```toml
     OPENAI_API_KEY = "sk-proj-YOUR_ACTUAL_KEY_HERE"
     ```
5. **Launch**: Click **Deploy** and wait for the containers to build.

---

## 🔮 Future Enhancements

* **AI Exam Generator**: Create automated quizzing cards based on department topics.
* **Vector Document Uploads**: Feed syllabus PDFs directly into a RAG pipeline for study answers.
* **Analytics Reports**: Plot charts representing study time, topics questioned, and performance.
* **Social Connections**: Create public forum channels where students can invite peers.
