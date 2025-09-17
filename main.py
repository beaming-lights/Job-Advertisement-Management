from importlib import reload
from nicegui import ui, app
from services.api_service import APIService
from components.header import create_header
from components.hero import create_hero
from components.footer import create_footer
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
                #         "p-2 text-gray-600 hover:text-emerald-500 hover:bg-emerald-50 rounded-lg transition-all"
                #     ).props("flat dense").tooltip("Save Job")
                    
                #     ui.button(
                #         icon="share"
                #     ).classes(
                #         "p-2 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-all"
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
    </style>"""
    )

    ui.add_head_html(
        """
<style>
/* NiceGUI-Content Overrides */
.nicegui-content {
    display: block !important;
    flex-direction: unset !important;
    align-items: unset !important;
    gap: 0 !important;
    padding: 0 !important;
}
</style>
"""
    )

    # Header
    create_header()

    # Hero Section - remove any spacing
    create_hero()

    # Features Section
    with ui.element("section").classes("py-20 bg-gray-50"):
        with ui.element("div").classes("container mx-auto px-4"):
            ui.label("Why Choose JobBoard?").classes(
                "text-4xl font-bold text-center text-[#2b3940] mb-16"
            )
            with ui.row().classes("grid grid-cols-1 md:grid-cols-3 gap-8 relative"):
                # Card 1 - Smart Job Search
                with ui.column().classes(
                    "group relative overflow-hidden bg-white/80 backdrop-blur-sm p-8 rounded-3xl border border-white/20 shadow-2xl hover:shadow-3xl hover:scale-105 transition-all duration-500 flex items-center justify-center text-center"
                ).style("background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 197, 253, 0.05) 100%);"):
                    # Rectangular icon container clipped to top
                    with ui.element("div").classes(
                        "absolute -top-6 left-1/2 transform -translate-x-1/2 w-20 h-12 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform duration-500"
                    ):
                        # ui.icon("search", size="1.5rem").classes("text-white")
                        # Glow effect
                        with ui.element("div").classes(
                            "absolute inset-0 bg-emerald-400 rounded-md blur-lg opacity-30 group-hover:opacity-50 transition-opacity duration-500"
                        ):
                            pass
                    
                    ui.label("Smart Job Search").classes(
                        "text-2xl font-bold mb-4 mt-8 text-gray-800 group-hover:text-blue-600 transition-colors duration-300"
                    )
                    ui.label(
                        "Advanced filters and AI-powered recommendations to find the perfect job match."
                    ).classes("text-gray-600 text-center leading-relaxed")
                    
                    # Animated background particles
                    with ui.element("div").classes(
                        "absolute top-4 right-4 w-2 h-2 bg-blue-400 rounded-full opacity-40 group-hover:animate-ping"
                    ):
                        pass
                    with ui.element("div").classes(
                        "absolute bottom-8 left-6 w-1 h-1 bg-blue-300 rounded-full opacity-60"
                    ):
                        pass
                
                # Card 2 - Top Companies
                with ui.column().classes(
                    "group relative overflow-hidden bg-white/80 backdrop-blur-sm p-8 rounded-3xl border border-white/20 shadow-2xl hover:shadow-3xl hover:scale-105 transition-all duration-500 flex items-center justify-center text-center"
                ).style("background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(110, 231, 183, 0.05) 100%);"):
                    # Rectangular icon container clipped to top
                    with ui.element("div").classes(
                        "absolute -top-6 left-1/2 transform -translate-x-1/2 w-20 h-12 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform duration-500"
                    ):
                        # ui.icon("business", size="1.5rem").classes("text-white")
                        # Glow effect
                        with ui.element("div").classes(
                            "absolute inset-0 bg-emerald-400 rounded-md blur-lg opacity-30 group-hover:opacity-50 transition-opacity duration-500"
                        ):
                            pass
                    
                    ui.label("Top Companies").classes(
                        "text-2xl font-bold mb-4 mt-8 text-gray-800 group-hover:text-emerald-600 transition-colors duration-300"
                    )
                    ui.label(
                        "Connect with leading companies and startups looking for talented professionals."
                    ).classes("text-gray-600 text-center leading-relaxed")
                    
                    # Animated background particles
                    with ui.element("div").classes(
                        "absolute top-4 right-4 w-2 h-2 bg-emerald-400 rounded-full opacity-40 group-hover:animate-ping"
                    ):
                        pass
                    with ui.element("div").classes(
                        "absolute bottom-8 left-6 w-1 h-1 bg-emerald-300 rounded-full opacity-60"
                    ):
                        pass
                
                # Card 3 - Career Growth
                with ui.column().classes(
                    "group relative overflow-hidden bg-white/80 backdrop-blur-sm p-8 rounded-3xl border border-white/20 shadow-2xl hover:shadow-3xl hover:scale-105 transition-all duration-500 flex items-center justify-center text-center"
                ).style("background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(196, 181, 253, 0.05) 100%);"):
                    # Rectangular icon container clipped to top
                    with ui.element("div").classes(
                        "absolute -top-6 left-1/2 transform -translate-x-1/2 w-20 h-12 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform duration-500"
                    ):
                        # ui.icon("trending_up", size="1.5rem").classes("text-white")
                        # Glow effect
                        with ui.element("div").classes(
                            "absolute inset-0 bg-emerald-400 rounded-md blur-lg opacity-30 group-hover:opacity-50 transition-opacity duration-500"
                        ):
                            pass
                    
                    ui.label("Career Growth").classes(
                        "text-2xl font-bold mb-4 mt-8 text-gray-800 group-hover:text-violet-600 transition-colors duration-300"
                    )
                    ui.label(
                        "Access resources, tips, and opportunities to accelerate your career growth."
                    ).classes("text-gray-600 text-center leading-relaxed")
                    
                    # Animated background particles
                    with ui.element("div").classes(
                        "absolute top-4 right-4 w-2 h-2 bg-violet-400 rounded-full opacity-40 group-hover:animate-ping"
                    ):
                        pass
                    with ui.element("div").classes(
                        "absolute bottom-8 left-6 w-1 h-1 bg-violet-300 rounded-full opacity-60"
                    ):
                        pass

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


@ui.page("/jobs")
def jobs_page():
    # Add CSS to prevent white space below footer
    ui.add_head_html(
        """<style>
        html, body { 
            margin: 0 !important; 
            padding: 0 !important; 
            min-height: 100vh;
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
    </style>"""
    )

    # Page state
    jobs_data = []
    filtered_jobs = []
    current_filters = {"category": "", "job_type": "", "location": "", "search": ""}

    # Load jobs from API
    def load_jobs():
        nonlocal jobs_data, filtered_jobs
        jobs_data = api_service.get_jobs()
        filtered_jobs = jobs_data.copy()
        update_job_display()

    # Filter jobs based on current filters
    def filter_jobs():
        nonlocal filtered_jobs
        filtered_jobs = jobs_data.copy()

        if current_filters["search"]:
            search_term = current_filters["search"].lower()
            filtered_jobs = [
                job
                for job in filtered_jobs
                if search_term in job.get("title", "").lower()
                or search_term in job.get("company", "").lower()
                or search_term in job.get("description", "").lower()
            ]

        if current_filters["category"]:
            filtered_jobs = [
                job
                for job in filtered_jobs
                if job.get("category") == current_filters["category"]
            ]

        if current_filters["job_type"]:
            filtered_jobs = [
                job
                for job in filtered_jobs
                if job.get("job_type") == current_filters["job_type"]
            ]

        if current_filters["location"]:
            location_term = current_filters["location"].lower()
            filtered_jobs = [
                job
                for job in filtered_jobs
                if location_term in job.get("location", "").lower()
            ]

        update_job_display()

    # Create job card component
    def create_job_card(job):
        if not isinstance(job, dict):
            print(f"Skipping invalid job data: {job}")
            return

        with ui.card().classes(
            "w-full h-full flex flex-col hover:shadow-xl transition-shadow"
        ).props("flat bordered"):
            # Flyer image
            flyer_url = job.get("flyer")
            if flyer_url:
                ui.image(flyer_url).classes("w-full h-40 object-cover rounded-t-lg")

            # Job details
            with ui.column().classes("p-4 flex-grow"):
                with ui.column().classes("flex-grow"):
                    ui.label(job.get("title", "Job Title")).classes(
                        "text-lg font-bold text-[#2b3940]"
                    )
                    ui.label(job.get("company", "Company")).classes(
                        "text-sm text-gray-600"
                    )
                    if job.get("salary"):
                        ui.label(job["salary"]).classes(
                            "text-md font-semibold text-[#00b074] mt-2"
                        )

                    ui.separator().classes("my-3")

                    with ui.row().classes(
                        "items-center text-gray-500 text-xs space-x-3"
                    ):
                        ui.label(job.get("job_type", "N/A"))
                        ui.label(job.get("location", "N/A"))

                    description = job.get("description", "No description available.")
                    preview = (
                        (description[:80] + "...")
                        if len(description) > 80
                        else description
                    )
                    ui.label(preview).classes("text-xs text-gray-700 my-3 flex-grow")

            # Action buttons at the bottom
            with ui.card_actions():
                ui.button("View", on_click=lambda j=job: show_job_details(j)).props(
                    "flat dense size=sm"
                )
                ui.button("Apply", color="#00b074").props("unelevated dense size=sm")

    # Update job display
    def update_job_display():
        jobs_container.clear()
        with jobs_container:
            if not filtered_jobs:
                with ui.element("div").classes("text-center py-12"):
                    ui.icon("search_off", size="4rem").classes("text-gray-400 mb-4")
                    ui.label("No jobs found").classes("text-2xl text-gray-600 mb-2")
                    ui.label("Try adjusting your search criteria").classes(
                        "text-gray-500"
                    )
            else:
                ui.label(f"Found {len(filtered_jobs)} jobs").classes(
                    "text-lg font-semibold text-gray-700 mb-6"
                )

                with ui.element("div").classes(
                    "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
                ):
                    for job in filtered_jobs:
                        create_job_card(job)

    create_header()

    # Page Header
    with ui.element("section").classes("bg-[#00b074] text-white py-16"):
        with ui.element("div").classes("container mx-auto px-4 text-center"):
            ui.label("Find Your Perfect Job").classes(
                "text-4xl md:text-5xl font-bold mb-4"
            )
            ui.label("Discover opportunities from top companies worldwide").classes(
                "text-xl opacity-90"
            )

    # Search and Filters Section
    with ui.element("section").classes("bg-gray-100 py-12"):
        with ui.element("div").classes("container mx-auto px-4"):
            with ui.card().classes("p-6 shadow-md"):
                with ui.row().classes(
                    "w-full grid grid-cols-1 md:grid-cols-4 gap-6 items-center"
                ):
                    # Search input
                    search_input = (
                        ui.input(placeholder="Search by keyword...")
                        .props("outlined dense")
                        .classes("w-full col-span-2")
                    )
                    search_input.on(
                        "input",
                        lambda e: (
                            current_filters.update({"search": e.value}),
                            filter_jobs(),
                        ),
                    )

                    # Category filter
                    categories = [
                        "All Categories",
                        "Technology",
                        "Marketing",
                        "Sales",
                        "Design",
                        "Finance",
                        "Operations",
                    ]
                    category_select = (
                        ui.select(categories, value="All Categories")
                        .props("outlined dense")
                        .classes("w-full")
                    )
                    category_select.on(
                        "update:model-value",
                        lambda e: (
                            current_filters.update(
                                {
                                    "category": (
                                        "" if e.value == "All Categories" else e.value
                                    )
                                }
                            ),
                            filter_jobs(),
                        ),
                    )

                    # Job type filter
                    job_types = [
                        "All Types",
                        "Full-time",
                        "Part-time",
                        "Contract",
                        "Freelance",
                        "Internship",
                    ]
                    type_select = (
                        ui.select(job_types, value="All Types")
                        .props("outlined dense")
                        .classes("w-full")
                    )
                    type_select.on(
                        "update:model-value",
                        lambda e: (
                            current_filters.update(
                                {"job_type": "" if e.value == "All Types" else e.value}
                            ),
                            filter_jobs(),
                        ),
                    )

    # Jobs Container
    with ui.element("section").classes("py-12 bg-gray-50 min-h-screen"):
        with ui.element("div").classes("container mx-auto px-4"):
            jobs_container = ui.element("div")

    # Load initial jobs
    load_jobs()


@ui.page("/post-job")
def post_job_page():
    # Add CSS to prevent white space below footer
    ui.add_head_html(
        """<style>
        html, body { 
            margin: 0 !important; 
            padding: 0 !important; 
            min-height: 100vh;
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
    </style>"""
    )

    form_data = {
        "title": "",
        "company": "",
        "location": "",
        "description": "",
        "requirements": "",
        "salary_min": 0.0,
        "salary_max": 0.0,
        "currency": "USD",
        "job_type": "Full-time",
        "category": "Technology",
        "flyer": None,
    }

    def handle_upload(e):
        form_data["flyer_file"] = e.content
        form_data["flyer_name"] = e.name
        form_data["flyer_type"] = e.type
        ui.notify(f"Prepared {e.name} for upload")

    async def submit_job():
        required_fields = ["title", "company", "location", "description"]
        if not all(form_data.get(field) for field in required_fields):
            ui.notify("Please fill out all required fields.", type="negative")
            return

        # Map form data to the format expected by the API
        api_data = {
            "job_title": form_data.get("title"),
            "company": form_data.get("company"),
            "job_description": form_data.get("description"),
            "category": form_data.get("category"),
            "job_type": form_data.get("job_type"),
            "location": form_data.get("location"),
            "min_salary": float(form_data.get("salary_min", 0.0)),
            "max_salary": float(form_data.get("salary_max", 0.0)),
            "benefits": form_data.get("benefits", "Not specified"),  # Add missing field
            "requirements": form_data.get("requirements"),
            "date_posted": "2024-01-01",  # Placeholder, API requires this
            "contact_email": "Not specified",  # Add missing field
        }

        # Get the file object if it exists
        flyer_file = None
        if form_data.get("flyer_file"):

            class FileObject:
                pass

            flyer_file = FileObject()
            flyer_file.name = form_data["flyer_name"]
            flyer_file.content = form_data["flyer_file"]
            flyer_file.content_type = form_data["flyer_type"]

        result = api_service.create_job(api_data, file=flyer_file)
        if result:
            ui.notify("Job posted successfully!", type="positive")
            ui.navigate.to("/jobs")
        else:
            ui.notify(
                "Failed to post job. Please check the data and try again.",
                type="negative",
            )

    # Header
    create_header()

    # Page Header
    with ui.element("section").classes("bg-[#00b074] text-white py-16").style(
        "width: 100vw; margin-left: calc(-50vw + 50%);"
    ):
        with ui.element("div").classes("container mx-auto px-4 text-center"):
            ui.label("Post a New Job").classes("text-4xl md:text-5xl font-bold mb-4")
            ui.label("Fill out the form below to find your next great hire.").classes(
                "text-xl opacity-90"
            )

    # Form Section
    with ui.element("section").classes("py-12 bg-gray-100 min-h-screen w-full"):
        with ui.element("div").classes("flex justify-center px-4"):
            with ui.card().classes("p-8 w-full max-w-4xl"):
                with ui.column().classes("w-full space-y-8"):
                    # Section: Job Details
                    with ui.column().classes("w-full space-y-4"):
                        ui.label("Job Details").classes(
                            "text-2xl font-bold mb-6 text-[#2b3940]"
                        )
                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                        ):
                            ui.input(
                                "Job Title *",
                                on_change=lambda e: form_data.update(
                                    {"title": e.value}
                                ),
                            ).props("outlined dense")
                            ui.input(
                                "Company *",
                                on_change=lambda e: form_data.update(
                                    {"company": e.value}
                                ),
                            ).props("outlined dense")
                            ui.input(
                                "Location *",
                                on_change=lambda e: form_data.update(
                                    {"location": e.value}
                                ),
                            ).props("outlined dense")
                            ui.textarea(
                                "Job Description *",
                                on_change=lambda e: form_data.update(
                                    {"description": e.value}
                                ),
                            ).props("outlined dense")
                            ui.textarea(
                                "Requirements",
                                on_change=lambda e: form_data.update(
                                    {"requirements": e.value}
                                ),
                            ).props("outlined dense")
                            ui.input(
                                "Benefits",
                                on_change=lambda e: form_data.update(
                                    {"benefits": e.value}
                                ),
                            ).props("outlined dense")

                    # Section: Salary & Type
                    with ui.column().classes("w-full space-y-4"):
                        ui.label("Salary & Type").classes(
                            "text-2xl font-bold text-[#2b3940] border-b pb-2"
                        )
                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                        ):
                            ui.input(
                                "Min Salary",
                                on_change=lambda e: form_data.update(
                                    {"salary_min": e.value}
                                ),
                            ).props(
                                "outlined dense type=number prepend-icon=attach_money"
                            )
                            ui.input(
                                "Max Salary",
                                on_change=lambda e: form_data.update(
                                    {"salary_max": e.value}
                                ),
                            ).props("outlined dense type=number")
                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                        ):
                            ui.select(
                                [
                                    "Technology",
                                    "Marketing",
                                    "Sales",
                                    "Design",
                                    "Finance",
                                    "Operations",
                                ],
                                value="Technology",
                                label="Category",
                                on_change=lambda e: form_data.update(
                                    {"category": e.value}
                                ),
                            ).props("outlined dense")
                            ui.select(
                                [
                                    "Full-time",
                                    "Part-time",
                                    "Contract",
                                    "Freelance",
                                    "Internship",
                                ],
                                value="Full-time",
                                label="Job Type",
                                on_change=lambda e: form_data.update(
                                    {"job_type": e.value}
                                ),
                            ).props("outlined dense")

                    # Section: Job Flyer
                    with ui.column().classes("w-full space-y-4"):
                        ui.label("Job Flyer").classes(
                            "text-2xl font-bold text-[#2b3940] border-b pb-2"
                        )
                        ui.upload(on_upload=handle_upload, auto_upload=True).props(
                            "accept=.jpg,.jpeg,.png flat bordered"
                        ).classes("w-full")

                    # Action Buttons
                    with ui.row().classes("w-full justify-end space-x-4 pt-4"):
                        ui.button(
                            "Cancel",
                            on_click=lambda: ui.navigate.back(),
                            color="grey-8",
                        ).props("flat")
                        ui.button(
                            "Post Job", on_click=submit_job, color="#00b074"
                        ).props("unelevated")

    # Footer
    create_footer()


@ui.page("/vendor-dashboard")
def vendor_dashboard_page():
    # Header
    create_header()

    # Main Content with Side Navigation
    with ui.row().classes("w-full h-screen no-wrap"):
        # Left Navigation
        with ui.column().classes("w-1/5 bg-gray-100 p-4 space-y-2 border-r"):
            ui.label("Dashboard").classes("text-xl font-bold p-2 mb-4")
            overview_button = (
                ui.button(
                    "Overview",
                    icon="dashboard",
                    on_click=lambda: show_content("overview"),
                )
                .props("flat dense align=left")
                .classes("w-full text-sm")
            )
            settings_button = (
                ui.button(
                    "Settings",
                    icon="settings",
                    on_click=lambda: show_content("settings"),
                )
                .props("flat dense align=left")
                .classes("w-full text-sm")
            )
            jobs_button = (
                ui.button(
                    "Posted Jobs",
                    icon="work_history",
                    on_click=lambda: show_content("posted_jobs"),
                )
                .props("flat dense align=left")
                .classes("w-full text-sm")
            )
            applicants_button = (
                ui.button(
                    "Applicants",
                    icon="people",
                    on_click=lambda: show_content("applicants"),
                )
                .props("flat dense align=left")
                .classes("w-full text-sm")
            )

        # Right Content Area
        with ui.column().classes("w-4/5 p-8 overflow-y-auto"):
            with ui.row().classes("w-full justify-between items-center mb-6"):
                ui.label("Vendor Dashboard").classes(
                    "text-3xl font-bold text-[#2b3940]"
                )
                ui.button(
                    "Post a New Job",
                    icon="add",
                    on_click=lambda: ui.navigate.to("/post-job"),
                ).props('color="#00b074"')

            # Content Containers
            overview_content = ui.column().classes("w-full")
            settings_content = ui.column().classes("w-full")
            jobs_content = ui.column().classes("w-full")
            applicants_content = ui.column().classes("w-full")
            settings_content.set_visibility(False)
            jobs_content.set_visibility(False)
            applicants_content.set_visibility(False)

            def show_content(section: str):
                overview_content.set_visibility(section == "overview")
                settings_content.set_visibility(section == "settings")
                jobs_content.set_visibility(section == "posted_jobs")
                applicants_content.set_visibility(section == "applicants")
                overview_button.props(
                    'color="#00b074"' if section == "overview" else "color=default"
                )
                settings_button.props(
                    'color="#00b074"' if section == "settings" else "color=default"
                )
                jobs_button.props(
                    'color="#00b074"' if section == "posted_jobs" else "color=default"
                )
                applicants_button.props(
                    'color="#00b074"' if section == "applicants" else "color=default"
                )

            # --- Overview Content ---
            with overview_content:
                overview_container = ui.column().classes("w-full")

                def create_stat_card(icon, value, label, color):
                    with ui.card().classes(f"w-full p-6 border-l-4 {color}"):
                        with ui.row().classes("items-center justify-between"):
                            with ui.column():
                                ui.label(value).classes("text-3xl font-bold")
                                ui.label(label).classes("text-gray-500")
                            ui.icon(icon, size="2.5rem").classes("text-gray-400")

                async def load_overview():
                    overview_container.clear()
                    jobs = api_service.get_jobs()
                    applicants = api_service.get_applicants()

                    with overview_container:
                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
                        ):
                            create_stat_card(
                                "work",
                                f"{len(jobs)}",
                                "Posted Jobs",
                                "border-[#00b074]",
                            )
                            create_stat_card(
                                "people",
                                f"{len(applicants)}",
                                "Total Applicants",
                                "border-[#00b074]",
                            )
                            create_stat_card(
                                "visibility", "16.5K", "Jobs View", "border-[#00b074]"
                            )
                            create_stat_card(
                                "trending_up",
                                "18.6%",
                                "Applied Rate",
                                "border-[#00b074]",
                            )

                        with ui.row().classes(
                            "w-full grid grid-cols-1 lg:grid-cols-2 gap-8"
                        ):
                            with ui.column().classes("w-full"):
                                ui.label("Recent Job Postings").classes(
                                    "text-xl font-bold mb-4"
                                )
                                with ui.card().classes("w-full p-4"):
                                    for job in jobs[:3]:
                                        with ui.row().classes(
                                            "w-full items-center border-b py-2"
                                        ):
                                            ui.label(job["title"]).classes(
                                                "font-semibold w-1/2"
                                            )
                                            ui.label(job["location"]).classes(
                                                "text-gray-500 w-1/2"
                                            )

                            with ui.column().classes("w-full"):
                                ui.label("Recent Applicants").classes(
                                    "text-xl font-bold mb-4"
                                )
                                with ui.card().classes("w-full p-4"):
                                    for app in applicants[:3]:
                                        with ui.row().classes(
                                            "w-full items-center border-b py-3"
                                        ):
                                            with ui.column().classes("space-y-0"):
                                                ui.label(app["name"]).classes(
                                                    "font-semibold"
                                                )
                                                ui.label(app["job_title"]).classes(
                                                    "text-gray-500 text-sm"
                                                )

                overview_button.on("click", load_overview)

            # --- Settings Content ---
            with settings_content:
                with ui.card().classes("w-full p-8"):
                    ui.label("Update Company Profile").classes(
                        "text-2xl font-bold text-[#2b3940] border-b pb-4 mb-6"
                    )

                    # Logo Upload Section
                    with ui.column().classes("w-full items-center mb-8"):
                        with ui.element("div").classes(
                            "w-48 h-48 border-2 border-dashed rounded-lg flex flex-col items-center justify-center text-center p-4"
                        ):
                            ui.label("Browse or Drag and Drop").classes(
                                "text-gray-500 text-sm"
                            )
                            ui.upload(
                                on_upload=lambda e: ui.notify(f"Uploaded {e.name}"),
                                auto_upload=True,
                            ).props(
                                'flat dense text-color="#00b074" label="Upload Logo"'
                            )

                    # Form Fields
                    with ui.column().classes("w-full space-y-6"):
                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                        ):
                            ui.input("Company Name", placeholder="eg. Apple").props(
                                "outlined"
                            )
                            ui.select(
                                ["B2B", "B2C", "Non-profit", "Startup"],
                                label="Corporate Type",
                            ).props("outlined")

                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                        ):
                            ui.select(
                                ["1-10", "10-50", "50-200", "200+"],
                                label="Employee Size",
                            ).props("outlined")
                            ui.input(
                                "Location or (Remote)", placeholder="eg. New York, USA"
                            ).props("outlined")

                        ui.textarea(
                            "About Company",
                            placeholder="Describe about the company what makes it unique",
                        ).props("outlined")
                        ui.input(
                            "Company Website Link",
                            placeholder="https://www.example.com",
                        ).props("outlined")

                        with ui.row().classes("w-full justify-start mt-4"):
                            ui.button("Update Profile", color="#00b074").props(
                                "unelevated"
                            ).classes("min-w-[210px] h-12")

            # --- Posted Jobs Content ---
            with jobs_content:
                ui.label("Your Posted Jobs").classes(
                    "text-2xl font-bold text-[#2b3940] mb-4"
                )
                jobs_container = ui.column().classes("w-full space-y-2")

                def edit_job_dialog(job: dict):
                    with ui.dialog() as edit_dialog, ui.card().classes(
                        "w-full max-w-2xl p-8"
                    ):
                        ui.label("Edit Job").classes("text-xl font-bold mb-4")
                        edit_form_data = job.copy()
                        # Map API fields back to form fields for display
                        edit_form_data["title"] = job.get("job_title", job.get("title"))
                        edit_form_data["description"] = job.get(
                            "job_description", job.get("description")
                        )
                        edit_form_data["salary_min"] = job.get(
                            "min_salary", job.get("salary_min")
                        )
                        edit_form_data["salary_max"] = job.get(
                            "max_salary", job.get("salary_max")
                        )

                        ui.input(
                            "Job Title",
                            value=edit_form_data.get("title"),
                            on_change=lambda e: edit_form_data.update(
                                {"title": e.value}
                            ),
                        ).props("outlined")
                        ui.textarea(
                            "Description",
                            value=edit_form_data.get("description"),
                            on_change=lambda e: edit_form_data.update(
                                {"description": e.value}
                            ),
                        ).props("outlined")
                        ui.input(
                            "Location",
                            value=edit_form_data.get("location"),
                            on_change=lambda e: edit_form_data.update(
                                {"location": e.value}
                            ),
                        ).props("outlined")
                        ui.input(
                            "Min Salary",
                            value=str(edit_form_data.get("salary_min", "")),
                            on_change=lambda e: edit_form_data.update(
                                {"salary_min": e.value}
                            ),
                        ).props("outlined type=number")
                        ui.input(
                            "Max Salary",
                            value=str(edit_form_data.get("salary_max", "")),
                            on_change=lambda e: edit_form_data.update(
                                {"salary_max": e.value}
                            ),
                        ).props("outlined type=number")

                        ui.separator().classes("my-4")
                        ui.label("Update Job Flyer").classes("text-lg font-bold")
                        ui.upload(
                            on_upload=lambda e: edit_form_data.update(
                                {
                                    "flyer_file": e.content,
                                    "flyer_name": e.name,
                                    "flyer_type": e.type,
                                }
                            ),
                            auto_upload=True,
                        ).props('accept=.jpg,.jpeg,.png flat label="Upload New Flyer"')

                        async def save_changes():
                            min_salary = edit_form_data.get("salary_min") or 0.0
                            max_salary = edit_form_data.get("salary_max") or 0.0

                            update_data = {
                                "job_title": edit_form_data.get("title"),
                                "job_description": edit_form_data.get("description"),
                                "location": edit_form_data.get("location"),
                                "min_salary": float(min_salary),
                                "max_salary": float(max_salary),
                                "company": job.get("company"),
                                "category": job.get("category"),
                                "job_type": job.get("job_type"),
                                "benefits": edit_form_data.get(
                                    "benefits", "Not specified"
                                ),
                                "requirements": edit_form_data.get("requirements", ""),
                                "date_posted": job.get("posted_date", "2024-01-01"),
                                "contact_email": edit_form_data.get(
                                    "contact_email", "Not specified"
                                ),
                            }

                            flyer_file = None
                            if edit_form_data.get("flyer_file"):

                                class FileObject:
                                    pass

                                flyer_file = FileObject()
                                flyer_file.name = edit_form_data["flyer_name"]
                                flyer_file.content = edit_form_data["flyer_file"]
                                flyer_file.content_type = edit_form_data["flyer_type"]

                            if api_service.update_job(
                                job["id"], update_data, file=flyer_file
                            ):
                                ui.notify("Job updated successfully!", type="positive")
                                edit_dialog.close()
                                await load_posted_jobs()
                            else:
                                ui.notify("Failed to update job.", type="negative")

                        with ui.row().classes("w-full justify-end mt-4"):
                            ui.button("Cancel", on_click=edit_dialog.close).props(
                                "flat"
                            )
                            ui.button(
                                "Save Changes", on_click=save_changes, color="#00b074"
                            )
                    edit_dialog.open()

                async def delete_job(job_id: str):
                    async def confirm_delete():
                        dialog.close()
                        if api_service.delete_job(job_id):
                            ui.notify("Job deleted successfully.", type="positive")
                            await load_posted_jobs()
                        else:
                            ui.notify("Failed to delete job.", type="negative")

                    with ui.dialog() as dialog, ui.card():
                        ui.label(f"Are you sure you want to delete this job?")
                        with ui.row().classes("w-full justify-end"):
                            ui.button("Cancel", on_click=dialog.close).props("flat")
                            ui.button(
                                "Delete", on_click=confirm_delete, color="negative"
                            )
                    await dialog

                def create_job_row(job: dict, applicant_count: int):
                    with ui.card().classes("w-full p-4"):
                        with ui.row().classes("w-full items-center no-wrap"):
                            ui.label(job.get("title", "N/A")).classes(
                                "font-bold w-4/12"
                            )
                            ui.label(job.get("company", "N/A")).classes("w-2/12")
                            ui.label(job.get("location", "N/A")).classes("w-2/12")
                            ui.label(f"{applicant_count} Applicants").classes("w-2/12")
                            with ui.row().classes(
                                "justify-end w-2/12 space-x-2 no-wrap"
                            ):
                                ui.button(
                                    "Edit",
                                    on_click=lambda j=job: edit_job_dialog(j),
                                    color="#00b074",
                                ).props("flat dense")
                                ui.button(
                                    "Delete",
                                    on_click=lambda j=job: delete_job(j.get("id")),
                                    color="red",
                                ).props("flat dense")

                async def load_posted_jobs():
                    jobs_container.clear()
                    jobs = api_service.get_jobs()
                    applicants = api_service.get_applicants()

                    applicant_counts = {}
                    for app in applicants:
                        job_id = app.get("job_id")
                        if job_id:
                            applicant_counts[job_id] = (
                                applicant_counts.get(job_id, 0) + 1
                            )

                    if not jobs:
                        with jobs_container:
                            ui.label("No jobs posted yet.").classes("text-gray-500")
                        return

                    with jobs_container:
                        with ui.row().classes(
                            "w-full font-bold text-gray-500 px-4 items-center no-wrap"
                        ):
                            ui.label("Job Title").classes("w-4/12")
                            ui.label("Company").classes("w-2/12")
                            ui.label("Location").classes("w-2/12")
                            ui.label("Applicants").classes("w-2/12")
                            ui.label("Actions").classes("w-2/12 text-right")
                        for job in jobs:
                            count = applicant_counts.get(job.get("id"), 0)
                            create_job_row(job, count)

                jobs_button.on("click", load_posted_jobs)

            # --- Applicants Content ---
            with applicants_content:
                applicant_list_container = ui.column().classes("w-full")

                def create_applicant_row(applicant: dict):
                    with ui.row().classes("w-full items-center border-b py-4 no-wrap"):
                        with ui.row().classes("w-3/12 items-center no-wrap"):
                            ui.avatar(f"{applicant['avatar']}", size="md").classes(
                                "mr-4"
                            )
                            ui.label(applicant["name"]).classes("font-semibold")
                        ui.label(applicant["job_title"]).classes("w-3/12")
                        ui.label(applicant["applied_on"]).classes("w-2/12")
                        with ui.row().classes("w-4/12 justify-end space-x-2 no-wrap"):
                            ui.button(
                                "View",
                                on_click=lambda: ui.notify("View not implemented"),
                            ).props("flat dense")
                            ui.button(
                                "Contact",
                                on_click=lambda: ui.notify("Contact not implemented"),
                                color="#00b074",
                            ).props("flat dense")
                            ui.button(
                                "Reject",
                                on_click=lambda: ui.notify("Reject not implemented"),
                                color="red",
                            ).props("flat dense")

                async def load_applicants(filter_by: Optional[str] = None):
                    applicant_list_container.clear()
                    filters = {"job_title": filter_by} if filter_by else {}
                    applicants = api_service.get_applicants(filters=filters)

                    with applicant_list_container:
                        with ui.row().classes("w-full items-center mb-6"):
                            with ui.column().classes("w-1/2"):
                                ui.label(
                                    f"Applicants List ({len(applicants)})"
                                ).classes("text-2xl font-bold")
                            with ui.column().classes("w-1/2"):
                                with ui.row().classes(
                                    "justify-end w-full items-center"
                                ):
                                    ui.label("Filter by Job:").classes("mr-2")
                                    job_titles = list(
                                        set(
                                            app["job_title"]
                                            for app in api_service.get_applicants()
                                        )
                                    )
                                    ui.select(
                                        job_titles,
                                        label="All Jobs",
                                        on_change=lambda e: load_applicants(e.value),
                                    ).classes("min-w-[200px]")

                        # Table Header
                        with ui.row().classes(
                            "w-full font-bold text-gray-500 border-b pb-2 no-wrap"
                        ):
                            ui.label("Name").classes("w-3/12")
                            ui.label("Applied as").classes("w-3/12")
                            ui.label("Applied on").classes("w-2/12")
                            ui.label("Actions").classes("w-4/12 text-right")

                        # Applicant Rows
                        if not applicants:
                            ui.label("No applicants found.").classes(
                                "text-gray-500 p-4"
                            )
                        else:
                            for applicant in applicants:
                                create_applicant_row(applicant)

                        # Pagination (Placeholder)
                        with ui.row().classes("w-full justify-center mt-8"):
                            with ui.pagination(
                                min=1,
                                max=5,
                                direction_links=True,
                                on_change=lambda e: ui.notify(f"Page {e.value}"),
                            ) as pagination:
                                pass

                applicants_button.on("click", lambda: load_applicants())

            # Set initial view
            show_content("overview")
            ui.timer(0.1, load_overview, once=True)


if __name__ in {"__main__", "__mp_main__"}:
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    ui.run(title="JobBoard", port=8080)


if __name__ in {"__main__", "__mp_main__"}:
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    ui.run(title="JobBoard", port=8080)


if __name__ in {"__main__", "__mp_main__"}:
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    ui.run(title="JobBoard", port=8080)
