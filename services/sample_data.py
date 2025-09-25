"""Sample data for the job board application"""

def get_sample_jobs():
    """Return sample job data with company logos and images"""
    return [
        {
            'id': '1',
            'title': 'Senior Frontend Developer',
            'company': 'TechCorp Inc.',
            'location': 'San Francisco, CA',
            'description': 'Join our innovative team building the next generation of web applications! We are seeking a passionate Senior Frontend Developer to create exceptional user experiences using cutting-edge technologies. You\'ll work on high-impact projects in a collaborative, fast-paced environment with opportunities for growth and learning.',
            'requirements': ['5+ years frontend development', 'React & TypeScript expertise', 'Modern build tools (Vite, Webpack)', 'Responsive design principles', 'Team collaboration', 'Problem-solving skills'],
            'salary': '$120,000 - $160,000',
            'job_type': 'Full-time',
            'category': 'Technology',
            'posted_date': '2 days ago',
            'remote': True,
            'vendor_id': 'vendor_1',
            'flyer': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&h=400&fit=crop&crop=center',
            'company_logo': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=100&h=100&fit=crop&crop=center',
            'benefits': ['Health Insurance', 'Remote Work', '401k Match', 'Learning Budget', 'Flexible Hours'],
            'experience_level': 'Senior',
            'urgent': False
        },
        {
            'id': '2',
            'title': 'Nanny Job',
            'company': 'Family Solutions',
            'location': 'Cananda - Ablekuma',
            'description': 'Join our creative team as a UX/UI Designer! You\'ll work on exciting projects for various clients, creating intuitive and beautiful user interfaces. We\'re looking for someone with a strong portfolio and experience in user research, wireframing, and prototyping.',
            'requirements': 'Requirements:\n• 3+ years of UX/UI design experience\n• Proficiency in Figma, Sketch, Adobe Creative Suite\n• Strong portfolio showcasing web and mobile designs\n• Experience with user research and testing\n• Understanding of design systems\n• Excellent communication skills',
            'salary': '$80,000 - $110,000',
            'job_type': 'Full-time',
            'category': 'Design',
            'posted_date': '2024-01-12',
            'vendor_id': 'vendor_2'
        },
        {
            'id': '3',
            'title': 'Videographer',
            'company': 'Media Group',
            'location': 'Abelemkpe',
            'description': 'We\'re seeking a Digital Marketing Manager to lead our online marketing efforts. You\'ll develop and execute comprehensive digital marketing strategies across multiple channels including social media, email, SEO, and paid advertising.',
            'requirements': 'Requirements:\n• 4+ years of digital marketing experience\n• Expertise in Google Analytics, Google Ads, Facebook Ads\n• Strong knowledge of SEO and content marketing\n• Experience with marketing automation tools\n• Data-driven approach to marketing\n• Bachelor\'s degree in Marketing or related field',
            'salary': '$70,000 - $95,000',
            'job_type': 'Full-time',
            'category': 'Marketing',
            'posted_date': '2024-01-10',
            'vendor_id': 'vendor_3'
        },
        {
            'id': '4',
            'title': 'Financial Analyst',
            'company': 'Finance Pro',
            'location': 'Chicago, IL',
            'description': 'Join our finance team as a Financial Analyst. You\'ll be responsible for financial modeling, budgeting, forecasting, and providing insights to support business decisions. This is a great opportunity for someone looking to advance their career in corporate finance.',
            'requirements': 'Requirements:\n• 2+ years of financial analysis experience\n• Strong Excel and financial modeling skills\n• Knowledge of financial statements and accounting principles\n• Experience with financial software (SAP, Oracle, etc.)\n• CFA or MBA preferred\n• Strong analytical and communication skills',
            'salary': '$65,000 - $85,000',
            'job_type': 'Full-time',
            'category': 'Finance',
            'posted_date': '2024-01-08',
            'vendor_id': 'vendor_4'
        },
        {
            'id': '5',
            'title': 'Full Stack Developer',
            'company': 'StartupX',
            'location': 'Austin, TX',
            'description': 'Exciting opportunity to join a fast-growing startup as a Full Stack Developer! You\'ll work on cutting-edge projects using modern technologies and have the chance to make a significant impact on our product development.',
            'requirements': 'Requirements:\n• 3+ years of full stack development experience\n• Proficiency in JavaScript, Python, or Node.js\n• Experience with React/Vue.js and modern frontend frameworks\n• Knowledge of databases (PostgreSQL, MongoDB)\n• Familiarity with cloud platforms (AWS, GCP)\n• Startup experience preferred',
            'salary': '$90,000 - $120,000',
            'job_type': 'Full-time',
            'category': 'Technology',
            'posted_date': '2024-01-05',
            'vendor_id': 'vendor_5'
        },
        {
            'id': '6',
            'title': 'Content Marketing Specialist',
            'company': 'Marketing Inc',
            'location': 'Remote',
            'description': 'We\'re looking for a creative Content Marketing Specialist to develop engaging content across various channels. You\'ll create blog posts, social media content, email campaigns, and other marketing materials to drive brand awareness and engagement.',
            'requirements': 'Requirements:\n• 2+ years of content marketing experience\n• Excellent writing and editing skills\n• Experience with content management systems\n• Knowledge of SEO best practices\n• Social media marketing experience\n• Creative mindset with attention to detail',
            'salary': '$50,000 - $70,000',
            'job_type': 'Full-time',
            'category': 'Marketing',
            'posted_date': '2024-01-03',
            'vendor_id': 'vendor_3'
        },
        {
            'id': '7',
            'title': 'Product Manager',
            'company': 'Tech Corp',
            'location': 'Seattle, WA',
            'description': 'Join our product team as a Product Manager! You\'ll work closely with engineering, design, and business teams to define product strategy, prioritize features, and drive product development from concept to launch.',
            'requirements': 'Requirements:\n• 4+ years of product management experience\n• Strong analytical and problem-solving skills\n• Experience with agile development methodologies\n• Knowledge of user research and data analysis\n• Excellent communication and leadership skills\n• Technical background preferred',
            'salary': '$110,000 - $140,000',
            'job_type': 'Full-time',
            'category': 'Technology',
            'posted_date': '2024-01-01',
            'vendor_id': 'vendor_1'
        },
        {
            'id': '8',
            'title': 'Graphic Designer',
            'company': 'Design Studio',
            'location': 'Portland, OR',
            'description': 'Creative Graphic Designer needed to join our award-winning design team. You\'ll work on diverse projects including branding, print design, digital graphics, and marketing materials for clients across various industries.',
            'requirements': 'Requirements:\n• 3+ years of graphic design experience\n• Proficiency in Adobe Creative Suite (Photoshop, Illustrator, InDesign)\n• Strong portfolio showcasing diverse design work\n• Understanding of print and digital design principles\n• Attention to detail and ability to meet deadlines\n• Bachelor\'s degree in Graphic Design or related field',
            'salary': '$55,000 - $75,000',
            'job_type': 'Full-time',
            'category': 'Design',
            'posted_date': '2023-12-28',
            'vendor_id': 'vendor_2'
        }
    ]

