from fasthtml.common import *

# ==========================================
# 1. SETUP & ASSETS
# ==========================================
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

app = FastHTML(hdrs=hdrs)

# ==========================================
# 2. KOMPONEN UI (ICONS & WIDGETS)
# ==========================================


def ChatMessage(msg, user):
    if user:
        return Div(cls="flex justify-end mb-4 animate-in fade-in slide-in-from-bottom-2")(
            Div(msg, cls="bg-primary text-primary-content py-3 px-5 rounded-3xl max-w-[80%] rounded-tr-md shadow-sm")
        )
    else:
        return Div(cls="flex justify-start mb-4 items-start gap-3 animate-in fade-in slide-in-from-bottom-2")(
            Div(cls="avatar placeholder")(
                Div(cls="bg-accent text-accent-content rounded-full w-8 h-8 flex items-center justify-center font-bold text-xs")("AI")
            ),
            Div(cls="flex-1")(
                Div(msg, cls="prose prose-sm dark:prose-invert max-w-none p-2")
            )
        )

def ChatInputForm(is_landing=False):
    if is_landing:
        input_cls = "input input-lg w-full rounded-2xl shadow-xl h-14 text-lg bg-base-200 border-transparent focus:border-primary focus:bg-base-100 transition-all duration-300 pl-6"
        # HAPUS 'absolute', tambahkan 'ml-auto' untuk mendorong ke kanan jika perlu
        btn_cls = "btn btn-primary h-11 min-h-11 px-6 rounded-xl shadow-md hover:scale-105 transition-transform"
    else:
        input_cls = "input input-md w-full rounded-2xl shadow-sm h-12 bg-base-200 border-transparent focus:border-primary focus:bg-base-100 transition-all duration-300 pl-4"
        btn_cls = "btn btn-primary h-10 min-h-10 px-4 rounded-xl shadow-md hover:scale-105 transition-transform"

    return Form(
        hx_post="/send", 
        hx_target="#main-content", 
        hx_swap="innerHTML",
        cls="w-full max-w-2xl mx-auto",
        hx_on__after_request="this.reset(); setTimeout(scrollToBottom, 100);"
    )(
        # KUNCI: Tambahkan 'relative items-center' agar komponen di dalam Group tertata rapi
        # 'w-full' memastikan Group mengambil seluruh ruang yang tersedia
        Group(cls="relative flex items-center w-full")(
            Input(
                name='msg', 
                placeholder="Type a message...", 
                cls=input_cls,
                autocomplete="off",
                autofocus=True
            ),
            # KUNCI: Menggunakan 'absolute' dan 'right-2' DI DALAM Group
            # Pastikan tidak ada 'left-5.5' yang tertinggal
            Button(
                "Send", 
                cls=f"{btn_cls} absolute right-2 z-10", 
                type="submit"
            )
        ),
        Hidden(value="landing" if is_landing else "chat", name="mode")
    )

def Sidebar():
    return Div(cls="drawer-side z-40")(
        Label(_for="my-drawer", cls="drawer-overlay"), 
        Div(cls="menu p-4 w-64 min-h-full bg-base-200 text-base-content flex flex-col")(
            # Header Sidebar
            Div(cls="mb-6 px-2 pt-2")(
                H2("My ChatBot", cls="text-xl font-bold tracking-tight")
            ),
            
            # Area History
            Div(cls="flex-1 overflow-y-auto space-y-2")(
                Button("+ New Chat", cls="btn btn-ghost btn-sm w-full justify-start font-normal border border-base-300"),
                Div(cls="divider my-2"),
                Div("History chat dummy...", cls="text-xs opacity-50 px-4")
            ),

            # Footer Sidebar
            Div(cls="mt-auto pt-4 border-t border-base-300 space-y-3")(
                Div(cls="form-control")(
                    Label(cls="label")(
                        Span("API Key", cls="label-text text-xs font-bold opacity-70")
                    ),
                    Input(type="password", placeholder="sk-...", cls="input input-sm input-bordered w-full bg-base-100")
                ),
                Button(
                    Span("Toggle Theme", cls="ml-2"),
                    cls="btn btn-ghost btn-sm w-full justify-start gap-2", 
                    onclick="toggleTheme()"
                ),
                Div(cls="divider my-2"),
                Div(cls="flex items-center gap-3 p-2 rounded-lg hover:bg-base-300 cursor-pointer transition-colors")(
                    Div(cls="avatar placeholder")(
                        Div(cls="bg-neutral text-neutral-content rounded-full w-8 text-xs")("K")
                    ),
                    Span("Kurnia 313", cls="text-sm font-medium")
                )
            )
        )
    )
    
    
    
