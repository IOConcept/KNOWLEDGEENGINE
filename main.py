from flask import Flask, render_template, request, jsonify
import openai
import subprocess
from datetime import datetime
import os

app = Flask(__name__)

# Initialize the OpenAI API client
openai.api_key = "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"

# Define the path to the Mimic executable
mimic_path = r"C:\\Users\\Eric\\PycharmProjects\\ChattyBot\\models\\mimic_windows_amd64\\mimic.exe"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")

    if question.lower() == "quit":
        return jsonify({"text": "", "audio": ""})

    # Sanitize input here if necessary
    prompt = f"You are a wise old elder and legendary story teller,you are creative and long winded. {question}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=1.0,
            max_tokens=4000
        )
    except Exception as e:
        return jsonify({"error": str(e)})

    text = response.choices[0].text.strip()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Ensure that the "static" directory exists
    os.makedirs('static', exist_ok=True)

    # Save the audio file in the "static" directory
    audio_file = f"static/response_{timestamp}.wav"

    try:
        subprocess.run([mimic_path, "-t", text, "-o", audio_file], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)})

    return jsonify({"text": text, "audio": audio_file})

if __name__ == "__main__":
    app.run(debug=True)
