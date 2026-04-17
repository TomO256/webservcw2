import sys
import os
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.indexer import createIndex, save, load

def test_create():
    content = [("url1", "Hello world"),("url2", "Hello again")]
    index = createIndex(content)
    assert isinstance(index, dict)
    assert "hello" in index
    assert "world" in index
    assert "again" in index
    assert "url1" in index["hello"]
    assert "url2" in index["hello"]
    assert index["hello"]["url1"] == [0]
    assert index["world"]["url1"] == [1]

def test_capitals():
    content = [("url1", "Hello, HELLO!! world...")]
    index = createIndex(content)
    assert "hello" in index
    assert "world" in index
    assert index["hello"]["url1"] == [0, 1]

def test_empty():
    content = [("url1", "!!! ??? ...")]
    index = createIndex(content)
    assert index == {}

def test_save(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    index = {"hello": {"url1": [0, 2]}}
    os.chdir(tmp_path)
    save(index)
    assert os.path.exists("data/index.json")
    loaded = load()
    assert loaded == index

def test_missing(tmp_path, capsys):
    os.chdir(tmp_path)
    result = load()
    captured = capsys.readouterr()
    assert result is False
    assert "Unable to find index.json" in captured.out