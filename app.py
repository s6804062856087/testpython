from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "✅ Python is running on Azure Web App"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
