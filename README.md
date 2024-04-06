# Project Setup Guide

Welcome to our project! This guide will walk you through setting up the project on your local machine. Our project is built using React.js and Material UI for the frontend, FastAPI for the backend, and Langchain for orchestration, with interactions with Large Language Models (LLMs) via OpenAI API.

## Prerequisites

- Python 3.8 or higher
- Node.js and npm
- Git

### Cloning the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Omkarthipparthi/VATS_AI.git
cd VATS_AI
```

### Create an Python virtual environment

```bash
python -m venv venv
```

### Activating the Virtual Environment
Activate the virtual environment on Windows:


```bash
.\venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```
### Installing Dependencies
Install all required Python packages from the requirements.txt file:



```bash
pip install -r requirements.txt
```

### Setting Up Environment Variables
Create a .env file in the root directory of the project and add the following content:

```bash
OPENAI_API_KEY=" "
```

Make sure to add the .env file to your .gitignore to avoid exposing your API key.

# Running the Backend Server
Use Uvicorn to run the FastAPI backend server:

```bash
uvicorn app.main:app --reload
```

## Frontend Setup
### Installing Node Modules
Navigate to the frontend directory and install the required node modules:

```bash
cd VATS_AI
npm install
```

### Starting the React App

Start the React application:

```bash
npm start
```

This command runs the app in the development mode. Open http://localhost:3000 to view it in the browser.

## Additional Information

- The project uses Material UI for styling. Refer to the [Material UI documentation](https://material-ui.com/) for components and usage.
- For more information on FastAPI, visit the [FastAPI documentation](https://fastapi.tiangolo.com/).
- Learn about Langchain for orchestrating your LLMs [here](https://langchain.com/).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
