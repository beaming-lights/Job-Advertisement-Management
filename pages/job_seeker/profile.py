from nicegui import ui

def candidate_profile_page():
    """Candidate profile page with modern design."""
    
    # Force all buttons to use green theme with absolute CSS override and NiceGUI content override
    ui.add_head_html("""
    <style>
        .q-btn:not(.glassmorphic-btn) {
            background-color: #00b074 !important;
            color: white !important;
        }
        .q-btn:not(.glassmorphic-btn):hover {
            background-color: #009960 !important;
        }
        .q-btn.glassmorphic-btn {
            background: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }
        .q-btn.glassmorphic-btn:hover {
            background: rgba(255, 255, 255, 0.3) !important;
        }
        
        /* NiceGUI Content Override - Force full width layout */
        .nicegui-content {
            overflow: visible !important;
            position: relative !important;
            width: 100vw !important;
            max-width: 100vw !important;
            margin-left: calc(-50vw + 50%) !important;
            margin-right: calc(-50vw + 50%) !important;
            left: 0 !important;
            right: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Override page container constraints */
        .q-page-container, .q-layout, .q-page {
            padding: 0 !important;
            margin: 0 !important;
            width: 100vw !important;
            max-width: 100vw !important;
        }
    </style>
    """)
    
    # Set page title
    ui.page_title("Candidate Profile - JobBoard")
    
    # Add page-specific CSS
    ui.add_head_html("""
    <style>
    body {
        overflow-x: hidden !important;
    }
    .profile-card {
        background: white;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 0;
    }
    .skill-tag {
        background: #f8f9fa;
        color: #495057;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        margin: 0.25rem;
        display: inline-block;
        border: 1px solid #e9ecef;
    }
    .experience-card {
        border-bottom: 1px solid #e9ecef;
        padding: 1.5rem 0;
    }
    .experience-card:last-child {
        border-bottom: none;
    }
    .social-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #f8f9fa;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0.25rem;
        transition: all 0.3s ease;
    }
    .social-icon:hover {
        background: #16a085;
        color: white;
    }
    .tab-button {
        padding: 1rem 2rem;
        border: none;
        background: none;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.875rem;
        color: #6c757d;
        border-bottom: 3px solid transparent;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .tab-button.active {
        color: #16a085;
        border-bottom-color: #16a085;
    }
    .green-button {
        background: #16a085 !important;
        color: white !important;
        border: none !important;
    }
    .green-button:hover {
        background: #138d75 !important;
    }
    </style>
    """)
    
    # Sample candidate data (in real app, this would come from database)
    candidate_data = {
        "name": "David Henricks",
        "title": "Senior Product Designer",
        "location": "New York, USA",
        "email": "david.henricks@email.com",
        "phone": "+1 (555) 123-4567",
        "website": "www.davidhenricks.com",
        "about": "A talented professional with an academic background in Design and proven commercial development experience as a Product Designer since 2015. Has a sound knowledge of the design process and user experience principles. Was involved in more than 50+ successful product launches.",
        "skills": ["UI/UX Design", "Figma", "Sketch", "Adobe Creative Suite", "Prototyping", "User Research", "Wireframing", "Design Systems"],
        "experience": [
            {
                "title": "Lead Product Designer",
                "company": "Airbnb",
                "duration": "Jun 2020 - Present - 3+ years",
                "location": "San Francisco, USA",
                "logo": "🏢"
            },
            {
                "title": "Senior UI/UX Designer", 
                "company": "Google Inc",
                "duration": "Jan 2018 - May 2020 - 2 years",
                "location": "Mountain View, USA",
                "logo": "🔍"
            }
        ],
        "education": [
            {
                "degree": "Masters in Design",
                "institution": "Stanford University",
                "duration": "2014 - 2016 - 2 years",
                "location": "Stanford, USA",
                "logo": "🎓"
            },
            {
                "degree": "Bachelor in Computer Science",
                "institution": "UC Berkeley",
                "duration": "2010 - 2014 - 4 years", 
                "location": "Berkeley, USA",
                "logo": "🏛️"
            }
        ]
    }
    
    # Main container
    with ui.element("div").classes("min-h-screen bg-gray-50 py-8"):
        with ui.element("div").classes("container mx-auto px-4"):
            
            # Green page title header
            with ui.element("div").classes("text-white rounded-xl p-8 mb-8 shadow-lg").style("background: linear-gradient(to right, #00b074, #009960)"):
                with ui.row().classes("items-center justify-between"):
                    with ui.column():
                        ui.label("Candidate Profile").classes("text-sm font-medium text-white/80 mb-2 uppercase tracking-wide")
                        ui.label(candidate_data["name"]).classes("text-4xl font-bold text-white mb-2")
                        ui.label(candidate_data["title"]).classes("text-xl text-white/80")
                    
                    # Download CV button - glassmorphic
                    ui.button("Download CV", 
                        on_click=lambda: ui.notify("CV download started", type="info")).classes(
                        "glassmorphic-btn text-white px-8 py-3 rounded-lg font-semibold transition-all shadow-md backdrop-blur-sm")
            
            with ui.row().classes("gap-8"):
                
                # Left Sidebar - Profile Info
                with ui.column().classes("w-full lg:w-1/4"):
                    with ui.card().classes("profile-card p-0 overflow-hidden shadow-lg border-0"):
                        # Profile header with gradient
                        with ui.element("div").classes("p-8 text-center text-white").style("background: linear-gradient(135deg, #00b074, #009960)"):
                            # Profile image placeholder
                            with ui.element("div").classes("w-24 h-24 bg-white/20 rounded-full mx-auto mb-4 flex items-center justify-center backdrop-blur-sm"):
                                ui.icon("person", size="2.5rem").classes("text-white")
                            
                            ui.label(candidate_data["name"]).classes("text-xl font-bold text-white mb-2")
                            ui.label(candidate_data["title"]).classes("text-white/80 mb-4")
                            
                            # Social links with better styling
                            with ui.row().classes("justify-center gap-3"):
                                social_icons = ["business", "facebook", "chat", "code"]
                                for icon in social_icons:
                                    with ui.element("div").classes("w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center hover:bg-white/30 cursor-pointer transition-all"):
                                        ui.icon(icon, size="1.3rem").classes("text-white")
                        
                        # Contact info with enhanced styling
                        with ui.column().classes("p-8 bg-gray-50"):
                            ui.label("Contact Information").classes("text-lg font-bold text-gray-900 mb-6")
                            
                            # Location with icon
                            with ui.row().classes("items-center gap-3 mb-4 p-3 bg-white rounded-lg"):
                                ui.icon("location_on", size="1.2rem").style("color: #00b074")
                                ui.label(candidate_data["location"]).classes("font-semibold text-gray-900")
                            
                            # Email with icon
                            with ui.row().classes("items-center gap-3 mb-4 p-3 bg-white rounded-lg"):
                                ui.icon("email", size="1.2rem").style("color: #00b074")
                                ui.label(candidate_data["email"]).classes("font-semibold text-gray-900 break-all")
                            
                            # Phone with icon
                            with ui.row().classes("items-center gap-3 mb-4 p-3 bg-white rounded-lg"):
                                ui.icon("phone", size="1.2rem").style("color: #00b074")
                                ui.label(candidate_data["phone"]).classes("font-semibold text-gray-900")
                            
                            # Website with icon
                            with ui.row().classes("items-center gap-3 mb-4 p-3 bg-white rounded-lg"):
                                ui.icon("language", size="1.2rem").style("color: #00b074")
                                ui.label(candidate_data["website"]).classes("font-semibold").style("color: #00b074")
                
                # Main Content Area
                with ui.column().classes("w-full lg:w-1/2"):
                    with ui.card().classes("profile-card p-0 shadow-lg border-0"):
                        # Main content
                        with ui.column().classes("p-8"):
                            # About section with better styling
                            ui.label("About Me").classes("text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2")
                            with ui.element("div").classes("bg-gray-50 p-6 rounded-lg mb-8"):
                                ui.label(candidate_data["about"]).classes("text-gray-700 leading-relaxed text-lg")
                            
                            # Skills section with enhanced tags
                            ui.label("Skills & Expertise").classes("text-2xl font-bold text-gray-900 mb-4")
                            with ui.element("div").classes("flex flex-wrap gap-3 mb-8"):
                                for skill in candidate_data["skills"]:
                                    with ui.element("span").classes("px-4 py-2 rounded-full font-medium").style("background: rgba(0, 176, 116, 0.1); color: #00b074"):
                                        ui.label(skill)
                            
                            # Work Experience with enhanced cards
                            ui.label("Work Experience").classes("text-2xl font-bold text-gray-900 mb-4")
                            with ui.column().classes("mb-8 gap-4"):
                                for exp in candidate_data["experience"]:
                                    with ui.element("div").classes("bg-white rounded-lg p-2 transition-shadow"):
                                        with ui.column().classes("w-full"):
                                            ui.label(exp["title"]).classes("text-xl font-bold text-gray-900 mb-1")
                                            ui.label(exp["company"]).classes("font-semibold text-lg mb-3").style("color: #00b074")
                                            with ui.row().classes("gap-6 text-sm text-gray-600"):
                                                ui.label(exp["duration"])
                                                ui.label(exp["location"])
                            
                            # Education with enhanced styling
                            ui.label("Education").classes("text-2xl font-bold text-gray-900 mb-4")
                            with ui.column().classes("gap-4"):
                                for edu in candidate_data["education"]:
                                    with ui.element("div").classes("bg-white rounded-lg p-2 transition-shadow"):
                                        with ui.column().classes("w-full"):
                                            ui.label(edu["degree"]).classes("text-xl font-bold text-gray-900 mb-1")
                                            ui.label(edu["institution"]).classes("font-semibold text-lg mb-3").style("color: #00b074")
                                            with ui.row().classes("gap-6 text-sm text-gray-600"):
                                                ui.label(edu["duration"])
                                                ui.label(edu["location"])
                        
                            
                            # Contact section
                            ui.label("Get in Touch").classes("text-2xl font-bold text-gray-900 mb-6")
                            
                            with ui.element("div").classes("bg-gray-50 p-6 rounded-lg"):
                                with ui.column().classes("gap-4"):
                                    ui.input("Your Name", placeholder="John Doe").classes("w-full p-3 border border-gray-300 rounded-lg").style("focus: {border-color: #00b074; ring-color: rgba(0, 176, 116, 0.2)}")
                                    
                                    with ui.row().classes("gap-4 w-full"):
                                        ui.input("Email", placeholder="john@example.com").classes("flex-1 p-3 border border-gray-300 rounded-lg").style("focus: {border-color: #00b074; ring-color: rgba(0, 176, 116, 0.2)}")
                                        ui.input("Subject", placeholder="Job Opportunity").classes("flex-1 p-3 border border-gray-300 rounded-lg").style("focus: {border-color: #00b074; ring-color: rgba(0, 176, 116, 0.2)}")
                                    
                                    ui.textarea("Message", placeholder="Type your message here...").classes("w-full p-3 border border-gray-300 rounded-lg").props("rows=6").style("focus: {border-color: #00b074; ring-color: rgba(0, 176, 116, 0.2)}")
                                    
                                    ui.button("Send Message", 
                                        on_click=lambda: ui.notify("Message sent successfully!", type="positive")).classes(
                                        "text-white px-8 py-3 rounded-lg font-semibold transition-all w-full shadow-md").style("background-color: #00b074; hover: {background-color: #009960}")
                
               
        
        # Edit Profile Button (floating)
        with ui.element("div").classes("fixed bottom-8 right-8"):
            ui.button("Edit Profile", 
                on_click=lambda: ui.navigate.to("/candidate-edit-profile")).classes(
                "text-white px-6 py-3 rounded-full shadow-lg transition-all hover:shadow-xl").style("background-color: #00b074; hover: {background-color: #009960; transform: scale(1.05)}")
