/**
 * NeuralChat — Frontend Application
 * ──────────────────────────────────
 * Handles all UI interactions, API calls, voice input,
 * theme switching, markdown rendering, and chat history.
 */

// ════════════════════════════════════════════════════
// CONFIGURATION
// ════════════════════════════════════════════════════

const CONFIG = {
  API_BASE:       'http://localhost:5000',  // Change for production
  MAX_MSG_LENGTH: 2000,
  WARN_THRESHOLD: 1800,
};

// ════════════════════════════════════════════════════
// DOM REFERENCES
// ════════════════════════════════════════════════════

const $ = id => document.getElementById(id);

const DOM = {
  sidebar:        $('sidebar'),
  sidebarToggle:  $('sidebarToggle'),
  mobileMenuBtn:  $('mobileMenuBtn'),
  themeToggle:    $('themeToggle'),

  // User / login
  loginSection:   $('loginSection'),
  usernameInput:  $('usernameInput'),
  loginBtn:       $('loginBtn'),
  userPanel:      $('userPanel'),
  userAvatar:     $('userAvatar'),
  displayName:    $('displayName'),
  sidebarNav:     $('sidebarNav'),

  // Chat
  welcomeScreen:  $('welcomeScreen'),
  messagesList:   $('messagesList'),
  messagesArea:   $('messagesArea'),
  msgCount:       $('msgCount'),

  // Input
  messageInput:   $('messageInput'),
  sendBtn:        $('sendBtn'),
  charCounter:    $('charCounter'),
  voiceBtn:       $('voiceBtn'),

  // Actions
  newChatBtn:     $('newChatBtn'),
  downloadBtn:    $('downloadBtn'),
  clearBtn:       $('clearBtn'),

  toast:          $('toast'),
};

// ════════════════════════════════════════════════════
// STATE
// ════════════════════════════════════════════════════

const state = {
  username:        localStorage.getItem('nc_username') || '',
  theme:           localStorage.getItem('nc_theme')    || 'dark',
  isLoading:       false,
  messageCount:    0,
  voiceRecognition: null,
  isRecording:     false,
};

// ════════════════════════════════════════════════════
// INIT
// ════════════════════════════════════════════════════

function init() {
  applyTheme(state.theme);
  setupEventListeners();
  setupMarkdown();
  setupVoiceInput();

  // Restore session if username exists
  if (state.username) {
    applyUsername(state.username);
    loadHistory();
  }
}

// ════════════════════════════════════════════════════
// THEME
// ════════════════════════════════════════════════════

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  state.theme = theme;
  localStorage.setItem('nc_theme', theme);
}

DOM.themeToggle.addEventListener('click', () => {
  applyTheme(state.theme === 'dark' ? 'light' : 'dark');
});

// ════════════════════════════════════════════════════
// SIDEBAR
// ════════════════════════════════════════════════════

// Mobile sidebar overlay
const overlay = document.createElement('div');
overlay.className = 'sidebar-overlay';
document.body.appendChild(overlay);

function openMobileSidebar() {
  DOM.sidebar.classList.add('mobile-open');
  overlay.classList.add('active');
}

function closeMobileSidebar() {
  DOM.sidebar.classList.remove('mobile-open');
  overlay.classList.remove('active');
}

DOM.mobileMenuBtn.addEventListener('click', openMobileSidebar);
overlay.addEventListener('click', closeMobileSidebar);

DOM.sidebarToggle.addEventListener('click', () => {
  DOM.sidebar.classList.toggle('collapsed');
});

// ════════════════════════════════════════════════════
// USER AUTHENTICATION (Simple Username)
// ════════════════════════════════════════════════════

function applyUsername(name) {
  state.username = name;
  localStorage.setItem('nc_username', name);

  // Update UI
  DOM.displayName.textContent     = name;
  DOM.userAvatar.textContent       = name.charAt(0).toUpperCase();
  DOM.loginSection.style.display   = 'none';
  DOM.sidebarNav.style.display     = 'flex';
}

DOM.loginBtn.addEventListener('click', handleLogin);
DOM.usernameInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') handleLogin();
});

function handleLogin() {
  const name = DOM.usernameInput.value.trim();
  if (!name) {
    showToast('Please enter your name', 'error');
    return;
  }
  applyUsername(name);
  loadHistory();
  showToast(`Welcome, ${name}! 👋`, 'success');
}

