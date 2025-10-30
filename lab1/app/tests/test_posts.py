def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.text

def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert "Об авторе" in response.text

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Задание к лабораторной работе" in response.text

def test_post(client):
    for i in range(5):
        response = client.get(f"/posts/{i}")
        assert response.status_code == 200
        assert "Заголовок поста" in response.text

def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1

def test_about_template(client, captured_templates):
    with captured_templates as templates:
        response = client.get('/about')
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'about.html'
        assert context['title'] == 'Об авторе'

def test_index_template(client, captured_templates):
    with captured_templates as templates:
        response = client.get('/')
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'index.html'

def test_post_template(client, captured_templates, mocker, posts_list):
    for i, post in enumerate(posts_list):
        with captured_templates as templates:
            mocker.patch(
                "app.posts_list",
                return_value=posts_list,
                autospec=True
            )

            response = client.get(f'/posts/{i}')
            assert response.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'post.html'
            assert context['title'] == post['title']
            assert context['post'] == post

def test_post_title(client, captured_templates, mocker, posts_list):
    for i, post in enumerate(posts_list):
        with captured_templates as templates:
            mocker.patch(
                "app.posts_list",
                return_value=posts_list,
                autospec=True
            )
            response = client.get(f'/posts/{i}')
            assert response.status_code == 200
            assert post['title'] in response.text

def test_post_text(client, captured_templates, mocker, posts_list):
    for i, post in enumerate(posts_list):
        with captured_templates as templates:
            mocker.patch(
                "app.posts_list",
                return_value=posts_list,
                autospec=True
            )
            response = client.get(f'/posts/{i}')
            assert response.status_code == 200
            assert post['text'] in response.text

def test_post_autor(client, captured_templates, mocker, posts_list):
    for i, post in enumerate(posts_list):
        with captured_templates as templates:
            mocker.patch(
                "app.posts_list",
                return_value=posts_list,
                autospec=True
            )
            response = client.get(f'/posts/{i}')
            assert response.status_code == 200
            assert post['author'] in response.text

def test_post_image(client, captured_templates, mocker, posts_list):
    for i, post in enumerate(posts_list):
        with captured_templates as templates:
            mocker.patch(
                "app.posts_list",
                return_value=posts_list,
                autospec=True
            )
            response = client.get(f'/posts/{i}')
            assert response.status_code == 200
            assert post['image_id'] in response.text

def test_post_comments(client, captured_templates, mocker, posts_list):
    for i, post in enumerate(posts_list):
        with captured_templates as templates:
            mocker.patch(
                "app.posts_list",
                return_value=posts_list,
                autospec=True
            )
            response = client.get(f'/posts/{i}')
            assert response.status_code == 200
            for comment in post['comments']:
                assert comment['author'] in response.text
                assert comment['text'] in response.text
                if comment['replies']:
                    for reply in comment['replies']:
                        assert reply['author'] in response.text
                        assert reply['text'] in response.text

def test_post_date_format(client, captured_templates, mocker, posts_list):
    for i, post in enumerate(posts_list):
        with captured_templates as templates:
            mocker.patch(
                "app.posts_list",
                return_value=posts_list,
                autospec=True
            )
            response = client.get(f'/posts/{i}')
            assert response.status_code == 200
            assert post['date'].strftime('%d.%m.%Y') in response.text

def test_post_not_found(client):
    response = client.get("/posts/9999")
    assert response.status_code == 404
