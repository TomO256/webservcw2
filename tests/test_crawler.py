import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock

from src.crawler import crawlQuotes, crawlAuthors, crawl
from tests.offline_pages import *

@patch("src.crawler.requests.get")
def test_normal(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, text=get_page_one()),
        Mock(status_code=200, text=get_custom_quote_page("Final Quote","FinalAuthor"))
    ]
    content, authors = crawlQuotes([], "https://quotes.toscrape.com")
    assert isinstance(content, list)
    assert isinstance(authors, set)
    assert any("The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking" in text for _, text in content)
    assert any("Final Quote" in text for _, text in content)
    assert any("/author/Albert-Einstein" in a for a in authors)
    assert any("/author/FinalAuthor" in a for a in authors)

@patch("src.crawler.requests.get")
def test_crawl_quotes_stops_at_last_page(mock_get):
    mock_get.return_value = Mock(status_code=200, text=get_custom_quote_page("Final Page","Final Author"))
    content, authors = crawlQuotes([], "https://quotes.toscrape.com")
    assert len(content) == 1
    assert len(authors) >= 1

@patch("src.crawler.requests.get")
def test_crawl_authors(mock_get):
    mock_get.return_value = Mock(status_code=200, text=get_author_page("Author","Author's Bio"))
    authors = {"https://quotes.toscrape.com/author/Author1"}
    content = crawlAuthors([], authors)
    assert len(content) == 1
    url, text = content[0]
    assert "Author" in text
    assert "Author's Bio" in text

@patch("src.crawler.requests.get")
def test_full_crawl(mock_get):
    def fake_get(url, *args, **kwargs):
        if "/page/2" in url:
            return Mock(status_code=200, text=get_custom_quote_page("Second page quote","Second author"))
        return Mock(status_code=200, text=get_page_one())
    mock_get.side_effect = fake_get
    content = crawl()
    assert isinstance(content, list)
    assert len(content) >= 2
    texts = [t for _, t in content]
    assert any("The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking" in t for t in texts)
    assert any("Second page quote" in t for t in texts)


@patch("src.crawler.requests.get")
def test_handles_bad_response(mock_get):
    mock_get.return_value = Mock(status_code=404, text="")
    content, authors = crawlQuotes([], "https://quotes.toscrape.com")
    assert content == []
    assert authors == set()