// ════════════════════════════════════════════════════
// MARKDOWN SETUP
// ════════════════════════════════════════════════════

function setupMarkdown() {
  if (typeof marked === 'undefined') return;

  // Configure marked with syntax highlighting
  marked.setOptions({
    highlight: (code, lang) => {
      if (typeof hljs !== 'undefined' && lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value;
      }
      return typeof hljs !== 'undefined' ? hljs.highlightAuto(code).value : code;
    },
    breaks:   true,
    gfm:      true,
    sanitize: false,
  });
}

/** Render markdown + add copy buttons to code blocks */
function renderMarkdown(text) {
  if (typeof marked === 'undefined') return escapeHtml(text);
  return marked.parse(text);
}

// ════════════════════════════════════════════════════
// MESSAGE RENDERING
// ════════════════════════════════════════════════════

/**
 * Create and append a message bubble to the list.
 * @param {string} role   - 'user' or 'bot'
 * @param {string} text   - message content
 * @param {string} time   - timestamp string (ISO)
 * @returns {HTMLElement} - the message row element
 */
function appendMessage(role, text, time = new Date().toISOString()) {
  // Hide welcome screen on first message
  if (state.messageCount === 0) {
    DOM.welcomeScreen.style.display = 'none';
  }

  state.messageCount++;
  updateMsgCount();

  const row = document.createElement('div');
  row.className = `message-row ${role}`;

  const avatarLabel = role === 'bot' ? '⬡' : (state.username ? state.username.charAt(0).toUpperCase() : 'U');
  const senderName  = role === 'bot' ? 'NeuralChat' : (state.username || 'You');
  const timeStr     = formatTime(time);

  const renderedContent = role === 'bot' ? renderMarkdown(text) : `<p>${escapeHtml(text)}</p>`;

  row.innerHTML = `
    <div class="msg-avatar ${role}">${avatarLabel}</div>
    <div class="msg-content">
      <div class="msg-meta">
        <span class="msg-sender">${escapeHtml(senderName)}</span>
        <span class="msg-time">${timeStr}</span>
      </div>
      <div class="msg-bubble">${renderedContent}</div>
      <div class="msg-actions">
        <button class="msg-action-btn copy-btn" title="Copy message">⎘ Copy</button>
      </div>
    </div>
  `;

  // Add copy-to-clipboard listener
  row.querySelector('.copy-btn').addEventListener('click', () => {
    copyToClipboard(text);
    showToast('Copied!', 'success');
  });

  // Attach copy buttons to code blocks within bot messages
  if (role === 'bot') {
    row.querySelectorAll('pre').forEach(pre => {
      const btn = document.createElement('button');
      btn.className = 'code-copy-btn';
      btn.textContent = 'Copy code';
      btn.addEventListener('click', () => {
        const code = pre.querySelector('code');
        copyToClipboard(code ? code.innerText : pre.innerText);
        btn.textContent = '✓ Copied!';
        setTimeout(() => { btn.textContent = 'Copy code'; }, 2000);
      });
      pre.style.position = 'relative';
      pre.appendChild(btn);
    });
  }

  DOM.messagesList.appendChild(row);
  scrollToBottom();

  return row;
}

/** Show the animated typing indicator */
function showTypingIndicator() {
  const indicator = document.createElement('div');
  indicator.id = 'typingIndicator';
  indicator.className = 'typing-indicator';
  indicator.innerHTML = `
    <div class="msg-avatar bot">⬡</div>
    <div class="typing-bubble">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>
  `;
  DOM.messagesList.appendChild(indicator);
  scrollToBottom();
}

/** Remove the typing indicator */
function removeTypingIndicator() {
  const el = $('typingIndicator');
  if (el) el.remove();
}

/** Append an error bubble */
function appendError(msg) {
  const div = document.createElement('div');
  div.className = 'error-message';
  div.innerHTML = `<span>⚠</span> ${escapeHtml(msg)}`;
  DOM.messagesList.appendChild(div);
  scrollToBottom();
}

// ════════════════════════════════════════════════════
// API CALLS
// ════════════════════════════════════════════════════

