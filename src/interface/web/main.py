from fasthtml.common import (Div, Title, Label, 
                             Input, I, serve,
                             FastHTML)

from .components.config import hdrs
from .components.views import LandingView, ChatView
from .components.bars import Sidebar


app = FastHTML(hdrs=hdrs)
# app = FastHTMLWithLiveReload(hdrs=hdrs)

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

    
messages_history = []

@app.get("/") # type: ignore
def index():
    return (
        Div(cls="drawer lg:drawer-open")( 
            Input(id="my-drawer", type="checkbox", cls="drawer-toggle"),
            Div(cls="drawer-content flex flex-col h-screen bg-base-100")(
                LandingView()
            ),
            Sidebar()
        )
    )
    

@app.post("/send") # type: ignore
def send(msg: str, mode: str):
    if not msg.strip(): 
        return ChatView(messages_history) if mode == "chat" else LandingView()
    messages_history.append(ChatMessage(msg, True))
    
    response_text = f"Ini adalah respon AI untuk: '{msg}'. Tampilan sekarang sudah dalam mode percakapan!"
    messages_history.append(ChatMessage(response_text, False))
    
    return ChatView(messages_history)

def main():
    serve()