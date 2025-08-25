#!/usr/bin/env python

import json
import os
import time
from urllib.parse import quote
import requests
from flask import Flask, render_template_string, request, jsonify, send_from_directory

app = Flask(__name__)

# --- Configuration ---
ENV_BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ENV_CHAT_ID = os.getenv("CHAT_ID", "").strip()
FLASK_PORT = os.getenv("FLASK_PORT", 8080)
STREAM_URL = os.getenv("STREAM_URL", "http://localhost:8081").strip('/')

# Telegram API base URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{ENV_BOT_TOKEN}"

# --- Main HTML Template ---
SINGLE_PAGE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Telegram Uploader & Downloader</title>
  <link rel="icon" type="image/png" href="{{ url_for('favicon') }}">
  <style>
    :root {
      --bg-dark: #2c3531; --bg-darker: #1a201e; --text-light: #d1e0d1;
      --accent-sage: #5b8e7d; --accent-sage-hover: #6c9f8f; --border-color: #4a5c53;
      --success-color: #6bb06b; --error-color: #d9534f; --info-color: #6c9f8f;
    }
    body {
      font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
      background-color: var(--bg-darker); color: var(--text-light);
      max-width: 700px; margin: 40px auto; padding: 18px;
    }
    .container {
      background-color: var(--bg-dark); padding: 24px;
      border-radius: 12px; border: 1px solid var(--border-color);
    }
    /* --- Collapsible Header --- */
    #header-container.collapsed #credentials-content { max-height: 0; }
    #header-container.collapsed #toggle-arrow { transform: rotate(-90deg); }
    .header-title {
      display: flex; justify-content: center; align-items: center;
      cursor: pointer; user-select: none; position: relative;
    }
    h1 { font-size: 24px; margin-bottom: 20px; text-align: center; }
    #toggle-arrow { transition: transform 0.3s ease; position: absolute; right: 0; top: 5px; }
    #credentials-content { max-height: 500px; overflow: hidden; transition: max-height 0.4s ease-in-out; }
    label { display: block; margin-top: 12px; font-weight: 600; font-size: 14px; }
    input[type=text], textarea {
      width: 100%; padding: 10px; margin-top: 6px; border: 1px solid var(--border-color);
      border-radius: 6px; background-color: var(--bg-darker); color: var(--text-light);
      box-sizing: border-box; font-family: inherit;
    }
    textarea { resize: vertical; }
    .env-warning { font-size: 13px; color: var(--info-color); margin-top: 6px; }
    /* --- Uploader & Downloader Zones --- */
    #drop-zone {
      border: 2px dashed var(--border-color); border-radius: 8px; padding: 40px 20px;
      text-align: center; margin-top: 20px; transition: border-color 0.3s, background-color 0.3s; cursor: pointer;
    }
    #drop-zone.drag-over { border-color: var(--accent-sage); background-color: rgba(91, 142, 125, 0.1); }
    #file-name { margin-top: 10px; font-style: italic; color: var(--accent-sage); }
    #paste-zone {
      border-top: 1px solid var(--border-color); margin-top: 20px; padding-top: 15px;
      text-align: center; color: #aaa; font-size: 14px; cursor: pointer;
    }
    input[type=file] { display: none; }
    /* --- File Lister --- */
    #file-list-container { margin-top: 25px; border-top: 1px solid var(--border-color); padding-top: 15px; }
    #file-list { list-style: none; padding: 0; max-height: 300px; overflow-y: auto; }
    #file-list li {
      display: flex; justify-content: space-between; align-items: center;
      padding: 8px 12px; border-radius: 6px; margin-bottom: 5px;
      background-color: var(--bg-darker);
    }
    #file-list a { color: var(--text-light); text-decoration: none; word-break: break-all; }
    #file-list a:hover { text-decoration: underline; }
    #file-list .file-size { color: #aaa; font-size: 12px; white-space: nowrap; margin-left: 15px;}
    .spinner { display: none; margin: 10px auto; width: 24px; height: 24px; border: 3px solid var(--border-color); border-top-color: var(--accent-sage); border-radius: 50%; animation: spin 1s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    /* --- Buttons and Result Area --- */
    button {
      margin-top: 16px; padding: 12px 18px; border-radius: 8px; border: 0;
      background: var(--accent-sage); color: white; font-weight: 600; cursor: pointer;
      transition: background-color 0.2s; font-family: inherit;
    }
    button:hover:not(:disabled) { background: var(--accent-sage-hover); }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    #result {
      margin-top: 25px; padding: 15px; border-radius: 6px; display: none;
      background: var(--bg-darker); border: 1px solid var(--border-color);
      opacity: 0; transition: opacity 0.5s ease;
    }
    #result.visible { display: block; opacity: 1; }
    #result pre { white-space: pre-wrap; word-break: break-word; margin: 0; font-size: 14px; }
    #result.success { border-left: 4px solid var(--success-color); }
    #result.error { border-left: 4px solid var(--error-color); }
  </style>
