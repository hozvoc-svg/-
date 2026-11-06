"""Розрахунок вільного часу. Без Telegram — легко тестувати."""
from datetime import date, datetime, time, timedelta


def _hm(value: str) -> time:
    h, m = value.split(":")
    return time(int(h), int(m))


def free_starts(day: date, hours, minutes: int, busy, now: datetime,
                step: int = 30, lead: int = 60) -> list[datetime]:
    """Початки, з яких послуга тривалістю `minutes` влазить у робочий день
    і не перетинається з жодним інтервалом із `busy` [(start, end), ...]."""
    if not hours:
        return []
    start = datetime.combine(day, _hm(hours[0]))
    close = datetime.combine(day, _hm(hours[1]))
    earliest = now + timedelta(minutes=lead)
    length = timedelta(minutes=minutes)
    result = []
    t = start
    while t + length <= close:
        end = t + length
        if t >= earliest and all(end <= b0 or t >= b1 for b0, b1 in busy):
            result.append(t)
        t += timedelta(minutes=step)
    return result


WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
MONTHS = ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня",
          "серпня", "вересня", "жовтня", "листопада", "грудня"]


def human_day(d: date, today: date | None = None) -> str:
    if today is not None:
        if d == today:
            return f"Сьогодні, {d.day} {MONTHS[d.month - 1]}"
        if d == today + timedelta(days=1):
            return f"Завтра, {d.day} {MONTHS[d.month - 1]}"
    return f"{WEEKDAYS[d.weekday()]}, {d.day} {MONTHS[d.month - 1]}"
