from fasthtml.common import (Input, Button, Div, Label, H2, Span)   


def Sidebar():
    return Div(cls="drawer-side z-40")(
        Label(_for="my-drawer", cls="drawer-overlay"), 
        Div(cls="menu p-4 w-64 min-h-full bg-base-200 text-base-content flex flex-col")(
            Div(cls="mb-6 px-2 pt-2")(
                H2("My ChatBot", cls="text-xl font-bold tracking-tight")
            ),
            
            Div(cls="flex-1 overflow-y-auto space-y-2")(
                Button("+ New Chat", cls="btn btn-ghost btn-sm w-full justify-start font-normal border border-base-300"),
                Div(cls="divider my-2"),
                Div("History chat dummy...", cls="text-xs opacity-50 px-4")
            ),
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