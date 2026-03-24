import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const SettingsIcon = ({ className }) => <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>;
const Loader2 = ({ className, style }) => <svg className={className} style={style} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>;
const RefreshCw = ({ className }) => <svg className={className} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>;
const Send = ({ className }) => <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>;
const Download = ({ className }) => <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>;

// File Icons
const FileText = ({ className }) => <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>;
const Image = ({ className }) => <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>;
const FileSvg = ({ className }) => <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>;

const getFileDetails = (filename) => {
  const ext = filename?.split('.').pop().toLowerCase() || '';
  if (['pdf'].includes(ext)) return { Icon: FileText, colorClass: 'color-pdf' };
  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext)) return { Icon: Image, colorClass: 'color-img' };
  if (['doc', 'docx'].includes(ext)) return { Icon: FileText, colorClass: 'color-doc' };
  return { Icon: FileSvg, colorClass: 'color-other' };
};

export default function App() {
  const [botToken, setBotToken] = useState(() => localStorage.getItem('tg_bot_token') || '');
  const [chatId, setChatId] = useState(() => localStorage.getItem('tg_chat_id') || '');
  const [credentialsOpen, setCredentialsOpen] = useState(botToken === '' || chatId === '');
  const [message, setMessage] = useState('');
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
    if (botToken && chatId) {
      fetchRecent();
    }
  }, [botToken, chatId]);

  useEffect(() => {
    const handlePaste = (e) => {
      if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') return;
      
      const item = Array.from(e.clipboardData.items).find(i => i.kind === 'file');
      if (item) {
        const pastedFile = item.getAsFile();
        const ext = pastedFile.type.split('/')[1] || 'png';
        const newFile = new File([pastedFile], `pasted-${Date.now()}.${ext}`, { type: pastedFile.type });
        setFile(newFile);
      }
    };
    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!botToken || !chatId || (!file && !message.trim())) return;

    setUploading(true);
    setResult(null);

    try {
      if (file) {
        const isImage = file.type.startsWith('image/');
        const apiMethod = isImage ? 'sendPhoto' : 'sendDocument';
        const fileKey = isImage ? 'photo' : 'document';
        
        const formData = new FormData();
        formData.append('chat_id', chatId);
        if (message.trim()) formData.append('caption', message.trim());
        formData.append(fileKey, file);

        const res = await fetch(`https://api.telegram.org/bot${botToken}/${apiMethod}`, {
          method: 'POST',
          body: formData,
        });
        const data = await res.json();
        if (data.ok) {
          setResult({ ok: true, message: 'Sent!' });
          setFile(null);
          setMessage('');
          if (fileInputRef.current) fileInputRef.current.value = '';
          fetchRecent();
        } else {
          setResult({ ok: false, message: `API Error: ${data.description}` });
        }
      } else {
        const res = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: chatId, text: message.trim() }),
        });
        const data = await res.json();
        if (data.ok) {
          setResult({ ok: true, message: 'Message sent!' });
          setMessage('');
          fetchRecent();
        } else {
          setResult({ ok: false, message: `API Error: ${data.description}` });
        }
      }
    } catch (err) {
      setResult({ ok: false, message: `Network Error: ${err.message}` });
    } finally {
      setUploading(false);
      setTimeout(() => setResult(null), 3000);
    }
  };

  const fetchRecent = async () => {
    if (!botToken || !chatId) return;
    setFetching(true);
    setResult(null);

    const timeAgo = Math.floor(Date.now() / 1000) - (24 * 60 * 60);
    
    try {
      const res = await fetch(`https://api.telegram.org/bot${botToken}/getUpdates?chat_id=${chatId}&limit=100`);
      const data = await res.json();
      if (!data.ok) {
        setFetching(false);
        return;
      }

      const files = [];
      const messages = (data.result || []).map(item => item.message || item.channel_post).filter(Boolean);

      for (const msg of messages) {
        if (String(msg.chat?.id) !== String(chatId) || msg.date < timeAgo) continue;
        
        const media = msg.document || (msg.photo ? msg.photo[msg.photo.length - 1] : null);
        if (media) {
          files.push({
            name: media.file_name || `photo_${msg.message_id}.jpg`,
            file_id: media.file_id,
            size: media.file_size || 0
          });
        }
        
        if (msg.text) {
          files.push({
            name: msg.text.length > 30 ? msg.text.substring(0, 30) + '...' : msg.text,
            isText: true,
            size: 0,
            text: msg.text,
            id: msg.message_id
          });
        }
      }
      
      const uniqueFiles = [];
      const seen = new Set();
      for (const f of files.reverse()) {
        const key = f.isText ? f.id : f.file_id;
        if (!seen.has(key)) {
          seen.add(key);
          uniqueFiles.push(f);
        }
      }
      setRecentFiles(uniqueFiles);
    } catch (err) {
      console.error(err);
    } finally {
      setFetching(false);
    }
  };

  const downloadFile = async (e, fileId) => {
    e.stopPropagation();
    try {
      const res = await fetch(`https://api.telegram.org/bot${botToken}/getFile?file_id=${fileId}`);
      const data = await res.json();
      if (data.ok) {
        const filePath = data.result.file_path;
        window.open(`https://api.telegram.org/file/bot${botToken}/${filePath}`, '_blank');
      }
    } catch (err) {
      console.error(err);
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
    <div className="app-wrapper">
      <div className="top-bar">
        <div className="title-area">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
          To-Leaflet
        </div>
        <button 
          type="button"
          className={`settings-btn ${credentialsOpen ? 'open' : ''}`}
          onClick={() => setCredentialsOpen(!credentialsOpen)}
        >
          <SettingsIcon />
        </button>
      </div>

      <div className={`credentials-panel ${credentialsOpen ? 'open' : ''}`}>
        <div className="form-group">
          <label>Bot Token</label>
          <input 
            type="password" 
            placeholder="Token"
            value={botToken}
            onChange={(e) => setBotToken(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Chat ID</label>
          <input 
            type="text" 
            placeholder="Chat ID"
            value={chatId}
            onChange={(e) => setChatId(e.target.value)}
          />
        </div>
      </div>

      <div className="content-split">
        <div className="send-zone">
          <form className="send-area" onSubmit={handleSend}>
            <textarea 
              className="textarea-message"
              placeholder="Type a message or caption..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

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
                <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px'}}>
                  <div style={{ color: 'var(--text-light)', fontFamily: "'Fira Code', monospace", fontSize: '13px' }}>{file.name}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{formatSize(file.size)}</div>
                  <button type="button" className="btn" style={{width: 'auto', padding: '4px 12px', marginTop: '8px', fontSize: '12px'}} onClick={(e) => { e.stopPropagation(); setFile(null); }}>
                    Remove
                  </button>
                </div>
              ) : (
                <>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  <div style={{fontSize: '13px'}}>Select File</div>
                </>
              )}
            </div>

            <button 
              type="submit" 
              className="btn" 
              disabled={(!file && !message.trim()) || !botToken || !chatId || uploading}
            >
              {uploading ? <Loader2 className="spin" /> : <Send />}
              {uploading ? 'Sending...' : 'Send'}
            </button>
          </form>

          {result && (
            <div className={`result ${result.ok ? 'success' : 'error'}`}>
              {result.message}
            </div>
          )}
        </div>

        <div className="receive-zone">
          <div className="receive-header">
            <h2>Recent Files</h2>
            <button className="btn-icon" onClick={fetchRecent} disabled={fetching}>
              <RefreshCw className={fetching ? "spin" : ""} />
            </button>
          </div>
          
          <div className="file-list">
            {recentFiles.length > 0 ? (
              recentFiles.map((f, i) => {
                if (f.isText) {
                  return (
                    <div key={i} className="file-item">
                      <div className="file-icon color-other">
                        <FileText />
                      </div>
                      <div className="file-info">
                        <span className="file-name" title={f.text}>{f.name}</span>
                        <span className="file-size">Message</span>
                      </div>
                      <button className="btn-icon" onClick={(e) => {
                        e.stopPropagation();
                        navigator.clipboard.writeText(f.text);
                      }} title="Copy Message">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                      </button>
                    </div>
                  );
                }

                const { Icon, colorClass } = getFileDetails(f.name);
                return (
                  <div key={i} className="file-item" onClick={(e) => downloadFile(e, f.file_id)}>
                    <div className={`file-icon ${colorClass}`}>
                      <Icon />
                    </div>
                    <div className="file-info">
                      <span className="file-name" title={f.name}>{f.name}</span>
                      <span className="file-size">{formatSize(f.size)}</span>
                    </div>
                    <button className="btn-icon" onClick={(e) => downloadFile(e, f.file_id)} title="Download">
                      <Download />
                    </button>
                  </div>
                );
              })
            ) : (
              <div style={{ fontSize: '12px', color: 'var(--text-muted)', textAlign: 'center', padding: '32px 0' }}>
                No recent files found.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