/** Send a message and display the AI response */
async function sendMessage(text) {
  if (!state.username) {
    showToast('Please set your name first', 'error');
    return;
  }
  if (state.isLoading) return;
  if (!text.trim()) return;

  const trimmed = text.trim();

  // Validate length
  if (trimmed.length > CONFIG.MAX_MSG_LENGTH) {
    showToast(`Message too long (max ${CONFIG.MAX_MSG_LENGTH} chars)`, 'error');
    return;
  }

  // Render user message immediately
  appendMessage('user', trimmed);

  // Clear input
  DOM.messageInput.value = '';
  DOM.messageInput.style.height = 'auto';
  updateCharCounter(0);
  DOM.sendBtn.disabled = true;

  // Start loading state
  state.isLoading = true;
  showTypingIndicator();
  closeMobileSidebar();

  try {
    const response = await fetch(`${CONFIG.API_BASE}/chat`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message:  trimmed,
        username: state.username,
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ error: 'Server error' }));
      throw new Error(err.error || `HTTP ${response.status}`);
    }

    const data = await response.json();

    removeTypingIndicator();
    appendMessage('bot', data.reply, data.timestamp);

  } catch (err) {
    removeTypingIndicator();
    appendError(`Failed to get response: ${err.message}`);
    console.error('[NeuralChat] API Error:', err);
  } finally {
    state.isLoading = false;
  }
}

/** Load chat history from the backend */
async function loadHistory() {
  if (!state.username) return;

  try {
    const res  = await fetch(`${CONFIG.API_BASE}/history?username=${encodeURIComponent(state.username)}`);
    if (!res.ok) return;

    const data = await res.json();
    const messages = data.history || [];

    if (messages.length === 0) return;

    // Clear welcome, render messages
    DOM.welcomeScreen.style.display = 'none';
    DOM.messagesList.innerHTML = '';
    state.messageCount = 0;

    messages.forEach(msg => {
      appendMessage('user', msg.message,  msg.timestamp);
      appendMessage('bot',  msg.reply,    msg.timestamp);
    });

    showToast(`Restored ${messages.length} previous messages`, 'success');

  } catch (err) {
    console.warn('[NeuralChat] History load failed:', err);
  }
}

/** Clear all chat history */
async function clearHistory() {
  if (!state.username) return;
  if (!confirm('Clear all chat history? This cannot be undone.')) return;

  try {
    const res = await fetch(`${CONFIG.API_BASE}/clear`, {
      method:  'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: state.username }),
    });

    if (res.ok) {
      DOM.messagesList.innerHTML   = '';
      DOM.welcomeScreen.style.display = 'flex';
      state.messageCount = 0;
      updateMsgCount();
      showToast('Chat history cleared', 'success');
    }
  } catch (err) {
    showToast('Failed to clear history', 'error');
  }
}

// ════════════════════════════════════════════════════
// EVENT LISTENERS
// ════════════════════════════════════════════════════

function setupEventListeners() {

  // Send on button click
  DOM.sendBtn.addEventListener('click', () => {
    sendMessage(DOM.messageInput.value);
  });

  // Send on Enter (Shift+Enter = newline)
  DOM.messageInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(DOM.messageInput.value);
    }
  });

  // Auto-resize textarea + char counter
  DOM.messageInput.addEventListener('input', () => {
    const len = DOM.messageInput.value.length;
    updateCharCounter(len);
    DOM.sendBtn.disabled = len === 0 || state.isLoading;

    // Auto height
    DOM.messageInput.style.height = 'auto';
    DOM.messageInput.style.height = Math.min(DOM.messageInput.scrollHeight, 180) + 'px';
  });

  // Suggestion chips
  document.querySelectorAll('.suggestion-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const msg = chip.dataset.msg;
      DOM.messageInput.value = msg;
      updateCharCounter(msg.length);
      DOM.sendBtn.disabled = false;
      DOM.messageInput.focus();
    });
  });

  // Sidebar actions
  DOM.clearBtn.addEventListener('click', clearHistory);
  DOM.downloadBtn.addEventListener('click', downloadChat);
  DOM.newChatBtn.addEventListener('click', () => {
    DOM.messagesList.innerHTML   = '';
    DOM.welcomeScreen.style.display = 'flex';
    state.messageCount = 0;
    updateMsgCount();
    closeMobileSidebar();
  });
}