</head>
<body>
  <div class="container">
    <div id="header-container" class="collapsed">
      <div class="header-title" onclick="toggleCredentials()">
        <h1>Telegram Tools</h1>
        <svg id="toggle-arrow" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
      </div>
      <div id="credentials-content">
        <label for="token">Bot token</label>
        <input id="token" name="token" type="text" placeholder="Read from server env" value="">
        <div id="envTokenMsg" class="env-warning" style="display:none">Using Bot Token from server environment.</div>
        <label for="chatid">Chat ID</label>
        <input id="chatid" name="chatid" type="text" placeholder="Read from server env" value="">
        <div id="envChatMsg" class="env-warning" style="display:none">Using Chat ID from server environment.</div>
      </div>
    </div>
    
    <!-- Uploader -->
    <form id="uploadForm">
      <label for="caption">Caption (optional)</label>
      <textarea id="caption" name="caption" rows="2" placeholder="Write a caption..."></textarea>
      <label>File Uploader</label>
      <div id="drop-zone">
        <span id="drop-zone-text">Drag & drop a file here, or click to select</span>
        <div id="file-name"></div>
      </div>
      <input id="file-input" name="file" type="file" required>
      <button id="uploadBtn" type="submit" disabled>Upload</button>
      <div id="paste-zone" tabindex="0">Or click here and paste an image (Ctrl+V)</div>
    </form>
    <div id="result"><pre id="result-text"></pre></div>
    
    <!-- File Lister -->
    <div id="file-list-container">
      <button id="fetchBtn">Fetch Recent Files (30 mins)</button>
      <div id="spinner" class="spinner"></div>
      <ul id="file-list"></ul>
    </div>
  </div>

  <script>
    // --- Global Vars ---
    const envToken = {{ env_token|tojson }};
    const envChat = {{ env_chatid|tojson }};
    const streamUrl = {{ stream_url|tojson }};
    let resultTimer = null;

    // --- Element Refs ---
    const elements = {
        tokenInput: document.getElementById('token'),
        chatInput: document.getElementById('chatid'),
        uploadBtn: document.getElementById('uploadBtn'),
        envTokenMsg: document.getElementById('envTokenMsg'),
        envChatMsg: document.getElementById('envChatMsg'),
        dropZone: document.getElementById('drop-zone'),
        fileInput: document.getElementById('file-input'),
        dropZoneText: document.getElementById('drop-zone-text'),
        fileNameDisplay: document.getElementById('file-name'),
        pasteZone: document.getElementById('paste-zone'),
        resultDiv: document.getElementById('result'),
        resultText: document.getElementById('result-text'),
        fetchBtn: document.getElementById('fetchBtn'),
        fileList: document.getElementById('file-list'),
        spinner: document.getElementById('spinner')
    };
    
    // --- Core Logic ---
    function hasTokenValue() { return elements.tokenInput.value.trim().length > 0; }
    function hasChatValue() { return elements.chatInput.value.trim().length > 0; }

    function updateEnvMessages() {
      elements.envTokenMsg.style.display = (!hasTokenValue() && envToken) ? 'block' : 'none';
      elements.envChatMsg.style.display = (!hasChatValue() && envChat) ? 'block' : 'none';
    }

    function checkReady() {
      const okToken = hasTokenValue() || envToken;
      const okChat = hasChatValue() || envChat;
      const okFile = elements.fileInput.files.length > 0;
      elements.uploadBtn.disabled = !(okToken && okChat && okFile);
    }
    
    function handleFileSelect(files) {
        if (files && files.length > 0) {
            elements.dropZoneText.textContent = 'File selected:';
            elements.fileNameDisplay.textContent = files[0].name;
        } else {
            resetFileSelection();
        }
        checkReady();
    }

    function resetFileSelection() {
        elements.fileInput.value = '';
        elements.dropZoneText.textContent = 'Drag & drop a file here, or click to select';
        elements.fileNameDisplay.textContent = '';
        checkReady();
    }

    function toggleCredentials() {
      document.getElementById('header-container').classList.toggle('collapsed');
    }

    function displayResult(message, isSuccess) {
        elements.resultText.textContent = message;
        elements.resultDiv.className = isSuccess ? 'success' : 'error';
        elements.resultDiv.classList.add('visible');
        resultTimer = setTimeout(() => {
            elements.resultDiv.classList.remove('visible');
            if(isSuccess) resetFileSelection();
        }, 3000);
    }

    // --- Uploader Events ---
    elements.tokenInput.addEventListener('input', () => { updateEnvMessages(); checkReady(); });
    elements.chatInput.addEventListener('input', () => { updateEnvMessages(); checkReady(); });
    elements.fileInput.addEventListener('change', () => handleFileSelect(elements.fileInput.files));
    elements.dropZone.addEventListener('click', () => elements.fileInput.click());
    elements.dropZone.addEventListener('dragover', (e) => { e.preventDefault(); elements.dropZone.classList.add('drag-over'); });
    elements.dropZone.addEventListener('dragleave', () => elements.dropZone.classList.remove('drag-over'));
    elements.dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      elements.dropZone.classList.remove('drag-over');
      if (e.dataTransfer.files.length) {
        elements.fileInput.files = e.dataTransfer.files;
        handleFileSelect(elements.fileInput.files);
        submitUpload();
      }
    });
    elements.pasteZone.addEventListener('paste', (e) => {
      e.preventDefault();
      const item = Array.from(e.clipboardData.items).find(i => i.kind === 'file' && i.type.startsWith('image/'));
      if (item) {
        const file = item.getAsFile();
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(new File([file], `pasted-${Date.now()}.png`, {type: file.type}));
        elements.fileInput.files = dataTransfer.files;
        handleFileSelect(elements.fileInput.files);
        submitUpload();
      }
    });
    document.getElementById('uploadForm').addEventListener('submit', (e) => { e.preventDefault(); submitUpload(); });

    async function submitUpload() {
        if (elements.uploadBtn.disabled) return;
        const formData = new FormData();
        formData.append('token', elements.tokenInput.value);
        formData.append('chatid', elements.chatInput.value);
        formData.append('caption', document.getElementById('caption').value);
        formData.append('file', elements.fileInput.files[0]);

        elements.uploadBtn.disabled = true;
        elements.uploadBtn.textContent = 'Uploading...';
        clearTimeout(resultTimer);
        elements.resultDiv.classList.remove('visible');

        try {
            const response = await fetch("{{ url_for('upload') }}", { method: 'POST', body: formData });
            const data = await response.json();
            displayResult(data.message, data.ok);
        } catch (error) {
            console.error('Upload Error:', error);
            displayResult('An unexpected network error occurred.', false);
        } finally {
            elements.uploadBtn.textContent = 'Upload';
            checkReady();
        }
    }

    // --- File Lister Events ---
    elements.fetchBtn.addEventListener('click', async () => {
        elements.fetchBtn.disabled = true;
        elements.spinner.style.display = 'block';
        elements.fileList.innerHTML = '';
        try {
            const response = await fetch("{{ url_for('get_recent_files') }}");
            const data = await response.json();
            if (data.ok) {
                if (data.files.length === 0) {
                   elements.fileList.innerHTML = '<li>No files found in the last 30 minutes.</li>';
                } else {
                    renderFileList(data.files);
                }
            } else {
                displayResult(data.message, false);
            }
        } catch (error) {
            console.error('Fetch Error:', error);
            displayResult('Failed to fetch recent files.', false);
        } finally {
            elements.fetchBtn.disabled = false;
            elements.spinner.style.display = 'none';
        }
    });

    function renderFileList(files) {
        const listHtml = files.map(file => {
            const downloadUrl = `${streamUrl}/stream?file_id=${encodeURIComponent(file.file_id)}&name=${encodeURIComponent(file.name)}&size=${file.size}&mime=${encodeURIComponent(file.mime)}`;
            const fileSize = (file.size / 1024 / 1024).toFixed(2);
            return `<li>
                        <a href="${downloadUrl}" target="_blank" rel="noopener noreferrer" download="${file.name}">${file.name}</a>
                        <span class="file-size">${fileSize} MB</span>
                    </li>`;
        }).join('');
        elements.fileList.innerHTML = listHtml;
    }
    
    // --- Initial State Setup ---
    updateEnvMessages();
    checkReady();
  </script>
