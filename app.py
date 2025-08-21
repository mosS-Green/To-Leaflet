#!/usr/bin/env python

import json
import os

import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Cache environment values globally so we don’t repeatedly query os.getenv
ENV_BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ENV_CHAT_ID = os.getenv("CHAT_ID", "").strip()
ENV_PORT = os.getenv("PORT")

# The main HTML template has been heavily modified to support the new features.
# The CSS is updated for the dark theme and new elements.
# The JavaScript now handles drag-and-drop, collapsible sections, and asynchronous form submission.
SINGLE_PAGE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Telegram File Uploader</title>
  <style>
    :root {
      --bg-dark: #2c3531;
      --bg-darker: #1a201e;
      --text-light: #d1e0d1;
      --accent-sage: #5b8e7d;
      --accent-sage-hover: #6c9f8f;
      --border-color: #4a5c53;
      --success-color: #6bb06b;
      --error-color: #d9534f;
      --info-color: #6c9f8f;
    }
    body {
      font-family: system-ui, -apple-system, Segoe UI, Roboto, 'Helvetica Neue', Arial;
      background-color: var(--bg-darker);
      color: var(--text-light);
      max-width: 700px;
      margin: 40px auto;
      padding: 18px;
    }
    .container {
      background-color: var(--bg-dark);
      padding: 24px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
    }
    h1 {
      font-size: 24px;
      margin-bottom: 20px;
      text-align: center;
      color: var(--text-light);
    }
    label {
      display: block;
      margin-top: 12px;
      font-weight: 600;
      font-size: 14px;
    }
    input[type=text], textarea {
      width: 100%;
      padding: 10px;
      margin-top: 6px;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      background-color: var(--bg-darker);
      color: var(--text-light);
      box-sizing: border-box;
    }
    textarea { resize: vertical; }
    /* --- Collapsible Credentials Section --- */
    .collapsible-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      padding: 8px 0;
      user-select: none;
    }
    .collapsible-header h2 {
      font-size: 16px;
      margin: 0;
      font-weight: 600;
    }
    #toggle-arrow {
      transition: transform 0.3s ease;
    }
    .collapsed #toggle-arrow {
      transform: rotate(-90deg);
    }
    #credentials-content {
      max-height: 500px; /* arbitrary large value */
      overflow: hidden;
      transition: max-height 0.4s ease-in-out;
    }
    .collapsed #credentials-content {
      max-height: 0;
    }
    /* --- Drag and Drop Zone --- */
    #drop-zone {
      border: 2px dashed var(--border-color);
      border-radius: 8px;
      padding: 40px 20px;
      text-align: center;
      margin-top: 20px;
      transition: border-color 0.3s, background-color 0.3s;
      cursor: pointer;
    }
    #drop-zone.drag-over {
      border-color: var(--accent-sage);
      background-color: rgba(91, 142, 125, 0.1);
    }
    #drop-zone-text { font-weight: 600; }
    #file-name {
      margin-top: 10px;
      font-style: italic;
      color: var(--accent-sage);
    }
    /* Hide the default file input */
    input[type=file] { display: none; }
    /* --- Buttons and Messages --- */
    button {
      margin-top: 16px;
      padding: 12px 18px;
      border-radius: 8px;
      border: 0;
      background: var(--accent-sage);
      color: white;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    button:hover:not(:disabled) { background: var(--accent-sage-hover); }
    button:active:not(:disabled) { transform: translateY(1px); }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    .hint { font-size: 13px; color: #aaa; margin-top: 6px; }
    .env-warning { font-size: 13px; color: var(--info-color); margin-top: 6px; }
    /* --- Result Area --- */
    #result {
      margin-top: 25px;
      padding: 15px;
      border-radius: 6px;
      display: none; /* Hidden by default */
      background: var(--bg-darker);
      border: 1px solid var(--border-color);
    }
    #result pre {
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
      font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
      font-size: 14px;
    }
    #result.success { border-left: 4px solid var(--success-color); }
    #result.error { border-left: 4px solid var(--error-color); }
  </style>
