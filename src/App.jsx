import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const SettingsIcon = ({ className }) => <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>;
const Loader2 = ({ className, style }) => <svg className={className} style={style} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>;
const RefreshCw = ({ className }) => <svg className={className} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>;
const Send = ({ className }) => <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>;
const Download = ({ className }) => <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>;
const XIcon = ({ className }) => <svg className={className} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>;

// File Icons
const FileText = ({ className }) => <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>;
const Image = ({ className }) => <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>;
const FileSvg = ({ className }) => <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>;

const MIME_TO_EXT = {
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
  'application/vnd.ms-excel': 'xls',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
  'application/msword': 'doc',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
  'application/vnd.ms-powerpoint': 'ppt',
  'application/pdf': 'pdf',
  'application/zip': 'zip',
  'application/x-7z-compressed': '7z',
  'application/x-rar-compressed': 'rar',
  'application/gzip': 'gz',
  'text/plain': 'txt',
  'text/csv': 'csv',
  'text/html': 'html',
  'application/json': 'json',
  'application/xml': 'xml',
};

function getExtFromMime(mime) {
  if (MIME_TO_EXT[mime]) return MIME_TO_EXT[mime];
  const sub = (mime.split('/')[1] || 'bin');
  // If subtype contains dots or plus, it's a complex MIME — fall back to 'bin'
  return (sub.includes('.') || sub.includes('+')) ? 'bin' : sub;
}

const getFileDetails = (filename) => {
  const ext = filename?.split('.').pop().toLowerCase() || '';
  if (['pdf'].includes(ext)) return { Icon: FileText, colorClass: 'color-pdf' };
  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext)) return { Icon: Image, colorClass: 'color-img' };
  if (['doc', 'docx'].includes(ext)) return { Icon: FileText, colorClass: 'color-doc' };
  return { Icon: FileSvg, colorClass: 'color-other' };
};

const isImageFile = (filename) => {
  const ext = filename?.split('.').pop().toLowerCase() || '';
  return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'].includes(ext);
};

const copyImageToClipboard = async (imageUrl) => {
  const response = await fetch(imageUrl);
  const blob = await response.blob();
  
  if (blob.type === 'image/png') {
    await navigator.clipboard.write([
      new ClipboardItem({ 'image/png': blob })
    ]);
    return;
  }
  
  const img = new window.Image();
  img.crossOrigin = 'anonymous';
  await new Promise((resolve, reject) => {
    img.onload = resolve;
    img.onerror = reject;
    img.src = URL.createObjectURL(blob);
  });
  
  const canvas = document.createElement('canvas');
  canvas.width = img.width;
  canvas.height = img.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  
  const pngBlob = await new Promise((resolve) => {
    canvas.toBlob(resolve, 'image/png');
  });
  
  await navigator.clipboard.write([
    new ClipboardItem({ 'image/png': pngBlob })
  ]);
};

const ImageThumbnail = ({ fileId, botToken, fallbackIcon: FallbackIcon }) => {
  const [src, setSrc] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    const fetchPath = async () => {
      try {
        const cacheKey = `tg_file_path_${fileId}`;
        let filePath = sessionStorage.getItem(cacheKey);
        if (!filePath) {
          const res = await fetch(`https://moss.leafyakeru.workers.dev/bot${botToken}/getFile?file_id=${fileId}`);
          const data = await res.json();
          if (data.ok) {
            filePath = data.result.file_path;
            sessionStorage.setItem(cacheKey, filePath);
          }
        }
        if (filePath && active) {
          setSrc(`https://moss.leafyakeru.workers.dev/file/bot${botToken}/${filePath}`);
        }
      } catch (err) {
        console.error('Failed to load image preview:', err);
      } finally {
        if (active) setLoading(false);
      }
    };
    fetchPath();
    return () => { active = false; };
  }, [fileId, botToken]);

  if (loading) {
    return <div className="spin-mini" style={{ width: '16px', height: '16px', border: '2px solid var(--text-muted)', borderTopColor: 'transparent', borderRadius: '50%' }}></div>;
  }

  if (src) {
    return <img src={src} alt="preview" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '4px' }} />;
  }

  return <FallbackIcon />;
};

