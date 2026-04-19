# 🚀 AI DevOps Agent (Autonomous CI/CD Healing System)

An intelligent autonomous DevOps agent that detects, fixes, and validates CI CD pipeline failures automatically using AI driven workflows.

# 📌 Overview

Modern CI CD pipelines often fail due to syntax errors, logic bugs, linting issues, or integration problems.
This project builds a self healing AI agent that can analyze repositories, detect issues, generate fixes, and re run pipelines until all tests pass.

# ⚙️ Features

- Automated repository analysis
- AI based bug detection (syntax, logic, linting)
- Auto fix generation and commit with AI tagging
- Iterative CI CD monitoring
- React dashboard for visualization
- Docker based sandbox execution

# 🧠 How It Works

1. User provides a GitHub repository URL
2. Agent clones and scans the repository
3. Detects failing test cases and issues
4. Generates fixes using AI
5. Commits changes to a new branch
6. Runs CI CD pipeline
7. Repeats until success

# 🏗️ Architecture

Frontend: React.js
Backend: Python
AI Layer: LLM Agents (LangGraph or CrewAI)
Execution: Docker
Version Control: GitHub API
CI CD: Automated pipelines

# 🛠️ Tech Stack

Python
React.js
AI Agents (LangGraph or CrewAI)
GitHub API
Docker
CI CD Tools

# 📊 Dashboard Features

- Repository input and execution trigger
- Run summary with status
- Fixes applied with details
- CI CD timeline visualization
- Score and performance metrics

# 🚀 Installation and Setup

git clone https://github.com/abhay-labs/AI-DevOps-Agent-Autonomous-CI-CD-Healing-System-.git

## Backend Setup
cd backend
pip install -r requirements.txt
python main.py

## Frontend Setup
cd frontend
npm install
npm start

# ▶️ Usage

1. Open the dashboard
2. Enter GitHub repository URL
3. Click Run Agent
4. View results and fixes

# 📁 Project Structure

ai-devops-agent/
backend/
agents/
utils/
main.py
requirements.txt

frontend/
src/
components/
package.json

docker/
results.json
README.md

# 📈 Supported Bug Types

- Linting Errors
- Syntax Errors
- Logic Bugs
- Type Errors
- Import Issues
- Indentation Errors

# ⚠️ Limitations

- Complex bugs may require multiple iterations
- Depends on test cases availability
- Performance may vary on large repos

# 🔮 Future Improvements

- Real time alerts
- Better LLM fine tuning
- Multi language support
- Cloud CI CD integration

# 👨‍💻 Author

Abhay Jaiswal
GitHub: https://github.com/abhay-labs
LinkedIn: https://www.linkedin.com/in/abhayjaiswal79/

# ⭐ Contributing

Fork the repo and create a pull request

# 📜 License

MIT License