# ==========================================
# 3. LAYOUT VIEWS
# ==========================================

def LandingView():
    return Div(id="main-content", cls="flex flex-col h-full relative")(
        # Header with Menu Button
        Div(cls="absolute top-0 left-0 right-0 p-4 flex items-center justify-between z-10")(
            Label(
                _for="my-drawer", 
                cls="btn btn-ghost btn-circle lg:hidden"
            ),
            Div()
        ),
        
        # Center Content
        Div(cls="flex-1 flex flex-col items-center justify-center p-4 space-y-8 animate-in fade-in zoom-in duration-500")(
            Div(cls="text-center space-y-2")(
                H1("Ada yang bisa saya bantu?", cls="text-4xl md:text-5xl font-bold"),
            ),
            Div(cls="w-full max-w-2xl px-4")(
                ChatInputForm(is_landing=True)
            )
        ),
        
        # Footer
        Div(cls="p-4 text-center text-xs opacity-50")(
            "Chatbot can make mistakes. Check important info."
        )
    )

def ChatView(history_elements):
    return Div(id="main-content", cls="flex flex-col h-full relative")(
        # Sticky Header with Menu Button
        Div(cls="sticky top-0 left-0 right-0 p-3 bg-base-100/90 backdrop-blur-md z-10 border-b border-base-300")(
            Label(
                _for="my-drawer", 
                cls="btn btn-ghost btn-circle btn-sm"
            )
        ),
        
        # Chat Area
        Div(
            id="chat-list", 
            cls="flex-1 overflow-y-auto p-4 md:p-8 space-y-4",
            style="padding-bottom: 120px;"
        )(
            *history_elements
        ),
        
        # Fixed Input Area
        Div(cls="fixed bottom-0 left-0 right-0 lg:left-64 p-4 bg-gradient-to-t from-base-100 via-base-100 to-transparent pointer-events-none")(
            Div(cls="pointer-events-auto")(
                ChatInputForm(is_landing=False)
            ),
            Div("Chatbot can make mistakes.", cls="text-[10px] text-center mt-2 opacity-50")
        )
    )

# ==========================================
# 4. ROUTING & LOGIC
# ==========================================

@app.get("/")
def index():
    return (
        Title("ChatBot Pro"),
        Div(cls="drawer lg:drawer-open")( # lg:drawer-open menjaga sidebar tetap terbuka di desktop
            Input(id="my-drawer", type="checkbox", cls="drawer-toggle"),
            
            # Main Content Area
            Div(cls="drawer-content flex flex-col h-screen bg-base-100")(
                # Tombol Toggle (Hanya muncul di mobile secara default, atau sesuaikan class-nya)
                Div(cls="p-4 lg:hidden")( 
                    Label(_for="my-drawer", cls="btn btn-square btn-ghost")(
                        # Icon Hamburger (Garis 3)
                        I(cls="fa-solid fa-bars") if "fa-solid" in str(hdrs) else "Menu"
                    )
                ),
                LandingView()
            ),
            
            # Sidebar Area
            Sidebar()
        )
    )
    
messages_history = []

@app.post("/send")
def send(msg: str, mode: str):
    if not msg.strip(): 
        return ChatView(messages_history) if mode == "chat" else LandingView()
    
    messages_history.append(ChatMessage(msg, True))
    
    response_text = f"Ini adalah respon AI untuk: '{msg}'. Tampilan sekarang sudah dalam mode percakapan!"
    messages_history.append(ChatMessage(response_text, False))
    
    return ChatView(messages_history)

def main():
    serve()