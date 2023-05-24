# DLL_Mass_Grading
> Author: [Can Wang](mailto:canw7@uci.edu)

Project for digital learning lab at UC, Irvine. 

Please follow the user guide to set up the project properly before using.

# User Guide

## Facts

### Assumptions
 - All essays are formatted as docx files under the same directory
 - The grading can be finished or aborted before the timeout
 - The token size of one request and response pair and instructing prompts mentioned below is lower than the limitation of OpenAI API (GPT-3.5 model)

### Tech Stack
 - Backend: Flask
 - Front-end: HTML, CSS, Vue, Element UI
 - OpenAI model: gpt-3.5-turbo

## Project Setup

### Prerequisites
 - Python version: 3.9 or newer

### Instruction
1. Use `Git` to clone the repo to the local machine

`git clone https://github.com/UCI-DLL/MassGradingProject.git`

2. Create a `.flaskenv` file and a `.env` file to properly set up runtime variables under the project root directory.

`.flaskenv` on Mac/Linux
```
    export FLASK_APP='massgrading_app'
    export FLASK_DEBUG='true'
```

`.env` on Mac/Linux
```
    export API_KEY='your_API_key'
    export ORG_ID='your_org_ID'
    export MODEL_ENGINE='gpt-3.5-turbo'
```

`.flaskenv` on Windows
```
    FLASK_APP=massgrading_app/__init__.py
    FLASK_DEBUG='true'
```

`.env` on Windows
```
    API_KEY=your_API_key
    ORG_ID=your_org_ID
    MODEL_ENGINE=gpt-3.5-turbo
```

You may see this issue:
```
    openai.error.RateLimitError: That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID e3c35f00d1d5611b5493aa05509711f0 in your message.)
```

3. Create a virtual environment and activate it. We'll do this in a directory called `venv`
    cd DLL_Mass_Grading

    # Mac/Linux
    python3 -m venv venv

    # Windows
    python -m venv venv

4. Activate the virtual environment
    # Mac/Linux
    . venv/bin/activate

    # Windows
    venv\Scripts\activate

5. Install third-party packages
`pip install -r "requirements.txt"`

6. Run the Flask app
`flask run`

Open [https://127.0.0.1:5000](https://127.0.0.1:5000) in your web browser.

## How to Use the App

If you've already completed steps 1-6 in a previous session, do the following:

- Navigate to the project directory
- `venv\Scripts\activate` or `. venv/bin/activate`
- `flask run`

And then do the following steps:

1. Put the essays in `.docx` format under one directory, then put the directory under `..../DLL_Mass_Grading/massgrading_app/static/files`

2. Put the prompt instructions in a file named `chatgpt_instructions.txt` in the **same** folder as the essay files. Also, make sure your prompt formats the output with JSON!

3. On the web browser, click Select Local Directory, find the directory with the essays, and click on it. Then use the slider to set the temperature value properly.

4. Click Start Grading, double-check the selections, then wait for it to finish!

5. Look for your outcome assets, two files under a newly created directory in the same folder as your essay files. The new directory should have a timestamp as its name. You're looking for two files:
 - `grading_result.csv`
 - `execution_log.log`