import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    # Récupère la version gravée dans l'image ou par défaut "Unknown"
    version = os.environ.get("APP_VERSION", "Unknown")
    color = "blue" if version == "1" else "red"
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1 style="color: {color};">Hello from Version {version}</h1>
        <p>Deployment & Rollback Demo</p>
    </div>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)