</body>
</html>
"""

# --- Flask Routes ---
@app.route('/icon.png')
def favicon():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'icon.png', mimetype='image/png')

@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        SINGLE_PAGE_HTML,
        env_token=bool(ENV_BOT_TOKEN),
        env_chatid=bool(ENV_CHAT_ID),
        stream_url=STREAM_URL
    )

@app.route("/upload", methods=["POST"])
def upload():
    token = request.form.get("token", "").strip() or ENV_BOT_TOKEN
    chat_id = request.form.get("chatid", "").strip() or ENV_CHAT_ID
    if not token or not chat_id:
        return jsonify({"ok": False, "message": "❌ Missing Bot Token or Chat ID."}), 400
    
    file = request.files.get("file")
    if not file:
        return jsonify({"ok": False, "message": "❌ No file was provided."}), 400

    api_method = 'sendPhoto' if file.mimetype.lower().startswith('image/') else 'sendDocument'
    file_type_key = 'photo' if api_method == 'sendPhoto' else 'document'
    
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/{api_method}",
            data={"chat_id": chat_id, "caption": request.form.get("caption", "").strip()},
            files={file_type_key: (file.filename, file.stream, file.mimetype)},
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok"):
            return jsonify({"ok": True, "message": "✅ Upload successful!"})
        else:
            return jsonify({"ok": False, "message": f"❌ API Error: {data.get('description', 'Unknown')}"}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"ok": False, "message": f"❌ Network Error: {e}"}), 500
    except json.JSONDecodeError:
        return jsonify({"ok": False, "message": f"❌ Invalid API response from Telegram."}), 500

@app.route("/get_recent_files", methods=["GET"])
def get_recent_files():
    """Fetches messages from the last 30 minutes and returns a list of files."""
    if not ENV_BOT_TOKEN or not ENV_CHAT_ID:
        return jsonify({"ok": False, "message": "❌ Server is not configured with BOT_TOKEN and CHAT_ID."}), 500

    # Get updates from the last 30 minutes. We fetch updates and filter by date on our side.
    thirty_mins_ago = int(time.time()) - (30 * 60)
    
    try:
        # getUpdates is a bit tricky. We fetch the last 100 messages and filter.
        resp = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params={'chat_id': ENV_CHAT_ID, 'limit': 100}, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if not data.get("ok"):
            return jsonify({"ok": False, "message": f"API Error: {data.get('description')}"}), 500
        
        files = []
        # The update can be a 'message' or 'channel_post'
        messages = [item.get('message') or item.get('channel_post') for item in data.get('result', [])]

        for msg in messages:
            if not msg or msg.get('chat', {}).get('id') != int(ENV_CHAT_ID):
                continue

            if msg.get('date', 0) < thirty_mins_ago:
                continue

            # Check for 'document' or 'photo'
            media = msg.get('document') or (msg.get('photo')[-1] if msg.get('photo') else None)
            if media:
                files.append({
                    "name": media.get('file_name', f"photo_{msg['message_id']}.jpg"),
                    "file_id": media['file_id'],
                    "size": media.get('file_size', 0),
                    "mime": media.get('mime_type', 'image/jpeg')
                })
        
        # Reverse to show newest first
        return jsonify({"ok": True, "files": files[::-1]})

    except requests.exceptions.RequestException as e:
        return jsonify({"ok": False, "message": f"❌ Network Error: {e}"}), 500
    except (json.JSONDecodeError, KeyError) as e:
        return jsonify({"ok": False, "message": f"❌ Error parsing API response: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(FLASK_PORT), debug=True)
