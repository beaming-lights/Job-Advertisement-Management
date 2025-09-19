from nicegui import ui


def home_page():
    """Create the home page with a full-screen hero slider and feature sections."""
    # Hero Section with official ui.carousel
    with ui.element("div").classes(
        "w-full h-full"
    ):  # A container to fill the available space
        with (
            ui.carousel(animated=True, arrows=True, navigation=True)
            .props("autoplay=5000")
            .classes("w-full h-full")
        ):
            slides = [
                {
                    "image": "https://picsum.photos/id/1018/1920/1080",
                    "title": "Find Your Dream Job",
                    "subtitle": "Connect with top companies and discover opportunities that match your skills.",
                    "cta": "Browse Jobs",
                    "cta_link": "/jobs",
                },
                {
                    "image": "https://picsum.photos/id/1015/1920/1080",
                    "title": "Post Jobs & Find Talent",
                    "subtitle": "Reach thousands of qualified candidates and build your dream team.",
                    "cta": "Post a Job",
                    "cta_link": "/post-job",
                },
                {
                    "image": "https://picsum.photos/id/10/1920/1080",
                    "title": "Career Growth Awaits",
                    "subtitle": "Take the next step in your career with opportunities from leading companies.",
                    "cta": "Get Started",
                    "cta_link": "/jobs",
                },
            ]
            for slide in slides:
                with ui.carousel_slide().classes("p-0"):
                    ui.image(slide["image"]).classes(
                        "absolute w-full h-full object-cover"
                    )
                    ui.element("div").classes("absolute inset-0 bg-black opacity-50")
                    with ui.column().classes(
                        "absolute inset-0 flex items-center justify-center text-center text-white p-4"
                    ):
                        ui.label(slide["title"]).classes(
                            "text-5xl md:text-7xl font-bold drop-shadow-lg"
                        )
                        ui.label(slide["subtitle"]).classes(
                            "text-xl md:text-2xl mt-4 mb-8 opacity-90 drop-shadow-md"
                        )
                        ui.button(
                            slide["cta"],
                            on_click=lambda link=slide["cta_link"]: ui.navigate.to(
                                link
                            ),
                        ).classes(
                            "bg-white text-gray-800 px-8 py-4 text-lg font-semibold rounded-lg hover:bg-gray-100 transition-colors shadow-lg"
                        )

    # Features Section
    with ui.element("section").classes("py-20 bg-gray-50"):
        with ui.element("div").classes("container mx-auto px-4"):
            ui.label("Why Choose JobBoar?").classes(
                "text-4xl font-bold text-center text-gray-800 mb-16"
            )
            with ui.row().classes("flex flex-wrap justify-center gap-8"):
                # Card 1: Smart Job Search
                with ui.card().classes(
                    "w-full md:w-96 p-8 text-center bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2"
                ):
                    with ui.element("div").classes("flex flex-col items-center"):
                        with ui.element("div").classes(
                            "bg-blue-100 rounded-full p-4 w-20 h-20 flex items-center justify-center mb-6"
                        ):
                            ui.icon("search", size="2.5rem").classes("text-blue-600")
                        ui.label("Smart Job Search").classes(
                            "text-xl font-semibold mb-4 text-gray-800 text-center w-full"
                        )
                        ui.label(
                            "Advanced filters and AI-powered recommendations to find the perfect job match."
                        ).classes("text-gray-600 text-center")

                # Card 2: Top Companies
                with ui.card().classes(
                    "w-full md:w-96 p-8 text-center bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2"
                ):
                    with ui.element("div").classes("flex flex-col items-center"):
                        with ui.element("div").classes(
                            "bg-green-100 rounded-full p-4 w-20 h-20 flex items-center justify-center mb-6"
                        ):
                            ui.icon("business", size="2.5rem").classes("text-green-600")
                        ui.label("Top Companies").classes(
                            "text-xl font-semibold mb-4 text-gray-800 text-center w-full"
                        )
                        ui.label(
                            "Connect with leading companies and startups looking for talented professionals."
                        ).classes("text-gray-600 text-center")

                # Card 3: Career Growth
                with ui.card().classes(
                    "w-full md:w-96 p-8 text-center bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2"
                ):
                    with ui.element("div").classes("flex flex-col items-center"):
                        with ui.element("div").classes(
                            "bg-purple-100 rounded-full p-4 w-20 h-20 flex items-center justify-center mb-6"
                        ):
                            ui.icon("trending_up", size="2.5rem").classes(
                                "text-purple-600"
                            )
                        ui.label("Career Growth").classes(
                            "text-xl font-semibold mb-4 text-gray-800 text-center w-full"
                        )
                        ui.label(
                            "Access resources, tips, and opportunities to accelerate your career growth."
                        ).classes("text-gray-600 text-center")

        # Stats Section
        with ui.element("section").classes("py-20 bg-blue-600 text-white"):
            with ui.element("div").classes("container mx-auto px-4"):
                with ui.row().classes(
                    "grid grid-cols-2 md:grid-cols-4 gap-8 text-center"
                ):
                    with ui.column():
                        ui.label("10,000+").classes("text-4xl font-bold mb-2")
                        ui.label("Active Jobs").classes("text-lg opacity-90")
                    with ui.column():
                        ui.label("5,000+").classes("text-4xl font-bold mb-2")
                        ui.label("Companies").classes("text-lg opacity-90")
                    with ui.column():
                        ui.label("50,000+").classes("text-4xl font-bold mb-2")
                        ui.label("Job Seekers").classes("text-lg opacity-90")
                    with ui.column():
                        ui.label("95%").classes("text-4xl font-bold mb-2")
                        ui.label("Success Rate").classes("text-lg opacity-90")

    # # CTA Section
    # with ui.element('section').classes('py-20 bg-gray-50'):
    #     with ui.element('div').classes('container mx-auto px-4'):
    #         ui.label('Why Choose JobBoard?').classes('text-4xl font-bold text-center text-gray-800 mb-16')
    #         with ui.row().classes('grid grid-cols-1 md:grid-cols-3 gap-8'):
    #             ui.label('Ready to Get Started?').classes('text-4xl font-bold mb-6')
    #             ui.label('Join thousands of professionals who found their dream jobs through JobBoard').classes('text-xl mb-8 opacity-90')
    #         with ui.row().classes('justify-center space-x-4'):
    #             ui.button('Browse Jobs', on_click=lambda: ui.navigate.to('/jobs')).classes('bg-blue-600 text-white px-8 py-4 text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors')
    #             ui.button('Post a Job', on_click=lambda: ui.navigate.to('/post-job')).classes('bg-transparent border-2 border-white text-white px-8 py-4 text-lg font-semibold rounded-lg hover:bg-white hover:text-gray-900 transition-colors')
