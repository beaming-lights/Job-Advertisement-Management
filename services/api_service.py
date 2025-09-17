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
        self.base_url = os.getenv('API_BASE_URL', 'http://localhost:3000/api').rstrip('/').rstrip('/')
        self.api_key = os.getenv('API_KEY', '')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
        }

    def _normalize_job(self, job: Dict) -> Dict:
        """Normalizes a job dictionary to a standard format."""
        salary = ""
        if 'salary_min' in job and 'salary_max' in job:
            salary = f"${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}"
        elif 'min_salary' in job and 'max_salary' in job:
            salary = f"${job['min_salary']:,.0f} - ${job['max_salary']:,.0f}"

        return {
            'id': job.get('id'),
            'title': job.get('title') or job.get('job_title'),
            'company': job.get('company', 'N/A'),
            'location': job.get('location'),
            'description': job.get('description') or job.get('job_description'),
            'requirements': job.get('requirements', ''),
            'salary': salary,
            'job_type': job.get('job_type') or job.get('employment_type'),
            'category': job.get('category'),
            'posted_date': job.get('date_posted') or job.get('posted_date'),
            'flyer': job.get('flyer'),
        }
    
    def get_jobs(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Fetch all jobs with optional filters"""
        try:
            params = filters or {}
            response = requests.get(
                f"{self.base_url}/jobs",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            raw_jobs = data.get('data', [])
            # Normalize each job object to a consistent format
            return [self._normalize_job(job) for job in raw_jobs]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs: {e}")
            # Fallback to sample data when API is not available
            from .sample_data import get_sample_jobs
            return get_sample_jobs()
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """Fetch a specific job by ID"""
        try:
            response = requests.get(
                f"{self.base_url}/jobs/{job_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job {job_id}: {e}")
            return None
    
    def create_job(self, job_data: Dict, file: Optional[Any] = None) -> Optional[Dict]:
        """Create a new job posting with optional file upload."""
        try:
            # For multipart/form-data, requests sets the Content-Type header automatically.
            # We need to remove it from our custom headers.
            multipart_headers = self.headers.copy()
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
            multipart_headers = self.headers.copy()
            if 'Content-Type' in multipart_headers:
                del multipart_headers['Content-Type']

            files = None
            if file:
                files = {'flyer': (file.name, file.content, file.content_type)}

            # The API might expect a PUT or POST for updates with multipart.
            # If PUT doesn't work, the API might require POST with a method override, or just POST.
            # For now, we'll use PUT as is standard for updates.
            response = requests.put(
                f"{self.base_url}/jobs/{job_id}",
                data=job_data,
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
            return None
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job posting"""
        try:
            response = requests.delete(
                f"{self.base_url}/jobs/{job_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting job {job_id}: {e}")
            return False
    
    def get_job_categories(self) -> List[str]:
        """Fetch available job categories"""
        try:
            response = requests.get(
                f"{self.base_url}/categories",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching categories: {e}")
            return ["Technology", "Marketing", "Sales", "Design", "Finance", "Operations"]
    
    def get_applicants(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Fetch all applicants with optional filters"""
        # This is a mock implementation using sample data.
        # In a real application, this would fetch from an API endpoint.
        try:
            # Simulate filtering
            all_applicants = get_sample_applicants()
            if filters and 'job_title' in filters:
                return [app for app in all_applicants if app['job_title'] == filters['job_title']]
            return all_applicants
        except Exception as e:
            print(f"Error fetching applicants: {e}")
            return []

    def search_jobs(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Search jobs by query and filters"""
        try:
            params = {"q": query}
            if filters:
                params.update(filters)
            
            response = requests.get(
                f"{self.base_url}/jobs/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching jobs: {e}")
            return []
