from nicegui import ui

def show_sidebar():
    """Display the sidebar component"""
    with ui.column().classes("w-full space-y-4 p-4 bg-white shadow-lg rounded-lg"):
        ui.label("Sidebar").classes("text-lg font-bold text-[#2b3940] mb-4")

        # Navigation items
        ui.button("Dashboard", on_click=lambda: ui.navigate.to("/vendor")).classes("w-full text-left")
        ui.button("Post Job", on_click=lambda: ui.navigate.to("/post-job")).classes("w-full text-left")
        ui.button("My Jobs", on_click=lambda: ui.navigate.to("/vendor")).classes("w-full text-left")
        ui.button("Applicants", on_click=lambda: ui.navigate.to("/vendor")).classes("w-full text-left")
        ui.button("Settings", on_click=lambda: ui.navigate.to("/vendor")).classes("w-full text-left")