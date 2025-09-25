from nicegui import ui
from services.api_service import APIService
from datetime import datetime
from time import monotonic
from urllib.parse import urlencode, quote_plus


def jobs_page():
    """Jobs page with client-side search, sorting, load-more pagination, placeholders, and a quick-view modal.

    Keeps the exact flyer rendering code from Manage Jobs when a flyer exists.
    """

    api_service = APIService()

    # ---------------------- Data fetch ----------------------
    def fetch_jobs():
        try:
            return api_service.get_jobs()
        except Exception as e:
            print(f"Error fetching jobs: {e}")
            return []

    # Initial fetch (no filters)
    jobs = fetch_jobs()

    # ---------------------- State ----------------------
    # Read initial query params (best-effort; gracefully falls back)
    def _read_query_params():
        try:
            client = ui.get_client()
            req = getattr(client, 'request', None)
            qp = getattr(req, 'query_params', None) if req is not None else None
            if qp is not None:
                try:
                    return dict(qp)
                except Exception:
                    return {}
        except Exception:
            return {}
        return {}

    params = _read_query_params()

    search_query = (params.get("search") or "")
    sort_mode = params.get("sort") or "Newest"  # Newest | Company | Title
    items_per_page = 9
    loaded_count = items_per_page
    server_paging = False
    page = 1

    # Debounce machinery
    debounce_delay = 0.35
    _dirty = False
    _due = 0.0
    last_server_query = None

    # UI control placeholders (set to None, assigned later in UI block)
    search_input = None
    sort_select = None
    count_label = None
    location_input = None
    job_type_select = None
    category_select = None
    remote_checkbox = None
    salary_min_input = None
    salary_max_input = None
    grid = None
    load_more_row = None
    dialog = None
    dialog_container = None

    # ---------------------- Helpers ----------------------
    def _text(v):
        return (str(v or "").strip()).lower()

    def _extract_timestamp(j: dict) -> float:
        v = j.get("posted_date") or j.get("date_posted") or j.get("created_at") or ""
        # Epoch milliseconds/seconds
        try:
            if isinstance(v, (int, float)):
                # assume seconds if small, ms if large
                return float(v if v < 10_000_000_000 else v / 1000.0)
            if isinstance(v, str):
                sv = v.strip()
                if sv.isdigit():
                    num = int(sv)
                    return float(num if num < 10_000_000_000 else num / 1000.0)
                # ISO-ish handling
                s = sv.replace("Z", "+00:00")
                try:
                    return datetime.fromisoformat(s).timestamp()
                except Exception:
                    pass
        except Exception:
            pass
        return 0.0

    def _is_active(j: dict) -> bool:
        status = _text(j.get("status"))
        if status in {"active", "open", "published"}:
            return True
        if status in {"closed", "inactive", "archived", "draft"}:
            return False
        # Heuristic: if posted_date exists, assume active
        return True

    def _job_matches(j: dict) -> bool:
        # Search match
        hay = " ".join([
            _text(j.get("title") or j.get("job_title")),
            _text(j.get("company")),
            _text(j.get("location")),
        ])
        if _text(search_query) not in hay:
            return False

        # Location filter
        try:
            if location_input is not None:
                loc_val = (location_input.value or "").strip().lower()
                if loc_val and loc_val not in _text(j.get("location")):
                    return False
        except Exception:
            pass

        # Job type filter
        try:
            if job_type_select is not None:
                jt = (job_type_select.value or "All")
                if jt != "All" and _text(j.get("job_type")) != _text(jt):
                    return False
        except Exception:
            pass

        # Category filter
        try:
            if category_select is not None:
                cat = (category_select.value or "All")
                if cat != "All" and _text(j.get("category")) != _text(cat):
                    return False
        except Exception:
            pass

        # Remote filter (heuristic)
        try:
            if remote_checkbox is not None and remote_checkbox.value:
                loc = _text(j.get("location"))
                typ = _text(j.get("job_type"))
                is_remote = bool(j.get("remote")) or ("remote" in loc) or ("remote" in typ)
                if not is_remote:
                    return False
        except Exception:
            pass

        # Salary filters (best-effort heuristic on salary string)
        try:
            if (salary_min_input is not None and salary_min_input.value not in (None, "")) or \
               (salary_max_input is not None and salary_max_input.value not in (None, "")):
                import re
                sal = j.get("salary") or ""
                nums = [int(n.replace(",", "")) for n in re.findall(r"\d{1,3}(?:,\d{3})*", sal)]
                j_min = nums[0] if nums else None
                j_max = nums[1] if len(nums) > 1 else j_min
                if salary_min_input is not None and salary_min_input.value not in (None, ""):
                    try:
                        if j_max is not None and j_max < int(float(salary_min_input.value)):
                            return False
                    except Exception:
                        pass
                if salary_max_input is not None and salary_max_input.value not in (None, ""):
                    try:
                        if j_min is not None and j_min > int(float(salary_max_input.value)):
                            return False
                    except Exception:
                        pass
        except Exception:
            pass

        return True

    def _apply_filters() -> list:
        # Client-side filtering + sorting fallback
        filtered = [j for j in jobs if _job_matches(j)]
        if sort_mode == "Company":
            filtered.sort(key=lambda j: _text(j.get("company")))
        elif sort_mode == "Title":
            filtered.sort(key=lambda j: _text(j.get("title") or j.get("job_title")))
        else:  # Newest
            filtered.sort(key=_extract_timestamp, reverse=True)
        return filtered

    def _push_url_state():
        try:
            q = {}
            if search_query:
                q["search"] = search_query
            if sort_mode and sort_mode != "Newest":
                q["sort"] = sort_mode
            query = ("?" + urlencode(q)) if q else ""
            js = (
                "(function(){try{var u=new URL(window.location);u.search='" + query.replace("'", "%27") + "';"
                "window.history.replaceState({},'',u.toString());}catch(e){}})();"
            )
            ui.run_javascript(js)
        except Exception:
            pass

    def _open_quick_view(job: dict):
        print(f"DEBUG: Opening job modal for job: {job.get('title')}")
        print(f"DEBUG: Job keys available: {list(job.keys())}")
        print(f"DEBUG: Description: {job.get('description', 'None')[:100] if job.get('description') else 'None'}")
        print(f"DEBUG: Requirements: {job.get('requirements', 'None')}")
        dialog_container.clear()
        with dialog_container:
            with ui.card().classes("w-[min(90vw,700px)] p-0"):
                # Header image
                if job.get("flyer"):
                    ui.image(job.get("flyer")).classes("w-full h-56 object-cover rounded-t-xl")
                else:
                    with ui.element("div").classes("w-full h-56 rounded-t-xl bg-gray-100 flex items-center justify-center border-b border-gray-200"):
                        ui.icon("insert_photo", size="2.5rem").classes("text-gray-400")

                with ui.column().classes("p-6 space-y-4"):
                    # Job title and company header
                    ui.label(job.get("title") or job.get("job_title", "Unknown")).classes("text-2xl font-bold text-[#2b3940]")
                    with ui.row().classes("gap-6 text-gray-600 items-center mb-4"):
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("business", size="1.2rem").classes("text-[#00b074]")
                            ui.label(job.get("company", "N/A")).classes("font-medium")
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("place", size="1.2rem").classes("text-[#00b074]")
                            ui.label(job.get("location", "N/A"))
                        
                    # Job badges (type, category, etc.)
                    with ui.row().classes("gap-3 mb-4 flex-wrap"):
                        if job.get("job_type"):
                            with ui.element("span").classes("px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"):
                                ui.label(job.get("job_type"))
                        if job.get("category"):
                            with ui.element("span").classes("px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium"):
                                ui.label(job.get("category"))
                        if job.get("salary"):
                            with ui.element("span").classes("px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"):
                                ui.label(job.get("salary"))
                        # Remote badge if applicable
                        if job.get("remote") or "remote" in str(job.get("location", "")).lower():
                            with ui.element("span").classes("px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium"):
                                ui.label("Remote")

                    # Job description section - ALWAYS SHOW
                    ui.label("Job Description").classes("text-lg font-semibold text-[#2b3940] mt-4 mb-2")
                    desc = job.get("description") or job.get("job_description") or "No job description available."
                    ui.label(str(desc)).classes("text-sm text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg mb-4")
                    
                    # Requirements section - ALWAYS SHOW
                    ui.label("Requirements").classes("text-lg font-semibold text-[#2b3940] mt-4 mb-2")
                    requirements = job.get("requirements") or job.get("job_requirements")
                    if requirements:
                        if isinstance(requirements, list):
                            with ui.column().classes("bg-gray-50 p-4 rounded-lg mb-4"):
                                for req in requirements:
                                    with ui.row().classes("items-start gap-2 mb-2"):
                                        ui.icon("check_circle", size="1rem").classes("text-[#00b074] mt-0.5 flex-shrink-0")
                                        ui.label(str(req)).classes("text-sm text-gray-700")
                        else:
                            ui.label(str(requirements)).classes("text-sm text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg whitespace-pre-line mb-4")
                    else:
                        ui.label("Requirements will be discussed during the application process.").classes("text-sm text-gray-500 leading-relaxed bg-gray-50 p-4 rounded-lg italic mb-4")

                    # Benefits section
                    benefits = job.get("benefits")
                    if benefits:
                        ui.label("Benefits").classes("text-lg font-semibold text-[#2b3940] mt-4")
                        if isinstance(benefits, list):
                            with ui.row().classes("gap-2 flex-wrap bg-gray-50 p-4 rounded-lg"):
                                for benefit in benefits:
                                    with ui.element("span").classes("px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm"):
                                        ui.label(benefit)
                        else:
                            ui.label(str(benefits)).classes("text-sm text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg")

                    # Company details section
                    ui.label("Company Information").classes("text-lg font-semibold text-[#2b3940] mt-4")
                    with ui.column().classes("bg-gray-50 p-4 rounded-lg space-y-2"):
                        if job.get("company"):
                            with ui.row().classes("items-center gap-2"):
                                ui.icon("business", size="1rem").classes("text-[#00b074]")
                                ui.label(f"Company: {job.get('company')}").classes("text-sm text-gray-700")
                        if job.get("location"):
                            with ui.row().classes("items-center gap-2"):
                                ui.icon("place", size="1rem").classes("text-[#00b074]")
                                ui.label(f"Location: {job.get('location')}").classes("text-sm text-gray-700")
                        if job.get("job_type"):
                            with ui.row().classes("items-center gap-2"):
                                ui.icon("work", size="1rem").classes("text-[#00b074]")
                                ui.label(f"Type: {job.get('job_type')}").classes("text-sm text-gray-700")

                    # Additional job details
                    with ui.row().classes("gap-6 mt-4 text-sm text-gray-600"):
                        if job.get("posted_date") or job.get("date_posted"):
                            with ui.row().classes("items-center gap-1"):
                                ui.icon("schedule", size="1rem").classes("text-[#00b074]")
                                ui.label(f"Posted: {job.get('posted_date') or job.get('date_posted')}")
                        if job.get("experience_level"):
                            with ui.row().classes("items-center gap-1"):
                                ui.icon("school", size="1rem").classes("text-[#00b074]")
                                ui.label(f"Level: {job.get('experience_level')}")
                        if job.get("application_count", 0) > 0:
                            with ui.row().classes("items-center gap-1"):
                                ui.icon("people", size="1rem").classes("text-[#00b074]")
                                ui.label(f"{job.get('application_count')} applications")

                    with ui.row().classes("justify-between mt-4"):
                        ui.button("Close", on_click=dialog.close).props("outline").style("border-color: #2b3940 !important; color: #2b3940 !important;")
                        ui.button("Apply Now", on_click=lambda j=job: (ui.notify(f"Applied to {j.get('title', 'job')}", type="positive"), dialog.close())).style("background-color: #00b074 !important; color: white !important;")

        dialog.open()

    def _translate_sort_for_server(mode: str) -> str:
        # Heuristic mapping; server can ignore unknown values safely
        if mode == "Company":
            return "company:asc"
        if mode == "Title":
            return "title:asc"
        return "created_at:desc"  # Newest

    def _build_filters(include_pagination: bool = False) -> dict:
        f = {}
        if search_query:
            # Send common alternatives; server will ignore unknowns
            f["search"] = search_query
            f["q"] = search_query
            f["keyword"] = search_query
        # Sort hint for server
        f["sort"] = _translate_sort_for_server(sort_mode)
        # Sidebar filters -> server
        try:
            loc_val = (location_input.value or "").strip()
            if loc_val:
                f["location"] = loc_val
        except Exception:
            pass
        try:
            jt = (job_type_select.value or "All")
            if jt and jt != "All":
                f["employment_type"] = jt
                f["job_type"] = jt
        except Exception:
            pass
        try:
            cat = (category_select.value or "All")
            if cat and cat != "All":
                f["category"] = cat
        except Exception:
            pass
        try:
            if remote_checkbox.value:
                f["remote"] = True
        except Exception:
            pass
        try:
            if 'salary_min_input' in locals() and salary_min_input.value not in (None, ""):
                f["min_salary"] = int(float(salary_min_input.value))
        except Exception:
            pass
        try:
            if 'salary_max_input' in locals() and salary_max_input.value not in (None, ""):
                f["max_salary"] = int(float(salary_max_input.value))
        except Exception:
            pass
        if include_pagination:
            f["page"] = page
            f["limit"] = items_per_page
        return f

    def _analyze_meta_and_set_paging(meta: dict, batch_count: int):
        nonlocal server_paging
        # Consider server paging active if meta hints at pagination or batch size equals page size
        if meta and ("total" in meta or "page" in meta or "limit" in meta or "next" in meta or "prev" in meta):
            server_paging = True
        elif batch_count == items_per_page:
            server_paging = True
        else:
            server_paging = False

    def _server_fetch(reset: bool = False):
        nonlocal jobs
        filters = _build_filters(include_pagination=True)
        result = api_service.get_jobs_with_meta(filters)
        batch = result.get("jobs", [])
        meta = result.get("meta", {})
        _analyze_meta_and_set_paging(meta, len(batch))
        if reset:
            jobs = batch
        else:
            # Append unique by id to avoid duplicates
            seen = {j.get("id") for j in jobs}
            jobs.extend([b for b in batch if b.get("id") not in seen])

    def _refetch_from_server_if_needed():
        nonlocal jobs, last_server_query, page
        q = _text(search_query)
        try:
            # Only query server when search has at least 2 chars to avoid noisy calls
            if q and len(q) >= 2 and q != _text(last_server_query or ""):
                page = 1
                _server_fetch(reset=True)
                last_server_query = search_query
            # When search is cleared, refresh from server once to reset
            if not q and last_server_query is not None:
                page = 1
                _server_fetch(reset=True)
                last_server_query = None
        except Exception as ex:
            print(f"Server search fallback due to error: {ex}")

    # ---------------------- UI ----------------------
    with ui.element("div").classes("container mx-auto px-6 py-8"):
        # Hero
        with ui.element("div").classes("mb-6 rounded-xl bg-gradient-to-r from-[#e6f7f1] to-white p-8 border border-[#d9efe7]"):
            ui.label("Discover Jobs").classes("text-3xl font-bold text-[#2b3940] mb-2")
            ui.label("Find your next opportunity. Filter, sort, and preview quickly.").classes("text-[#556a76]")

        # Layout: Sidebar (filters) + Main content
        with ui.element("div").classes("grid grid-cols-1 lg:grid-cols-4 gap-6"):
            # Sidebar: Filters
            with ui.element("div").classes("order-1 lg:order-1 lg:col-span-1"):
                with ui.card().classes("p-4 sticky top-4"):
                    ui.label("Filters").classes("text-lg font-semibold mb-2")

                    # Search
                    search_input = ui.input(placeholder="Search by title, company, or location").props("clearable dense").classes("w-full mb-3")

                    # Location
                    location_input = ui.input(label="Location", placeholder="e.g., Remote or City").props("dense").classes("w-full mb-3")

                    # Job Type
                    job_type_select = ui.select(["All", "Full-time", "Part-time", "Contract", "Internship", "Temporary"], value="All", label="Job Type").props("dense").classes("w-full mb-3")

                    # Category
                    try:
                        categories = api_service.get_job_categories() or []
                    except Exception:
                        categories = []
                    category_select = ui.select(["All", *categories], value="All", label="Category").props("dense").classes("w-full mb-3")

                    # Remote only
                    remote_checkbox = ui.checkbox("Remote only").classes("mb-3")

                    # # Salary range
                    # with ui.row().classes("gap-3"):
                    #     salary_min_input = ui.number(label="Min Salary", format="%.0f").props("dense").classes("w-1/2")
                    #     salary_max_input = ui.number(label="Max Salary", format="%.0f").props("dense").classes("w-1/2")

                    with ui.row().classes("justify-between mt-4"):
                        ui.button("Reset", on_click=lambda: _reset_filters()).props("outline").style("border-color: #2b3940 !important; color: #2b3940 !important;").classes("hover:bg-[#2b3940] hover:text-white")
                        ui.button("Apply", on_click=lambda: _on_filters_change()).style("background-color: #00b074 !important; color: white !important;")

            # Main content
            with ui.element("div").classes("order-2 lg:order-2 lg:col-span-3"):
                with ui.row().classes("items-center justify-between gap-4 mb-2 flex-wrap"):
                    # Count label
                    count_label = ui.label().classes("text-sm text-gray-600")
                    sort_select = ui.select(["Newest", "Company", "Title"], value=sort_mode, label="Sort by").props("dense").classes("w-full md:w-44")

                # Grid container and dialog setup
                grid = ui.element("div").classes("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-2")
                load_more_row = ui.row().classes("justify-center mt-6")

                dialog = ui.dialog()
                with dialog:
                    dialog_container = ui.element("div")

    # ---------------------- Actions ----------------------
    def _refresh():
        nonlocal loaded_count
        filtered = _apply_filters()
        count_label.set_text(f"Jobs ({len(filtered)})")

        grid.clear()

        for job in filtered[:loaded_count]:
            # Clickable card for quick view
            with grid:
                card = ui.element("div").classes("bg-white rounded-xl shadow-sm border border-gray-200 p-4 cursor-pointer hover:shadow-md transition-shadow flex flex-col justify-between").on("click", lambda e=None, j=job: _open_quick_view(j))
                with card:
                    with ui.column().classes("w-full space-y-4"):
                        # EXACT flyer code from Manage Jobs (preserved) + skeleton shimmer + status badge
                        if job.get("flyer"):
                            with ui.element("div").classes("relative w-full h-40 rounded-md overflow-hidden"):
                                skeleton = ui.element("div").classes("absolute inset-0 animate-pulse bg-gray-200")
                                # EXACT vendor image classes preserved
                                img = ui.image(job.get("flyer")).classes("w-full h-40 object-cover rounded-md")
                                img.on("load", lambda e=None, sk=skeleton: sk.delete())
                                # Active/Closed status badge on top right of flyer
                                active = _is_active(job)
                                badge_color = "bg-[#00b074] text-white" if active else "bg-gray-500 text-white"
                                with ui.element("div").classes(f"absolute top-2 right-2 px-2 py-1 rounded-full text-xs font-medium {badge_color}"):
                                    ui.label("Active" if active else "Closed")
                        else:
                            # Placeholder with the same size to preserve layout + status badge
                            with ui.element("div").classes("relative w-full h-40 rounded-md bg-gray-100 flex items-center justify-center border border-gray-200"):
                                ui.icon("insert_photo", size="2rem").classes("text-gray-400")
                                # Active/Closed status badge on top right of placeholder
                                active = _is_active(job)
                                badge_color = "bg-[#00b074] text-white" if active else "bg-gray-500 text-white"
                                with ui.element("div").classes(f"absolute top-2 right-2 px-2 py-1 rounded-full text-xs font-medium {badge_color}"):
                                    ui.label("Active" if active else "Closed")

                        with ui.column().classes("space-y-1"):
                            ui.label(job.get("title") or job.get("job_title", "Unknown")).classes("font-semibold text-lg text-[#2b3940]")
                            ui.label(job.get("company", "N/A")).classes("text-sm text-gray-600")
                            ui.label(job.get("location", "N/A")).classes("text-sm text-gray-500")

                        with ui.row().classes("justify-between text-sm"):
                            with ui.row().classes("items-center space-x-1"):
                                ui.icon("people", size="1rem").classes("text-[#00b074]")
                                ui.label(f"{job.get('application_count', 0)} applications").classes("text-gray-600")
                            with ui.row().classes("items-center space-x-1"):
                                ui.icon("visibility", size="1rem").classes("text-[#00b074]")
                                ui.label(f"{job.get('view_count', 0)} views").classes("text-gray-600")

                    with ui.row().classes("w-full justify-center items-center pt-4 border-t border-gray-100 mt-4 space-x-3"):
                        ui.button("View", on_click=lambda j=job: _open_quick_view(j)).style("background-color: #00b074 !important; color: white !important; font-size: 0.75rem !important; padding: 0.25rem 0.75rem !important;")
                        ui.button("Save", on_click=lambda j=job: ui.notify("Saved to Favourite")).props("outline").style("border-color: #2b3940 !important; color: #2b3940 !important; font-size: 0.75rem !important; padding: 0.25rem 0.75rem !important;")

        # Load more control
        load_more_row.clear()
        # If server paging active, always show load more when last batch likely not final
        show_load_more = False
        if server_paging:
            show_load_more = True
        else:
            show_load_more = len(filtered) > loaded_count
        if show_load_more:
            with load_more_row:
                ui.button("Load more", on_click=lambda: _load_more()).props("outline").style("border-color: #2b3940 !important; color: #2b3940 !important; padding-left: 1.5rem !important; padding-right: 1.5rem !important;")
        # Update URL after refresh
        _push_url_state()

    def _load_more():
        nonlocal loaded_count, page
        if server_paging:
            page += 1
            try:
                _server_fetch(reset=False)
            except Exception as ex:
                print(f"Server paging fallback due to error: {ex}")
        else:
            loaded_count += items_per_page
        _refresh()

    def _open_quick_view(job: dict):
        dialog_container.clear()
        with dialog_container:
            with ui.card().classes("w-[min(90vw,700px)] p-0"):
                # Header image
                if job.get("flyer"):
                    ui.image(job.get("flyer")).classes("w-full h-56 object-cover rounded-t-xl")
                else:
                    with ui.element("div").classes("w-full h-56 rounded-t-xl bg-gray-100 flex items-center justify-center border-b border-gray-200"):
                        ui.icon("insert_photo", size="2.5rem").classes("text-gray-400")

                with ui.column().classes("p-5 space-y-2"):
                    ui.label(job.get("title") or job.get("job_title", "Unknown")).classes("text-xl font-semibold text-[#2b3940]")
                    with ui.row().classes("gap-4 text-gray-600 items-center"):
                        ui.icon("business", size="1rem").classes("text-[#00b074]")
                        ui.label(job.get("company", "N/A"))
                        ui.icon("place", size="1rem").classes("ml-4 text-[#00b074]")
                        ui.label(job.get("location", "N/A"))

                    desc = job.get("description") or job.get("job_description") or "No description available."
                    ui.label(desc).classes("text-sm text-gray-700 leading-relaxed")

                    with ui.row().classes("justify-between mt-4"):
                        ui.button("Close", on_click=dialog.close).props("outline").style("border-color: #2b3940 !important; color: #2b3940 !important;")
                        ui.button("Apply Now", on_click=lambda j=job: (ui.notify(f"Applied to {j.get('title', 'job')}", type="positive"), dialog.close())).style("background-color: #00b074 !important; color: white !important;")

        dialog.open()

    # Wire up controls
    def _on_search_change():
        nonlocal search_query, loaded_count, _dirty, _due
        search_query = _text(search_input.value)
        loaded_count = items_per_page
        _dirty = True
        _due = monotonic() + debounce_delay

    def _on_sort_change():
        nonlocal sort_mode, loaded_count
        sort_mode = sort_select.value or "Newest"
        loaded_count = items_per_page
        _refresh()

    def _debounce_tick():
        nonlocal _dirty
        if _dirty and monotonic() >= _due:
            _dirty = False
            _refetch_from_server_if_needed()
            _refresh()

    def _on_filters_change():
        nonlocal loaded_count, page
        loaded_count = items_per_page
        page = 1
        _refetch_from_server_if_needed()
        _refresh()

    def _reset_filters():
        try:
            search_input.set_value("")
        except Exception:
            pass
        try:
            location_input.set_value("")
            job_type_select.set_value("All")
            category_select.set_value("All")
            remote_checkbox.set_value(False)
            salary_min_input.set_value(None)
            salary_max_input.set_value(None)
        except Exception:
            pass
        _on_filters_change()

    search_input.on("change", lambda e: _on_search_change())
    # Update on typing with debounce
    search_input.on("keydown", lambda e: _on_search_change())
    sort_select.on("change", lambda e: _on_sort_change())
    # Sidebar filters
    try:
        location_input.on("change", lambda e: (_on_filters_change()))
        job_type_select.on("change", lambda e: (_on_filters_change()))
        category_select.on("change", lambda e: (_on_filters_change()))
        remote_checkbox.on("change", lambda e: (_on_filters_change()))
        salary_min_input.on("change", lambda e: (_on_filters_change()))
        salary_max_input.on("change", lambda e: (_on_filters_change()))
    except Exception:
        pass

    # Initial render
    # Initialize controls with query param values
    if search_query:
        try:
            search_input.set_value(search_query)
        except Exception:
            pass
    # ensure sort_mode is valid
    if sort_mode not in {"Newest", "Company", "Title"}:
        sort_mode = "Newest"
    try:
        sort_select.set_value(sort_mode)
    except Exception:
        pass

    # Start debounce timer (temporarily disabled for debugging)
    # ui.timer(0.15, _debounce_tick)

    # Initial render with flyers and modal
    if not jobs:
        with grid:
            ui.label("No jobs available").classes("text-center text-gray-500 col-span-full")
    else:
        # Show jobs with flyers
        for i, job in enumerate(jobs[:9]):  # Show 9 jobs (3x3 grid)
            with grid:
                # Clickable card for quick view
                card = ui.element("div").classes("bg-white rounded-xl shadow-sm border border-gray-200 p-4 cursor-pointer hover:shadow-md transition-shadow flex flex-col justify-between").on("click", lambda e=None, j=job: _open_quick_view(j))
                with card:
                    with ui.column().classes("w-full space-y-4"):
                        # EXACT flyer code from Manage Jobs (preserved) + skeleton shimmer + status badge
                        if job.get("flyer"):
                            with ui.element("div").classes("relative w-full h-40 rounded-md overflow-hidden"):
                                skeleton = ui.element("div").classes("absolute inset-0 animate-pulse bg-gray-200")
                                # EXACT vendor image classes preserved
                                img = ui.image(job.get("flyer")).classes("w-full h-40 object-cover rounded-md")
                                img.on("load", lambda e=None, sk=skeleton: sk.delete())
                                # Active/Closed status badge on top right of flyer
                                active = _is_active(job)
                                badge_color = "bg-[#00b074] text-white" if active else "bg-gray-500 text-white"
                                with ui.element("div").classes(f"absolute top-2 right-2 px-2 py-1 rounded-full text-xs font-medium {badge_color}"):
                                    ui.label("Active" if active else "Closed")
                        else:
                            # Placeholder with the same size to preserve layout + status badge
                            with ui.element("div").classes("relative w-full h-40 rounded-md bg-gray-100 flex items-center justify-center border border-gray-200"):
                                ui.icon("insert_photo", size="2rem").classes("text-gray-400")
                                # Active/Closed status badge on top right of placeholder
                                active = _is_active(job)
                                badge_color = "bg-[#00b074] text-white" if active else "bg-gray-500 text-white"
                                with ui.element("div").classes(f"absolute top-2 right-2 px-2 py-1 rounded-full text-xs font-medium {badge_color}"):
                                    ui.label("Active" if active else "Closed")

                        with ui.column().classes("space-y-1"):
                            ui.label(job.get("title") or job.get("job_title", "Unknown")).classes("font-semibold text-lg text-[#2b3940]")
                            ui.label(job.get("company", "N/A")).classes("text-sm text-gray-600")
                            ui.label(job.get("location", "N/A")).classes("text-sm text-gray-500")

                        with ui.row().classes("justify-between text-sm"):
                            with ui.row().classes("items-center space-x-1"):
                                ui.icon("people", size="1rem").classes("text-[#00b074]")
                                ui.label(f"{job.get('application_count', 0)} applications").classes("text-gray-600")
                            with ui.row().classes("items-center space-x-1"):
                                ui.icon("visibility", size="1rem").classes("text-[#00b074]")
                                ui.label(f"{job.get('view_count', 0)} views").classes("text-gray-600")

                    with ui.row().classes("w-full justify-center items-center pt-4 border-t border-gray-100 mt-4 space-x-3"):
                        ui.button("View", on_click=lambda j=job: _open_quick_view(j)).style("background-color: #00b074 !important; color: white !important; font-size: 0.75rem !important; padding: 0.25rem 0.75rem !important;")
                        ui.button("Save", on_click=lambda j=job: ui.notify("Saved")).props("outline").style("border-color: #2b3940 !important; color: #2b3940 !important; font-size: 0.75rem !important; padding: 0.25rem 0.75rem !important;")