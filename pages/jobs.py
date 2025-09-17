from nicegui import ui
from components.header import create_header
from components.footer import create_footer
from services.api_service import APIService
from main import show_job_details, get_company_logos
import base64

def jobs_page():
    """Create the jobs listing page with search and filters"""
    api_service = APIService()
    
    # Page state
    jobs_data = []
    filtered_jobs = []
    current_filters = {
        'category': '',
        'job_type': '',
        'location': '',
        'search': ''
    }
    
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
        
        if current_filters['search']:
            search_term = current_filters['search'].lower()
            filtered_jobs = [job for job in filtered_jobs 
                           if search_term in job.get('title', '').lower() 
                           or search_term in job.get('company', '').lower()
                           or search_term in job.get('description', '').lower()]
        
        if current_filters['category']:
            filtered_jobs = [job for job in filtered_jobs 
                           if job.get('category') == current_filters['category']]
        
        if current_filters['job_type']:
            filtered_jobs = [job for job in filtered_jobs 
                           if job.get('job_type') == current_filters['job_type']]
        
        if current_filters['location']:
            location_term = current_filters['location'].lower()
            filtered_jobs = [job for job in filtered_jobs 
                           if location_term in job.get('location', '').lower()]
        
        update_job_display()
    
    # Create job card component
    def create_job_card(job):
        company_logos = get_company_logos()
        company_name = job.get('company', 'Company Name')
        default_svg = '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#6B7280"/><text x="50%" y="50%" font-family="Arial" font-size="40" fill="white" text-anchor="middle" dy=".3em">CO</text></svg>'
        logo_svg = company_logos.get(company_name, default_svg)
        
        # Convert SVG string to data URL
        b64_svg = base64.b64encode(logo_svg.encode('utf-8')).decode('utf-8')
        logo_data_url = f'data:image/svg+xml;base64,{b64_svg}'
        
        with ui.element('div').classes('bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-gray-200'):
            # Job header with company logo
            with ui.row().classes('justify-between items-start mb-4'):
                with ui.row().classes('items-center space-x-4 flex-1'):
                    # Company logo
                    ui.image(logo_data_url).classes('w-12 h-12 rounded-lg')
                    
                    with ui.column():
                        ui.label(job.get('title', 'Job Title')).classes('text-xl font-semibold text-gray-800 mb-1')
                        ui.label(company_name).classes('text-lg text-blue-600 font-medium')
                
                with ui.column().classes('text-right'):
                    if job.get('salary'):
                        ui.label(job['salary']).classes('text-lg font-semibold text-green-600')
                    ui.label(job.get('job_type', 'Full-time')).classes('text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded')
            
            # Job details
            with ui.row().classes('items-center space-x-4 mb-4 text-gray-600'):
                with ui.row().classes('items-center'):
                    ui.icon('location_on', size='1rem')
                    ui.label(job.get('location', 'Location'))
                
                with ui.row().classes('items-center'):
                    ui.icon('category', size='1rem')
                    ui.label(job.get('category', 'Category'))
                
                if job.get('posted_date'):
                    with ui.row().classes('items-center'):
                        ui.icon('schedule', size='1rem')
                        ui.label(job['posted_date'])
            
            # Job description preview
            description = job.get('description', 'No description available')
            preview = description[:150] + '...' if len(description) > 150 else description
            ui.label(preview).classes('text-gray-700 mb-4')
            
            # Action buttons
            with ui.row().classes('justify-between items-center'):
                ui.button('View Details', 
                         on_click=lambda j=job: show_job_details(j)).classes('bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors')
                
                ui.button('Apply Now').classes('bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors')
    
    # Show job details modal
    def show_job_details(job_id):
        job = next((j for j in jobs_data if j.get('id') == job_id), None)
        if not job:
            return
        
        with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl'):
            with ui.row().classes('justify-between items-center mb-4'):
                ui.label('Job Details').classes('text-2xl font-bold')
                ui.button(icon='close', on_click=dialog.close).classes('text-gray-500')
            
            with ui.column().classes('space-y-4'):
                ui.label(job.get('title', 'Job Title')).classes('text-3xl font-bold text-gray-800')
                ui.label(job.get('company', 'Company')).classes('text-xl text-blue-600')
                
                with ui.row().classes('space-x-6 text-gray-600'):
                    ui.label(f"📍 {job.get('location', 'Location')}")
                    ui.label(f"💼 {job.get('job_type', 'Full-time')}")
                    ui.label(f"🏷️ {job.get('category', 'Category')}")
                    if job.get('salary'):
                        ui.label(f"💰 {job['salary']}")
                
                ui.separator()
                
                ui.label('Job Description').classes('text-xl font-semibold')
                ui.label(job.get('description', 'No description available')).classes('text-gray-700 whitespace-pre-wrap')
                
                if job.get('requirements'):
                    ui.label('Requirements').classes('text-xl font-semibold mt-4')
                    ui.label(job['requirements']).classes('text-gray-700 whitespace-pre-wrap')
                
                with ui.row().classes('justify-end space-x-4 mt-6'):
                    ui.button('Apply Now').classes('bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors')
                    ui.button('Save Job').classes('bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors')
        
        dialog.open()
    
    # Update job display
    def update_job_display():
        jobs_container.clear()
        with jobs_container:
            if not filtered_jobs:
                with ui.element('div').classes('text-center py-12'):
                    ui.icon('search_off', size='4rem').classes('text-gray-400 mb-4')
                    ui.label('No jobs found').classes('text-2xl text-gray-600 mb-2')
                    ui.label('Try adjusting your search criteria').classes('text-gray-500')
            else:
                ui.label(f'Found {len(filtered_jobs)} jobs').classes('text-lg font-semibold text-gray-700 mb-6')
                
                with ui.column().classes('space-y-4'):
                    for job in filtered_jobs:
                        create_job_card(job)
    
    # Page Header
    with ui.element('section').classes('bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16'):
        with ui.element('div').classes('container mx-auto px-4 text-center'):
            ui.label('Find Your Perfect Job').classes('text-4xl md:text-5xl font-bold mb-4')
            ui.label('Discover opportunities from top companies worldwide').classes('text-xl opacity-90')
    
    # Search and Filters Section
    with ui.element('section').classes('bg-white shadow-lg -mt-8 relative z-10'):
        with ui.element('div').classes('container mx-auto px-4 py-8'):
            with ui.row().classes('grid grid-cols-1 md:grid-cols-4 gap-4'):
                # Search input
                search_input = ui.input('Search jobs, companies, keywords...').classes('w-full')
                search_input.on('input', lambda e: (
                    current_filters.update({'search': e.value}),
                    filter_jobs()
                ))
                
                # Category filter
                categories = ['All Categories', 'Technology', 'Marketing', 'Sales', 'Design', 'Finance', 'Operations']
                category_select = ui.select(categories, value='All Categories').classes('w-full')
                category_select.on('update:model-value', lambda e: (
                    current_filters.update({'category': '' if e.value == 'All Categories' else e.value}),
                    filter_jobs()
                ))
                
                # Job type filter
                job_types = ['All Types', 'Full-time', 'Part-time', 'Contract', 'Freelance', 'Internship']
                type_select = ui.select(job_types, value='All Types').classes('w-full')
                type_select.on('update:model-value', lambda e: (
                    current_filters.update({'job_type': '' if e.value == 'All Types' else e.value}),
                    filter_jobs()
                ))
                
                # Location filter
                location_input = ui.input('Location').classes('w-full')
                location_input.on('input', lambda e: (
                    current_filters.update({'location': e.value}),
                    filter_jobs()
                ))
    
    # Jobs Container
    with ui.element('section').classes('py-12 bg-gray-50 min-h-screen'):
        with ui.element('div').classes('container mx-auto px-4'):
            jobs_container = ui.element('div')
    
    # Load initial jobs
    load_jobs()
