#!/usr/bin/env python

import json
import os
import requests
from flask import Flask, render_template_string, request, jsonify, send_from_directory

app = Flask(__name__)

# Cache environment values globally so we don’t repeatedly query os.getenv
ENV_BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ENV_CHAT_ID = os.getenv("CHAT_ID", "").strip()
ENV_PORT = os.getenv("PORT")

# The HTML, CSS, and JS have been updated for the new features.
SINGLE_PAGE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Telegram File Uploader</title>
  <link rel="icon" type="image/png" href="{{ url_for('favicon') }}">
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
      font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
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
    /* --- Collapsible Header --- */
    #header-container.collapsed #credentials-content {
      max-height: 0;
    }
    #header-container.collapsed #toggle-arrow {
      transform: rotate(-90deg);
    }
    .header-title {
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      user-select: none;
      position: relative; /* For arrow positioning */
    }
    h1 {
      font-size: 24px;
      margin-bottom: 20px;
      text-align: center;
    }
    #toggle-arrow {
      transition: transform 0.3s ease;
      position: absolute;
      right: 0;
      top: 5px;
    }
    #credentials-content {
      max-height: 500px;
      overflow: hidden;
      transition: max-height 0.4s ease-in-out;
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
      font-family: inherit;
    }
    textarea { resize: vertical; }
    .env-warning { font-size: 13px; color: var(--info-color); margin-top: 6px; }
    /* --- Drag and Drop & Paste Zones --- */
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
    #file-name {
      margin-top: 10px;
      font-style: italic;
      color: var(--accent-sage);
    }
    #paste-zone {
      border-top: 1px solid var(--border-color);
      margin-top: 20px;
      padding-top: 15px;
      text-align: center;
      color: #aaa;
      font-size: 14px;
      cursor: pointer;
    }
    input[type=file] { display: none; }
    /* --- Buttons and Result Area --- */
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
      font-family: inherit;
    }
    button:hover:not(:disabled) { background: var(--accent-sage-hover); }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    #result {
      margin-top: 25px;
      padding: 15px;
      border-radius: 6px;
      display: none;
      background: var(--bg-darker);
      border: 1px solid var(--border-color);
      opacity: 0;
      transition: opacity 0.5s ease;
    }
    #result.visible {
      display: block;
      opacity: 1;
    }
    #result pre {
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
      font-size: 14px;
    }
    #result.success { border-left: 4px solid var(--success-color); }
    #result.error { border-left: 4px solid var(--error-color); }
  </style>
