import requests
import os
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from .sample_data import get_sample_jobs, get_company_logos, get_sample_applicants

class Job(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    location: str
    description: str
    requirements: str
    salary: Optional[str] = None
    job_type: str  # full-time, part-time, contract, etc.
    category: str
    posted_date: Optional[str] = None
    vendor_id: Optional[str] = None

class APIService:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'https://advertisement-management-api-91xh.onrender.com/api').rstrip('/').rstrip('/')
        self.api_key = os.getenv('API_KEY', '')
        self.default_headers = {
            'Content-Type': 'application/json'
        }
        # Note: Authentication now handled by enhanced auth_service with Bearer tokens
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers from enhanced auth service"""
        try:
            # Use the enhanced auth service directly since it's integrated
            from .auth_service import auth_service
            return auth_service.get_authenticated_headers()
        except Exception as e:
            print(f"Error getting auth headers: {e}")
            # Fallback to basic headers with API key if available
            headers = self.default_headers.copy()
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            return headers

    def _to_absolute_url(self, url: Optional[str]) -> Optional[str]:
        """Make a possibly relative URL absolute using the API origin.

        Examples:
        - '/uploads/flyers/abc.jpg' -> 'http://localhost:3000/uploads/flyers/abc.jpg'
        - 'http://...' remains unchanged
        - None remains None
        """
        if not url:
            return url
        if isinstance(url, str) and (url.startswith('http://') or url.startswith('https://') or url.startswith('data:')):
            return url
        # Derive server origin from base_url (strip trailing '/api')
        api_origin = self.base_url
        if api_origin.endswith('/api'):
            api_origin = api_origin[:-4]
        from urllib.parse import urljoin
        return urljoin(api_origin + '/', str(url).lstrip('/'))

    def _normalize_job(self, job: Dict) -> Dict:
        """Normalizes a job dictionary to a standard format."""
        print(f"DEBUG: _normalize_job called with keys: {list(job.keys()) if job else 'None'}")
        print(f"DEBUG: _normalize_job input: {job}")

        salary = ""
        if 'salary_min' in job and 'salary_max' in job:
            salary = f"${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}"
        elif 'min_salary' in job and 'max_salary' in job:
            salary = f"${job['min_salary']:,.0f} - ${job['max_salary']:,.0f}"
        elif 'salary' in job:
            # Handle case where salary is a single string
            salary = job['salary']

        # Debug: Check what description fields are available
        description_value = (job.get('description') or
                           job.get('job_description') or
                           job.get('jobDetail') or
                           job.get('details') or
                           'Job description not available')

        company_value = (job.get('company') or
                        job.get('company_name') or
                        job.get('employer') or
                        'Company not specified')

        title_value = (job.get('title') or
                      job.get('job_title') or
                      job.get('jobTitle') or
                      'Untitled Job')

        print(f"DEBUG: Description mapping - description: '{job.get('description')}', job_description: '{job.get('job_description')}', final: '{description_value}'")
        print(f"DEBUG: Company mapping - company: '{job.get('company')}', company_name: '{job.get('company_name')}', final: '{company_value}'")
        print(f"DEBUG: Title mapping - title: '{job.get('title')}', job_title: '{job.get('job_title')}', final: '{title_value}'")

        # Normalize flyer URL from various possible API fields
        flyer_value = (job.get('flyer') or
                       job.get('flyer_url') or job.get('flyerUrl') or
                       job.get('image') or job.get('image_url') or job.get('imageUrl') or
                       job.get('banner') or job.get('banner_url') or job.get('file_url') or job.get('file'))
        flyer_value = self._to_absolute_url(flyer_value) if flyer_value else None

        normalized = {
            'id': job.get('id') or job.get('_id') or job.get('job_id'),
            'title': title_value,
            'company': company_value,
            'location': (job.get('location') or
                        job.get('job_location') or
                        job.get('city') or
                        'Location not specified'),
            'description': description_value,
            'requirements': (job.get('requirements') or
                           job.get('job_requirements') or
                           job.get('qualifications') or
                           ''),
            'salary': salary,
            'job_type': (job.get('job_type') or
                        job.get('employment_type') or
                        job.get('type') or
                        'Full-time'),
            'category': (job.get('category') or
                        job.get('job_category') or
                        'Technology'),  # Use Technology as default instead of General
            'posted_date': (job.get('date_posted') or
                           job.get('posted_date') or
                           job.get('created_at') or
                           'Recently'),
            'flyer': flyer_value,
        }

        print(f"DEBUG: _normalize_job output: {normalized}")
        return normalized
    
    def get_jobs(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Fetch all jobs with optional filters"""
        try:
            params = filters or {}
            response = requests.get(
                f"{self.base_url}/jobs",
                params=params,
                headers=self._get_auth_headers(),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            # Support both list and dict API response shapes
            if isinstance(data, list):
                raw_jobs = data
            elif isinstance(data, dict):
                raw_jobs = data.get('data') or data.get('jobs') or data.get('results') or []
            else:
                raw_jobs = []
            # Normalize each job object to a consistent format
            return [self._normalize_job(job) for job in raw_jobs]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs: {e}")
            # Fallback to sample data when API is not available
            from .sample_data import get_sample_jobs
            return get_sample_jobs()

    def get_jobs_with_meta(self, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Fetch jobs and preserve any metadata returned by the API.

        Returns a dict with keys:
        - 'jobs': List[Dict] normalized jobs
        - 'meta': Dict[Any, Any] extra metadata from the response (may be empty)
        """
        try:
            params = filters or {}
            response = requests.get(
                f"{self.base_url}/jobs",
                params=params,
                headers=self._get_auth_headers(),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            meta: Dict[str, Any] = {}
            if isinstance(data, list):
                raw_jobs = data
            elif isinstance(data, dict):
                raw_jobs = data.get('data') or data.get('jobs') or data.get('results') or []
                # retain any other fields as meta
                meta = {k: v for k, v in data.items() if k not in ('data', 'jobs', 'results')}
            else:
                raw_jobs = []
            jobs = [self._normalize_job(job) for job in raw_jobs]
            return {"jobs": jobs, "meta": meta}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs (with meta): {e}")
            # Fallback retains behavior while offering a minimal meta
            from .sample_data import get_sample_jobs
            return {"jobs": get_sample_jobs(), "meta": {"source": "fallback"}}
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """Fetch a specific job by ID"""
        try:
            print(f"DEBUG: get_job_by_id called with job_id: {job_id}")
            response = requests.get(
                f"{self.base_url}/jobs/{job_id}",
                headers=self._get_auth_headers(),
                timeout=10
            )
            response.raise_for_status()
            job_data = response.json()
            print(f"DEBUG: API returned job data: {job_data}")
            if isinstance(job_data, dict):
                # Some APIs wrap in {'data': {...}}
                maybe_job = job_data.get('data') if 'data' in job_data and isinstance(job_data.get('data'), dict) else job_data
                normalized = self._normalize_job(maybe_job)
                print(f"DEBUG: Normalized job data: {normalized}")
                return normalized
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job {job_id}: {e}")
            return None
    
    def create_job(self, job_data: Dict, file: Optional[Any] = None) -> Optional[Dict]:
        """Create a new job posting with optional file upload."""
        try:
            # Get authenticated headers
            multipart_headers = self._get_auth_headers().copy()
            # For multipart/form-data, requests sets the Content-Type header automatically.
            if 'Content-Type' in multipart_headers:
                del multipart_headers['Content-Type']

            files = None
            if file:
                files = {'flyer': (file.name, file.content, file.content_type)}

            print(f"--- SENDING MULTIPART TO API: {self.base_url}/jobs ---")
            print("DATA:", job_data)
            print("FILES:", files)
            print("--------------------------------------------------")

            response = requests.post(
                f"{self.base_url}/jobs",
                data=job_data,
                files=files,
                headers=multipart_headers,
                timeout=20 # Increased timeout for file upload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"--- API ERROR RESPONSE ---")
            print(f"Error creating job: {e}")
            if e.response is not None:
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Body: {e.response.text}")
            print("--------------------------")
            return None
    
    def update_job(self, job_id: str, job_data: Dict, file: Optional[Any] = None) -> Optional[Dict]:
        """Update an existing job posting with optional file upload."""
        try:
            multipart_headers = self._get_auth_headers().copy()
            if 'Content-Type' in multipart_headers:
                del multipart_headers['Content-Type']

            # Debug: Print what we're receiving
            print(f"DEBUG: update_job called with job_id: {job_id}")
            print(f"DEBUG: job_data keys: {list(job_data.keys()) if job_data else 'None'}")
            print(f"DEBUG: job_data values: {job_data}")

            # Normalize the job data for API compatibility
            api_data = self._normalize_job_for_api(job_data)

            print(f"DEBUG: Normalized API data: {api_data}")

            files = None
            if file:
                files = {'flyer': (file.name, file.content, file.content_type)}

            # The API might expect a PUT or POST for updates with multipart.
            # If PUT doesn't work, the API might require POST with a method override, or just POST.
            # For now, we'll use PUT as is standard for updates.
            print(f"DEBUG: Sending PUT request to {self.base_url}/jobs/{job_id}")
            print(f"DEBUG: API data being sent: {api_data}")

            response = requests.put(
                f"{self.base_url}/jobs/{job_id}",
                data=api_data,
                files=files,
                headers=multipart_headers,
                timeout=20
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating job {job_id}: {e}")
            if e.response is not None:
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Body: {e.response.text}")
            print("--------------------------")
            return None
    
    def _normalize_job_for_api(self, job_data: Dict) -> Dict:
        """Normalize job data for API submission/update"""
        # Parse salary range if it's a string like "$120,000 - $150,000"
        min_salary = None
        max_salary = None
        if job_data.get('salary'):
            salary_str = job_data.get('salary', '')
            # Try to extract numbers from salary string
            import re
            numbers = re.findall(r'\d{1,3}(?:,\d{3})*', salary_str.replace('$', '').replace(',', ''))
            if len(numbers) >= 2:
                min_salary = int(numbers[0])
                max_salary = int(numbers[1])
            elif len(numbers) == 1:
                min_salary = max_salary = int(numbers[0])

        # Get current date for date_posted if not provided
        from datetime import datetime
        date_posted = datetime.now().isoformat()

        # Transform to API format
        api_data = {
            "job_title": job_data.get('title', ''),
            "company": job_data.get('company', ''),
            "job_description": job_data.get('description', ''),  # Ensure this gets the description
            "location": job_data.get('location', ''),
            "employment_type": job_data.get('job_type', ''),
            "category": job_data.get('category', ''),
            "min_salary": min_salary if min_salary is not None else 0,
            "max_salary": max_salary if max_salary is not None else 0,
            "benefits": job_data.get('benefits', ''),  # Use benefits field directly
            "job_type": job_data.get('job_type', ''),  # Add job_type field as required
            "requirements": job_data.get('requirements', ''),  # Add requirements field
            "date_posted": date_posted,
            "contact_email": job_data.get('contact_email', f"vendor-{job_data.get('vendor_id', 'unknown')}@company.com"),  # Use form data or generate
            "flyer": job_data.get('flyer', '')  # Keep flyer field even if empty - API might require it
        }

        # Debug: Print the input data to see what's being passed
        print(f"DEBUG: Input job_data keys: {list(job_data.keys())}")
        print(f"DEBUG: Description value: '{job_data.get('description', 'EMPTY')}'")
        print(f"DEBUG: API data keys: {list(api_data.keys())}")

        # Remove None values but keep empty strings (since API expects them)
        api_data = {k: v for k, v in api_data.items() if v is not None}

        # Don't remove flyer field since API requires it
        # if not api_data.get('flyer'):
        #     api_data.pop('flyer', None)

        return api_data

    def delete_job(self, job_id: str) -> bool:
        """Delete a job posting"""
        try:
            response = requests.delete(
                f"{self.base_url}/jobs/{job_id}",
                headers=self._get_auth_headers(),
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting job {job_id}: {e}")
            return False
    
    def get_applicants(self):
        """Get all applicants"""
        try:
            response = requests.get(f"{self.base_url}/applicants", headers=self._get_auth_headers())
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching applicants: {e}")
            return []
    
    def get_saved_jobs(self):
        """Get user's saved jobs"""
        try:
            # Mock data for now - replace with actual API call
            return [
                {
                    "id": "1",
                    "title": "Senior Python Developer",
                    "company": "Tech Corp",
                    "location": "San Francisco, CA",
                    "salary": "$120,000 - $150,000",
                    "job_type": "Full-time",
                    "saved_date": "2024-01-15"
                },
                {
                    "id": "2", 
                    "title": "Frontend React Developer",
                    "company": "StartupXYZ",
                    "location": "Remote",
                    "salary": "$90,000 - $120,000",
                    "job_type": "Full-time",
                    "saved_date": "2024-01-14"
                }
            ]
        except Exception as e:
            print(f"Error fetching saved jobs: {e}")
            return []
    
    def get_applications(self):
        """Get user's job applications"""
        try:
            # Mock data for now - replace with actual API call
            return [
                {
                    "id": "1",
                    "job_title": "Senior Python Developer",
                    "company": "Tech Corp",
                    "applied_date": "2024-01-15",
                    "status": "interview",
                    "resume_name": "John_Doe_Resume_2024.pdf"
                },
                {
                    "id": "2",
                    "job_title": "Data Scientist",
                    "company": "AI Solutions Inc",
                    "applied_date": "2024-01-12",
                    "status": "applied",
                    "resume_name": "John_Doe_Resume_2024.pdf"
                },
                {
                    "id": "3",
                    "job_title": "Full Stack Developer",
                    "company": "WebDev Co",
                    "applied_date": "2024-01-10",
                    "status": "rejected",
                    "resume_name": "John_Doe_Resume_2024.pdf"
                }
            ]
        except Exception as e:
            print(f"Error fetching applications: {e}")
            return []
    
    def get_recommendations(self):
        """Get AI-powered job recommendations"""
        try:
            # Mock data for now - replace with actual AI API call
            return [
                {
                    "id": "1",
                    "title": "Senior Software Engineer",
                    "company": "Google",
                    "location": "Mountain View, CA",
                    "salary": "$150,000 - $200,000",
                    "match_score": 95,
                    "match_reasons": ["Python expertise", "5+ years experience", "Location preference"]
                },
                {
                    "id": "2",
                    "title": "Machine Learning Engineer", 
                    "company": "OpenAI",
                    "location": "San Francisco, CA",
                    "salary": "$160,000 - $220,000",
                    "match_score": 88,
                    "match_reasons": ["AI/ML skills", "Python proficiency", "Research background"]
                },
                {
                    "id": "3",
                    "title": "Backend Developer",
                    "company": "Netflix",
                    "location": "Los Gatos, CA", 
                    "salary": "$140,000 - $180,000",
                    "match_score": 82,
                    "match_reasons": ["Backend experience", "Scalability focus", "Tech stack match"]
                }
            ]
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []
    
    def get_user_profile(self):
        """Get user profile information"""
        try:
            # Mock data for now - replace with actual API call
            return {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "skills": ["Python", "JavaScript", "React", "Django"],
                "experience_level": "Senior",
                "location": "San Francisco, CA",
                "github": "https://github.com/johndoe",
                "linkedin": "https://linkedin.com/in/johndoe"
            }
        except Exception as e:
            print(f"Error fetching user profile: {e}")
            return {}

    def get_job_categories(self) -> List[str]:
        """Get available job categories"""
        # Since the API doesn't have a categories endpoint, always return fallback categories
        print("Using fallback job categories (API doesn't support categories endpoint)")
        return ["Technology", "Finance", "Healthcare", "Education", "Marketing", "Sales", "Operations"]

    def search_jobs(self, filters: Dict) -> List[Dict]:
        """Search jobs with filters"""
        try:
            # Convert search filters to API parameters
            api_filters = {}

            # Handle query/keyword search
            if filters.get('query'):
                api_filters['search'] = filters['query']

            # Handle location filter
            if filters.get('location'):
                api_filters['location'] = filters['location']

            # Handle job type filter
            if filters.get('job_type') and filters['job_type'] != 'all':
                api_filters['employment_type'] = filters['job_type']

            # Handle salary filters
            if filters.get('salary_min'):
                api_filters['min_salary'] = int(filters['salary_min'])
            if filters.get('salary_max'):
                api_filters['max_salary'] = int(filters['salary_max'])

            # Handle remote work filter
            if filters.get('remote'):
                api_filters['remote'] = True

            # Use the existing get_jobs method with filters
            return self.get_jobs(filters=api_filters)

        except Exception as e:
            print(f"Error searching jobs: {e}")
            # Fallback to all jobs if search fails
            return self.get_jobs()

    def get_jobs_by_vendor(self, vendor_id: str) -> List[Dict]:
        """Fetch jobs for a specific vendor using API filtering"""
        try:
            # Use the existing get_jobs method with vendor_id filter
            filters = {'vendor_id': vendor_id}
            return self.get_jobs(filters=filters)
        except Exception as e:
            print(f"Error fetching jobs for vendor {vendor_id}: {e}")
            # Fallback to local filtering if API doesn't support vendor filtering
            try:
                all_jobs = self.get_jobs()
                return [job for job in all_jobs if job.get('vendor_id') == vendor_id]
            except:
                return []

    def get_applicants_by_vendor(self, vendor_id: str) -> List[Dict]:
        """Fetch applicants for jobs posted by a specific vendor"""
        try:
            # Get all jobs for this vendor
            vendor_jobs = self.get_jobs_by_vendor(vendor_id)
            vendor_job_ids = [job.get('id') for job in vendor_jobs if job.get('id')]

            # Get all applicants and filter by vendor's job IDs
            all_applicants = self.get_applicants()
            vendor_applicants = [app for app in all_applicants if app.get('job_id') in vendor_job_ids]

            return vendor_applicants
        except Exception as e:
            print(f"Error fetching applicants for vendor {vendor_id}: {e}")
            return []

    def save_job(self, job_id: str) -> Dict:
        """Save a job to user's saved jobs list"""
        try:
            # For now, this is a placeholder - implement actual save functionality
            print(f"Saving job {job_id} to user's saved jobs")
            return {"success": True, "message": "Job saved successfully"}
        except Exception as e:
            print(f"Error saving job {job_id}: {e}")
            return {"success": False, "message": "Failed to save job"}