def get_company_logos():
    """Return company logo SVG content"""
    return {
        'Tech Corp': '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#4F46E5"/><text x="50%" y="50%" font-family="Arial" font-size="40" fill="white" text-anchor="middle" dy=".3em">TC</text></svg>',
        'Design Studio': '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#EC4899"/><text x="50%" y="50%" font-family="Arial" font-size="40" fill="white" text-anchor="middle" dy=".3em">DS</text></svg>',
        'Marketing Inc': '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#10B981"/><text x="50%" y="50%" font-family="Arial" font-size="40" fill="white" text-anchor="middle" dy=".3em">MI</text></svg>',
        'Finance Pro': '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#F59E0B"/><text x="50%" y="50%" font-family="Arial" font-size="40" fill="white" text-anchor="middle" dy=".3em">FP</text></svg>',
        'StartupX': '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#8B5CF6"/><text x="50%" y="50%" font-family="Arial" font-size="40" fill="white" text-anchor="middle" dy=".3em">SX</text></svg>'
    }

def get_sample_applicants():
    """Return sample applicant data."""
    return [
        {
            'id': '1', 'job_id': '1', 'name': 'Nicolas Bradley',
            'avatar': 'https://randomuser.me/api/portraits/men/1.jpg',
            'job_title': 'Senior Frontend Developer', 'applied_on': '12 July, 2020',
        },
        {
            'id': '2', 'job_id': '1', 'name': 'Elizabeth Gomez',
            'avatar': 'https://randomuser.me/api/portraits/women/2.jpg',
            'job_title': 'Senior Frontend Developer', 'applied_on': '14 July, 2020',
        },
        {
            'id': '3', 'job_id': '2', 'name': 'Joe Wade',
            'avatar': 'https://randomuser.me/api/portraits/men/3.jpg',
            'job_title': 'UX/UI Designer', 'applied_on': '14 July, 2020',
        },
        {
            'id': '4', 'job_id': '3', 'name': 'Roger Hawkins',
            'avatar': 'https://randomuser.me/api/portraits/men/4.jpg',
            'job_title': 'Digital Marketing Manager', 'applied_on': '16 July, 2020',
        },
        {
            'id': '5', 'job_id': '1', 'name': 'Marie Green',
            'avatar': 'https://randomuser.me/api/portraits/women/5.jpg',
            'job_title': 'Senior Frontend Developer', 'applied_on': '21 July, 2020',
        },
    ]
