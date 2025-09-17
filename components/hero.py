from nicegui import ui

# Define color constants
PRIMARY_COLOR = "#00b074"  # New primary color
SECONDARY_COLOR = "#00b074"  # Using primary for consistency

def create_hero():
    """Create a modern hero section with search functionality."""
    # Hero section with full width stretch - responsive
    with ui.column().classes("w-full relative min-h-[90vh] flex items-center overflow-hidden").style("width: 100vw; max-width: 100vw; margin-left: calc(-50vw + 50%); margin-right: calc(-50vw + 50%); box-sizing: border-box;"):
        # Background image container
        with ui.element('div').classes("absolute inset-0 w-full h-full -z-10 overflow-hidden").style("width: 100%; height: 100%;"):
            # Background image
            ui.image("https://images.pexels.com/photos/3756681/pexels-photo-3756681.jpeg") \
                .classes("w-full h-full object-cover").style("width: 100%; height: 100%; object-fit: cover;")
            
            # Dark overlay for better text readability
            ui.element('div').classes("absolute inset-0 bg-gradient-to-r from-black/70 via-black/40 to-black/20")
        
        # Decorative elements container
        with ui.column().classes("absolute inset-0 -z-10 overflow-visible"):
            # Decorative shapes - positioned within container bounds
            with ui.element('div').classes(f"absolute top-[20%] -left-10 w-48 h-48 rounded-full bg-{PRIMARY_COLOR[1:]}/5 blur-2xl"):
                pass
            with ui.element('div').classes(f"absolute bottom-[30%] -right-10 w-60 h-60 rounded-full bg-{SECONDARY_COLOR[1:]}/5 blur-2xl"):
                pass
        
        # Main content with proper spacing and containment
        with ui.row().classes("w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-20 justify-center") as hero_content:
            # Main content container
            with ui.column().classes("w-full max-w-4xl mx-auto text-center px-4 space-y-8 text-white flex flex-col items-center"):
                # Badge
                with ui.row().classes("inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border border-gray-200 shadow-sm mx-auto"):
                    ui.icon("rocket_launch", size="sm", color=PRIMARY_COLOR)
                    ui.label("Join 10,000+ professionals").classes("text-sm font-medium text-gray-700")
                
                # Main heading with gradient text
                with ui.column().classes("items-center w-full"):
                    ui.label("Find Your Dream").classes("text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black leading-tight text-white w-full")
                    ui.label("Job Today").classes(f"text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black leading-tight text-white mb-6 w-full")
                
                # Subheading
                ui.label(
                    "Connect with top companies and land your next career opportunity. "
                    "We've helped over 50,000 professionals find their perfect match."
                ).classes("text-lg text-white/90 max-w-2xl mx-auto leading-relaxed mb-8")
                
                # Modern search bar with glass effect - responsive
                with ui.column().classes("w-full max-w-2xl mx-auto space-y-4 mb-8 px-4"):
                    with ui.row().classes(
                        "w-full items-center bg-white/10 backdrop-blur-md rounded-sm shadow-lg p-1 border border-white/20 flex-col sm:flex-row"
                    ).style("box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);"):
                        with ui.row().classes("flex-1 items-center px-4 py-3 w-full sm:w-auto"):
                            ui.icon("search", size="sm", color="white").classes("mr-3")
                            ui.input(
                                placeholder="Job title or company"
                            ).classes(
                                "flex-1 bg-transparent border-0 text-white placeholder-white/70 focus:outline-none focus:ring-0 text-base w-full"
                            ).props('readonly')

                        with ui.row().classes("hidden sm:block h-8 w-px bg-white/30 mx-2"):
                            pass

                        with ui.row().classes("w-full sm:w-64 items-center px-4 py-3"):
                            ui.icon("location_on", size="sm", color="white").classes("mr-3")
                            ui.input(
                                placeholder="Location)"
                            ).classes(
                                "flex-1 bg-transparent border-0 text-white placeholder-white focus:outline focus:ring-0 text-base w-full"
                            ).props('')

                        ui.button(
                            "SEARCH",
                            on_click=lambda: ui.navigate.to("/jobs")
                        ).style(f"background-color: {PRIMARY_COLOR} !important")\
                         .classes("hover:opacity-90 text-white font-semibold px-6 py-3 rounded-sm "
                                "min-h-[40px] text-sm transition-all duration-300 transform hover:scale-105 shadow-lg w-full sm:w-auto mt-2 sm:mt-0")
                
                # Trusted by section with company logos
                with ui.column().classes("mt-12 items-center w-full"):
                    ui.label("Trusted by leading corporations").classes("text-sm text-white-500 mb-4 text-center")
                    with ui.row().classes("flex flex-wrap justify-center items-center gap-6 md:gap-10 opacity-80"):
                        companies = ["Google", "Microsoft", "Amazon", "Netflix", "Adobe"]
                        for company in companies:
                            with ui.element('div').classes("text-white-700 font-medium text-lg"):
                                ui.label(company)