</head>
<body>
  <div class="container">
    <div id="header-container" class="collapsed">
      <div class="header-title" onclick="toggleCredentials()">
        <h1>Telegram Uploader</h1>
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

    <form id="uploadForm">
      <label for="caption">Caption (optional)</label>
      <textarea id="caption" name="caption" rows="2" placeholder="Write a caption...">{{ caption|default('') }}</textarea>
      
      <label>File</label>
      <div id="drop-zone">
        <span id="drop-zone-text">Drag & drop a file here, or click to select</span>
        <div id="file-name"></div>
      </div>
      <input id="file-input" name="file" type="file" required>
      
      <button id="uploadBtn" type="submit" disabled>Upload</button>
      
      <div id="paste-zone" tabindex="0">
        Or click here and paste an image (Ctrl+V)
      </div>
    </form>
    
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
    const pasteZone = document.getElementById('paste-zone');
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    let resultTimer = null;

    // --- State and Validation ---
    function hasTokenValue() { return tokenInput.value && tokenInput.value.trim().length > 0; }
    function hasChatValue() { return chatInput.value && chatInput.value.trim().length > 0; }

    function updateEnvMessages() {
      envTokenMsg.style.display = (!hasTokenValue() && envToken) ? 'block' : 'none';
      envChatMsg.style.display = (!hasChatValue() && envChat) ? 'block' : 'none';
    }

    function checkReady() {
      const okToken = hasTokenValue() || envToken;
      const okChat = hasChatValue() || envChat;
      const okFile = fileInput.files.length > 0;
      uploadBtn.disabled = !(okToken && okChat && okFile);
    }
    
    tokenInput.addEventListener('input', () => { updateEnvMessages(); checkReady(); });
    chatInput.addEventListener('input', () => { updateEnvMessages(); checkReady(); });
    fileInput.addEventListener('change', () => {
        handleFileSelect(fileInput.files);
    });

    function handleFileSelect(files) {
        if (files && files.length > 0) {
            dropZoneText.textContent = 'File selected:';
            fileNameDisplay.textContent = files[0].name;
        } else {
            resetFileSelection();
        }
        checkReady();
    }

    function resetFileSelection() {
        fileInput.value = ''; // Important to clear the file input
        dropZoneText.textContent = 'Drag & drop a file here, or click to select';
        fileNameDisplay.textContent = '';
        checkReady(); // Re-evaluate button state
    }

    // --- Collapsible Credentials ---
    function toggleCredentials() {
      document.getElementById('header-container').classList.toggle('collapsed');
    }

    // --- Drag and Drop & Paste Logic ---
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelect(fileInput.files);
        submitForm();
      }
    });
    pasteZone.addEventListener('paste', (e) => {
      e.preventDefault();
      const items = (e.clipboardData || e.originalEvent.clipboardData).items;
      for (const item of items) {
        if (item.kind === 'file' && item.type.startsWith('image/')) {
          const blob = item.getAsFile();
          const timestamp = new Date().toISOString().replace(/[-:.]/g, '');
          const fileName = `pasted-image-${timestamp}.png`;
          const imageFile = new File([blob], fileName, { type: blob.type });
          
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(imageFile);
          fileInput.files = dataTransfer.files;

          handleFileSelect(fileInput.files);
          submitForm();
          return;
        }
      }
    });

    // --- Form Submission (AJAX) ---
    uploadForm.addEventListener('submit', (e) => {
        e.preventDefault();
        submitForm();
    });

    function submitForm() {
        if (uploadBtn.disabled) {
            if (!hasTokenValue() && !envToken || !hasChatValue() && !envChat) {
                document.getElementById('header-container').classList.remove('collapsed');
                alert('Missing Bot Token or Chat ID. Please provide them.');
            } else {
                alert('Please select a file to upload.');
            }
            return;
        }

        const formData = new FormData();
        formData.append('token', tokenInput.value);
        formData.append('chatid', chatInput.value);
        formData.append('caption', document.getElementById('caption').value);
        formData.append('file', fileInput.files[0]);

        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Uploading...';
        clearTimeout(resultTimer);
        resultDiv.classList.remove('visible');

        fetch("{{ url_for('upload') }}", { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => displayResult(data.message, data.ok))
        .catch(error => {
            console.error('Error:', error);
            displayResult('An unexpected error occurred. Check the console.', false);
        })
        .finally(() => {
            uploadBtn.textContent = 'Upload';
            checkReady();
        });
    }

    function displayResult(message, isSuccess) {
        resultText.textContent = message;
        resultDiv.className = isSuccess ? 'success' : 'error';
        resultDiv.classList.add('visible');

        resultTimer = setTimeout(() => {
            resultDiv.classList.remove('visible');
            // Reset file selection after feedback disappears
            resetFileSelection();
        }, 3000);
    }
    
    // --- Initial State Setup ---
    updateEnvMessages();
    checkReady();
  </script>
</body>
</html>
"""

@app.route('/icon.png')
def favicon():
    """Serves the favicon."""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)),
                               'icon.png', mimetype='image/png')

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
            "message": "❌ Missing Bot Token or Chat ID. Provide them via URL params or server environment variables."
        }), 400

    if not file or not file.filename:
        return jsonify({"ok": False, "message": "❌ No file was provided."}), 400

    mimetype = file.mimetype.lower()
    if mimetype.startswith('image/'):
        api_method = 'sendPhoto'
        file_type_key = 'photo'
    else:
        api_method = 'sendDocument'
        file_type_key = 'document'
    
    url = f"https://api.telegram.org/bot{token}/{api_method}"
    
    try:
        resp = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={file_type_key: (file.filename, file.stream, file.mimetype)},
            timeout=60
        )
        resp.raise_for_status()

        data = resp.json()
        if data.get("ok"):
            msg = data["result"]
            file_details = msg.get(file_type_key)
            if file_type_key == 'photo':
                if isinstance(file_details, list) and file_details:
                    file_details = max(file_details, key=lambda x: x.get('file_size', 0))
                else:
                    file_details = {} 

            message = (
                f"✅ Upload successful!\n\n"
                f"  Message ID: {msg['message_id']}\n"
                f"  Chat: {msg['chat'].get('title', msg['chat']['id'])}\n"
                f"  File ID: {file_details.get('file_id', 'N/A')}\n"
                f"  File Name: {file.filename}\n"
                f"  File Size: {file_details.get('file_size', 0):,} bytes"
            )
            return jsonify({"ok": True, "message": message})
        else:
            return jsonify({
                "ok": False,
                "message": f"❌ Telegram API Error: {data.get('description', 'Unknown error')}"
            }), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"ok": False, "message": f"❌ Network or HTTP Error: {e}"}), 500
    except (json.JSONDecodeError, KeyError) as e:
        return jsonify({"ok": False, "message": f"❌ Error parsing API response or missing data: {e}\nResponse: {resp.text}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=ENV_PORT, debug=True)