</head>
<body>
  <div class="container">
    <h1>Telegram File Uploader</h1>
    <form id="uploadForm">
      
      <!-- Collapsible Credentials Section -->
      <div id="credentials-container" class="collapsed">
        <div class="collapsible-header" onclick="toggleCredentials()">
          <h2>Credentials</h2>
          <svg id="toggle-arrow" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
        </div>
        <div id="credentials-content">
          <label for="token">Bot token</label>
          <input id="token" name="token" type="text" placeholder="123456789:AAH..." value="{{ url_token|default('') }}">
          <div id="envTokenMsg" class="env-warning" style="display:none">Default server value will be used for Bot Token.</div>
          
          <label for="chatid">Chat ID</label>
          <input id="chatid" name="chatid" type="text" placeholder="-1001234567890" value="{{ url_chatid|default('') }}">
          <div id="envChatMsg" class="env-warning" style="display:none">Default server value will be used for Chat ID.</div>
        </div>
      </div>
      
      <label for="caption">Caption (optional)</label>
      <textarea id="caption" name="caption" rows="2" placeholder="Write a caption...">{{ caption|default('') }}</textarea>
      
      <!-- Drag and Drop Zone -->
      <label>File</label>
      <div id="drop-zone">
        <span id="drop-zone-text">Drag & drop a file here, or click to select</span>
        <div id="file-name"></div>
      </div>
      <input id="file-input" name="file" type="file" required>
      
      <button id="uploadBtn" type="submit" disabled>Upload</button>
    </form>
    
    <!-- API Response Area -->
    <div id="result">
      <pre id="result-text"></pre>
    </div>
  </div>

  <script>
    const envToken = {{ env_token|tojson }};
    const envChat = {{ env_chatid|tojson }};

    const uploadForm = document.getElementById('uploadForm');
    const tokenInput = document.getElementById('token');
    const chatInput = document.getElementById('chatid');
    const uploadBtn = document.getElementById('uploadBtn');
    const envTokenMsg = document.getElementById('envTokenMsg');
    const envChatMsg = document.getElementById('envChatMsg');
    
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const dropZoneText = document.getElementById('drop-zone-text');
    const fileNameDisplay = document.getElementById('file-name');
    
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');

    // --- State and Validation ---
    function hasTokenValue() { return tokenInput.value && tokenInput.value.trim().length > 0; }
    function hasChatValue() { return chatInput.value && chatInput.value.trim().length > 0; }

    function updateEnvMessages() {
      envTokenMsg.style.display = (!hasTokenValue() && envToken) ? 'block' : 'none';
      envChatMsg.style.display = (!hasChatValue() && envChat) ? 'block' : 'none';
    }

    function updateUploadButton() {
      const okToken = hasTokenValue() || envToken;
      const okChat = hasChatValue() || envChat;
      const okFile = fileInput.files.length > 0;
      uploadBtn.disabled = !(okToken && okChat && okFile);
    }
    
    tokenInput.addEventListener('input', () => { updateEnvMessages(); updateUploadButton(); });
    chatInput.addEventListener('input', () => { updateEnvMessages(); updateUploadButton(); });
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            dropZoneText.textContent = 'File selected:';
            fileNameDisplay.textContent = fileInput.files[0].name;
        } else {
            dropZoneText.textContent = 'Drag & drop a file here, or click to select';
            fileNameDisplay.textContent = '';
        }
        updateUploadButton();
    });

    // --- Collapsible Section ---
    function toggleCredentials() {
      document.getElementById('credentials-container').classList.toggle('collapsed');
    }

    // --- Drag and Drop Logic ---
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        // Manually trigger the 'change' event to update UI
        fileInput.dispatchEvent(new Event('change'));
        // Automatically submit the form on drop
        submitForm();
      }
    });

    // --- Form Submission (AJAX) ---
    uploadForm.addEventListener('submit', (e) => {
        e.preventDefault();
        submitForm();
    });

    function submitForm() {
        if (uploadBtn.disabled) {
            // Un-collapse credentials if they are required and empty
            if (!hasTokenValue() && !envToken) toggleCredentials(false);
            if (!hasChatValue() && !envChat) toggleCredentials(false);
            alert('Please provide Bot Token, Chat ID, and select a file.');
            return;
        }

        const formData = new FormData(uploadForm);
        
        // Show loading state
        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Uploading...';
        resultDiv.style.display = 'none';

        fetch("{{ url_for('upload') }}", {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultText.textContent = data.message;
            resultDiv.className = data.ok ? 'success' : 'error';
            resultDiv.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            resultText.textContent = 'An unexpected error occurred. Check the console for details.';
            resultDiv.className = 'error';
            resultDiv.style.display = 'block';
        })
        .finally(() => {
            uploadBtn.textContent = 'Upload';
            // Re-enable button based on current form state
            updateUploadButton();
        });
    }
    
    // --- Initial State Setup ---
    updateEnvMessages();
    updateUploadButton();

  </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    """Renders the main single-page application."""
    env_token_present = bool(ENV_BOT_TOKEN)
    env_chatid_present = bool(ENV_CHAT_ID)

    url_token = request.args.get("token", "")
    url_chatid = request.args.get("chatid", "")
    caption = request.args.get("caption", "")

    return render_template_string(
        SINGLE_PAGE_HTML,
        env_token=env_token_present,
        env_chatid=env_chatid_present,
        url_token=url_token,
        url_chatid=url_chatid,
        caption=caption,
    )


@app.route("/upload", methods=["POST"])
def upload():
    """Handles the file upload and returns a JSON response."""
    token = request.form.get("token", "").strip()
    chat_id = request.form.get("chatid", "").strip()
    caption = request.form.get("caption", "").strip()
    file = request.files.get("file")

    if not token and ENV_BOT_TOKEN:
        token = ENV_BOT_TOKEN
    if not chat_id and ENV_CHAT_ID:
        chat_id = ENV_CHAT_ID

    if not token or not chat_id:
        return jsonify({
            "ok": False,
            "message": "❌ Missing Bot token or Chat ID. Provide them in the form or set server environment variables."
        }), 400

    if not file:
        return jsonify({"ok": False, "message": "❌ No file was provided."}), 400

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    try:
        resp = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"document": (file.filename, file.stream, file.mimetype)},
            timeout=60  # Add a timeout for robustness
        )
        resp.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = resp.json()
        if data.get("ok"):
            msg = data["result"]
            message = (
                f"✅ Upload successful!\n\n"
                f"  Message ID: {msg['message_id']}\n"
                f"  Chat: {msg['chat'].get('title', msg['chat']['id'])}\n"
                f"  File ID: {msg['document']['file_id']}\n"
                f"  File Name: {msg['document'].get('file_name', file.filename)}\n"
                f"  File Size: {msg['document'].get('file_size', 0):,} bytes"
            )
            return jsonify({"ok": True, "message": message})
        else:
            return jsonify({
                "ok": False,
                "message": f"❌ Telegram API Error: {data.get('description', 'Unknown error')}"
            }), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"ok": False, "message": f"❌ Network or HTTP Error: {e}"}), 500
    except json.JSONDecodeError:
        return jsonify({"ok": False, "message": f"❌ Failed to parse Telegram API response."}), 500


if __name__ == "__main__":
    # Use debug=True for development, but turn it off for production
    app.run(host="0.0.0.0", port=ENV_PORT, debug=True)
