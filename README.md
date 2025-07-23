
# Project Roberto: Your Personal AI Assistant

Welcome to Project Roberto! This project is your very own personal AI assistant, designed to be a super-intelligent, multi-skilled agent that can help you with a wide variety of tasks. Whether you need help with coding, writing notes, managing your to-do list, or just getting information, Roberto is here to help.

## What is Roberto?

Imagine having a brilliant assistant who knows you, remembers your conversations, and can help you with almost anything. That's Roberto. He's like a super-powered version of ChatGPT, but he lives on your computer and can be customized to your exact needs.

Roberto is built with some of the latest and greatest AI technology, including:

*   **LangGraph:** A powerful framework for building smart, stateful AI agents.
*   **Ollama:** A tool that lets you run powerful language models like Mistral right on your own computer, for free.
*   **ChromaDB:** A super-fast database for storing and retrieving information, which acts as Roberto's memory.
*   **LlamaIndex:** A tool that helps Roberto read and understand your documents, so he can learn from them.

## What Can Roberto Do?

Roberto has a variety of skills, which we call "tools." These tools allow him to do things like:

*   **Remember Information:** You can ask Roberto to remember things about you, and he'll store them in his memory.
*   **Read Your Notes:** You can give Roberto a folder of your notes, and he can read and understand them.
*   **Answer Questions:** You can ask Roberto questions about your notes, and he'll use his knowledge to give you answers.
*   **Write Notes:** You can ask Roberto to write notes for you, and he'll save them to a file.
*   **Create To-Do Lists:** You can ask Roberto to create a to-do list for you, and he'll save it to a file.
*   **Search the Web:** You can ask Roberto to search the web for information, and he'll give you a summary of what he finds.
*   **Refactor Code:** You can give Roberto a piece of code, and he can help you improve it.

## How Does Roberto Work? (The Architecture)

Roberto is built like a team of specialists who all report to a manager. The manager is the "Super Agent," and the specialists are the "tools."

Here's a look at the project's folder structure:

```
/project-roberto
├── agents/             # The "brain" of the agent
│   └── super_agent.py
├── models/             # The different language models Roberto can use
│   ├── gemini_model.py
│   ├── ollama_model.py
│   └── openai_model.py
├── tools/              # The different skills Roberto has
│   ├── code_refactor.py
│   ├── note_writer.py
│   ├── rag_service.py
│   ├── todo_writer.py
│   └── ...
├── .env                # Your secret API keys
├── main.py             # The main entry point for the application
├── requirements.txt    # A list of all the Python packages you need
└── README.md           # This file!
```

When you give Roberto a task, the `Super Agent` decides which tool is best for the job. For example, if you ask him to write a note, he'll use the `note_writer` tool. If you ask him a question, he might use the `rag_service` to check his memory or the `web_search` tool to look for information online.

## Getting Started

Ready to give Roberto a try? Here's how to get him set up on your computer.

### Assumptions

This guide assumes you have the following installed on your computer:

*   **Python 3:** Roberto is written in Python, so you'll need to have it installed.
*   **Homebrew:** This is a package manager for macOS that makes it easy to install software.
*   **Git:** This is a version control system that you'll use to download the project.
*   **Obsidian or Heynote (Optional):** If you want to use Roberto to manage your notes, you'll need to have a note-taking app like Obsidian or Heynote installed. These apps store your notes as plain text files in a folder on your computer, which makes it easy for Roberto to read them.

### Requirements

Before you can run Roberto, you'll need to install a few things. Open your terminal and run the following commands:

1.  **Install Ollama:** This will allow you to run language models on your computer.

    ```bash
    brew install ollama
    ```

2.  **Download the Mistral Model:** This is the language model that Roberto will use.

    ```bash
    ollama pull mistral
    ```

3.  **Clone the Project:** This will download the project to your computer.

    ```bash
    git clone https://github.com/jacksalillas/project-roberto.git
    cd project-roberto
    ```

4.  **Create a Virtual Environment:** This will create a special, isolated environment for Roberto's Python packages.

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

5.  **Install the Python Packages:** This will install all the Python packages that Roberto needs.

    ```bash
    pip install -r requirements.txt
    ```

6.  **Set Up Your API Keys:** If you want to use OpenAI or Gemini, you'll need to add your API keys to the `.env` file. You can do this by copying the `.env.example` file to `.env` and then adding your keys.

### How to Use Roberto

Now that Roberto is all set up, you can start using him. Here are a few examples of how to interact with him from your terminal:

*   **Index Your Notes:** To give Roberto access to your notes, you'll need to index them first. You only need to do this once.

    ```bash
    python3 main.py index --path /path/to/your/notes
    ```

*   **Ask a Question:** You can ask Roberto a question about your notes or anything else.

    ```bash
    python3 main.py task --llm ollama --task "What is the main topic of my notes?"
    ```

*   **Write a Note:** You can ask Roberto to write a note for you.

    ```bash
    python3 main.py task --llm ollama --task "Write a note about my meeting with Jane Doe."
    ```

*   **Search the Web:** You can ask Roberto to search the web for information.

    ```bash
    python3 main.py task --llm ollama --task "What's the latest news on AI?"
    ```

## Using Roberto with Your Notes

One of the most powerful features of Roberto is his ability to read and understand your notes. This allows you to create a personalized knowledge base that you can query and interact with in natural language.

To use Roberto with your notes, you'll need to have a note-taking app that stores your notes as plain text files in a folder on your computer. Some popular apps that do this are:

*   **Obsidian:** A powerful knowledge base that works on top of a local folder of Markdown files.
*   **Heynote:** A simple and elegant note-taking app for your terminal.

Once you have your notes in a folder, you can use the `index` command to add them to Roberto's memory. For example, if your notes are in a folder called `~/MyNotes`, you would run the following command:

```bash
python3 main.py index --path ~/MyNotes
```

Once your notes are indexed, you can ask Roberto questions about them. For example, you could ask:

*   "What are the main points from my notes on project planning?"
*   "Summarize my notes on the book 'The Pragmatic Programmer'."
*   "What did I write about my meeting with John Doe?"

Roberto can also help you create new notes. For example, you could say:

*   "Write a note about my idea for a new app."
*   "Create a to-do list for my weekend projects."

By combining Roberto with a note-taking app like Obsidian or Heynote, you can create a powerful and personalized knowledge management system that helps you stay organized and informed.
