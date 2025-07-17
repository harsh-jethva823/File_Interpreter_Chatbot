from flask import Flask, render_template_string, request
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyCOYJIhNLGDZ5WHKyydveQ2UU0__SC92eM")  # Replace with your real key
model = genai.GenerativeModel('gemini-1.5-flash')

# HTML + JS Frontend in a single page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title> File Interpreter Chatbot</title>
</head>
<body style="font-family:Arial; padding:20px;">
    <h2>📄 Gemini Chatbot with File Insight</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Upload File:</label>
        <input type="file" name="file" required>
        <br><br>
        <label>Your Question:</label><br>
        <textarea name="query" rows="4" cols="60" placeholder="Ask something..." required></textarea>
        <br><br>
        <button type="submit">Ask ChatBot</button>
    </form>

    {% if response %}
        <h3>🔍 ChatBot Response:</h3>
        <div style="white-space: pre-wrap; border:1px solid #ccc; padding:10px;">{{ response }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None
    if request.method == 'POST':
        file = request.files['file']
        query = request.form['query']

        if file:
            content = file.read().decode('utf-8', errors='ignore')
            prompt = f"Here's a file content:\n{content[:3000]}\n\nNow answer this:\n{query}"

            try:
                response = model.generate_content(prompt)
                response_text = response.text
            except Exception as e:
                response_text = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