const CopyImageButton = ({ fileId, botToken, showToast }) => {
  const [copied, setCopied] = useState(false);
  const [copying, setCopying] = useState(false);

  const handleCopy = async (e) => {
    e.stopPropagation();
    if (copying) return;
    setCopying(true);
    try {
      const cacheKey = `tg_file_path_${fileId}`;
      let filePath = sessionStorage.getItem(cacheKey);
      if (!filePath) {
        const res = await fetch(`https://moss.leafyakeru.workers.dev/bot${botToken}/getFile?file_id=${fileId}`);
        const data = await res.json();
        if (data.ok) {
          filePath = data.result.file_path;
          sessionStorage.setItem(cacheKey, filePath);
        }
      }
      if (filePath) {
        const fileUrl = `https://moss.leafyakeru.workers.dev/file/bot${botToken}/${filePath}`;
        await copyImageToClipboard(fileUrl);
        setCopied(true);
        showToast('Image copied to clipboard!', 'success');
        setTimeout(() => setCopied(false), 2000);
      } else {
        showToast('Failed to retrieve image URL.', 'error');
      }
    } catch (err) {
      console.error('Failed to copy image:', err);
      showToast('Failed to copy image to clipboard.', 'error');
    } finally {
      setCopying(false);
    }
  };

  return (
    <button 
      className="btn-icon" 
      onClick={handleCopy} 
      title={copied ? "Copied!" : "Copy Image"}
      disabled={copying}
    >
      {copied ? (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="green" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
      ) : copying ? (
        <div className="spin-mini" style={{ width: '14px', height: '14px', border: '2px solid currentColor', borderTopColor: 'transparent', borderRadius: '50%' }}></div>
      ) : (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
      )}
    </button>
  );
};

