import pytest

from src.infra.cache_keys import CacheKeys


class TestCacheKeys:
    def test_mark_key_format(self):
        assert CacheKeys.mark("food") == "mark:food"

    def test_mark_key_with_special_chars(self):
        assert CacheKeys.mark("На еду") == "mark:На еду"

    def test_marks_all_key(self):
        assert CacheKeys.marks_all() == "marks:all"

    def test_mark_cards_key_format(self):
        assert CacheKeys.mark_cards("savings") == "mark:savings:cards"

    def test_default_ttl(self):
        assert CacheKeys.DEFAULT_TTL == 3600

    def test_short_ttl(self):
        assert CacheKeys.SHORT_TTL == 300

    def test_mark_pattern(self):
        assert CacheKeys.mark_pattern() == "mark:*"
