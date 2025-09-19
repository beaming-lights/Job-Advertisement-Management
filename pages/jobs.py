from nicegui import ui
from components.header import create_header
from components.footer import create_footer
from services.api_service import APIService
import base64

@ui.page("/jobs")
def jobs_page():
    """Jobs listing page with search and filtering"""
    # Add CSS overrides
    ui.add_head_html(
        """
    <style>
    /* Your CSS overrides here */
    body {
        overflow-x: hidden !important;
    }
    .nicegui-content,
    .nicegui-column {
        display: block !important;
        flex-direction: unset !important;
        align-items: unset !important;
        gap: 0 !important;
        padding: 0 !important;
    }
    /* Fix for full-width sections */
    section[style*="100vw"] {
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw !important;
        margin-right: -50vw !important;
        width: 100vw !important;
        max-width: none !important;
    }
    </style>
    """
    )
    
    # Header
    create_header()
    
    api_service = APIService()
    
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

    # Show job details modal
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
                            with ui.column().classes("flex-1"):
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

                    # Benefits
                    if job.get("benefits"):
                        with ui.element("div").classes("bg-white rounded-lg border p-4"):
                            with ui.row().classes("items-center space-x-2 mb-3"):
                                ui.label("Benefits").classes("text-lg font-bold text-gray-900")
                            
                            ui.label(job.get("benefits")).classes(
                                "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                            )

                    # Skills
                    if job.get("skills"):
                        with ui.element("div").classes("bg-white rounded-lg border p-4"):
                            with ui.row().classes("items-center space-x-2 mb-3"):
                                ui.label("Skills").classes("text-lg font-bold text-gray-900")
                            
                            # Display skills as tags if it's a list, otherwise as text
                            skills = job.get("skills", [])
                            if isinstance(skills, list):
                                with ui.row().classes("flex-wrap gap-2"):
                                    for skill in skills:
                                        ui.label(skill).classes(
                                            "px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-medium"
                                        )
                            else:
                                ui.label(skills).classes(
                                    "text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"
                                )

            # Compact Action Bar
            with ui.element("div").classes("bg-gray-50 border-t border-gray-200 p-4"):
                with ui.row().classes("w-full justify-end items-center"):
                    # Primary Action
                    ui.button(
                        "Apply Now",
                        color="#00b074"
                    ).classes(
                        "px-6 py-2 rounded-lg font-semibold text-white"
                    ).props("unelevated")
        
        dialog.open()

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
                ).style("color: #00b074 !important;")
                ui.button("Apply", color="#00b074").props("unelevated dense size=sm").style("color: white !important;")

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
    
    # Footer
    create_footer()
