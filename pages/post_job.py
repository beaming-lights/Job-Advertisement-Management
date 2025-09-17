from nicegui import ui
from services.api_service import APIService

def post_job_page():
    """Create the job posting form for vendors"""
    api_service = APIService()
    
    # Form state
    form_data = {
        'title': '',
        'company': '',
        'location': '',
        'description': '',
        'requirements': '',
        'salary': '',
        'job_type': 'Full-time',
        'category': 'Technology'
    }
    
    # Submit job posting
    def submit_job():
        # Validate required fields
        required_fields = ['title', 'company', 'location', 'description']
        for field in required_fields:
            if not form_data[field].strip():
                ui.notify(f'{field.title()} is required', type='negative')
                return
        
        # Submit to API
        result = api_service.create_job(form_data)
        if result:
            ui.notify('Job posted successfully!', type='positive')
            # Reset form
            for key in form_data:
                form_data[key] = '' if key not in ['job_type', 'category'] else form_data[key]
            # Refresh form display
            update_form_display()
        else:
            ui.notify('Failed to post job. Please try again.', type='negative')
    
    # Update form display
    def update_form_display():
        # This would refresh form inputs if needed
        pass
    
    # Page Header
    with ui.element('section').classes('bg-gradient-to-r from-green-500 to-blue-600 text-white py-16'):
        with ui.element('div').classes('container mx-auto px-4 text-center'):
            ui.label('Post a Job').classes('text-4xl md:text-5xl font-bold mb-4')
            ui.label('Find the perfect candidate for your team').classes('text-xl opacity-90')
    
    # Form Section
    with ui.element('section').classes('py-12 bg-gray-50 min-h-screen w-full'):
        with ui.element('div').classes('flex justify-center px-4'):
            with ui.card().classes('p-8 w-full max-w-4xl'):
                ui.label('Job Details').classes('text-2xl font-bold mb-6 text-gray-800')
                
                with ui.column().classes('space-y-6'):
                    # Basic Information
                    with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-6'):
                        title_input = ui.input('Job Title *').classes('w-full')
                        title_input.bind_value_to(form_data, 'title')
                        
                        company_input = ui.input('Company Name *').classes('w-full')
                        company_input.bind_value_to(form_data, 'company')
                    
                    with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-6'):
                        location_input = ui.input('Location *').classes('w-full')
                        location_input.bind_value_to(form_data, 'location')
                        
                        salary_input = ui.input('Salary (Optional)').classes('w-full')
                        salary_input.bind_value_to(form_data, 'salary')
                    
                    # Job Type and Category
                    with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-6'):
                        job_types = ['Full-time', 'Part-time', 'Contract', 'Freelance', 'Internship']
                        type_select = ui.select(job_types, label='Job Type', value='Full-time').classes('w-full')
                        type_select.bind_value_to(form_data, 'job_type')
                        
                        categories = ['Technology', 'Marketing', 'Sales', 'Design', 'Finance', 'Operations', 'Healthcare', 'Education', 'Other']
                        category_select = ui.select(categories, label='Category', value='Technology').classes('w-full')
                        category_select.bind_value_to(form_data, 'category')
                    
                    # Job Description
                    description_textarea = ui.textarea('Job Description *').classes('w-full min-h-32')
                    description_textarea.bind_value_to(form_data, 'description')
                    
                    # Requirements
                    requirements_textarea = ui.textarea('Requirements (Optional)').classes('w-full min-h-24')
                    requirements_textarea.bind_value_to(form_data, 'requirements')
                    
                    # Submit Button
                    with ui.row().classes('justify-end space-x-4 pt-6'):
                        ui.button('Cancel', on_click=lambda: ui.navigate.to('/')).classes('bg-gray-500 text-white px-6 py-3 rounded-lg hover:bg-gray-600 transition-colors')
                        ui.button('Post Job', on_click=submit_job).classes('bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors')
    
    # Tips Section
    with ui.element('section').classes('py-12 bg-white'):
        with ui.element('div').classes('container mx-auto px-4 max-w-4xl'):
            ui.label('Tips for a Great Job Posting').classes('text-2xl font-bold mb-6 text-gray-800')
            
            with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-8'):
                with ui.column().classes('space-y-4'):
                    with ui.row().classes('items-start space-x-3'):
                        ui.icon('lightbulb', size='1.5rem').classes('text-yellow-500 mt-1')
                        with ui.column():
                            ui.label('Be Specific').classes('font-semibold text-gray-800')
                            ui.label('Include specific skills, experience level, and responsibilities').classes('text-gray-600 text-sm')
                    
                    with ui.row().classes('items-start space-x-3'):
                        ui.icon('trending_up', size='1.5rem').classes('text-green-500 mt-1')
                        with ui.column():
                            ui.label('Highlight Benefits').classes('font-semibold text-gray-800')
                            ui.label('Mention salary range, benefits, and growth opportunities').classes('text-gray-600 text-sm')
                
                with ui.column().classes('space-y-4'):
                    with ui.row().classes('items-start space-x-3'):
                        ui.icon('group', size='1.5rem').classes('text-blue-500 mt-1')
                        with ui.column():
                            ui.label('Company Culture').classes('font-semibold text-gray-800')
                            ui.label('Describe your work environment and team culture').classes('text-gray-600 text-sm')
                    
                    with ui.row().classes('items-start space-x-3'):
                        ui.icon('schedule', size='1.5rem').classes('text-purple-500 mt-1')
                        with ui.column():
                            ui.label('Clear Timeline').classes('font-semibold text-gray-800')
                            ui.label('Specify start date and application deadline').classes('text-gray-600 text-sm')
