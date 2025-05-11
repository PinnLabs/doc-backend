import io


def test_convert_markdown_to_html_success(client):
    markdown_text = "# Hello\n\nThis is a *test*."
    file = {
        "file": ("test.md", io.BytesIO(markdown_text.encode("utf-8")), "text/markdown")
    }

    response = client.post("/api/v1/markdown/convert-to-html/", files=file)

    assert response.status_code == 200
    assert response.headers["content-disposition"].startswith("attachment; filename=")
    assert "<h1>Hello</h1>" in response.text
    assert "<em>test</em>" in response.text
    assert "<style>" in response.text  # CSS is included


def test_convert_html_with_empty_file(client):
    file = {"file": ("empty.md", io.BytesIO(b""), "text/markdown")}

    response = client.post("/api/v1/markdown/convert-to-html/", files=file)

    assert response.status_code == 200
    assert "<body></body>" in response.text or "<body>" in response.text


def test_convert_html_missing_file(client):
    response = client.post("/api/v1/markdown/convert-to-html/")

    assert response.status_code == 422  # Unprocessable Entity (missing required file)
