from nicegui import ui
from services.auth_service import auth_service


def create_header():
    """Create header with authentication-aware navigation"""

    def handle_logout():
        """Handle user logout"""
        auth_service.logout()
        ui.navigate.to("/")
        ui.notify("You have been logged out successfully.", type="positive")

    def handle_login():
        """Navigate to login page"""
        ui.navigate.to("/login")

    # Get current user info
    current_user = auth_service.get_current_user()
    is_authenticated = current_user is not None
    is_vendor = current_user and current_user["role"] == "vendor"

    with ui.header(fixed=True).classes("bg-white/80 backdrop-blur-sm shadow-lg"):
        with ui.row().classes(
            "container mx-auto px-4 py-2 w-full justify-between items-center"
        ):
            # Logo
            with ui.link(target="/").classes(
                "flex items-center q-gutter-sm no-underline"
            ):
                ui.icon("work", size="2rem").classes("text-[#00b074]")
                ui.label("JobBoard").classes("text-2xl text-bold").style(
                    "color: #2b3940 !important"
                )

            # Desktop Nav - only visible on md and up (≥1024px)
            with ui.row().classes("hidden md:flex q-gutter-md items-center"):
                ui.link("HOME", target="/").style("color: #2b3940 !important").classes(
                    "no-underline uppercase"
                )
                ui.link("BROWSE JOBS", target="/jobs").style(
                    "color: #2b3940 !important"
                ).classes("no-underline uppercase")

                # Show "POST A JOB" only for vendors (not for unauthenticated users)
                if is_vendor:
                    ui.link("POST A JOB", target="/post-job").style(
                        "color: #2b3940 !important"
                    ).classes("no-underline uppercase")

                # Authentication buttons
                if not is_authenticated:
                    # Not logged in - show login/signup buttons
                    with ui.row().classes("q-gutter-sm"):
                        ui.button(
                            "Login", on_click=handle_login, color="#00b074"
                        ).props("outline").style('border-color: #00b074 !important; color: #00b074 !important')
                        ui.button(
                            "Sign Up",
                            on_click=lambda: ui.navigate.to("/signup"),
                            color="#00b074",
                        ).props("unelevated")
                else:
                    # Logged in - show user menu
                    with ui.button(icon="person", color="#00b074").props("round flat"):
                        with ui.menu().classes("w-64"):
                            # User info header
                            with ui.row().classes(
                                "q-pa-md bg-grey-1 items-center q-gutter-sm"
                            ):
                                ui.icon("account_circle", size="md").classes(
                                    "text-grey-7"
                                )
                                with ui.column().classes("no-wrap"):
                                    ui.label(current_user["name"]).classes(
                                        "text-weight-medium"
                                    )
                                    ui.label(current_user["email"]).classes(
                                        "text-caption text-grey-6"
                                    )
                                    ui.label(
                                        f'Role: {current_user["role"].title()}'
                                    ).classes("text-caption text-primary")

                            ui.separator()

                            # Menu items based on role
                            if is_vendor:
                                ui.menu_item(
                                    "Dashboard",
                                    on_click=lambda: ui.navigate.to(
                                        "/vendor-dashboard"
                                    ),
                                    auto_close=True,
                                )
                                ui.menu_item(
                                    "Post a Job",
                                    on_click=lambda: ui.navigate.to("/post-job"),
                                    auto_close=True,
                                )
                                ui.separator()

                            # Home link for all authenticated users
                            ui.menu_item(
                                "Home",
                                on_click=lambda: ui.navigate.to("/"),
                                auto_close=True,
                            )
                            ui.menu_item(
                                "Browse Jobs",
                                on_click=lambda: ui.navigate.to("/jobs"),
                                auto_close=True,
                            )
                            ui.menu_item(
                                "Profile Settings",
                                on_click=lambda: ui.notify(
                                    "Profile settings coming soon!"
                                ),
                                auto_close=True,
                            )
                            ui.separator()
                            ui.menu_item(
                                "Logout", on_click=handle_logout, auto_close=True
                            )

            # MOBILE MENU BUTTON (visible on small screens only, <1024px)
            menu_btn = ui.button(icon="menu", color="#00b074").classes(
                "block md:hidden"
            ).props("flat")

            # MOBILE MENU (hidden by default, only visible on small screens <1024px)
            with ui.element("div").classes(
                "bg-white border-t q-pa-md block md:hidden w-full no-underline uppercase text-lg font-medium)"
            ) as mobile_menu:
                mobile_menu.visible = False
                with ui.column().classes("q-gutter-md w-full"):
                    # Navigation Links
                    with ui.column().classes("q-gutter-sm w-full"):
                        ui.link("Home", target="/").classes(
                            "text-dark text-lg py-2 px-4 hover:bg-gray-100 rounded w-full block no-underline uppercase text-sm font-medium"
                        )
                        ui.link("Browse Jobs", target="/jobs").classes(
                            "text-dark text-lg py-2 px-4 hover:bg-gray-100 rounded w-full block no-underline uppercase text-sm font-medium"
                        )
                        
                        # Show "POST A JOB" only for vendors (not for unauthenticated users)
                        if is_vendor:
                            ui.link("Post a Job", target="/post-job").classes(
                                "text-dark text-lg py-2 px-4 hover:bg-gray-100 rounded w-full block no-underline uppercase text-sm font-medium"
                            )

                    # Authentication Section
                    ui.separator().classes("my-4")
                    
                    if not is_authenticated:
                        # Not logged in - show login/signup buttons vertically
                        with ui.column().classes("q-gutter-sm w-full"):
                            ui.button(
                                "Login", on_click=handle_login, color="#00b074"
                            ).props("outline").classes("w-full").style('border-color: #00b074 !important; color: #00b074 !important')
                            ui.button(
                                "Sign Up",
                                on_click=lambda: ui.navigate.to("/signup"),
                                color="#00b074",
                            ).props("unelevated").classes("w-full")
                    else:
                        # Logged in - show user options vertically
                        with ui.column().classes("q-gutter-sm w-full"):
                            if is_vendor:
                                ui.link("Dashboard", target="/vendor-dashboard").classes(
                                    "text-dark text-lg py-2 px-4 hover:bg-gray-100 rounded w-full block"
                                )
                            ui.button(
                                "Logout", on_click=handle_logout, color="negative"
                            ).props("flat").classes("w-full")

            # TOGGLE MOBILE MENU VISIBILITY
            def toggle_mobile_menu():
                # Only toggle on small screens (lt-md)
                mobile_menu.visible = not mobile_menu.visible
            
            menu_btn.on("click", toggle_mobile_menu)
            
            # Add responsive CSS and JavaScript
            ui.add_head_html("""
            <style>
            /* Ensure proper responsive behavior */
            @media (max-width: 1023px) {
                .hidden.md\\:flex {
                    display: none !important;
                }
                .block.md\\:hidden {
                    display: block;
                }
            }
            
            @media (min-width: 1024px) {
                .hidden.md\\:flex {
                    display: flex !important;
                }
                .block.md\\:hidden {
                    display: none !important;
                    visibility: hidden !important;
                }
            }
            </style>
            <script>
            // Responsive behavior management
            function handleResponsiveLayout() {
                const isMobile = window.innerWidth < 1024;
                const desktopNav = document.querySelector('.hidden.md\\:flex');
                const mobileButton = document.querySelector('.block.md\\:hidden');
                const mobileMenu = document.querySelectorAll('.block.md\\:hidden');
                
                if (isMobile) {
                    // Mobile: hide desktop nav, show mobile button
                    if (desktopNav) desktopNav.style.display = 'none';
                    if (mobileButton) mobileButton.style.display = 'block';
                } else {
                    // Desktop: show desktop nav, hide mobile elements
                    if (desktopNav) desktopNav.style.display = 'flex';
                    mobileMenu.forEach(menu => {
                        menu.style.display = 'none';
                        menu.style.visibility = 'hidden';
                    });
                }
            }
            
            window.addEventListener('resize', handleResponsiveLayout);
            window.addEventListener('load', handleResponsiveLayout);
            
            // Auto-hide mobile menu when resizing to desktop
            window.addEventListener('resize', function() {
                if (window.innerWidth >= 1024) {
                    const mobileMenus = document.querySelectorAll('.block.md\\:hidden');
                    mobileMenus.forEach(menu => {
                        if (menu.style.display === 'block') {
                            menu.style.display = 'none';
                        }
                    });
                }
            });
            </script>
            """)
