import os
import re
import requests
from daytona import Daytona
from dotenv import load_dotenv

load_dotenv()

daytona = Daytona()

sandbox = daytona.create()

def get_claude_response(api_key, prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude-3-7-sonnet-latest",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        content = response.json().get("content", [])
        return "".join([item["text"] for item in content if item["type"] == "text"])
    else:
        return f"Error {response.status_code}: {response.text}"

prompt = "Python code that returns the factorial of 25. Output only the code. No explanation. No intro. No comments. Just raw code in a single code block."

result = get_claude_response(os.environ["ANTHROPIC_API_KEY"], prompt)

code_match = re.search(r"```python\n(.*?)```", result, re.DOTALL)

code = code_match.group(1) if code_match else result
code = code.replace('\\', '\\\\')

# Run Python code inside the Sandbox and get the output

response = sandbox.process.code_run(code)
print("The factorial of 25 is", response.result)
