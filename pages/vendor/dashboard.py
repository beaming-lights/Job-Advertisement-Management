"""Vendor Dashboard - Enhanced Modern Interface"""

from nicegui import ui
from services.api_service import APIService
from services.auth_service import auth_service
from components.header import create_header
from components.footer import create_footer
from typing import Optional
import json
from datetime import datetime
from components.sidebar import show_sidebar

show_sidebar()


def show_applications_summary():
    """Show a summary of applications for the vendor's jobs"""
    try:
        api_service = APIService()
        current_user = auth_service.get_current_user()

        # Get applications for vendor's jobs
        applications = api_service.get_applicants_by_vendor(current_user.get("id"))

        if applications:
            ui.notify(
                f"You have {len(applications)} total applications across all your jobs",
                type="positive",
            )
        else:
            ui.notify("No applications found for your jobs yet", type="info")

    except Exception as e:
        ui.notify(f"Unable to load applications: {str(e)}", type="warning")


def export_dashboard_data():
    """Export dashboard data as JSON"""
    try:
        api_service = APIService()
        current_user = auth_service.get_current_user()

        # Gather all dashboard data
        vendor_jobs = api_service.get_jobs_by_vendor(current_user.get("id"))
        applications = api_service.get_applicants_by_vendor(current_user.get("id"))

        export_data = {
            "export_date": datetime.now().isoformat(),
            "vendor_id": current_user.get("id"),
            "vendor_name": current_user.get("name"),
            "summary": {
                "total_jobs": len(vendor_jobs),
                "total_applications": len(applications),
                "active_jobs": len(
                    [job for job in vendor_jobs if job.get("status") == "active"]
                ),
            },
            "jobs": vendor_jobs,
            "applications": applications,
        }

        # Create download (simplified notification for now)
        ui.notify(
            "Dashboard data exported successfully! (Feature in development)",
            type="positive",
        )

    except Exception as e:
        ui.notify(f"Export failed: {str(e)}", type="negative")


