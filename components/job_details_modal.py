"""
Job Details Modal Component - Reusable modal for displaying job details
"""

from nicegui import ui


def show_job_details(job):
    """Global function for showing job details modal - Compact Box Layout"""
    with ui.dialog() as dialog, ui.card().classes(
        "w-full max-w-4xl p-0 overflow-hidden rounded-xl shadow-2xl"
    ):
        # Header with Close Button
        with ui.element("div").classes("bg-white border-b border-gray-200 p-4"):
            with ui.row().classes("w-full justify-between items-center"):
                ui.label("Job Details").classes("text-lg font-semibold text-gray-900")
                ui.button(icon="close", on_click=dialog.close).classes(
                    "text-gray-400 hover:text-emerald-600 hover:bg-emerald-100 rounded-full p-1"
                ).props("flat round dense")
        
        # Scrollable Content in Box
        with ui.scroll_area().classes("max-h-96"):
            with ui.element("div").classes("p-6 space-y-6"):
                
                # Compact Job Header
                with ui.element("div").classes("bg-gray-50 rounded-lg p-4"):
                    with ui.row().classes("items-start space-x-4"):
                        # Company Logo
                        company_name = job.get("company", "Unknown")
                        with ui.element("div").classes("w-12 h-12 bg-emerald-500 rounded-lg flex items-center justify-center flex-shrink-0"):
                            ui.label(company_name[0].upper() if company_name else "U").classes("text-lg font-bold text-white")
                        
                        # Job Info
                        with ui.column().classes("flex-1 space-y-2"):
                            ui.label(job.get("title", "Job Title")).classes(
                                "text-2xl font-bold text-gray-900"
                            )
                            with ui.row().classes("items-center space-x-4 text-gray-600 text-sm"):
                                with ui.row().classes("items-center space-x-1"):
                                    ui.icon("business", size="1rem").classes("text-emerald-500")
                                    ui.label(job.get("company", "Company"))
                                with ui.row().classes("items-center space-x-1"):
                                    ui.icon("location_on", size="1rem").classes("text-emerald-500")
                                    ui.label(job.get("location", "N/A"))

                # Compact Info Grid - 2x2 Layout
                with ui.row().classes("grid grid-cols-2 gap-4"):
                    # Left Column
                    with ui.element("div").classes("space-y-3"):
                        # Salary
                        with ui.element("div").classes("bg-white rounded-lg p-3 border text-center"):
                            ui.label("Salary").classes("text-xs text-gray-500")
                            ui.label(job.get("salary", "Competitive")).classes("text-sm font-semibold text-gray-900")
                        
                        # Job Type
                        with ui.element("div").classes("bg-white rounded-lg p-3 border text-center"):
                            ui.label("Type").classes("text-xs text-gray-500")
                            ui.label(job.get("job_type", "Full-time")).classes("text-sm font-semibold text-gray-900")
                    
                    # Right Column
                    with ui.element("div").classes("space-y-3"):
                        # Experience
                        with ui.element("div").classes("bg-white rounded-lg p-3 border text-center"):
                            ui.label("Level").classes("text-xs text-gray-500")
                            ui.label(job.get("experience_level", "Mid-level")).classes("text-sm font-semibold text-gray-900")
                        
                        # Posted
                        with ui.element("div").classes("bg-white rounded-lg p-3 border text-center"):
                            ui.label("Posted").classes("text-xs text-gray-500")
                            ui.label(job.get("posted_date", "Recently")).classes("text-sm font-semibold text-gray-900")

                # Compact Content Sections
                # Job Description
                with ui.element("div").classes("bg-white rounded-lg border p-4"):
                    with ui.row().classes("items-center space-x-2 mb-3"):
                        ui.label("Job Description").classes("text-lg font-bold text-gray-900")
                    
                    ui.label(job.get("description", "No description available.")).classes(
                        "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                    )

                # Requirements
                if job.get("requirements"):
                    with ui.element("div").classes("bg-white rounded-lg border p-4"):
                        with ui.row().classes("items-center space-x-2 mb-3"):
                            ui.label("Requirements").classes("text-lg font-bold text-gray-900")
                        
                        ui.label(job.get("requirements")).classes(
                            "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                        )

                # Benefits (if available)
                if job.get("benefits"):
                    with ui.element("div").classes("bg-white rounded-lg border p-4"):
                        with ui.row().classes("items-center space-x-2 mb-3"):
                            ui.label("Benefits").classes("text-lg font-bold text-gray-900")
                        
                        ui.label(job.get("benefits")).classes(
                            "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                        )

                # Skills (if available)
                if job.get("skills"):
                    with ui.element("div").classes("bg-white rounded-lg border p-4"):
                        with ui.row().classes("items-center space-x-2 mb-3"):
                            ui.label("Skills").classes("text-lg font-bold text-gray-900")
                        
                        # Display skills as tags if it's a list, otherwise as text
                        skills = job.get("skills")
                        if isinstance(skills, list):
                            with ui.row().classes("flex-wrap gap-2"):
                                for skill in skills:
                                    ui.label(skill).classes("px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs font-medium")
                        else:
                            ui.label(skills).classes("text-gray-700 leading-relaxed text-sm whitespace-pre-wrap")

        # Compact Action Bar
        with ui.element("div").classes("bg-gray-50 border-t border-gray-200 p-4"):
            with ui.row().classes("w-full justify-between items-center"):
                # Primary Action
                ui.button(
                    "Apply Now",
                    color="#00b074"
                ).classes(
                    "px-6 py-2 rounded-lg font-semibold text-white"
                ).props("unelevated")
    
    dialog.open()