export default function App() {
  const [botToken, setBotToken] = useState(() => localStorage.getItem('tg_bot_token') || '');
  const [chatId, setChatId] = useState(() => localStorage.getItem('tg_chat_id') || '');
  const [credentialsOpen, setCredentialsOpen] = useState(botToken === '' || chatId === '');
  const [message, setMessage] = useState('');
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [fetching, setFetching] = useState(false);
  const [recentFiles, setRecentFiles] = useState([]);
  const [dragOver, setDragOver] = useState(false);
  const [pinAfterSend, setPinAfterSend] = useState(() => localStorage.getItem('tg_pin_after_send') === 'true');
  const [hiddenFileIds, setHiddenFileIds] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('tg_hidden_files') || '[]');
    } catch {
      return [];
    }
  });
  const [toasts, setToasts] = useState([]);

  const showToast = (msg, type = 'success') => {
    const id = Date.now() + Math.random().toString(36).substr(2, 9);
    setToasts(prev => [...prev, { id, message: msg, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 4000);
  };

  const addFiles = (newFiles) => {
    const validFiles = [];
    const rejectedFiles = [];
    
    for (const f of newFiles) {
      if (f.size > 25 * 1024 * 1024) {
        rejectedFiles.push(f.name);
      } else {
        validFiles.push(f);
      }
    }
    
    if (rejectedFiles.length > 0) {
      showToast(`File size exceeds 25 MB limit: ${rejectedFiles.join(', ')}`, 'error');
    }
    
    if (validFiles.length > 0) {
      setFiles(prev => [...prev, ...validFiles]);
    }
  };

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };
  
  const fileInputRef = useRef(null);
  const captionRef = useRef(null);
  const handleSendRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('tg_bot_token', botToken);
  }, [botToken]);
  
  useEffect(() => {
    localStorage.setItem('tg_chat_id', chatId);
  }, [chatId]);

  useEffect(() => {
    localStorage.setItem('tg_pin_after_send', pinAfterSend);
  }, [pinAfterSend]);

  useEffect(() => {
    localStorage.setItem('tg_hidden_files', JSON.stringify(hiddenFileIds));
  }, [hiddenFileIds]);

  useEffect(() => {
    if (botToken && chatId) {
      fetchRecent();
    }
  }, [botToken, chatId]);

  useEffect(() => {
    const handlePaste = (e) => {
      const items = Array.from(e.clipboardData.items).filter(i => i.kind === 'file');
      if (items.length > 0) {
        e.preventDefault();
        const newFiles = [];
        for (const item of items) {
          const pastedFile = item.getAsFile();
          if (pastedFile) {
            const ext = getExtFromMime(pastedFile.type || 'application/octet-stream');
            const hasGenericName = !pastedFile.name || pastedFile.name === 'blob';
            const fileName = hasGenericName ? `pasted-${Date.now()}-${Math.floor(Math.random() * 1000)}.${ext}` : pastedFile.name;
            const newFile = new File([pastedFile], fileName, { type: pastedFile.type });
            newFiles.push(newFile);
          }
        }
        addFiles(newFiles);
        captionRef.current?.focus();
      }
    };
    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  useEffect(() => {
    const handleGlobalKeyDown = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendRef.current?.();
      }
    };
    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, []);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!botToken || !chatId || (files.length === 0 && !message.trim())) return;

    setUploading(true);
    setResult(null);

    const pinMessage = async (messageId) => {
      try {
        const pinRes = await fetch(`https://moss.leafyakeru.workers.dev/bot${botToken}/pinChatMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: chatId,
            message_id: messageId,
            disable_notification: false,
          }),
        });
        const pinData = await pinRes.json();
        if (!pinData.ok) {
          console.error('Failed to pin message:', pinData.description);
        }
      } catch (pinErr) {
        console.error('Error pinning message:', pinErr);
      }
    };

    try {
      let successCount = 0;
      let hasError = false;

      if (files.length > 0) {
        for (let i = 0; i < files.length; i++) {
          const currentFile = files[i];
          setResult({ ok: true, message: `Sending file ${i + 1} of ${files.length} (${currentFile.name})...` });

          if (currentFile.size > 25 * 1024 * 1024) {
            showToast(`Skipped "${currentFile.name}": exceeds 25 MB limit.`, 'error');
            continue;
          }

          const isImage = currentFile.type.startsWith('image/');
          const apiMethod = isImage ? 'sendPhoto' : 'sendDocument';
          const fileKey = isImage ? 'photo' : 'document';
          
          const formData = new FormData();
          formData.append('chat_id', chatId);
          if (i === 0 && message.trim()) {
            formData.append('caption', message.trim());
          }
          formData.append(fileKey, currentFile);

          const res = await fetch(`https://moss.leafyakeru.workers.dev/bot${botToken}/${apiMethod}`, {
            method: 'POST',
            body: formData,
          });
          const data = await res.json();
          if (data.ok) {
            successCount++;
            if (pinAfterSend && data.result?.message_id) {
              await pinMessage(data.result.message_id);
            }
          } else {
            hasError = true;
            setResult({ ok: false, message: `Failed to send "${currentFile.name}": ${data.description}` });
            showToast(`Failed to send "${currentFile.name}".`, 'error');
            break;
          }
        }
      } else if (message.trim()) {
        setResult({ ok: true, message: 'Sending message...' });
        const res = await fetch(`https://moss.leafyakeru.workers.dev/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: chatId, text: message.trim() }),
        });
        const data = await res.json();
        if (data.ok) {
          successCount++;
          if (pinAfterSend && data.result?.message_id) {
            await pinMessage(data.result.message_id);
          }
        } else {
          hasError = true;
          setResult({ ok: false, message: `Failed to send message: ${data.description}` });
          showToast('Failed to send message.', 'error');
        }
      }

      if (!hasError) {
        setResult({ ok: true, message: `Sent ${successCount} item(s) successfully!` });
        showToast(`Successfully sent ${successCount} item(s)!`, 'success');
        setFiles([]);
        setMessage('');
        setPinAfterSend(false);
        if (fileInputRef.current) fileInputRef.current.value = '';
        fetchRecent();
      }
    } catch (err) {
      setResult({ ok: false, message: `Network Error: ${err.message}` });
      showToast('Network error occurred.', 'error');
    } finally {
      setUploading(false);
      setTimeout(() => setResult(null), 4000);
    }
  };

  useEffect(() => {
    handleSendRef.current = handleSend;
  });

  const handleDismiss = (key) => {
    const stringKey = String(key);
    setHiddenFileIds(prev => {
      if (prev.includes(stringKey)) return prev;
      return [...prev, stringKey];
    });
    setRecentFiles(prev => prev.filter(f => {
      const fKey = String(f.isText ? f.id : f.file_id);
      return fKey !== stringKey;
    }));
  };

  const fetchRecent = async () => {
    if (!botToken || !chatId) return;
    setFetching(true);
    setResult(null);
    
    try {
      const res = await fetch(`https://moss.leafyakeru.workers.dev/bot${botToken}/getUpdates?limit=100&offset=-100`);
      const data = await res.json();
      if (!data.ok) {
        console.error('getUpdates error:', data);
        setFetching(false);
        return;
      }

      const files = [];
      const messages = (data.result || []).map(item => item.message || item.channel_post).filter(Boolean);
      const allFetchedKeys = new Set();

      for (const msg of messages) {
        if (String(msg.chat?.id) !== String(chatId)) continue;
        
        const media = msg.document || (msg.photo ? msg.photo[msg.photo.length - 1] : null);
        if (media) {
          const fileId = String(media.file_id);
          allFetchedKeys.add(fileId);
          files.push({
            name: media.file_name || `photo_${msg.message_id}.jpg`,
            file_id: fileId,
            size: media.file_size || 0
          });
        }
        
        if (msg.text) {
          const msgId = String(msg.message_id);
          allFetchedKeys.add(msgId);
          files.push({
            name: msg.text.length > 30 ? msg.text.substring(0, 30) + '...' : msg.text,
            isText: true,
            size: 0,
            text: msg.text,
            id: msgId
          });
        }
      }
      
      const uniqueFiles = [];
      const seen = new Set();
      for (const f of files.reverse()) {
        const key = String(f.isText ? f.id : f.file_id);
        if (!seen.has(key)) {
          seen.add(key);
          if (!hiddenFileIds.includes(key)) {
            uniqueFiles.push(f);
          }
        }
      }

      // Garbage collection: Keep only the hidden keys that are still in this batch of updates.
      setHiddenFileIds(prev => prev.filter(key => allFetchedKeys.has(String(key))));

      setRecentFiles(uniqueFiles.slice(0, 10));
    } catch (err) {
      console.error('fetchRecent error:', err);
      setResult({ ok: false, message: `Fetch error: ${err.message}` });
      setTimeout(() => setResult(null), 4000);
    } finally {
      setFetching(false);
    }
  };

  const downloadFile = async (e, fileId, fileName) => {
    e.stopPropagation();
    try {
      const res = await fetch(`https://moss.leafyakeru.workers.dev/bot${botToken}/getFile?file_id=${fileId}`);
      const data = await res.json();
      if (data.ok) {
        const filePath = data.result.file_path;
        const fileUrl = `https://moss.leafyakeru.workers.dev/file/bot${botToken}/${filePath}`;
        const finalFileName = fileName || filePath.split('/').pop() || 'download';
        
        try {
          // Attempt to fetch as blob to avoid opening a new tab and force download with filename
          const fileRes = await fetch(fileUrl);
          if (!fileRes.ok) throw new Error('File fetch failed');
          const blob = await fileRes.blob();
          const blobUrl = window.URL.createObjectURL(blob);
          
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = blobUrl;
          a.download = finalFileName;
          document.body.appendChild(a);
          a.click();
          
          setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(blobUrl);
          }, 100);
        } catch (fetchErr) {
          console.warn('Blob download failed, falling back to anchor click:', fetchErr);
          // Fallback if CORS or other error prevents blob fetching
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = fileUrl;
          a.download = finalFileName;
          a.target = '_top'; // Try to keep it in the same window/tab if possible
          document.body.appendChild(a);
          a.click();
          
          setTimeout(() => {
            document.body.removeChild(a);
          }, 100);
        }
      } else {
        console.error('getFile error:', data);
      }
    } catch (err) {
      console.error('downloadFile error:', err);
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
              ref={captionRef}
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
                  addFiles(Array.from(e.dataTransfer.files));
                }
              }}
            >
              <input 
                type="file" 
                ref={fileInputRef}
                multiple
                style={{ display: 'none' }}
                onChange={(e) => {
                   if (e.target.files?.length) {
                      addFiles(Array.from(e.target.files));
                   }
                }}
              />
              {files.length > 0 ? (
                <div style={{display: 'flex', flexDirection: 'column', width: '100%', gap: '8px', padding: '0 12px'}}>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px', textAlign: 'left' }}>Selected ({files.length}):</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', maxHeight: '150px', overflowY: 'auto', width: '100%' }} onClick={e => e.stopPropagation()}>
                    {files.map((f, idx) => (
                      <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(255,255,255,0.03)', padding: '6px 12px', borderRadius: '4px', border: '1px solid var(--border)' }}>
                        <div style={{ textAlign: 'left', minWidth: 0, flex: 1, marginRight: '12px' }}>
                          <div style={{ color: 'var(--text-light)', fontFamily: "'Fira Code', monospace", fontSize: '12px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={f.name}>{f.name}</div>
                          <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>{formatSize(f.size)}</div>
                        </div>
                        <button type="button" className="btn-icon" style={{ padding: '4px', color: 'var(--error)' }} onClick={() => removeFile(idx)} title="Remove file">
                          <XIcon />
                        </button>
                      </div>
                    ))}
                  </div>
                  <button type="button" className="btn" style={{width: 'auto', padding: '4px 12px', marginTop: '8px', fontSize: '12px', alignSelf: 'center'}} onClick={(e) => { e.stopPropagation(); setFiles([]); }}>
                    Clear All
                  </button>
                </div>
              ) : (
                <>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  <div style={{fontSize: '13px'}}>Select File(s)</div>
                </>
              )}
            </div>

            <div className="options-zone">
              <label className="checkbox-container">
                <input 
                  type="checkbox" 
                  checked={pinAfterSend} 
                  onChange={(e) => setPinAfterSend(e.target.checked)} 
                />
                <span className="checkbox-custom"></span>
                <span className="checkbox-label">Pin after sending</span>
              </label>
            </div>

            <button 
              type="submit" 
              className="btn" 
              disabled={(files.length === 0 && !message.trim()) || !botToken || !chatId || uploading}
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
          
          <div className="toast-container">
            {toasts.map(t => (
              <div key={t.id} className={`toast ${t.type}`}>
                {t.type === 'success' ? (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2"><polyline points="20 6 9 17 4 12"/></svg>
                ) : (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--error)" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                )}
                {t.message}
              </div>
            ))}
          </div>
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
                      <button className="btn-icon" onClick={(e) => {
                        e.stopPropagation();
                        handleDismiss(f.id);
                      }} title="Hide Message">
                        <XIcon />
                      </button>
                    </div>
                  );
                }

                const { Icon, colorClass } = getFileDetails(f.name);
                const isImg = isImageFile(f.name);
                return (
                  <div key={i} className="file-item" onClick={(e) => downloadFile(e, f.file_id, f.name)}>
                    <div className={`file-icon ${colorClass} ${isImg ? 'has-thumbnail' : ''}`}>
                      {isImg ? (
                        <ImageThumbnail fileId={f.file_id} botToken={botToken} fallbackIcon={Icon} />
                      ) : (
                        <Icon />
                      )}
                    </div>
                    <div className="file-info">
                      <span className="file-name" title={f.name}>{f.name}</span>
                      <span className="file-size">{formatSize(f.size)}</span>
                    </div>
                    <button className="btn-icon" onClick={(e) => downloadFile(e, f.file_id, f.name)} title="Download">
                      <Download />
                    </button>
                    {isImg && (
                      <CopyImageButton fileId={f.file_id} botToken={botToken} showToast={showToast} />
                    )}
                    <button className="btn-icon" onClick={(e) => {
                      e.stopPropagation();
                      handleDismiss(f.file_id);
                    }} title="Hide File">
                      <XIcon />
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
