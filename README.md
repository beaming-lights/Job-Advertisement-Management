# JobBoard - Modern Job Website

A modern, responsive job board website built with NiceGUI and Tailwind CSS. This application allows job seekers to browse and search for jobs, while vendors can post, edit, and manage their job listings.

## Features

### For Job Seekers
-  **Advanced Job Search** - Search by keywords, location, category, and job type
-  **Responsive Design** - Optimized for desktop, tablet, and mobile devices
-  **Smart Filters** - Filter jobs by category, type, location, and more
-  **Detailed Job Views** - Complete job descriptions with requirements and company info
-  **Modern UI** - Beautiful, intuitive interface with smooth animations

### For Vendors
-  **Job Posting** - Easy-to-use form for creating job listings
-  **Vendor Dashboard** - Manage all job postings in one place
-  **Edit & Delete** - Full CRUD operations for job management
-  **Analytics** - View job performance metrics and statistics
-  **Job Categories** - Organize jobs by industry and type

### General Features
-  **Full-Page Slider** - Engaging homepage with rotating hero sections
-  **Responsive Navigation** - Mobile-friendly header and footer
-  **API Integration** - Connects to your existing job API
-  **Fast Performance** - Built with modern web technologies

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd windsurf-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API**
   Edit the `.env` file and update the API configuration:
   ```env
   API_BASE_URL=http://your-api-domain.com/api
   API_KEY=your_api_key_here
   DEBUG=True
   PORT=8080
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8080` to view the website

## API Integration

The application is designed to work with your existing job API. Make sure your API supports the following endpoints:

### Required Endpoints

- `GET /api/jobs` - Get all jobs (with optional query parameters for filtering)
- `GET /api/jobs/{id}` - Get specific job by ID
- `POST /api/jobs` - Create new job posting
- `PUT /api/jobs/{id}` - Update existing job
- `DELETE /api/jobs/{id}` - Delete job posting
- `GET /api/jobs/search?q={query}` - Search jobs by query
- `GET /api/categories` - Get job categories (optional)

### Expected Job Data Format

```json
{
  "id": "string",
  "title": "string",
  "company": "string",
  "location": "string",
  "description": "string",
  "requirements": "string",
  "salary": "string (optional)",
  "job_type": "string (Full-time, Part-time, Contract, etc.)",
  "category": "string",
  "posted_date": "string (optional)",
  "vendor_id": "string (optional)"
}
```

## Project Structure

```
windsurf-project/
├── components/
│   ├── __init__.py
│   ├── header.py          # Responsive navigation header
│   └── footer.py          # Site footer with links
├── pages/
│   ├── __init__.py
│   ├── home.py            # Homepage with slider
│   ├── jobs.py            # Job listings with search/filter
│   ├── post_job.py        # Job posting form
│   └── vendor_dashboard.py # Vendor job management
├── services/
│   ├── __init__.py
│   └── api_service.py     # API integration service
├── .env                   # Environment configuration
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Customization

### Styling
The application uses Tailwind CSS for styling. You can customize the appearance by modifying the CSS classes in the component files.

### API Service
Update `services/api_service.py` to match your API's authentication method and endpoint structure.

### Branding
- Update the logo and company name in `components/header.py`
- Modify the footer content in `components/footer.py`
- Change the page titles and descriptions in each page file

## Pages Overview

1. **Homepage (`/`)** - Features a full-page slider, company stats, and call-to-action sections
2. **Jobs (`/jobs`)** - Browse and search job listings with advanced filtering
3. **Post Job (`/post-job`)** - Form for vendors to create new job postings
4. **Vendor Dashboard (`/vendor-dashboard`)** - Management interface for vendors to edit/delete jobs

## Technologies Used

- **NiceGUI** - Python web framework for building user interfaces
- **Tailwind CSS** - Utility-first CSS framework for styling
- **Font Awesome** - Icon library for UI elements
- **Requests** - HTTP library for API communication
- **Pydantic** - Data validation and settings management
- **Python-dotenv** - Environment variable management

## Support

If you encounter any issues or need help with the setup, please check:

1. Ensure all dependencies are installed correctly
2. Verify your API endpoints are accessible
3. Check the `.env` file configuration
4. Review the console output for any error messages

## License

This project is open source and available under the MIT License.
