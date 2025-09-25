"""
Home Page - Main landing page for the JobBoard website
"""

from nicegui import ui
from services.api_service import APIService
from components.job_details_modal import show_job_details


def home_page():
    """Main page content for the JobBoard website."""

    # Initialize API service
    api_service = APIService()

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

    # Features Section
    with ui.element("section").classes("py-20 bg-gray-50 card-section"):
        with ui.element("div").classes("container mx-auto px-4"):
            ui.label("Why Choose JobBoard?").classes(
                "text-4xl font-bold text-center text-[#2b3940] mb-16"
            )
            with ui.row().classes(
                "grid grid-cols-1 md:grid-cols-3 gap-8 relative card-container"
            ):
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
                            ui.icon("trending_up", size="2rem").classes(
                                "text-green-600"
                            )

                        ui.label("Career Growth").classes(
                            "text-xl font-bold text-gray-900 mb-3"
                        )
                        ui.label(
                            "Access resources, tips, and opportunities to accelerate your career growth."
                        ).classes("text-gray-600 text-sm leading-relaxed")

    # Stats Section - Modern Gradient Design
    with ui.element("section").classes(
        "py-24 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden"
    ).style("width: 100vw; margin-left: calc(-50vw + 50%);"):
        # Background decoration
        with ui.element("div").classes("absolute inset-0 opacity-10"):
            with ui.element("div").classes(
                "absolute top-20 left-10 w-72 h-72 bg-emerald-500 rounded-full blur-3xl"
            ):
                pass
            with ui.element("div").classes(
                "absolute bottom-20 right-10 w-96 h-96 bg-blue-500 rounded-full blur-3xl"
            ):
                pass

        with ui.element("div").classes("container mx-auto px-4 relative z-10"):
            ui.label("Platform Statistics").classes(
                "text-5xl font-bold text-center text-white mb-4"
            )
            ui.label("Trusted by thousands of professionals worldwide").classes(
                "text-xl text-center text-gray-300 mb-16"
            )

            with ui.row().classes(
                "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
            ):
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
    with ui.element("section").classes(
        "py-24 bg-gradient-to-b from-white to-gray-50 relative"
    ):
        # Background decoration
        with ui.element("div").classes("absolute inset-0 overflow-hidden"):
            with ui.element("div").classes(
                "absolute -top-40 -right-40 w-80 h-80 bg-emerald-100 rounded-full opacity-30"
            ):
                pass
            with ui.element("div").classes(
                "absolute -bottom-40 -left-40 w-96 h-96 bg-blue-100 rounded-full opacity-20"
            ):
                pass

        with ui.element("div").classes("container mx-auto px-4 relative z-10"):
            # Section Title
            with ui.element("div").classes("text-center mb-16"):
                ui.label("Featured Jobs").classes(
                    "text-5xl font-bold text-gray-900 mb-6"
                )
                ui.label(
                    "Discover hand-picked positions from leading companies"
                ).classes("text-xl text-gray-600 max-w-2xl mx-auto")

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
                            with ui.element("div").classes(
                                "flex items-center gap-3 mb-4"
                            ):
                                with ui.element("div").classes(
                                    "flex items-center gap-1"
                                ):
                                    ui.icon("location_on", size="1rem").classes(
                                        "text-gray-400"
                                    )
                                    ui.label(job.get("location", "N/A")).classes(
                                        "text-xs text-gray-500"
                                    )
                                with ui.element("div").classes(
                                    "flex items-center gap-1"
                                ):
                                    ui.icon("schedule", size="1rem").classes(
                                        "text-gray-400"
                                    )
                                    ui.label(job.get("job_type", "N/A")).classes(
                                        "text-xs text-gray-500"
                                    )

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
                                color="#00b074",
                            ).classes(
                                "w-full py-2 rounded-lg font-medium transition-all duration-300 text-white text-sm"
                            ).props(
                                "unelevated"
                            )

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
                    color="#00b074",
                ).classes(
                    "px-8 py-4 rounded-xl font-semibold transition-all duration-300"
                ).props(
                    "outline"
                )

    # CTA Section - Modern Gradient Design
    with ui.element("section").classes(
        "py-32 bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white relative overflow-hidden"
    ).style("width: 100vw; margin-left: calc(-50vw + 50%);"):
        # Animated background elements
        with ui.element("div").classes("absolute inset-0"):
            with ui.element("div").classes(
                "absolute top-20 left-20 w-64 h-64 bg-emerald-500 rounded-full opacity-10 blur-3xl animate-pulse"
            ):
                pass
            with ui.element("div").classes(
                "absolute bottom-20 right-20 w-80 h-80 bg-blue-500 rounded-full opacity-10 blur-3xl animate-pulse"
            ):
                pass
            with ui.element("div").classes(
                "absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-500 rounded-full opacity-5 blur-3xl"
            ):
                pass

        with ui.element("div").classes(
            "container mx-auto px-4 text-center relative z-10"
        ):
            # Main CTA content
            with ui.element("div").classes("max-w-4xl mx-auto"):
                ui.label("Transform Your Career Today").classes(
                    "text-6xl font-bold mb-6 bg-gradient-to-r from-white via-gray-100 to-emerald-100 bg-clip-text text-transparent"
                )
                ui.label(
                    "Join over 50,000 professionals who discovered their dream careers through our platform. Your next opportunity is just one click away."
                ).classes(
                    "text-2xl mb-12 text-gray-300 leading-relaxed max-w-3xl mx-auto"
                )

                # Action buttons with modern styling
                with ui.element("div").classes(
                    "flex flex-col sm:flex-row gap-6 justify-center items-center"
                ):
                    ui.button(
                        "Signup Today",
                        on_click=lambda: ui.navigate.to("/signup"),
                        color="#00b074",
                    ).classes(
                        "group relative text-white px-8 py-3 text-lg font-semibold rounded-xl transform hover:scale-105 transition-all duration-300 shadow-lg"
                    ).props(
                        "unelevated"
                    )

                    ui.button(
                        "Browse Jobs", on_click=lambda: ui.navigate.to("/jobs")
                    ).classes(
                        "group relative bg-transparent border-2 border-white/30 text-white px-8 py-3 text-lg font-semibold rounded-xl hover:bg-white/10 hover:border-white/50 backdrop-blur-sm transition-all duration-300"
                    )

                # Trust indicators
                with ui.element("div").classes("mt-16 pt-12 border-t border-white/10"):
                    ui.label("Trusted by leading companies worldwide").classes(
                        "text-lg text-gray-400 mb-8"
                    )
                    with ui.element("div").classes(
                        "flex justify-center items-center gap-12 opacity-60"
                    ):
                        # Company logos placeholder (you can replace with actual logos)
                        for company in [
                            "Google",
                            "Microsoft",
                            "Apple",
                            "Amazon",
                            "Meta",
                        ]:
                            with ui.element("div").classes(
                                "text-2xl font-bold text-white/40 hover:text-white/60 transition-colors duration-300"
                            ):
                                ui.label(company)
