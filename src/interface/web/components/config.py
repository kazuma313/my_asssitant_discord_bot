from fasthtml.common import (Script, Link, picolink)

hdrs = (
    picolink,
    Script(src="https://cdn.tailwindcss.com"),
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"),
    Script("""
        function toggleTheme() {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            const saved = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', saved);
        });
        
        function scrollToBottom() {
            const chatList = document.getElementById('chat-list');
            if (chatList) {
                chatList.scrollTop = chatList.scrollHeight;
            }
        }
    """)
)