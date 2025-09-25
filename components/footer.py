from nicegui import ui

# Add Themify Icons and Critical Footer CSS
ui.add_head_html('''
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/themify-icons@1.0.1/css/themify-icons.css">
<style>
/* Critical Footer CSS - Override any other footer styles */
footer, .footer, [data-footer], .q-footer {
    margin: 0 !important;
    padding: 0 !important;
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
    margin-top: 0 !important;
    border: none !important;
    position: relative !important;
    width: 100vw !important;
    max-width: 100vw !important;
    left: 0 !important;
    right: 0 !important;
    box-sizing: border-box !important;
    overflow-x: hidden !important;
}

/* Ensure body and html don't add spacing */
html, body {
    margin: 0 !important;
    padding: 0 !important;
    overflow-x: hidden !important;
}

/* Override NiceGUI container constraints and content overrides */
.q-page-container, .q-layout, .q-page {
    padding-bottom: 0 !important;
    margin-bottom: 0 !important;
}

/* NiceGUI Content Override - Force footer outside content container */
.nicegui-content {
    overflow: visible !important;
    position: relative !important;
}

.nicegui-content footer {
    position: relative !important;
    margin-left: calc(-50vw + 50%) !important;
    margin-right: calc(-50vw + 50%) !important;
    width: 100vw !important;
    max-width: 100vw !important;
    left: 0 !important;
    right: 0 !important;
}

/* Clear any floating elements before footer */
footer::before {
    content: "" !important;
    display: block !important;
    clear: both !important;
    height: 0 !important;
}

/* Force footer to bottom and prevent any gaps */
body {
    display: flex !important;
    flex-direction: column !important;
    min-height: 100vh !important;
}

main, .q-page-container {
    flex: 1 !important;
}

/* Override any framework-specific footer spacing */
.q-footer, .q-layout__footer {
    margin: 0 !important;
    padding: 0 !important;
}

/* Ensure no spacing after footer */
footer + *, footer ~ * {
    margin-top: 0 !important;
}

/* Force flush positioning */
footer {
    margin-top: auto !important;
}
</style>
''')

def create_footer():
    def scroll_to_top():
        ui.run_javascript("window.scrollTo({ top: 0, behavior: 'smooth' })")

    # Full-width footer - edge to edge with no bottom margin - IMPORTANT overrides
    with ui.element('footer').classes('bg-gray-900 text-white').style('position: relative !important; width: 100vw !important; max-width: 100vw !important; margin-left: calc(-50vw + 50%) !important; margin-right: calc(-50vw + 50%) !important; margin-bottom: 0 !important; padding-bottom: 0 !important; margin-top: 0 !important; box-sizing: border-box !important; overflow-x: hidden !important; left: 0 !important; right: 0 !important; border: none !important;'):
        
        # Main footer content - single row layout
        with ui.row().classes('w-full max-w-7xl mx-auto justify-between items-center p-6 flex-col md:flex-row gap-6'):
            
            # Left: Logo & Description
            with ui.column().classes('items-center md:items-start text-center md:text-left'):
                with ui.row().classes('items-center q-gutter-sm'):
                    ui.icon('work', size='1.5rem').classes('text-[#00b074]')
                    ui.label('JobBoard').classes('text-xl font-bold')
                    ui.label('Connecting talent with opportunity.').classes('text-sm text-gray-400 q-mt-sm')

            # Center: Quick Links (horizontal on desktop)
            with ui.row().classes('q-gutter-lg items-center flex justify-center'):
                ui.link('Home', target='/').classes('text-gray-400 hover:text-white text-sm no-underline')
                ui.link('Browse Jobs', target='/jobs').classes('text-gray-400 hover:text-white text-sm no-underline')

            # # Right: Social Media + k to Top
            # with ui.column().classes('items-center md:items-end flex-grow'):
            #     with ui.row().classes('q-gutter-sm items-center q-mb-sm'):
            #         ui.element('i').classes('ti-facebook text-gray-400 hover:text-[#00b074] text-lg cursor-pointer')
            #         ui.element('i').classes('ti-twitter-alt text-gray-400 hover:text-[#00b074] text-lg cursor-pointer')
            #         ui.element('i').classes('ti-linkedin text-gray-400 hover:text-[#00b074] text-lg cursor-pointer')
            #         ui.element('i').classes('ti-instagram text-gray-400 hover:text-[#00b074] text-lg cursor-pointer')
                
                ui.button('', icon='arrow_upward', on_click=scroll_to_top).props('flat dense color=white').classes('text-xs')

        # Divider
        ui.separator().classes('q-my-md bg-gray-700')

        # Bottom copyright
        with ui.row().classes('justify-center text-center w-full px-4 pb-4'):
            ui.label('© 2025 JobBoard Inc. All rights reserved.')
