import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from src.search import display, find, find_ranked


def test_single(capsys):
    index = {"hello": {1: 5, 2: 10}}
    display("hello", index)
    captured = capsys.readouterr()
    assert "Index position found for hello" in captured.out
    assert "Page: 1, Position: 5" in captured.out
    assert "Page: 2, Position: 10" in captured.out


def test_no_word(capsys):
    index = {"hello": {1: 5}}
    display("missing", index)
    captured = capsys.readouterr()
    assert "Word not found" in captured.out


def test_exactly_one(capsys):
    index = {"hello": {1: 5, 2: 10}}
    find("hello", index)
    captured = capsys.readouterr()
    assert "Pages containing query" in captured.out
    assert "1" in captured.out
    assert "2" in captured.out


def test_intersection(capsys):
    index = {"hello": {1: 5, 2: 10},"world": {2: 3, 3: 8}}
    find("hello world", index)
    captured = capsys.readouterr()
    assert "Pages containing query" in captured.out
    assert "2" in captured.out
    assert "1" not in captured.out
    assert "3" not in captured.out

def test_intersection_fail(capsys):
    index = {"hello": {1: 5}}
    find("hello missing", index)
    captured = capsys.readouterr()
    assert "Unable to find entry for: missing" in captured.out


def test_union_no_intersection(capsys):
    index = {"hello": {1: 5},"world": {2: 10}}
    find("hello world", index)
    captured = capsys.readouterr()
    assert "No pages located" in captured.out
    

def test_ranked():
    index = {"hello": {"page1": 1.0, "page2": 2.0},"world": {"page2": 1.5}}
    results = find_ranked("hello world", index)
    assert len(results) == 1
    assert results[0][0] == "page2"


def test_rankorder():
    index = {"hello": {"page1": 1.0, "page2": 3.0}}
    results = find_ranked("hello", index)
    assert results[0][0] == "page2"
    assert results[1][0] == "page1"


def test_rank_error(capsys):
    index = {"hello": {"page1": 1.0}}
    result = find_ranked("hello missing", index)
    captured = capsys.readouterr()
    assert "Unable to find entry for: missing" in captured.out
    assert result is None


def test_rank_intersection(capsys):
    index = {"hello": {"page1": 1.0},"world": {"page2": 1.0}}
    result = find_ranked("hello world", index)
    captured = capsys.readouterr()
    assert "No pages located" in captured.out
    assert result == [] or result is None


def test_ranked_all():
    index = {"hello": {"page1": 1.0, "page2": 2.0},"world": {"page1": 2.0, "page2": 1.0}}
    results = find_ranked("hello world", index)
    assert len(results) == 2
    assert set([r[0] for r in results]) == {"page1", "page2"}