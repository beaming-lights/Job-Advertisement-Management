from nicegui import ui

def create_header():
    is_vendor = False

    def logout():
        ui.navigate.to('/')
        ui.notify('You have been logged out.', color='positive')

    def vendor_login():
        ui.navigate.to('/vendor-dashboard')
        ui.notify('Welcome, Vendor!', color='positive')

    with ui.header(fixed=True).classes('bg-white/80 backdrop-blur-sm shadow-lg'):
        with ui.row().classes('container mx-auto px-4 py-2 w-full justify-between items-center'):
            # Logo
            with ui.link(target='/').classes('flex items-center q-gutter-sm no-underline'):
                ui.icon('work', size='2rem').classes('text-[#00b074]')
                ui.label('JobBoard').classes('text-2xl text-bold').style('color: #2b3940 !important')

            # Desktop Nav - only visible on md and up
            with ui.row().classes('q-hidden q-md-flex q-gutter-md items-center'):
                ui.link('HOME', target='/').style('color: #2b3940 !important').classes('no-underline uppercase')
                ui.link('BROWSE JOBS', target='/jobs').style('color: #2b3940 !important').classes('no-underline uppercase')
                ui.link('POST A JOB', target='/post-job').style('color: #2b3940 !important').classes('no-underline uppercase')

                if not is_vendor:
                    ui.button('Vendor Login', on_click=vendor_login).props('unelevated').style('background-color: #00b074 !important')
                else:
                    with ui.button(icon='person', color='#00b074').props('round flat'):
                        with ui.menu().classes('w-48'):
                            ui.menu_item('Dashboard', on_click=lambda: ui.navigate.to('/vendor-dashboard'))
                            ui.menu_item('Post a Job', on_click=lambda: ui.navigate.to('/post-job'))
                            ui.separator()
                            ui.menu_item('Logout', on_click=logout)

    #         # Mobile menu button (only visible on small screens)
    #         menu_btn = ui.button(icon='menu').classes('q-md-hidden')
    # # Mobile Menu (initially hidden on all screen sizes)
    # with ui.element('div').classes('bg-white border-t q-pa-md q-md-hidden q-hidden') as mobile_menu:
    #     with ui.column().classes('q-gutter-sm'):
    #         ui.link('Home', target='/').classes('text-dark')
    #         ui.link('Browse Jobs', target='/jobs').classes('text-dark')
    #         ui.link('Post a Job', target='/post-job').classes('text-dark')

    #         if not is_vendor:
    #             ui.button('Vendor Login', on_click=vendor_login).props('color=primary unelevated').classes('q-mt-sm')
    #         else:
    #             ui.link('Dashboard', target='/vendor-dashboard').classes('text-dark')
    #             ui.button('Logout', on_click=logout).props('color=negative flat').classes('q-mt-sm')

    # # Toggle the mobile menu on button click
    # menu_btn.on('click', lambda: mobile_menu.classes(toggle='q-hidden'))
