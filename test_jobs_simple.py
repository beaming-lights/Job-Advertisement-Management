from nicegui import ui
from services.api_service import APIService

def simple_jobs_test():
    """Simple test jobs page"""
    try:
        api_service = APIService()
        jobs = api_service.get_jobs()
        
        ui.label("Jobs Page Test").classes("text-2xl font-bold mb-4")
        ui.label(f"Fetched {len(jobs)} jobs").classes("mb-4")
        
        # Show first 3 jobs
        for i, job in enumerate(jobs[:3]):
            with ui.card().classes("p-4 mb-2"):
                ui.label(f"Job {i+1}: {job.get('title', 'Unknown')}").classes("font-bold")
                ui.label(f"Company: {job.get('company', 'Unknown')}")
                ui.button("Test Button", on_click=lambda: ui.notify("Button clicked!")).style("background-color: #00b074 !important; color: white !important;")
    
    except Exception as e:
        ui.label(f"Error: {str(e)}").classes("text-red-500")

@ui.page("/test-jobs")
def test_jobs_page():
    simple_jobs_test()

if __name__ == "__main__":
    ui.run(port=8081, show=False)