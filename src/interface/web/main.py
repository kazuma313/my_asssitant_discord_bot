from fasthtml.common import serve, FastHTML, FileResponse
from .components.config import hdrs
from .components.views import LandingView, ChatView, MainLayout, ChatMessage
from .components.profile import ProfileView
from .components.computer_vision import ComputerVisionView
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
ASSETS_DIR = BASE_DIR / "assets"

app = FastHTML(hdrs=hdrs,
               static_path=str(ASSETS_DIR))
# app = FastHTMLWithLiveReload(hdrs=hdrs)

messages_history = []

@app.get("/chatbot") # type: ignore
def index():
    return MainLayout(LandingView()) 


@app.get("/assets/{fname:path}") # type: ignore
def serve_assets(fname: str):
    file_path = ASSETS_DIR / fname
    if file_path.exists():
        return FileResponse(file_path)
    return "", 404


@app.get("/computer_vision") # type: ignore
def computer_vision():
    return MainLayout(
        ComputerVisionView(),
        show_sidebar=False 
    )

@app.get("/") # type: ignore
def profile():
    return MainLayout(
        ProfileView(),
        show_sidebar=False
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