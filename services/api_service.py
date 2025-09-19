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
    
    def get_applicants(self):
        """Get all applicants"""
        try:
            response = requests.get(f"{self.base_url}/applicants", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return []
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
