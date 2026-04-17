import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from src.search import display, find


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