from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Mark, Card
from src.entity.repositories.mark_repository import MarkRepository
from src.infra.models import Mark as MarkModel, Card as CardModel


def _to_domain_mark(model: MarkModel) -> Mark:
    """Convert SQLAlchemy MarkModel to domain Mark entity."""
    cards = [
        Card(name=card.name, value=card.value)
        for card in model.cards
    ]
    mark = Mark(
        name=model.name,
        current=model.current,
        cards=cards,
        required=model.required,
    )
    return mark


def _to_db_mark(domain_mark: Mark) -> MarkModel:
    """Convert domain Mark entity to SQLAlchemy MarkModel."""
    return MarkModel(
        name=domain_mark.get_name(),
        current=domain_mark.get_current(),
        required=domain_mark.get_required(),
    )


class SQLAlchemyMarkRepository(MarkRepository):
    """Pure SQLAlchemy implementation of MarkRepository without caching."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, mark: Mark) -> None:
        db_mark = _to_db_mark(mark)
        for card in mark.get_cards():
            db_card = CardModel(name=card.get_name(), value=card.get_value(), mark_name=mark.get_name())
            db_mark.cards.append(db_card)
        self._session.add(db_mark)
        await self._session.flush()

    async def update(self, mark: Mark) -> None:
        result = await self._session.execute(
            select(MarkModel).where(MarkModel.name == mark.get_name())
        )
        db_mark = result.scalar_one()
        db_mark.current = mark.get_current()
        db_mark.required = mark.get_required()

        # Sync cards
        existing_cards = {c.name: c for c in db_mark.cards}
        domain_card_names = {c.get_name() for c in mark.get_cards()}

        # Delete removed cards
        for name in set(existing_cards.keys()) - domain_card_names:
            await self._session.delete(existing_cards[name])

        # Add/update cards
        for card in mark.get_cards():
            if card.get_name() in existing_cards:
                existing_cards[card.get_name()].value = card.get_value()
            else:
                db_card = CardModel(
                    name=card.get_name(),
                    value=card.get_value(),
                    mark_name=mark.get_name(),
                )
                db_mark.cards.append(db_card)

        await self._session.flush()

    async def delete(self, mark: Mark) -> None:
        result = await self._session.execute(
            select(MarkModel).where(MarkModel.name == mark.get_name())
        )
        db_mark = result.scalar_one()
        await self._session.delete(db_mark)
        await self._session.flush()

    async def get_by_name(self, name: str) -> Mark | None:
        result = await self._session.execute(
            select(MarkModel).where(MarkModel.name == name)
        )
        db_mark = result.scalar_one_or_none()
        if db_mark is None:
            return None
        return _to_domain_mark(db_mark)

    async def get_all(self) -> list[Mark]:
        result = await self._session.execute(select(MarkModel))
        db_marks = result.scalars().all()
        return [_to_domain_mark(m) for m in db_marks]
