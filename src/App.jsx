import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const ChevronDown = ({ className }) => <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6"/></svg>;
const Loader2 = ({ className, style }) => <svg className={className} style={style} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>;
const CloudUpload = ({ className, style }) => <svg className={className} style={style} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m8 16 4-4 4 4"/></svg>;

export default function App() {
  const [botToken, setBotToken] = useState(() => localStorage.getItem('tg_bot_token') || '');
  const [chatId, setChatId] = useState(() => localStorage.getItem('tg_chat_id') || '');
  const [credentialsOpen, setCredentialsOpen] = useState(botToken === '' || chatId === '');
  const [caption, setCaption] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [fetching, setFetching] = useState(false);
  const [recentFiles, setRecentFiles] = useState([]);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('tg_bot_token', botToken);
  }, [botToken]);
  
  useEffect(() => {
    localStorage.setItem('tg_chat_id', chatId);
  }, [chatId]);

  useEffect(() => {
    const handlePaste = (e) => {
      if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') return;
      
      const item = Array.from(e.clipboardData.items).find(i => i.kind === 'file' && i.type.startsWith('image/'));
      if (item) {
        const pastedFile = item.getAsFile();
        const newFile = new File([pastedFile], `pasted-${Date.now()}.png`, { type: pastedFile.type });
        setFile(newFile);
      }
    };
    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  const handleUpload = async (e) => {
    e?.preventDefault();
    if (!botToken || !chatId || !file) return;

    setUploading(true);
    setResult(null);

    const isImage = file.type.startsWith('image/');
    const apiMethod = isImage ? 'sendPhoto' : 'sendDocument';
    const fileKey = isImage ? 'photo' : 'document';
    
    const formData = new FormData();
    formData.append('chat_id', chatId);
    if (caption) formData.append('caption', caption);
    formData.append(fileKey, file);

    try {
      const res = await fetch(`https://api.telegram.org/bot${botToken}/${apiMethod}`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.ok) {
        setResult({ ok: true, message: '✅ Upload successful!' });
        setFile(null);
        setCaption('');
        if (fileInputRef.current) fileInputRef.current.value = '';
      } else {
        setResult({ ok: false, message: `❌ API Error: ${data.description}` });
      }
    } catch (err) {
      setResult({ ok: false, message: `❌ Network Error: ${err.message}` });
    } finally {
      setUploading(false);
      setTimeout(() => setResult(null), 3000);
    }
  };

  const fetchRecent = async () => {
    if (!botToken || !chatId) return;
    setFetching(true);
    setResult(null);
    setRecentFiles([]);

    const thirtyMinsAgo = Math.floor(Date.now() / 1000) - (30 * 60);
    
    try {
      const res = await fetch(`https://api.telegram.org/bot${botToken}/getUpdates?chat_id=${chatId}&limit=100`);
      const data = await res.json();
      if (!data.ok) {
        setResult({ ok: false, message: `API Error: ${data.description}` });
        setFetching(false);
        return;
      }

      const files = [];
      const messages = (data.result || []).map(item => item.message || item.channel_post).filter(Boolean);

      for (const msg of messages) {
        if (String(msg.chat?.id) !== String(chatId) || msg.date < thirtyMinsAgo) continue;
        const media = msg.document || (msg.photo ? msg.photo[msg.photo.length - 1] : null);
        if (media) {
          files.push({
            name: media.file_name || `photo_${msg.message_id}.jpg`,
            file_id: media.file_id,
            size: media.file_size || 0
          });
        }
      }
      setRecentFiles(files.reverse());
    } catch (err) {
      setResult({ ok: false, message: `❌ Network Error: ${err.message}` });
    } finally {
      setFetching(false);
    }
  };

  const downloadFile = async (fileId) => {
    try {
      const res = await fetch(`https://api.telegram.org/bot${botToken}/getFile?file_id=${fileId}`);
      const data = await res.json();
      if (data.ok) {
        const filePath = data.result.file_path;
        window.open(`https://api.telegram.org/file/bot${botToken}/${filePath}`, '_blank');
      } else {
        alert('Failed to get file: ' + data.description);
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const formatSize = (bytes) => {
    if (!bytes) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="app-container">
      <div className="header">
        <div className="header-title">
          <CloudUpload className="text-accent" style={{ color: 'var(--accent)' }}/>
          <h2>Telegram Uploader</h2>
        </div>
        <button 
          type="button"
          className={`settings-btn ${credentialsOpen ? 'open' : ''}`}
          onClick={() => setCredentialsOpen(!credentialsOpen)}
          title="Settings"
        >
          <ChevronDown />
        </button>
      </div>

      <div className={`credentials-panel ${credentialsOpen ? 'open' : ''}`}>
        <div className="form-group">
          <label>Bot Token</label>
          <input 
            type="text" 
            placeholder="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            value={botToken}
            onChange={(e) => setBotToken(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Chat ID</label>
          <input 
            type="text" 
            placeholder="-1001234567890"
            value={chatId}
            onChange={(e) => setChatId(e.target.value)}
          />
        </div>
      </div>

      <div className="main-content">
        <form onSubmit={handleUpload}>
          <div className="form-group">
            <label>Caption (Optional)</label>
            <textarea 
              rows="2" 
              placeholder="Write a caption..."
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
            />
          </div>

          <div 
            className={`drop-zone ${dragOver ? 'drag-over' : ''}`}
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              if (e.dataTransfer.files?.length) {
                setFile(e.dataTransfer.files[0]);
              }
            }}
          >
            <input 
              type="file" 
              ref={fileInputRef}
              style={{ display: 'none' }}
              onChange={(e) => {
                 if (e.target.files?.length) {
                    setFile(e.target.files[0]);
                 }
              }}
            />
            {file ? (
              <>
                <div style={{ color: 'var(--accent)', fontWeight: '600' }}>{file.name}</div>
                <div style={{ fontSize: '13px' }}>{formatSize(file.size)}</div>
              </>
            ) : (
              <>
                <CloudUpload />
                <div>Drag & drop a file here, or click to select<br/><span style={{fontSize: '12px', opacity: 0.7}}>You can also Paste (Ctrl+V) anywhere</span></div>
              </>
            )}
          </div>

          <button 
            type="submit" 
            className="btn" 
            style={{ marginTop: '20px' }}
            disabled={!file || !botToken || !chatId || uploading}
          >
            {uploading ? <><Loader2 className="spin" /> Uploading...</> : 'Upload to Telegram'}
          </button>
        </form>

        {result && (
          <div className={`result ${result.ok ? 'success' : 'error'}`}>
            {result.message}
          </div>
        )}
      </div>

      <div className="recent-files-section">
        <div className="recent-files-header">
          <h2>Recent Files (30m)</h2>
          <button 
            type="button"
            className="btn btn-secondary"
            onClick={fetchRecent}
            disabled={fetching || !botToken || !chatId}
          >
            {fetching ? <><Loader2 className="spin" style={{ width: '16px', height: '16px', marginRight: '6px', verticalAlign: 'middle', display: 'inline-block'}} /> Fetching...</> : 'Refresh Files'}
          </button>
        </div>
        
        {recentFiles.length > 0 ? (
          <div className="file-list">
            {recentFiles.map((f, i) => (
              <div key={i} className="file-item" onClick={() => downloadFile(f.file_id)}>
                <span className="file-item-name" title={f.name}>{f.name}</span>
                <span className="file-item-size">{formatSize(f.size)}</span>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ fontSize: '13px', color: 'var(--text-muted)', textAlign: 'center', padding: '16px 0' }}>
            No recent files found in this chat.
          </div>
        )}
      </div>
    </div>
  );
}
