"""Job Details Page - Full page view for individual job postings"""

from nicegui import ui
from components.header import create_header
from components.footer import create_footer
from services.api_service import APIService

# Initialize API service
api_service = APIService()

@ui.page("/job/{job_id}")
def job_details_page(job_id: str):
    """Full page view for job details"""
    
    # Get job data from API only
    jobs = api_service.get_jobs()
    print(f"Looking for job ID: {job_id}")
    print(f"Available job IDs: {[j.get('id') for j in jobs]}")
    job = next((j for j in jobs if str(j.get('id')) == str(job_id)), None)
    
    if not job:
        # Create header and show error message
        create_header()
        with ui.element("main").classes("min-h-screen bg-gray-50"):
            with ui.element("div").classes("container mx-auto px-4 py-20 text-center"):
                ui.icon("error_outline", size="4rem").classes("text-gray-400 mb-4")
                ui.label("Job Not Found").classes("text-4xl font-bold text-gray-900 mb-4")
                ui.label("The job you're looking for doesn't exist or has been removed.").classes("text-xl text-gray-600 mb-8")
                ui.button(
                    "Back to Jobs",
                    icon="arrow_back",
                    on_click=lambda: ui.navigate.to("/jobs"),
                    color="#00b074"
                ).classes("px-8 py-3 rounded-xl font-semibold")
        create_footer()
        return
    
    # Add custom styles
    ui.add_head_html("""
        <style>
            html, body { 
                overflow-x: hidden; 
                max-width: 100vw; 
                margin: 0 !important; 
                padding: 0 !important; 
                min-height: 100vh;
            }
        </style>
    """)
    
    # Header
    create_header()
    
    # Main Content
    with ui.element("main").classes("min-h-screen bg-gray-50"):
        # Back to Jobs Link
        with ui.element("div").classes("bg-white border-b border-gray-200 py-4"):
            with ui.element("div").classes("container mx-auto px-4"):
                with ui.row().classes("items-center space-x-3"):
                    ui.button(
                        icon="arrow_back"
                    ).classes(
                        "p-2 text-gray-600 hover:text-emerald-500 hover:bg-emerald-50 rounded-lg transition-all"
                    ).props("flat").on_click(lambda: ui.navigate.to("/jobs"))
                    
                    ui.label("Back to Jobs").classes(
                        "text-lg font-medium text-gray-700 cursor-pointer hover:text-emerald-500 transition-colors"
                    ).on("click", lambda: ui.navigate.to("/jobs"))
        
        # Job Details Content
        with ui.element("div").classes("container mx-auto px-4 py-8"):
            with ui.element("div").classes("max-w-4xl mx-auto"):
                
                # Job Header Card
                with ui.element("div").classes("bg-white rounded-2xl shadow-lg p-8 mb-8"):
                    # Company Logo and Basic Info
                    with ui.row().classes("items-start space-x-6 mb-6"):
                        # Company Logo
                        company_name = job.get("company", "Unknown")
                        with ui.element("div").classes("w-20 h-20 bg-emerald-500 rounded-xl flex items-center justify-center flex-shrink-0"):
                            ui.label(company_name[0].upper() if company_name else "U").classes("text-3xl font-bold text-white")
                        
                        # Job Info
                        with ui.column().classes("flex-1 space-y-3"):
                            ui.label(job.get("title", "Job Title")).classes(
                                "text-4xl font-bold text-gray-900 leading-tight"
                            )
                            with ui.row().classes("items-center space-x-6 text-gray-600"):
                                with ui.row().classes("items-center space-x-2"):
                                    ui.icon("business", size="1.2rem").classes("text-emerald-500")
                                    ui.label(job.get("company", "Company")).classes("text-lg font-medium")
                                with ui.row().classes("items-center space-x-2"):
                                    ui.icon("location_on", size="1.2rem").classes("text-emerald-500")
                                    ui.label(job.get("location", "N/A")).classes("text-lg")
                    
                    # Action Buttons
                    with ui.row().classes("justify-end space-x-4"):
                        ui.button(
                            icon="bookmark_border"
                        ).classes(
                            "p-3 text-gray-600 hover:text-emerald-500 hover:bg-emerald-50 rounded-xl transition-all"
                        ).props("flat").tooltip("Save Job")
                        
                        ui.button(
                            icon="share"
                        ).classes(
                            "p-3 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-xl transition-all"
                        ).props("flat").tooltip("Share Job")
                        
                        ui.button(
                            "Apply Now",
                            icon="send",
                            color="#00b074"
                        ).classes(
                            "px-8 py-3 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
                        ).props("unelevated")

                # Job Info Grid
                with ui.element("div").classes("grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"):
                    # Salary
                    with ui.element("div").classes("bg-white rounded-xl p-6 shadow-md text-center"):
                        ui.icon("payments", size="2rem").classes("text-emerald-500 mb-3")
                        ui.label("Salary").classes("text-sm text-gray-500 font-medium mb-1")
                        ui.label(job.get("salary", "Competitive")).classes("text-lg font-bold text-gray-900")
                    
                    # Job Type
                    with ui.element("div").classes("bg-white rounded-xl p-6 shadow-md text-center"):
                        ui.icon("work", size="2rem").classes("text-blue-500 mb-3")
                        ui.label("Employment").classes("text-sm text-gray-500 font-medium mb-1")
                        ui.label(job.get("job_type", "Full-time")).classes("text-lg font-bold text-gray-900")
                    
                    # Experience Level
                    with ui.element("div").classes("bg-white rounded-xl p-6 shadow-md text-center"):
                        ui.icon("trending_up", size="2rem").classes("text-purple-500 mb-3")
                        ui.label("Experience").classes("text-sm text-gray-500 font-medium mb-1")
                        ui.label(job.get("experience_level", "Mid-level")).classes("text-lg font-bold text-gray-900")
                    
                    # Posted Date
                    with ui.element("div").classes("bg-white rounded-xl p-6 shadow-md text-center"):
                        ui.icon("schedule", size="2rem").classes("text-orange-500 mb-3")
                        ui.label("Posted").classes("text-sm text-gray-500 font-medium mb-1")
                        ui.label(job.get("posted_date", "Recently")).classes("text-lg font-bold text-gray-900")

                # Main Content Sections
                with ui.element("div").classes("space-y-8"):
                    
                    # Job Description
                    with ui.element("div").classes("bg-white rounded-xl shadow-md p-8"):
                        with ui.row().classes("items-center space-x-3 mb-6"):
                            ui.icon("description", size="1.8rem").classes("text-emerald-500")
                            ui.label("Job Description").classes("text-3xl font-bold text-gray-900")
                        
                        ui.label(job.get("description", "No description available.")).classes(
                            "text-gray-700 leading-relaxed text-lg whitespace-pre-wrap"
                        )

                    # Requirements
                    if job.get("requirements"):
                        with ui.element("div").classes("bg-white rounded-xl shadow-md p-8"):
                            with ui.row().classes("items-center space-x-3 mb-6"):
                                ui.icon("checklist", size="1.8rem").classes("text-blue-500")
                                ui.label("Requirements").classes("text-3xl font-bold text-gray-900")
                            
                            ui.label(job.get("requirements")).classes(
                                "text-gray-700 leading-relaxed text-lg whitespace-pre-wrap"
                            )

                    # Benefits (if available)
                    if job.get("benefits"):
                        with ui.element("div").classes("bg-white rounded-xl shadow-md p-8"):
                            with ui.row().classes("items-center space-x-3 mb-6"):
                                ui.icon("star", size="1.8rem").classes("text-yellow-500")
                                ui.label("Benefits & Perks").classes("text-3xl font-bold text-gray-900")
                            
                            ui.label(job.get("benefits")).classes(
                                "text-gray-700 leading-relaxed text-lg whitespace-pre-wrap"
                            )

                    # Skills (if available)
                    if job.get("skills"):
                        with ui.element("div").classes("bg-white rounded-xl shadow-md p-8"):
                            with ui.row().classes("items-center space-x-3 mb-6"):
                                ui.icon("psychology", size="1.8rem").classes("text-purple-500")
                                ui.label("Required Skills").classes("text-3xl font-bold text-gray-900")
                            
                            # Display skills as tags if it's a list, otherwise as text
                            skills = job.get("skills")
                            if isinstance(skills, list):
                                with ui.row().classes("flex-wrap gap-3"):
                                    for skill in skills:
                                        ui.label(skill).classes("px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-base font-medium")
                            else:
                                ui.label(skills).classes("text-gray-700 leading-relaxed text-lg whitespace-pre-wrap")

                # Bottom Apply Section
                with ui.element("div").classes("bg-white rounded-xl shadow-md p-8 mt-8 text-center"):
                    ui.label("Ready to Apply?").classes("text-2xl font-bold text-gray-900 mb-4")
                    ui.label("Join our team and take your career to the next level.").classes("text-gray-600 mb-6")
                    
                    with ui.row().classes("justify-center space-x-4"):
                        ui.button(
                            "Save for Later",
                            icon="bookmark_border"
                        ).classes(
                            "px-6 py-3 text-gray-700 border-2 border-gray-300 rounded-xl hover:border-emerald-500 hover:text-emerald-500 transition-all"
                        ).props("flat")
                        
                        ui.button(
                            "Apply Now",
                            icon="send",
                            color="#00b074"
                        ).classes(
                            "px-10 py-3 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
                        ).props("unelevated")

    # Footer
    create_footer()