@ui.page("/vendor-dashboard")
def vendor_dashboard_page():
    """Vendor Dashboard - Protected route for vendors only"""

    # Check authentication and role
    if not auth_service.require_vendor("/login"):
        return

    # Add page title for browser tab
    ui.add_head_html("<title>Vendor Dashboard - JobBoard</title>")

    # Add enhanced dashboard CSS with full-width layout
    ui.add_head_html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Prevent horizontal scrolling */
        html, body {
            overflow-x: hidden !important;
            max-width: 100vw !important;
            background-color: #f1f5f9 !important;
            font-family: 'Inter', sans-serif;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* NiceGUI Content Override - Force full width layout */
        .nicegui-content,
        .nicegui-column {
            display: block !important;
            flex-direction: unset !important;
            align-items: unset !important;
            gap: 0 !important;
            padding: 0 !important;
            overflow-x: hidden !important;
            max-width: 100vw !important;
        }

        /* Override page container constraints */
        .q-page-container, .q-layout, .q-page {
            padding: 0 !important;
            margin: 0 !important;
            width: 100vw !important;
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }

        /* Ensure all containers don't exceed viewport width */
        * {
            box-sizing: border-box !important;
        }

        /* Flat Modern Dashboard Design */
        .flat-header {
            background: white;
            border-bottom: 1px solid #e5e7eb;
        }

        .flat-sidebar {
            background: #f9fafb;
            border-right: 1px solid #e5e7eb;
        }

        .flat-nav-item {
            color: #374151;
            transition: all 0.2s ease;
            border-radius: 6px;
            margin: 4px 0;
            font-weight: 500;
        }

        .flat-nav-item:hover {
            background: #00b074;
            color: white;
        }

        .flat-nav-item.active {
            background: #2b3940;
            color: white;
        }

        .flat-content {
            background: transparent; /* No card around the main content area */
        }

        .flat-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .flat-stat-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .flat-stat-icon {
            width: 48px;
            height: 48px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        /* Consistent Flat Button Theme */
        .flat-btn {
            border-radius: 6px;
            font-weight: 500;
            padding: 0.6rem 1.2rem;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
        }

        .flat-btn-primary {
            background: #00b074;
            color: white;
        }

        .flat-btn-primary:hover {
            background: #059669;
        }

        .flat-btn-secondary {
            background: #e5e7eb;
            color: #374151;
        }

        .flat-btn-secondary:hover {
            background: #d1d5db;
        }

        .flat-btn-outline {
            background: transparent;
            color: #00b074;
            border: 1px solid #00b074;
        }

        .flat-btn-outline:hover {
            background: #f0fdf4;
        }

        .flat-btn-danger {
            background: transparent;
            color: #ef4444;
            border: 1px solid #ef4444;
        }

        .flat-btn-danger:hover {
            background: #fee2e2;
        }

        /* Typography */
        .flat-title {
            color: #2b3940;
            font-weight: 700;
            font-size: 1.75rem;
        }

        .flat-subtitle {
            color: #6b7280;
            font-size: 1rem;
        }

        .flat-section-title {
            color: #2b3940;
            font-weight: 600;
            font-size: 1.25rem;
            margin-bottom: 1.5rem;
        }

        /* Status Badge */
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .status-active { background-color: #dcfce7; color: #166534; }
        .status-inactive { background-color: #fef3c7; color: #92400e; }

        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            border-color: #00b074;
        }

        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .stat-icon.green { background: #00b074; }
        .stat-icon.blue { background: #3b82f6; }
        .stat-icon.purple { background: #8b5cf6; }
        .stat-icon.yellow { background: #f59e0b; }

        .stat-info .value {
            font-size: 1.75rem;
            font-weight: 600;
            color: #2b3940;
        }

        .stat-info .label {
            font-size: 0.875rem;
            color: #6b7280;
        }

        /* Content Section */
        .content-section {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2rem;
        }

        .content-card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            border: 1px solid #e5e7eb;
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #2b3940;
            margin-bottom: 1.5rem;
        }

        /* Job List */
        .job-list {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            overflow: hidden;
        }

        .job-item-row {
            border-bottom: 1px solid #f3f4f6;
            transition: all 0.2s ease;
        }

        .job-item-row:last-child {
            border-bottom: none;
        }

        .job-item-row:hover {
            background-color: #f9fafb;
        }

        .job-title {
            font-weight: 500;
            color: #2b3940;
        }

        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .status-active { background-color: #dcfce7; color: #166534; }
        .status-paused { background-color: #fef3c7; color: #92400e; }

        /* Buttons */
        .btn-primary {
            background-color: #00b074;
            color: white;
            border: none;
            padding: 0.625rem 1.25rem;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .btn-primary:hover { background-color: #009d66; }

        </style>
    """
    )

    # Add header
    create_header()

    # Initialize API service
    api_service = APIService()
    current_user = auth_service.get_current_user()

    # Page Title Section with Classic Modern Design
    with ui.element("div").classes("w-full py-10 relative").style(
        "background: linear-gradient(135deg, #00b074 0%, #059669 100%); margin-top: 4rem;"
    ):
        # Add subtle modern styling
        ui.add_head_html(
            """
        <style>
        .classic-modern-bg {
            background-image: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 50%);
        }
        .classic-modern-title {
            color: #ffffff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            letter-spacing: -0.02em;
        }
        .classic-modern-subtitle {
            color: rgba(255,255,255,0.95);
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .classic-modern-icon {
            color: #ffffff;
            filter: drop-shadow(0 2px 8px rgba(0,0,0,0.2));
        }
        .classic-modern-divider {
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        }
        .perfect-center {
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        </style>
        """
        )

        with ui.element("div").classes(
            "container mx-auto px-8 text-center classic-modern-bg perfect-center w-full"
        ):
            with ui.row().classes("items-center justify-center w-full"):
                # Subtle divider line - perfectly centered
                with ui.element("div").classes("flex justify-center mt-6 w-full"):
                    with ui.element("div").classes(
                        "h-px w-32 classic-modern-divider mx-auto"
                    ):
                        pass

                # Title block with welcome text underneath - all centered
                with ui.column().classes(
                    "items-center justify-center space-y-2 mb-4 w-full"
                ):
                    # Main title - centered
                    ui.label("Vendor Dashboard").classes(
                        "text-4xl md:text-5xl font-bold classic-modern-title text-center"
                    )

                    # Welcome text directly under title - centered
                    welcome_text = f"Welcome back, {current_user.get('name', 'Vendor')}"
                    ui.label(welcome_text).classes(
                        "text-xl md:text-2xl font-medium classic-modern-subtitle text-center"
                    )

    # # Flat Modern Header
    # with ui.element("div").classes("flat-header w-full py-4 px-8"):
    #     with ui.row().classes("items-center justify-between w-full"):
    #         with ui.row().classes("items-center gap-4"):
    #             ui.icon("dashboard", size="2rem").classes("text-[#00b074]")
    #             ui.label("Quick Actions").classes("flat-title")

    with ui.element("div").classes("flex justify-center mt-6 w-full"):
        with ui.element("div").classes("h-px w-32 classic-modern-divider mx-auto"):
            pass

    # with ui.row().classes("items-center space-x-4"):
    #     ui.button(
    #         "Post New Job",
    #         color="#2b3940",
    #         on_click=lambda: ui.navigate.to("/post-job"),
    #     ).classes("flat-btn flat-btn-primary").style("color:#ffffff !important")
        # ui.button("Refresh", icon="refresh",color="#00b074", on_click=lambda: ui.navigate.reload()).classes("flat-btn flat-btn-secondary !important")

    # Main Content Container with proper spacing
    with ui.element("div").classes("container mx-auto px-8 py-6"):
        # Main Content with Side Navigation
        with ui.row().classes("w-full min-h-screen no-wrap gap-6"):
            # Flat Modern Sidebar
            with ui.column().classes("flat-sidebar w-1/4 p-3 rounded-lg"):
                # Sidebar Header
                with ui.element("div").classes("pb-3 border-b border-gray-200 mb-3"):
                    ui.label("Navigation").classes(
                        "text-lg font-semibold text-[#2b3940] mb-1"
                    )
                    ui.label(f"{current_user.get('name', 'Vendor')}").classes(
                        "text-sm text-gray-500"
                    )

                # Track current section
                current_section = {"value": "overview"}

                # Navigation Menu
                with ui.column().classes("space-y-1"):
                    overview_button = (
                        ui.button(
                            "Overview",
                            icon="dashboard",
                            on_click=lambda: show_content("overview"),
                        )
                        .props("flat dense align=left")
                        .classes("flat-nav-item w-full text-sm py-2 px-3")
                    )

                    jobs_button = (
                        ui.button(
                            "Manage Jobs",
                            icon="work_history",
                            on_click=lambda: show_content("posted_jobs"),
                        )
                        .props("flat dense align=left")
                        .classes("flat-nav-item w-full text-sm py-2 px-3")
                    )

                    applicants_button = (
                        ui.button(
                            "Applicants",
                            icon="people",
                            on_click=lambda: show_content("applicants"),
                        )
                        .props("flat dense align=left")
                        .classes("flat-nav-item w-full text-sm py-2 px-3")
                    )

                    settings_button = (
                        ui.button(
                            "Settings",
                            icon="settings",
                            on_click=lambda: show_content("settings"),
                        )
                        .props("flat dense align=left")
                        .classes("flat-nav-item w-full text-sm py-2 px-3")
                    )

                # Separator
                with ui.element("div").classes("my-4 h-px bg-gray-200"):
                    pass

                # Action Buttons
                with ui.column().classes("space-y-2"):
                    ui.button(
                        "Logout",
                        on_click=lambda: auth_service.logout()
                        or ui.navigate.to("/login"),
                        color="#00b074",
                    ).props("unelevated").style("color: white !important;").classes(
                        "w-full"
                    )

            # Flat Modern Content Area
            with ui.column().classes("flat-content w-3/4 p-4 overflow-y-auto"):
                with ui.row().classes("w-full justify-between items-center mb-4"):
                    # ui.label("Dashboard Overview").classes("flat-title")

                # Main content container that will be dynamically updated
                    main_content_container = ui.column().classes("w-full")

                def update_button_styles(active_section: str):
                    """Update button styles based on active section"""
                    overview_button.props(
                        'color="#00b074"'
                        if active_section == "overview"
                        else "color=default"
                    )
                    jobs_button.props(
                        'color="#00b074"'
                        if active_section == "posted_jobs"
                        else "color=default"
                    )
                    applicants_button.props(
                        'color="#00b074"'
                        if active_section == "applicants"
                        else "color=default"
                    )
                    settings_button.props(
                        'color="#00b074"'
                        if active_section == "settings"
                        else "color=default"
                    )

                def show_content(section: str):
                    """Clear and show only the selected section content"""
                    current_section["value"] = section
                    main_content_container.clear()
                    update_button_styles(section)

                    if section == "overview":
                        load_overview_content()
                    elif section == "posted_jobs":
                        load_posted_jobs_content()
                    elif section == "applicants":
                        load_applicants_content()
                    elif section == "settings":
                        load_settings_content()

                def create_stat_card(icon, value, label, color):
                    """Helper function to create flat modern stat cards"""
                    with ui.element("div").classes("flat-stat-card"):
                        with ui.element("div").classes(f"flat-stat-icon").style(
                            f"background-color: {color}"
                        ):
                            ui.icon(icon, size="1.5rem")
                        with ui.column().classes("space-y-0"):
                            ui.label(value).classes("text-2xl font-bold text-[#2b3940]")
                            ui.label(label).classes("text-sm text-gray-500")

                def load_overview_content():
                    """Load overview section content with API data"""
                    with main_content_container:
                        # Fetch real data from API
                        try:
                            vendor_jobs = api_service.get_jobs_by_vendor(
                                current_user.get("id")
                            )
                            applicants = api_service.get_applicants()
                            total_jobs = len(vendor_jobs)
                            total_applications = sum(
                                job.get("application_count", 0) for job in vendor_jobs
                            )
                            total_views = sum(
                                job.get("view_count", 0) for job in vendor_jobs
                            )
                            success_rate = (
                                round((total_applications / max(total_views, 1)) * 100)
                                if total_views > 0
                                else 0
                            )
                        except Exception as e:
                            print(f"Error loading overview data: {e}")
                            vendor_jobs = []
                            applicants = []
                            total_jobs = 0
                            total_applications = 0
                            total_views = 0
                            success_rate = 0

                        # Flat Modern Stats cards
                        with ui.row().classes(
                            "w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
                        ):
                            create_stat_card(
                                "work", f"{total_jobs}", "Posted Jobs", "#00b074"
                            )
                            create_stat_card(
                                "people",
                                f"{total_applications}",
                                "Applications",
                                "#2b3940",
                            )
                            create_stat_card(
                                "visibility",
                                f"{total_views:,}",
                                "Jobs Views",
                                "#00b074",
                            )
                            create_stat_card(
                                "trending_up",
                                f"{success_rate}%",
                                "Success Rate",
                                "#2b3940",
                            )

                        # Flat Modern Recent Data Section
                        with ui.row().classes(
                            "w-full grid grid-cols-1 lg:grid-cols-2 gap-6"
                        ):
                            with ui.column().classes("w-full"):
                                ui.label("Recent Job Postings").classes(
                                    "flat-section-title"
                                )
                                with ui.element("div").classes("flat-card"):
                                    if vendor_jobs:
                                        for job in vendor_jobs[:3]:
                                            with ui.row().classes(
                                                "w-full items-center justify-between border-b border-gray-100 py-3 last:border-b-0"
                                            ):
                                                with ui.column().classes("space-y-1"):
                                                    ui.label(
                                                        job.get("title", "Unknown")
                                                    ).classes(
                                                        "font-medium text-[#2b3940]"
                                                    )
                                                    ui.label(
                                                        job.get("location", "N/A")
                                                    ).classes("text-sm text-gray-500")
                                                with ui.element("span").classes(
                                                    "status-badge status-active"
                                                ):
                                                    ui.label("Active")
                                    else:
                                        with ui.column().classes(
                                            "items-center text-center py-8"
                                        ):
                                            ui.icon("work_off", size="2.5rem").classes(
                                                "text-gray-300 mb-2"
                                            )
                                            ui.label("No jobs posted yet").classes(
                                                "text-gray-500"
                                            )

                            with ui.column().classes("w-full"):
                                ui.label("Recent Applicants").classes(
                                    "flat-section-title"
                                )
                                with ui.element("div").classes("flat-card"):
                                    if applicants:
                                        for app in applicants[:3]:
                                            with ui.row().classes(
                                                "w-full items-center justify-between border-b border-gray-100 py-3 last:border-b-0"
                                            ):
                                                with ui.column().classes("space-y-1"):
                                                    ui.label(
                                                        app.get("name", "Unknown")
                                                    ).classes(
                                                        "font-medium text-[#2b3940]"
                                                    )
                                                    ui.label(
                                                        app.get("job_title", "N/A")
                                                    ).classes("text-sm text-gray-500")
                                                ui.icon(
                                                    "person", size="1.5rem"
                                                ).classes("text-[#00b074]")
                                    else:
                                        with ui.column().classes(
                                            "items-center text-center py-8"
                                        ):
                                            ui.icon(
                                                "people_off", size="2.5rem"
                                            ).classes("text-gray-300 mb-2")
                                            ui.label("No applicants yet").classes(
                                                "text-gray-500"
                                            )

                def load_posted_jobs_content():
                    """Load posted jobs section content"""
                    with main_content_container:
                        try:
                            vendor_jobs = api_service.get_jobs_by_vendor(
                                current_user.get("id")
                            )

                            # Flat Modern Header Section
                            with ui.row().classes(
                                "w-full justify-between items-center mb-6"
                            ):
                                with ui.column():
                                    ui.label(
                                        f"Posted Jobs ({len(vendor_jobs)})"
                                    ).classes("flat-title")
                                    ui.label(
                                        "Manage and track your job postings"
                                    ).classes("flat-subtitle")

                                ui.button(
                                    "Post New Job",
                                    on_click=lambda: ui.navigate.to("/post-job"),
                                    color="#00b074",
                                ).props("unelevated").style("color: white !important;")

                            if not vendor_jobs:
                                # Flat Modern Empty State
                                with ui.element("div").classes(
                                    "flat-card text-center py-16"
                                ):
                                    ui.icon("work_off", size="4rem").classes(
                                        "text-gray-300 mb-4"
                                    )
                                    ui.label("No jobs posted yet").classes(
                                        "text-xl font-semibold text-[#2b3940] mb-2"
                                    )
                                    ui.label(
                                        "Create your first job posting to get started"
                                    ).classes("text-gray-500 mb-6")
                                    ui.button(
                                        "Post Your First Job",
                                        icon="add_circle",
                                        on_click=lambda: ui.navigate.to("/post-job"),
                                        color="#00b074",
                                    ).props("unelevated").style(
                                        "color: white !important;"
                                    )
                            else:
                                # Flat Modern Jobs Grid
                                with ui.element("div").classes(
                                    "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                                ):
                                    for job in vendor_jobs:
                                        job_id = job.get("id")
                                        with ui.element("div").classes(
                                            "flat-card flex flex-col justify-between"
                                        ):
                                            with ui.column().classes(
                                                "w-full space-y-4"
                                            ):
                                                # Job Flyer
                                                if job.get("flyer"):
                                                    ui.image(job.get("flyer")).classes(
                                                        "w-full h-40 object-cover rounded-md"
                                                    )

                                                # Job Header
                                                with ui.column().classes("space-y-1"):
                                                    ui.label(
                                                        job.get("title", "Unknown")
                                                    ).classes(
                                                        "font-semibold text-lg text-[#2b3940]"
                                                    )
                                                    ui.label(
                                                        job.get("company", "N/A")
                                                    ).classes("text-sm text-gray-600")
                                                    ui.label(
                                                        job.get("location", "N/A")
                                                    ).classes("text-sm text-gray-500")

                                                # Job Stats
                                                with ui.row().classes(
                                                    "justify-between text-sm"
                                                ):
                                                    with ui.row().classes(
                                                        "items-center space-x-1"
                                                    ):
                                                        ui.icon(
                                                            "people", size="1rem"
                                                        ).classes("text-[#00b074]")
                                                        ui.label(
                                                            f"{job.get('application_count', 0)} applications"
                                                        ).classes("text-gray-600")
                                                    with ui.row().classes(
                                                        "items-center space-x-1"
                                                    ):
                                                        ui.icon(
                                                            "visibility", size="1rem"
                                                        ).classes("text-[#00b074]")
                                                        ui.label(
                                                            f"{job.get('view_count', 0)} views"
                                                        ).classes("text-gray-600")

                                            # Status and Actions
                                            with ui.row().classes(
                                                "w-full justify-between items-center pt-4 border-t border-gray-100 mt-4"
                                            ):
                                                with ui.element("span").classes(
                                                    "status-badge status-active"
                                                ):
                                                    ui.label("Active")
                                                with ui.row().classes("space-x-2"):
                                                    ui.button(
                                                        "Edit",
                                                        on_click=lambda j=job: edit_job_handler(
                                                            j
                                                        ),
                                                        color="#00b074",
                                                    ).props("unelevated").style(
                                                        "color: white !important; padding: 4px 8px; font-size: 11px;"
                                                    )
                                                    ui.button(
                                                        "Delete",
                                                        on_click=lambda j_id=job_id: delete_job_handler(
                                                            j_id
                                                        ),
                                                        color="#ef4444",
                                                    ).props("unelevated").style(
                                                        "color: white !important; padding: 4px 8px; font-size: 11px;"
                                                    )

                        except Exception as e:
                            ui.label("Error loading jobs").classes(
                                "text-xl text-red-600 mb-2"
                            )
                            ui.label(f"Details: {str(e)}").classes("text-gray-500")

                async def edit_job_handler(job_data: dict):
                    """Handle job editing with comprehensive form - inspired by modern dashboard design"""
                    try:
                        # Debug: Check what type of data we're receiving
                        print(
                            f"DEBUG: edit_job_handler called with job_data type: {type(job_data)}"
                        )
                        print(
                            f"DEBUG: edit_job_handler called with job_data: {job_data}"
                        )

                        # Ensure job_data is a dictionary
                        if not isinstance(job_data, dict):
                            ui.notify(
                                f"Invalid job data received. Expected dictionary, got {type(job_data)}",
                                type="negative",
                            )
                            return

                        # Check if job_data has the minimum required fields
                        if not job_data.get("id"):
                            ui.notify(
                                "Job data is missing required ID field", type="negative"
                            )
                            return

                        # Enhanced field mapping and validation
                        job_type_mapping = {
                            "full-time": "Full-time",
                            "Full-time": "Full-time",
                            "Full-Time": "Full-time",
                            "FULL-TIME": "Full-time",
                            "part-time": "Part-time",
                            "Part-time": "Part-time",
                            "Part-Time": "Part-time",
                            "PART-TIME": "Part-time",
                            "contract": "Contract",
                            "Contract": "Contract",
                            "CONTRACT": "Contract",
                            "internship": "Internship",
                            "Internship": "Internship",
                            "INTERNSHIP": "Internship",
                            "freelance": "Freelance",
                            "Freelance": "Freelance",
                            "FREELANCE": "Freelance",
                        }

                        # Enhanced category mapping
                        category_options = [
                            "Technology",
                            "Finance",
                            "Healthcare",
                            "Education",
                            "Marketing",
                            "Sales",
                            "Operations",
                        ]
                        category_mapping = {
                            "technology": "Technology",
                            "tech": "Technology",
                            "IT": "Technology",
                            "marketing": "Marketing",
                            "sales": "Sales",
                            "design": "Design",
                            "finance": "Finance",
                            "operations": "Operations",
                            "ops": "Operations",
                        }

                        # Parse salary with better error handling
                        salary_min = 0
                        salary_max = 0
                        if job_data and job_data.get("salary"):
                            try:
                                salary_str = (
                                    job_data.get("salary", "")
                                    .replace("$", "")
                                    .replace(",", "")
                                )
                                print(f"DEBUG: Parsing salary string: '{salary_str}'")
                                salary_parts = [
                                    int(x.strip())
                                    for x in salary_str.split("-")
                                    if x.strip().isdigit()
                                ]
                                print(f"DEBUG: Parsed salary parts: {salary_parts}")
                                if len(salary_parts) >= 2:
                                    salary_min = salary_parts[0]
                                    salary_max = salary_parts[1]
                                elif len(salary_parts) == 1:
                                    salary_min = salary_max = salary_parts[0]
                                print(
                                    f"DEBUG: Final salary values - min: {salary_min}, max: {salary_max}"
                                )
                            except (ValueError, IndexError, AttributeError) as e:
                                print(f"DEBUG: Error parsing salary: {e}")
                                pass
                        elif job_data and (
                            job_data.get("min_salary") or job_data.get("max_salary")
                        ):
                            try:
                                salary_min = int(job_data.get("min_salary", 0))
                                salary_max = int(job_data.get("max_salary", 0))
                                print(
                                    f"DEBUG: Using existing min_salary/max_salary: {salary_min}/{salary_max}"
                                )
                            except (ValueError, TypeError):
                                pass

                        # Normalize category with better fallback
                        current_category = (
                            job_data.get("category", "") if job_data else ""
                        )
                        normalized_category = category_mapping.get(
                            current_category.lower(), "Technology"
                        )
                        if current_category in category_options:
                            normalized_category = current_category

                        # Comprehensive form data initialization with safety checks
                        edit_form_data = {
                            "title": job_data.get("title", "") if job_data else "",
                            "company": job_data.get("company", "") if job_data else "",
                            "location": (
                                job_data.get("location", "") if job_data else ""
                            ),
                            "job_type": job_type_mapping.get(
                                job_data.get("job_type", "") if job_data else "",
                                "Full-time",
                            ),
                            "category": normalized_category,
                            "description": (
                                job_data.get("description", "") if job_data else ""
                            ),
                            "requirements": (
                                job_data.get("requirements", "") if job_data else ""
                            ),
                            "benefits": (
                                job_data.get("benefits", "") if job_data else ""
                            ),
                            "contact_email": (
                                job_data.get("contact_email", "") if job_data else ""
                            ),
                            "salary_min": salary_min,
                            "salary_max": salary_max,
                            "flyer_file": None,
                            "flyer_name": "",
                            "flyer_type": "",
                        }

                        def handle_flyer_upload(e):
                            """Handle flyer image upload with proper file object creation"""
                            try:
                                if hasattr(e, "content") and hasattr(e, "name"):
                                    edit_form_data["flyer_file"] = e.content
                                    edit_form_data["flyer_name"] = e.name
                                    edit_form_data["flyer_type"] = getattr(
                                        e, "type", "image/jpeg"
                                    )
                                    ui.notify(
                                        f'Flyer "{e.name}" uploaded successfully!',
                                        type="positive",
                                    )
                                else:
                                    ui.notify(
                                        "Failed to upload flyer. Please try again.",
                                        type="negative",
                                    )
                            except Exception as ex:
                                ui.notify(
                                    f"Error uploading flyer: {str(ex)}", type="negative"
                                )

                        def save_job_changes():
                            """Save job changes with comprehensive validation"""
                            try:
                                # Enhanced validation
                                required_fields = [
                                    "title",
                                    "company",
                                    "location",
                                    "description",
                                ]
                                form_values = {
                                    "title": edit_form_data.get("title"),
                                    "company": edit_form_data.get("company"),
                                    "location": edit_form_data.get("location"),
                                    "description": edit_form_data.get("description"),
                                }

                                # Check for empty required fields
                                missing_fields = [
                                    field
                                    for field in required_fields
                                    if not form_values.get(field, "").strip()
                                ]
                                if missing_fields:
                                    ui.notify(
                                        f"Please fill out all required fields: {', '.join(missing_fields)}",
                                        type="negative",
                                    )
                                    return

                                # Ensure we have a valid contact email
                                contact_email = edit_form_data.get(
                                    "contact_email", ""
                                ).strip()
                                if not contact_email:
                                    contact_email = f"vendor-{current_user.get('id', 'unknown')}@company.com"

                                api_data = {
                                    "title": edit_form_data.get("title"),
                                    "company": edit_form_data.get("company"),
                                    "location": edit_form_data.get("location"),
                                    "job_type": edit_form_data.get("job_type"),
                                    "category": edit_form_data.get("category"),
                                    "description": edit_form_data.get("description"),
                                    "requirements": edit_form_data.get(
                                        "requirements",
                                        "Requirements will be discussed during interview",
                                    ),
                                    "benefits": edit_form_data.get(
                                        "benefits", "Competitive benefits package"
                                    ),
                                    "contact_email": contact_email,
                                    "vendor_id": current_user.get("id", "vendor_1"),
                                }

                                # Handle salary formatting - ensure we always have valid numbers
                                print(
                                    f"DEBUG: Salary form data - min: {edit_form_data.get('salary_min')}, max: {edit_form_data.get('salary_max')}"
                                )
                                if (
                                    edit_form_data.get("salary_min", 0) > 0
                                    and edit_form_data.get("salary_max", 0) > 0
                                ):
                                    api_data["min_salary"] = edit_form_data.get(
                                        "salary_min"
                                    )
                                    api_data["max_salary"] = edit_form_data.get(
                                        "salary_max"
                                    )
                                    print(
                                        f"DEBUG: Using both min and max salary: {api_data['min_salary']}/{api_data['max_salary']}"
                                    )
                                elif edit_form_data.get("salary_min", 0) > 0:
                                    api_data["min_salary"] = edit_form_data.get(
                                        "salary_min"
                                    )
                                    api_data["max_salary"] = edit_form_data.get(
                                        "salary_min"
                                    )
                                    print(
                                        f"DEBUG: Using min salary for both: {api_data['min_salary']}/{api_data['max_salary']}"
                                    )
                                else:
                                    # If no salary provided, set reasonable defaults or omit fields
                                    # Since API requires these fields, set minimum values
                                    api_data["min_salary"] = 0
                                    api_data["max_salary"] = 0
                                    print(
                                        f"DEBUG: Using default salary values: {api_data['min_salary']}/{api_data['max_salary']}"
                                    )

                                # Handle file upload
                                flyer_file = None
                                if edit_form_data.get("flyer_file"):

                                    class FileUpload:
                                        def __init__(self, content, name, content_type):
                                            self.content = content
                                            self.name = name
                                            self.content_type = content_type

                                    flyer_file = FileUpload(
                                        edit_form_data["flyer_file"],
                                        edit_form_data["flyer_name"],
                                        edit_form_data["flyer_type"],
                                    )

                                print(
                                    f"DEBUG: Final API data before sending: {api_data}"
                                )
                                print(
                                    f"DEBUG: API data types - min_salary: {type(api_data.get('min_salary'))}, max_salary: {type(api_data.get('max_salary'))}"
                                )

                                # Update job using API
                                job_id = job_data.get("id") if job_data else ""
                                if not job_id:
                                    ui.notify(
                                        "Cannot update job: Missing job ID",
                                        type="negative",
                                    )
                                    return

                                result = api_service.update_job(
                                    job_id, api_data, file=flyer_file
                                )
                                if result:
                                    ui.notify(
                                        "Job updated successfully!", type="positive"
                                    )
                                    print("DEBUG: Update successful - closing dialog")

                                    # Simple and clean dialog closing
                                    dialog.close()

                                    # Refresh the jobs list
                                    show_content("posted_jobs")
                                    print("DEBUG: Dialog closed and content refreshed")
                                else:
                                    ui.notify(
                                        "Failed to update job. Please check the data and try again.",
                                        type="negative",
                                    )
                                    print(
                                        "DEBUG: Update failed - dialog should remain open"
                                    )

                            except Exception as e:
                                ui.notify(
                                    f"Error updating job: {str(e)}", type="negative"
                                )

                        def cancel_edit():
                            dialog.close()

                        # Create dialog using context manager pattern
                        with ui.dialog() as dialog, ui.card().classes(
                            "w-full max-w-5xl p-8 max-h-[90vh] overflow-y-auto shadow-2xl"
                        ):
                            job_title = (
                                job_data.get("title", "Unknown Job")
                                if job_data
                                else "Unknown Job"
                            )
                            ui.label(f"Edit Job: {job_title}").classes(
                                "text-3xl font-bold mb-8 text-[#00b074]"
                            )

                            with ui.column().classes("w-full space-y-8"):
                                # Section 1: Basic Job Information
                                with ui.column().classes("w-full space-y-6"):
                                    ui.label("Job Information").classes(
                                        "text-2xl font-bold text-[#2b3940] border-b-2 border-[#00b074] pb-2"
                                    )
                                    with ui.row().classes(
                                        "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                                    ):
                                        ui.input(
                                            "Job Title *",
                                            value=edit_form_data.get("title"),
                                            on_change=lambda e: edit_form_data.update(
                                                {"title": e.value}
                                            ),
                                        ).props("outlined dense").classes("w-full")
                                        ui.input(
                                            "Company *",
                                            value=edit_form_data.get("company"),
                                            on_change=lambda e: edit_form_data.update(
                                                {"company": e.value}
                                            ),
                                        ).props("outlined dense").classes("w-full")
                                        ui.input(
                                            "Location *",
                                            value=edit_form_data.get("location"),
                                            on_change=lambda e: edit_form_data.update(
                                                {"location": e.value}
                                            ),
                                        ).props("outlined dense").classes("w-full")
                                        ui.input(
                                            "Contact Email",
                                            value=edit_form_data.get("contact_email"),
                                            on_change=lambda e: edit_form_data.update(
                                                {"contact_email": e.value}
                                            ),
                                        ).props("outlined dense").classes("w-full")

                                # Section 2: Job Details
                                with ui.column().classes("w-full space-y-6"):
                                    ui.label("Job Details").classes(
                                        "text-2xl font-bold text-[#2b3940] border-b-2 border-[#00b074] pb-2"
                                    )
                                    with ui.row().classes(
                                        "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                                    ):
                                        ui.select(
                                            category_options,
                                            value=edit_form_data.get("category"),
                                            label="Category *",
                                            on_change=lambda e: edit_form_data.update(
                                                {"category": e.value}
                                            ),
                                        ).props("outlined dense").classes("w-full")
                                        ui.select(
                                            [
                                                "Full-time",
                                                "Part-time",
                                                "Contract",
                                                "Freelance",
                                                "Internship",
                                            ],
                                            value=edit_form_data.get("job_type"),
                                            label="Job Type *",
                                            on_change=lambda e: edit_form_data.update(
                                                {"job_type": e.value}
                                            ),
                                        ).props("outlined dense").classes("w-full")

                                # Section 3: Salary Information
                                with ui.column().classes("w-full space-y-6"):
                                    ui.label("Salary Information").classes(
                                        "text-2xl font-bold text-[#2b3940] border-b-2 border-[#00b074] pb-2"
                                    )
                                    with ui.row().classes(
                                        "w-full grid grid-cols-1 md:grid-cols-2 gap-6"
                                    ):
                                        ui.input(
                                            "Minimum Salary",
                                            value=(
                                                str(edit_form_data.get("salary_min", 0))
                                                if edit_form_data.get("salary_min") > 0
                                                else ""
                                            ),
                                            on_change=lambda e: edit_form_data.update(
                                                {
                                                    "salary_min": (
                                                        int(e.value)
                                                        if e.value.isdigit()
                                                        else 0
                                                    )
                                                }
                                            ),
                                        ).props("outlined dense type=number").classes(
                                            "w-full"
                                        )
                                        ui.input(
                                            "Maximum Salary",
                                            value=(
                                                str(edit_form_data.get("salary_max", 0))
                                                if edit_form_data.get("salary_max") > 0
                                                else ""
                                            ),
                                            on_change=lambda e: edit_form_data.update(
                                                {
                                                    "salary_max": (
                                                        int(e.value)
                                                        if e.value.isdigit()
                                                        else 0
                                                    )
                                                }
                                            ),
                                        ).props("outlined dense type=number").classes(
                                            "w-full"
                                        )

                                # Section 4: Job Content
                                with ui.column().classes("w-full space-y-6"):
                                    ui.label("Job Content").classes(
                                        "text-2xl font-bold text-[#2b3940] border-b-2 border-[#00b074] pb-2"
                                    )
                                    ui.textarea(
                                        "Job Description *",
                                        value=edit_form_data.get("description"),
                                        on_change=lambda e: edit_form_data.update(
                                            {"description": e.value}
                                        ),
                                    ).props("outlined dense autogrow").classes(
                                        "w-full min-h-[120px]"
                                    )
                                    ui.textarea(
                                        "Requirements",
                                        value=edit_form_data.get("requirements"),
                                        on_change=lambda e: edit_form_data.update(
                                            {"requirements": e.value}
                                        ),
                                    ).props("outlined dense autogrow").classes(
                                        "w-full min-h-[100px]"
                                    )
                                    ui.textarea(
                                        "Benefits",
                                        value=edit_form_data.get("benefits"),
                                        on_change=lambda e: edit_form_data.update(
                                            {"benefits": e.value}
                                        ),
                                    ).props("outlined dense autogrow").classes(
                                        "w-full min-h-[80px]"
                                    )

                                # Section 5: Job Flyer
                                with ui.column().classes("w-full space-y-6"):
                                    ui.label("Add Image").classes(
                                        "text-2xl font-bold text-[#2b3940] border-b-2 border-[#00b074] pb-2"
                                    )
                                    ui.upload(
                                        on_upload=handle_flyer_upload, auto_upload=True
                                    ).props(
                                        "accept=.jpg,.jpeg,.png flat bordered multiple=false color=#00b074 !important"
                                    ).classes(
                                        "w-full" 
                                    )

                                # Action Buttons
                                with ui.row().classes(
                                    "w-full justify-end space-x-4 pt-8 border-t-2 border-gray-200"
                                ):
                                    ui.button(
                                        "Cancel", on_click=cancel_edit, color="gray"
                                    ).props("outline size=lg").classes("px-8 py-3")
                                    ui.button(
                                        "Update Job",
                                        on_click=save_job_changes,
                                        color="#00b074",
                                    ).props("size=lg").classes(
                                        "px-8 py-3 text-white font-semibold"
                                    )

                        dialog.open()

                    except Exception as e:
                        ui.notify(f"Error opening edit dialog: {e}", type="negative")

                async def delete_job_handler(job_id: str):
                    """Handle the deletion of a job with a confirmation dialog."""
                    with ui.dialog() as dialog, ui.card():
                        ui.label(f"Are you sure you want to delete this job?").classes(
                            "text-lg font-semibold"
                        )
                        with ui.row().classes("w-full justify-end mt-4"):
                            ui.button(
                                "Cancel", on_click=dialog.close, color="gray"
                            ).props("outline").style("color: #6b7280 !important;")
                            ui.button(
                                "Delete",
                                on_click=lambda: dialog.submit(job_id),
                                color="#ef4444",
                            ).props("unelevated").style("color: white !important;")

                    result = await dialog
                    if result:
                        try:
                            api_service.delete_job(result)
                            ui.notify(
                                f"Job {result} deleted successfully.", type="positive"
                            )
                            # Refresh the jobs list
                            show_content("posted_jobs")
                        except Exception as e:
                            ui.notify(f"Error deleting job: {e}", type="negative")

                def load_applicants_content():
                    """Load applicants section content"""
                    with main_content_container:
                        try:
                            applicants = api_service.get_applicants_by_vendor(
                                current_user.get("id")
                            )

                            ui.label(f"Applicants ({len(applicants)})").classes(
                                "text-2xl font-bold mb-4"
                            )

                            if applicants:
                                with ui.element("div").classes(
                                    "grid grid-cols-1 md:grid-cols-2 gap-4"
                                ):
                                    for applicant in applicants:
                                        with ui.card().classes("w-full p-4"):
                                            ui.label(
                                                applicant.get("name", "Unknown")
                                            ).classes("text-lg font-semibold")
                                            ui.label(
                                                applicant.get("job_title", "N/A")
                                            ).classes("text-sm text-gray-600")
                                            ui.label(
                                                applicant.get("email", "N/A")
                                            ).classes("text-sm text-gray-600")
                            else:
                                ui.label("No applicants found.").classes(
                                    "text-gray-500"
                                )
                        except Exception as e:
                            ui.label("Error loading applicants").classes("text-red-600")

                def load_settings_content():
                    """Load settings section content"""
                    with main_content_container:
                        ui.label("Account Settings").classes(
                            "text-2xl font-bold text-gray-900 mb-6"
                        )

                        with ui.row().classes("w-full gap-8"):
                            # Left column - Profile Settings
                            with ui.column().classes("w-2/3"):
                                with ui.card().classes(
                                    "w-full bg-white shadow-sm rounded-lg p-8"
                                ):
                                    ui.label("Company Information").classes(
                                        "text-lg font-semibold text-gray-900 mb-6"
                                    )

                                    with ui.column().classes("space-y-6"):
                                        # Company name
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Company Name").classes(
                                                "text-sm font-medium text-gray-700"
                                            )
                                            ui.input(
                                                placeholder="Enter your company name"
                                            ).classes("w-full")

                                        # Email
                                        with ui.column().classes("space-y-2"):
                                            ui.label("Email Address").classes(
                                                "text-sm font-medium text-gray-700"
                                            )
                                            ui.input(
                                                placeholder="Enter your email address"
                                            ).classes("w-full")

                                        # Modern action buttons
                                        with ui.row().classes("space-x-4 pt-6"):
                                            ui.button(
                                                "Save Changes", color="#10b981"
                                            ).classes(
                                                "px-8 py-3 font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all"
                                            )
                                            ui.button("Cancel", color="gray").props(
                                                "outline"
                                            ).classes(
                                                "px-8 py-3 font-semibold rounded-lg hover:bg-gray-50 transition-all"
                                            )

                            # Right column - Additional Settings
                            with ui.column().classes("w-1/3"):
                                with ui.card().classes(
                                    "w-full bg-white shadow-sm rounded-lg p-6"
                                ):
                                    ui.label("Quick Actions").classes(
                                        "text-lg font-semibold text-gray-900 mb-4"
                                    )

                                    with ui.column().classes("space-y-3"):
                                        ui.button(
                                            "Change Password", color="#10b981"
                                        ).props("outline").classes(
                                            "w-full font-semibold"
                                        )
                                        ui.button("Download Data", color="gray").props(
                                            "outline"
                                        ).classes("w-full font-semibold")

                # Set initial view
                show_content("overview")
