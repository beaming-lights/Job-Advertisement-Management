from importlib import reload
from nicegui import ui, app
from services.api_service import APIService
from components.header import create_header
from components.hero import create_hero
from components.footer import create_footer
from pages.post_job import post_job_page
from pages.jobs import jobs_page
from pages.vendor_dashboard import vendor_dashboard_page
from pages.candidate_profile import candidate_profile_page
from pages.candidate_edit_profile import candidate_edit_profile_page
from pages.login import login_page
from pages.signup import signup_page
from pages.job_seeker_dashboard import job_seeker_dashboard_page
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
import base64

# Load environment variables
load_dotenv()

# Initialize API service
api_service = APIService()


# Global function for showing job details modal - Compact Box Layout
def show_job_details(job):
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
                            # ui.icon("payments", size="1.2rem").classes("text-emerald-500 mb-1")
                            ui.label("Salary").classes("text-xs text-gray-500")
                            ui.label(job.get("salary", "Competitive")).classes("text-sm font-semibold text-gray-900")
                        
                        # Job Type
                        with ui.element("div").classes("bg-white rounded-lg p-3 border text-center"):
                            # ui.icon("work", size="1.2rem").classes("text-blue-500 mb-1")
                            ui.label("Type").classes("text-xs text-gray-500")
                            ui.label(job.get("job_type", "Full-time")).classes("text-sm font-semibold text-gray-900")
                    
                    # Right Column
                    with ui.element("div").classes("space-y-3"):
                        # Experience
                        with ui.element("div").classes("bg-white rounded-lg p-3 border text-center"):
                            # ui.icon("trending_up", size="1.2rem").classes("text-purple-500 mb-1")
                            ui.label("Level").classes("text-xs text-gray-500")
                            ui.label(job.get("experience_level", "Mid-level")).classes("text-sm font-semibold text-gray-900")
                        
                        # Posted
                        with ui.element("div").classes("bg-white rounded-lg p-3 border text-center"):
                            # ui.icon("schedule", size="1.2rem").classes("text-orange-500 mb-1")
                            ui.label("Posted").classes("text-xs text-gray-500")
                            ui.label(job.get("posted_date", "Recently")).classes("text-sm font-semibold text-gray-900")

                # Compact Content Sections
                # Job Description
                with ui.element("div").classes("bg-white rounded-lg border p-4"):
                    with ui.row().classes("items-center space-x-2 mb-3"):
                        # ui.icon("description", size="1.2rem").classes("text-emerald-500")
                        ui.label("Job Description").classes("text-lg font-bold text-gray-900")
                    
                    ui.label(job.get("description", "No description available.")).classes(
                        "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                    )

                # Requirements
                if job.get("requirements"):
                    with ui.element("div").classes("bg-white rounded-lg border p-4"):
                        with ui.row().classes("items-center space-x-2 mb-3"):
                            # ui.icon("checklist", size="1.2rem").classes("text-blue-500")
                            ui.label("Requirements").classes("text-lg font-bold text-gray-900")
                        
                        ui.label(job.get("requirements")).classes(
                            "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                        )

                # Benefits (if available)
                if job.get("benefits"):
                    with ui.element("div").classes("bg-white rounded-lg border p-4"):
                        with ui.row().classes("items-center space-x-2 mb-3"):
                            # ui.icon("star", size="1.2rem").classes("text-yellow-500")
                            ui.label("Benefits").classes("text-lg font-bold text-gray-900")
                        
                        ui.label(job.get("benefits")).classes(
                            "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                        )

                # Skills (if available)
                if job.get("skills"):
                    with ui.element("div").classes("bg-white rounded-lg border p-4"):
                        with ui.row().classes("items-center space-x-2 mb-3"):
                            # ui.icon("psychology", size="1.2rem").classes("text-purple-500")
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
                # # Secondary Actions
                # with ui.row().classes("space-x-2"):
                #     ui.button(
                #         icon="bookmark_border"
                #     ).classes(
                #         "p-2 text-gray-600 hover:text-emerald-500 hover:bg-emerald-100 rounded-full p-1"
                #     ).props("flat dense").tooltip("Save Job")
                    
                #     ui.button(
                #         icon="share"
                #     ).classes(
                #         "p-2 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-full p-1"
                #     ).props("flat dense").tooltip("Share Job")
                
                # Primary Action
                ui.button(
                    "Apply Now",
                    color="#00b074"
                ).classes(
                    "px-6 py-2 rounded-lg font-semibold text-white"
                ).props("unelevated")
    
    dialog.open()


@ui.page("/")
def index():
    """Main page for the JobBoard website."""
    # Add global styles to force flush footer and eliminate white gaps
    ui.add_head_html(
        """<style>
        html, body { 
            overflow-x: hidden; 
            max-width: 100vw; 
            margin: 0 !important; 
            padding: 0 !important; 
            height: 100%; 
            min-height: 100vh;
        } 
        * { 
            box-sizing: border-box; 
        } 
        footer { 
            margin-bottom: 0 !important; 
            padding-bottom: 0 !important; 
            margin-top: 0 !important;
        }
        .q-page-container {
            padding-bottom: 0 !important;
            margin-bottom: 0 !important;
        }
        .q-layout {
            min-height: 100vh !important;
        }
        body::after {
            content: "";
            display: block;
            height: 0;
            clear: both;
        }
        
    .nicegui-content,
    .nicegui-column {
        display: block !important;
        flex-direction: unset !important;
        align-items: unset !important;
        gap: 0 !important;
        padding: 0 !important;
        }
    
    /* Exceptions for card sections to preserve flexbox layout */
    .card-section .nicegui-content,
    .card-section .nicegui-column {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 2rem !important;
        padding: initial !important;
        }
    
    .card-container .nicegui-row {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        align-items: stretch !important;
        gap: 2rem !important;
        flex-wrap: wrap !important;
        }
    </style>"""
    )


    # Header
    create_header()

    # Hero Section - remove any spacing
    create_hero()

    # Features Section
    with ui.element("section").classes("py-20 bg-gray-50 card-section"):
        with ui.element("div").classes("container mx-auto px-4"):
            ui.label("Why Choose JobBoard?").classes(
                "text-4xl font-bold text-center text-[#2b3940] mb-16"
            )
            with ui.row().classes("grid grid-cols-1 md:grid-cols-3 gap-8 relative card-container"):
                # Card 1 - Smart Job Search
                with ui.card().classes(
                    "w-full max-w-sm bg-white hover:bg-green-50 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0 overflow-hidden group"
                ):
                    # Green colored line on top
                    ui.element("div").classes("h-1 bg-green-600 w-full")
                    with ui.column().classes("p-8 text-center"):
                        # Icon container
                        with ui.element("div").classes(
                            "mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 group-hover:bg-green-200 transition-colors duration-300"
                        ):
                            ui.icon("search", size="2rem").classes("text-green-600")
                        
                        ui.label("Smart Job Search").classes(
                            "text-xl font-bold text-gray-900 mb-3"
                        )
                        ui.label(
                            "Advanced filters and AI-powered recommendations to find the perfect job match."
                        ).classes("text-gray-600 text-sm leading-relaxed")
                
                # Card 2 - Top Companies
                with ui.card().classes(
                    "w-full max-w-sm bg-white hover:bg-green-50 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0 overflow-hidden group"
                ):
                    # Green colored line on top
                    ui.element("div").classes("h-1 bg-green-600 w-full")
                    with ui.column().classes("p-8 text-center"):
                        # Icon container
                        with ui.element("div").classes(
                            "mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 group-hover:bg-green-200 transition-colors duration-300"
                        ):
                            ui.icon("business", size="2rem").classes("text-green-600")
                        
                        ui.label("Top Companies").classes(
                            "text-xl font-bold text-gray-900 mb-3"
                        )
                        ui.label(
                            "Connect with leading companies and startups looking for talented professionals."
                        ).classes("text-gray-600 text-sm leading-relaxed")
                
                # Card 3 - Career Growth
                with ui.card().classes(
                    "w-full max-w-sm bg-white hover:bg-green-50 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-0 overflow-hidden group"
                ):
                    # Green colored line on top
                    ui.element("div").classes("h-1 bg-green-600 w-full")
                    with ui.column().classes("p-8 text-center"):
                        # Icon container
                        with ui.element("div").classes(
                            "mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 group-hover:bg-green-200 transition-colors duration-300"
                        ):
                            ui.icon("trending_up", size="2rem").classes("text-green-600")
                        
                        ui.label("Career Growth").classes(
                            "text-xl font-bold text-gray-900 mb-3"
                        )
                        ui.label(
                            "Access resources, tips, and opportunities to accelerate your career growth."
                        ).classes("text-gray-600 text-sm leading-relaxed")

    # Stats Section - Modern Gradient Design
    with ui.element("section").classes("py-24 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden").style(
        "width: 100vw; margin-left: calc(-50vw + 50%);"
    ):
        # Background decoration
        with ui.element("div").classes("absolute inset-0 opacity-10"):
            with ui.element("div").classes("absolute top-20 left-10 w-72 h-72 bg-emerald-500 rounded-full blur-3xl"):
                pass
            with ui.element("div").classes("absolute bottom-20 right-10 w-96 h-96 bg-blue-500 rounded-full blur-3xl"):
                pass
        
        with ui.element("div").classes("container mx-auto px-4 relative z-10"):
            ui.label("Platform Statistics").classes(
                "text-5xl font-bold text-center text-white mb-4"
            )
            ui.label("Trusted by thousands of professionals worldwide").classes(
                "text-xl text-center text-gray-300 mb-16"
            )
            
            with ui.row().classes("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"):
                # Stat Card 1 - Modern Glass Design
                with ui.element("div").classes(
                    "group relative bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 text-center hover:bg-white/20 hover:scale-105 transition-all duration-500"
                ):
                    with ui.element("div").classes(
                        "w-16 h-16 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:rotate-12 transition-transform duration-500"
                    ):
                        ui.icon("work", size="2rem").classes("text-white")
                    ui.label("10,000+").classes("text-4xl font-bold text-white mb-2")
                    ui.label("Active Jobs").classes("text-lg text-gray-300")
                    
                    # Glow effect
                    with ui.element("div").classes(
                        "absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                    ):
                        pass
                
                # Stat Card 2
                with ui.element("div").classes(
                    "group relative bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 text-center hover:bg-white/20 hover:scale-105 transition-all duration-500"
                ):
                    with ui.element("div").classes(
                        "w-16 h-16 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:rotate-12 transition-transform duration-500"
                    ):
                        ui.icon("business", size="2rem").classes("text-white")
                    ui.label("5,000+").classes("text-4xl font-bold text-white mb-2")
                    ui.label("Companies").classes("text-lg text-gray-300")
                    
                    # Glow effect
                    with ui.element("div").classes(
                        "absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                    ):
                        pass
                
                # Stat Card 3
                with ui.element("div").classes(
                    "group relative bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 text-center hover:bg-white/20 hover:scale-105 transition-all duration-500"
                ):
                    with ui.element("div").classes(
                        "w-16 h-16 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:rotate-12 transition-transform duration-500"
                    ):
                        ui.icon("people", size="2rem").classes("text-white")
                    ui.label("50,000+").classes("text-4xl font-bold text-white mb-2")
                    ui.label("Job Seekers").classes("text-lg text-gray-300")
                    
                    # Glow effect
                    with ui.element("div").classes(
                        "absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                    ):
                        pass
                
                # Stat Card 4
                with ui.element("div").classes(
                    "group relative bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 text-center hover:bg-white/20 hover:scale-105 transition-all duration-500"
                ):
                    with ui.element("div").classes(
                        "w-16 h-16 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:rotate-12 transition-transform duration-500"
                    ):
                        ui.icon("check_circle", size="2rem").classes("text-white")
                    ui.label("95%").classes("text-4xl font-bold text-white mb-2")
                    ui.label("Success Rate").classes("text-lg text-gray-300")
                    
                    # Glow effect
                    with ui.element("div").classes(
                        "absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                    ):
                        pass

    # Featured Jobs Section - Modern Card Design
    with ui.element("section").classes("py-24 bg-gradient-to-b from-white to-gray-50 relative"):
        # Background decoration
        with ui.element("div").classes("absolute inset-0 overflow-hidden"):
            with ui.element("div").classes("absolute -top-40 -right-40 w-80 h-80 bg-emerald-100 rounded-full opacity-30"):
                pass
            with ui.element("div").classes("absolute -bottom-40 -left-40 w-96 h-96 bg-blue-100 rounded-full opacity-20"):
                pass
        
        with ui.element("div").classes("container mx-auto px-4 relative z-10"):
            # Section Title
            with ui.element("div").classes("text-center mb-16"):
                ui.label("Featured Jobs").classes(
                    "text-5xl font-bold text-gray-900 mb-6"
                )
                ui.label("Discover hand-picked positions from leading companies").classes(
                    "text-xl text-gray-600 max-w-2xl mx-auto"
                )

            # Job Cards Grid
            featured_jobs = api_service.get_jobs()[:3]
            if featured_jobs:
                with ui.row().classes("grid grid-cols-1 md:grid-cols-3 gap-8"):
                    for job in featured_jobs:
                        with ui.element("div").classes(
                            "group relative bg-white rounded-2xl p-6 shadow-md hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border border-gray-100 overflow-hidden"
                        ):
                            # Top accent bar
                            with ui.element("div").classes(
                                "absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 to-emerald-600"
                            ):
                                pass
                            
                            # Company logo/initial
                            company_name = job.get("company", "Unknown")
                            with ui.element("div").classes(
                                "w-16 h-16 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300"
                            ):
                                ui.label(
                                    company_name[0].upper() if company_name else "U"
                                ).classes("text-xl font-bold text-white")

                            # Job details
                            ui.label(job.get("title", "Job Title")).classes(
                                "text-xl font-bold text-gray-900 mb-2 group-hover:text-emerald-600 transition-colors"
                            )
                            ui.label(company_name).classes(
                                "text-base font-medium text-gray-600 mb-3"
                            )
                            
                            # Location and type
                            with ui.element("div").classes("flex items-center gap-3 mb-4"):
                                with ui.element("div").classes("flex items-center gap-1"):
                                    ui.icon("location_on", size="1rem").classes("text-gray-400")
                                    ui.label(job.get("location", "N/A")).classes("text-xs text-gray-500")
                                with ui.element("div").classes("flex items-center gap-1"):
                                    ui.icon("schedule", size="1rem").classes("text-gray-400")
                                    ui.label(job.get("job_type", "N/A")).classes("text-xs text-gray-500")
                            
                            # Salary badge
                            if job.get("salary"):
                                with ui.element("div").classes(
                                    "inline-block bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-semibold mb-4"
                                ):
                                    ui.label(job.get("salary"))
                            
                            # Action button
                            ui.button(
                                "View Details",
                                on_click=lambda j=job: show_job_details(j),
                                color="#00b074"
                            ).classes(
                                "w-full py-2 rounded-lg font-medium transition-all duration-300 text-white text-sm"
                            ).props("unelevated")
                            
                            # Decorative element
                            with ui.element("div").classes(
                                "absolute -bottom-2 -right-2 w-24 h-24 bg-emerald-100 rounded-full opacity-20 group-hover:opacity-40 transition-opacity"
                            ):
                                pass

            # See More Jobs Button
            with ui.element("div").classes("text-center mt-16"):
                ui.button(
                    "Explore All Jobs",
                    on_click=lambda: ui.navigate.to("/jobs"),
                    color="#00b074"
                ).classes(
                    "px-8 py-4 rounded-xl font-semibold transition-all duration-300"
                ).props("outline")

    # CTA Section - Modern Gradient Design
    with ui.element("section").classes("py-32 bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white relative overflow-hidden").style(
        "width: 100vw; margin-left: calc(-50vw + 50%);"
    ):
        # Animated background elements
        with ui.element("div").classes("absolute inset-0"):
            with ui.element("div").classes("absolute top-20 left-20 w-64 h-64 bg-emerald-500 rounded-full opacity-10 blur-3xl animate-pulse"):
                pass
            with ui.element("div").classes("absolute bottom-20 right-20 w-80 h-80 bg-blue-500 rounded-full opacity-10 blur-3xl animate-pulse"):
                pass
            with ui.element("div").classes("absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-500 rounded-full opacity-5 blur-3xl"):
                pass
        
        with ui.element("div").classes("container mx-auto px-4 text-center relative z-10"):
            # Main CTA content
            with ui.element("div").classes("max-w-4xl mx-auto"):
                ui.label("Transform Your Career Today").classes(
                    "text-6xl font-bold mb-6 bg-gradient-to-r from-white via-gray-100 to-emerald-100 bg-clip-text text-transparent"
                )
                ui.label(
                    "Join over 50,000 professionals who discovered their dream careers through our platform. Your next opportunity is just one click away."
                ).classes("text-2xl mb-12 text-gray-300 leading-relaxed max-w-3xl mx-auto")
                
                # Action buttons with modern styling
                with ui.element("div").classes("flex flex-col sm:flex-row gap-6 justify-center items-center"):
                    ui.button(
                        "Signup Today", 
                        on_click=lambda: ui.navigate.to("/signup"),
                        color="#00b074"
                    ).classes(
                        "group relative text-white px-8 py-3 text-lg font-semibold rounded-xl transform hover:scale-105 transition-all duration-300 shadow-lg"
                    ).props("unelevated")
                    
                    ui.button(
                        "Browse Jobs", 
                        on_click=lambda: ui.navigate.to("/jobs")
                    ).classes(
                        "group relative bg-transparent border-2 border-white/30 text-white px-8 py-3 text-lg font-semibold rounded-xl hover:bg-white/10 hover:border-white/50 backdrop-blur-sm transition-all duration-300"
                    )
                
                # Trust indicators
                with ui.element("div").classes("mt-16 pt-12 border-t border-white/10"):
                    ui.label("Trusted by leading companies worldwide").classes(
                        "text-lg text-gray-400 mb-8"
                    )
                    with ui.element("div").classes("flex justify-center items-center gap-12 opacity-60"):
                        # Company logos placeholder (you can replace with actual logos)
                        for company in ["Google", "Microsoft", "Apple", "Amazon", "Meta"]:
                            with ui.element("div").classes(
                                "text-2xl font-bold text-white/40 hover:text-white/60 transition-colors duration-300"
                            ):
                                ui.label(company)

    # Footer - remove any container constraints
    create_footer()


@ui.page("/candidate-profile")
def candidate_profile():
    """Candidate profile page."""
    create_header()
    candidate_profile_page()
    create_footer()


@ui.page("/candidate-edit-profile")
def candidate_edit_profile():
    """Candidate edit profile page."""
    create_header()
    candidate_edit_profile_page()
    create_footer()


if __name__ in {"__main__", "__mp_main__"}:
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    
    # Get secure storage secret from environment variables
    storage_secret = os.getenv('STORAGE_SECRET', 'dev-fallback-secret-change-in-production')
    
    ui.run(
        title="JobBoard - Modern Job Portal", 
        port=int(os.getenv('PORT', 8080)),
        host="0.0.0.0",
        storage_secret=storage_secret,  # Secure session storage
        show=True,  # Auto-open browser
        reload=True  # Enable auto-reload for stability
    )
