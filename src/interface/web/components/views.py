from fasthtml.common import (Form, Group, Input, Button, Hidden, Div, Label, H1)   

def ChatInputForm(is_landing=False):
    if is_landing:
        input_cls = "input input-lg w-full rounded-2xl shadow-xl h-14 text-lg bg-base-200 border-transparent focus:border-primary focus:bg-base-100 transition-all duration-300 pl-6"
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
        Group(cls="relative flex items-center w-full")(
            Input(
                name='msg', 
                placeholder="Type a message...", 
                cls=input_cls,
                autocomplete="off",
                autofocus=True
            ),
            Button(
                "Send", 
                cls=f"{btn_cls} absolute right-2 z-10", 
                type="submit"
            )
        ),
        Hidden(value="landing" if is_landing else "chat", name="mode")
    )
    

def LandingView():
    return Div(id="main-content", cls="flex flex-col h-full relative")(
        Div(cls="absolute top-0 left-0 right-0 p-4 flex items-center justify-between z-10")(
            Label(
                _for="my-drawer", 
                cls="btn btn-ghost btn-circle lg:hidden"
            ),
            Div()
        ),
        Div(cls="flex-1 flex flex-col items-center justify-center p-4 space-y-8 animate-in fade-in zoom-in duration-500")(
            Div(cls="text-center space-y-2")(
                H1("Ada yang bisa saya bantu?", cls="text-4xl md:text-5xl font-bold"),
            ),
            Div(cls="w-full max-w-2xl px-4")(
                ChatInputForm(is_landing=True)
            )
        ),

        Div(cls="p-4 text-center text-xs opacity-50")(
            "Chatbot can make mistakes. Check important info."
        )
    )

def ChatView(history_elements):
    return Div(id="main-content", cls="flex flex-col h-full relative")(
        Div(cls="sticky top-0 left-0 right-0 p-3 bg-base-100/90 backdrop-blur-md z-10 border-b border-base-300")(
            Label(
                _for="my-drawer", 
                cls="btn btn-ghost btn-circle btn-sm"
            )
        ),

        Div(
            id="chat-list", 
            cls="flex-1 overflow-y-auto p-4 md:p-8 space-y-4",
            style="padding-bottom: 120px;"
        )(
            *history_elements
        ),
        Div(cls="fixed bottom-0 left-0 right-0 lg:left-64 p-4 bg-gradient-to-t from-base-100 via-base-100 to-transparent pointer-events-none")(
            Div(cls="pointer-events-auto")(
                ChatInputForm(is_landing=False)
            ),
            Div("Chatbot can make mistakes.", cls="text-[10px] text-center mt-2 opacity-50")
        )
    )
