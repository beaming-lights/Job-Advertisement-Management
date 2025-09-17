from nicegui import ui
from services.api_service import APIService
from services.sample_data import get_company_logos
import base64

def vendor_dashboard_page():
    """Create the vendor dashboard for managing job postings"""
    api_service = APIService()
    
    # Dashboard state
    vendor_jobs = []
    selected_job = None
    
    # Load vendor jobs
    def load_vendor_jobs():
        nonlocal vendor_jobs
        # In a real app, this would filter by vendor_id
        vendor_jobs = api_service.get_jobs()
        update_jobs_display()
    
    # Delete job
    def delete_job(job_id):
        def confirm_delete():
            if api_service.delete_job(job_id):
                ui.notify('Job deleted successfully', type='positive')
                load_vendor_jobs()
            else:
                ui.notify('Failed to delete job', type='negative')
            delete_dialog.close()
        
        with ui.dialog() as delete_dialog, ui.card():
            ui.label('Confirm Deletion').classes('text-xl font-bold mb-4')
            ui.label('Are you sure you want to delete this job posting? This action cannot be undone.').classes('mb-4')
            
            with ui.row().classes('justify-end space-x-4'):
                ui.button('Cancel', on_click=delete_dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded')
                ui.button('Delete', on_click=confirm_delete).classes('bg-red-600 text-white px-4 py-2 rounded')
        
        delete_dialog.open()
    
    # Edit job
    def edit_job(job):
        nonlocal selected_job
        selected_job = job.copy()
        
        with ui.dialog() as edit_dialog, ui.card().classes('w-full max-w-4xl'):
            ui.label('Edit Job Posting').classes('text-2xl font-bold mb-6')
            
            with ui.column().classes('space-y-4'):
                # Form fields
                title_input = ui.input('Job Title', value=selected_job.get('title', '')).classes('w-full')
                company_input = ui.input('Company', value=selected_job.get('company', '')).classes('w-full')
                
                with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-4'):
                    location_input = ui.input('Location', value=selected_job.get('location', '')).classes('w-full')
                    salary_input = ui.input('Salary', value=selected_job.get('salary', '')).classes('w-full')
                
                with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-4'):
                    job_types = ['Full-time', 'Part-time', 'Contract', 'Freelance', 'Internship']
                    type_select = ui.select(job_types, value=selected_job.get('job_type', 'Full-time')).classes('w-full')
                    
                    categories = ['Technology', 'Marketing', 'Sales', 'Design', 'Finance', 'Operations']
                    category_select = ui.select(categories, value=selected_job.get('category', 'Technology')).classes('w-full')
                
                description_textarea = ui.textarea('Description', value=selected_job.get('description', '')).classes('w-full min-h-32')
                requirements_textarea = ui.textarea('Requirements', value=selected_job.get('requirements', '')).classes('w-full min-h-24')
                
                def save_changes():
                    updated_job = {
                        'title': title_input.value,
                        'company': company_input.value,
                        'location': location_input.value,
                        'salary': salary_input.value,
                        'job_type': type_select.value,
                        'category': category_select.value,
                        'description': description_textarea.value,
                        'requirements': requirements_textarea.value
                    }
                    
                    if api_service.update_job(selected_job['id'], updated_job):
                        ui.notify('Job updated successfully', type='positive')
                        load_vendor_jobs()
                        edit_dialog.close()
                    else:
                        ui.notify('Failed to update job', type='negative')
                
                with ui.row().classes('justify-end space-x-4 pt-4'):
                    ui.button('Cancel', on_click=edit_dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded')
                    ui.button('Save Changes', on_click=save_changes).classes('bg-blue-600 text-white px-4 py-2 rounded')
        
        edit_dialog.open()
    
    # Create job card for dashboard
    def create_dashboard_job_card(job):
        company_logos = get_company_logos()
        company_name = job.get('company', 'Company')
        default_svg = '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#6B7280"/><text x="50%" y="50%" font-family="Arial" font-size="40" fill="white" text-anchor="middle" dy=".3em">CO</text></svg>'
        logo_svg = company_logos.get(company_name, default_svg)

        # Convert SVG string to data URL
        b64_svg = base64.b64encode(logo_svg.encode('utf-8')).decode('utf-8')
        logo_data_url = f'data:image/svg+xml;base64,{b64_svg}'
        
        with ui.element('div').classes('bg-white rounded-lg shadow-md p-6 border border-gray-200'):
            # Job header with logo
            with ui.row().classes('justify-between items-start mb-4'):
                with ui.row().classes('items-center space-x-4 flex-1'):
                    # Company logo
                    ui.image(logo_data_url).classes('w-12 h-12 rounded-lg')
                    
                    with ui.column():
                        ui.label(job.get('title', 'Job Title')).classes('text-xl font-semibold text-gray-800 mb-1')
                        ui.label(company_name).classes('text-lg text-blue-600')
                
                # Status badge
                status = 'Active'  # In real app, this would come from API
                status_color = 'bg-green-100 text-green-800' if status == 'Active' else 'bg-yellow-100 text-yellow-800'
                ui.label(status).classes(f'px-3 py-1 rounded-full text-sm font-medium {status_color}')
            
            # Job details
            with ui.row().classes('items-center space-x-6 mb-4 text-gray-600 text-sm'):
                ui.label(f"📍 {job.get('location', 'Location')}")
                ui.label(f"💼 {job.get('job_type', 'Full-time')}")
                ui.label(f"🏷️ {job.get('category', 'Category')}")
                if job.get('posted_date'):
                    ui.label(f"📅 {job['posted_date']}")
            
            # Stats (mock data)
            with ui.row().classes('items-center space-x-6 mb-4 text-sm'):
                ui.label('245 views').classes('text-blue-600')
                ui.label('12 applications').classes('text-green-600')
                ui.label('⭐ 4.8 rating').classes('text-yellow-600')
            
            # Action buttons
            with ui.row().classes('justify-end space-x-2'):
                ui.button('View', on_click=lambda: ui.navigate.to(f'/jobs?id={job.get("id")}')).classes('bg-gray-100 text-gray-700 px-3 py-2 rounded text-sm hover:bg-gray-200')
                ui.button('Edit', on_click=lambda j=job: edit_job(j)).classes('bg-blue-100 text-blue-700 px-3 py-2 rounded text-sm hover:bg-blue-200')
                ui.button('Delete', on_click=lambda job_id=job.get('id'): delete_job(job_id)).classes('bg-red-100 text-red-700 px-3 py-2 rounded text-sm hover:bg-red-200')
    
    # Update jobs display
    def update_jobs_display():
        jobs_container.clear()
        with jobs_container:
            if not vendor_jobs:
                with ui.element('div').classes('text-center py-12'):
                    ui.icon('work_off', size='4rem').classes('text-gray-400 mb-4')
                    ui.label('No job postings yet').classes('text-2xl text-gray-600 mb-2')
                    ui.label('Create your first job posting to get started').classes('text-gray-500 mb-4')
                    ui.button('Post Your First Job', on_click=lambda: ui.navigate.to('/post-job')).classes('bg-blue-600 text-white px-6 py-3 rounded-lg')
            else:
                with ui.column().classes('space-y-4'):
                    for job in vendor_jobs:
                        create_dashboard_job_card(job)
    
    # Page Header
    with ui.element('section').classes('bg-gradient-to-r from-purple-600 to-blue-600 text-white py-16'):
        with ui.element('div').classes('container mx-auto px-4'):
            with ui.row().classes('justify-between items-center'):
                with ui.column():
                    ui.label('Vendor Dashboard').classes('text-3xl md:text-3xl font-bold mb-3')
                    ui.label('Manage your job postings and track applications').classes('text-xl opacity-90')
                
                ui.button('Vendor Login', on_click=vendor_login).props('unelevated').style('background-color: #00b074 !important')
    
    # Stats Overview
    with ui.element('section').classes('py-12 bg-gray-50'):
        with ui.element('div').classes('container mx-auto px-4'):
            with ui.row().classes('grid grid-cols-1 md:grid-cols-4 gap-6 mb-8'):
                # Total Jobs
                with ui.card().classes('p-6 text-center'):
                    ui.icon('work', size='2rem').classes('text-blue-600 mb-2')
                    ui.label('5').classes('text-3xl font-bold text-gray-800')
                    ui.label('Active Jobs').classes('text-gray-600')
                
                # Total Views
                with ui.card().classes('p-6 text-center'):
                    ui.icon('visibility', size='2rem').classes('text-green-600 mb-2')
                    ui.label('1,234').classes('text-3xl font-bold text-gray-800')
                    ui.label('Total Views').classes('text-gray-600')
                
                # Applications
                with ui.card().classes('p-6 text-center'):
                    ui.icon('person_add', size='2rem').classes('text-purple-600 mb-2')
                    ui.label('67').classes('text-3xl font-bold text-gray-800')
                    ui.label('Applications').classes('text-gray-600')
                
                # Success Rate
                with ui.card().classes('p-6 text-center'):
                    ui.icon('trending_up', size='2rem').classes('text-yellow-600 mb-2')
                    ui.label('85%').classes('text-3xl font-bold text-gray-800')
                    ui.label('Success Rate').classes('text-gray-600')
            
            # Jobs Management Section
            with ui.row().classes('justify-between items-center mb-6'):
                ui.label('Your Job Postings').classes('text-2xl font-bold text-gray-800')
                
                with ui.row().classes('space-x-4'):
                    ui.select(['All Jobs', 'Active', 'Paused', 'Expired'], value='All Jobs').classes('min-w-32')
                    ui.input(placeholder='Search your jobs...').classes('min-w-64')
            
            # Jobs Container
            jobs_container = ui.element('div')
    
    # Load initial data
    load_vendor_jobs()
