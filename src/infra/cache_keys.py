class CacheKeys:
    """Key patterns for Redis caching."""

    MARK = "mark:{name}"
    MARKS_ALL = "marks:all"
    MARK_CARDS = "mark:{name}:cards"

    # TTL in seconds
    DEFAULT_TTL = 3600
    SHORT_TTL = 300

    @classmethod
    def mark(cls, name: str) -> str:
        return cls.MARK.format(name=name)

    @classmethod
    def marks_all(cls) -> str:
        return cls.MARKS_ALL

    @classmethod
    def mark_cards(cls, name: str) -> str:
        return cls.MARK_CARDS.format(name=name)

    @classmethod
    def mark_pattern(cls) -> str:
        return "mark:*"
