from nicegui import ui
from services.api_service import APIService
from services.auth_service import auth_service
from components.header import create_header
from components.footer import create_footer


@ui.page("/post-job")
def post_job_page():
    """Create the job posting form for vendors"""
    
    # Check if user is authenticated and is a vendor
    if not auth_service.require_vendor("/login"):
        return
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
    /* Green styling for upload component */
    .q-uploader {
        border-color: #00b074 !important;
    }
    .q-uploader__header {
        background-color: #00b074 !important;
    }
    .q-uploader__dnd {
        border-color: #00b074 !important;
    }
    .q-uploader__dnd:hover {
        background-color: rgba(0, 176, 116, 0.1) !important;
    }
    </style>
    """
    )

    # Header
    create_header()

    api_service = APIService()

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
            "min_salary": str(int(form_data.get("salary_min", 0))),
            "max_salary": str(int(form_data.get("salary_max", 0))),
            "benefits": form_data.get("benefits", "Competitive benefits package"),
            "requirements": form_data.get("requirements", "Requirements will be discussed during interview"),
            "date_posted": "2024-01-15",
            "contact_email": "hr@company.com",
            "vendor_id": "vendor_1"
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
                        ).props("unelevated").style("color: white !important;")

    # Tips Section
    with ui.element("section").classes("py-12 bg-white"):
        with ui.element("div").classes("container mx-auto px-4 max-w-4xl"):
            ui.label("Tips for a Great Job Posting").classes(
                "text-2xl font-bold mb-6 text-gray-800"
            )

            with ui.row().classes("grid grid-cols-1 md:grid-cols-2 gap-8"):
                with ui.column().classes("space-y-4"):
                    with ui.row().classes("items-start space-x-3"):
                       
                        with ui.column():
                            ui.label("Be Specific").classes(
                                "font-semibold text-gray-800"
                            )
                            ui.label(
                                "Include specific skills, experience level, and responsibilities"
                            ).classes("text-gray-600 text-sm")

                    with ui.row().classes("items-start space-x-3"):
                      
                        with ui.column():
                            ui.label("Highlight Benefits").classes(
                                "font-semibold text-gray-800"
                            )
                            ui.label(
                                "Mention salary range, benefits, and growth opportunities"
                            ).classes("text-gray-600 text-sm")

                with ui.column().classes("space-y-4"):
                    with ui.row().classes("items-start space-x-3"):
                      
                        with ui.column():
                            ui.label("Company Culture").classes(
                                "font-semibold text-gray-800"
                            )
                            ui.label(
                                "Describe your work environment and team culture"
                            ).classes("text-gray-600 text-sm")

                    with ui.row().classes("items-start space-x-3"):
                      
                        with ui.column():
                            ui.label("Clear Timeline").classes(
                                "font-semibold text-gray-800"
                            )
                            ui.label(
                                "Specify start date and application deadline"
                            ).classes("text-gray-600 text-sm")

    # Footer
    create_footer()
