from app.repositories import ReportRepository

def test_get_visits_page_with_existing_visits(example_visit_logs):
    page = 1
    per_page = 2
    pagination = ReportRepository.get_visits_page(page, per_page)
    
    assert pagination.total == len(example_visit_logs)
    assert len(pagination.items) == per_page
    assert pagination.items[0].path == example_visit_logs[2].path

def test_get_visits_page_with_empty_db():
    page = 1
    per_page = 10
    pagination = ReportRepository.get_visits_page(page, per_page)
    
    assert pagination.total == 0
    assert len(pagination.items) == 0

def test_get_page_stats_with_visits(example_visit_logs):
    stats = ReportRepository.get_page_stats()
    
    assert len(stats) == 3
    assert stats[0].path == '/page3' or stats[0].path == '/page1'
    assert stats[0].count == 1

def test_get_page_stats_with_empty_db():
    stats = ReportRepository.get_page_stats()
    assert len(stats) == 0

def test_get_user_stats_with_visits(example_visit_logs, existing_user):
    stats = ReportRepository.get_user_stats()
    
    assert len(stats) == 2
    assert stats[0].last_name == existing_user.last_name
    assert stats[0].first_name == existing_user.first_name
    assert stats[0].count == 2

def test_get_user_stats_with_empty_db():
    stats = ReportRepository.get_user_stats()
    assert len(stats) == 1

def test_get_anonymous_visits_count_with_visits(example_visit_logs):
    count = ReportRepository.get_anonymous_visits_count()
    assert count == 1

def test_get_anonymous_visits_count_with_empty_db(db_connector):
    count = ReportRepository.get_anonymous_visits_count()
    assert count == 0

def test_get_paginated_visits_with_filters(example_visit_logs, existing_user):
    filtered = ReportRepository.get_paginated_visits(
        filters={'user_id': existing_user.id}
    )
    assert filtered.total == 2
    for visit in filtered.items:
        assert visit.user_id == existing_user.id
    
    filtered = ReportRepository.get_paginated_visits(
        filters={'path': '/page2'}
    )
    assert filtered.total == 1
    assert filtered.items[0].path == '/page2'

def test_get_paginated_visits_with_ordering( example_visit_logs):
    ordered = ReportRepository.get_paginated_visits(
        order_by='path'
    )
    paths = [visit.path for visit in ordered.items]
    assert paths == sorted(paths, reverse=True)

def test_get_paginated_visits_with_pagination(example_visit_logs):
    per_page = 2
    page1 = ReportRepository.get_paginated_visits(page=1, per_page=per_page)
    page2 = ReportRepository.get_paginated_visits(page=2, per_page=per_page)
    
    assert len(page1.items) == per_page
    assert len(page2.items) == 1
    assert page1.items[0].id != page2.items[0].id