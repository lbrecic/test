from daytona import Daytona, SessionExecuteRequest

daytona = Daytona()

sandbox = daytona.create()

app_code = b'''
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello World</title>
        <link rel="icon" href="https://www.daytona.io/favicon.ico">
    </head>
    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #0a0a0a; font-family: Arial, sans-serif;">
        <div style="text-align: center; padding: 2rem; border-radius: 10px; background-color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <img src="https://raw.githubusercontent.com/daytonaio/daytona/main/assets/images/Daytona-logotype-black.png" alt="Daytona Logo" style="width: 180px; margin: 10px 0px;">
            <p>This web app is running in a Daytona sandbox!</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
'''

# Save the Flask app to a file

sandbox.fs.upload_file(app_code, "app.py")

# Create a new session and execute a command

exec_session_id = "python-app-session"
sandbox.process.create_session(exec_session_id)

sandbox.process.execute_session_command(exec_session_id, SessionExecuteRequest(
    command="python /app.py",
    var_async=True
))

# Get the preview link for the Flask app

preview_info = sandbox.get_preview_link(3000)
print(f"Flask app is available at: {preview_info.url}")
