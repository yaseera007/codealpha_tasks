from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Gemini API Key from Environment Variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Warning: GEMINI_API_KEY not found")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "response": "Please enter a message."
            })

        prompt = f"""
You are an AI Chatbot Assistant.

Provide:
- Accurate answers
- Helpful explanations
- Professional responses
- Programming help
- Cloud Computing guidance
- General knowledge answers

Question:
{user_message}
"""

        response = model.generate_content(prompt)

        return jsonify({
            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "response": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)