// ════════════════════════════════════════════════════
// VOICE INPUT
// ════════════════════════════════════════════════════

function setupVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    DOM.voiceBtn.style.display = 'none';
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous       = false;
  recognition.interimResults   = true;
  recognition.lang             = 'en-US';
  state.voiceRecognition       = recognition;

  recognition.onresult = e => {
    const transcript = Array.from(e.results)
      .map(r => r[0].transcript)
      .join('');
    DOM.messageInput.value = transcript;
    updateCharCounter(transcript.length);
    DOM.sendBtn.disabled = transcript.length === 0;
    DOM.messageInput.style.height = 'auto';
    DOM.messageInput.style.height = Math.min(DOM.messageInput.scrollHeight, 180) + 'px';
  };

  recognition.onend = () => {
    state.isRecording = false;
    DOM.voiceBtn.classList.remove('recording');
    DOM.voiceBtn.title = 'Voice input';
  };

  recognition.onerror = e => {
    showToast(`Voice error: ${e.error}`, 'error');
    state.isRecording = false;
    DOM.voiceBtn.classList.remove('recording');
  };

  DOM.voiceBtn.addEventListener('click', () => {
    if (state.isRecording) {
      recognition.stop();
    } else {
      recognition.start();
      state.isRecording = true;
      DOM.voiceBtn.classList.add('recording');
      DOM.voiceBtn.title = 'Listening... (click to stop)';
      showToast('🎤 Listening...', '');
    }
  });
}

// ════════════════════════════════════════════════════
// DOWNLOAD CHAT
// ════════════════════════════════════════════════════

function downloadChat() {
  const rows = DOM.messagesList.querySelectorAll('.message-row');
  if (rows.length === 0) {
    showToast('No messages to download', 'error');
    return;
  }

  let content = `NeuralChat — Conversation Export\n`;
  content += `User: ${state.username}\n`;
  content += `Date: ${new Date().toLocaleString()}\n`;
  content += `${'═'.repeat(50)}\n\n`;

  rows.forEach(row => {
    const role   = row.classList.contains('user') ? state.username || 'You' : 'NeuralChat';
    const bubble = row.querySelector('.msg-bubble');
    const text   = bubble ? bubble.innerText.trim() : '';
    const time   = row.querySelector('.msg-time')?.textContent || '';
    content += `[${time}] ${role}:\n${text}\n\n`;
  });

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `neuralchat-${state.username}-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('Chat downloaded!', 'success');
}

// ════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ════════════════════════════════════════════════════

/** Scroll messages area to the bottom */
function scrollToBottom() {
  requestAnimationFrame(() => {
    DOM.messagesArea.scrollTop = DOM.messagesArea.scrollHeight;
  });
}

/** Update the character counter display */
function updateCharCounter(len) {
  DOM.charCounter.textContent = `${len} / ${CONFIG.MAX_MSG_LENGTH}`;
  DOM.charCounter.className = 'char-counter';
  if (len >= CONFIG.MAX_MSG_LENGTH)   DOM.charCounter.classList.add('error');
  else if (len >= CONFIG.WARN_THRESHOLD) DOM.charCounter.classList.add('warn');
}

/** Update the message count badge */
function updateMsgCount() {
  DOM.msgCount.textContent = `${state.messageCount} message${state.messageCount !== 1 ? 's' : ''}`;
}

/** Show a toast notification */
let toastTimer;
function showToast(msg, type = '') {
  clearTimeout(toastTimer);
  DOM.toast.textContent = msg;
  DOM.toast.className   = `toast ${type} show`;
  toastTimer = setTimeout(() => {
    DOM.toast.className = 'toast';
  }, 3000);
}

/** Copy text to clipboard */
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    // Fallback
    const el  = document.createElement('textarea');
    el.value  = text;
    el.style.position = 'fixed';
    el.style.opacity  = '0';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
  }
}

/** Escape HTML to prevent XSS in user messages */
function escapeHtml(text) {
  const map = { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' };
  return String(text).replace(/[&<>"']/g, m => map[m]);
}

/** Format an ISO timestamp to a readable time */
function formatTime(iso) {
  try {
    return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } catch {
    return '';
  }
}

// ════════════════════════════════════════════════════
// BOOTSTRAP
// ════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', init);
