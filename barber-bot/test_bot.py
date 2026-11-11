"""Тести без інтернету: python -m unittest -v"""
import asyncio
import os
import tempfile
import unittest
from datetime import date, datetime, timedelta
from unittest import mock

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession
from aiogram.methods import AnswerCallbackQuery, EditMessageText, SendMessage
from aiogram.types import CallbackQuery, Chat, Contact, Message, Update, User

import bot as B
from db import DB
from slots import free_starts, human_day


class SlotTests(unittest.TestCase):
    day = date(2026, 11, 9)  # понеділок
    now = datetime(2026, 11, 8, 12, 0)

    def test_full_day(self):
        s = free_starts(self.day, ("10:00", "20:00"), 60, [], self.now, 30, 60)
        self.assertEqual(s[0].strftime("%H:%M"), "10:00")
        self.assertEqual(s[-1].strftime("%H:%M"), "19:00")
        self.assertEqual(len(s), 19)

    def test_busy_blocks_overlaps(self):
        busy = [(datetime(2026, 11, 9, 12, 0), datetime(2026, 11, 9, 13, 0))]
        s = [t.strftime("%H:%M") for t in free_starts(self.day, ("10:00", "14:00"), 60, busy, self.now)]
        self.assertEqual(s, ["10:00", "10:30", "11:00", "13:00"])

    def test_lead_time_and_day_off(self):
        now = datetime(2026, 11, 9, 15, 10)
        s = free_starts(self.day, ("10:00", "20:00"), 30, [], now, 30, 60)
        self.assertEqual(s[0].strftime("%H:%M"), "16:30")
        self.assertEqual(free_starts(self.day, None, 30, [], now), [])

    def test_human_day(self):
        self.assertEqual(human_day(self.day), "Пн, 9 листопада")
        self.assertEqual(human_day(self.day, self.day), "Сьогодні, 9 листопада")


class DBTests(unittest.TestCase):
    def test_no_double_booking(self):
        db = DB(":memory:")
        st = datetime(2026, 11, 9, 10, 0)
        n = datetime(2026, 11, 8, 10, 0)
        self.assertIsNotNone(db.create(1, "b1", "cut", st, st + timedelta(hours=1), n))
        self.assertIsNone(db.create(2, "b1", "beard", st + timedelta(minutes=30), st + timedelta(hours=1), n))
        self.assertIsNotNone(db.create(2, "b2", "beard", st, st + timedelta(minutes=30), n))
        self.assertIsNotNone(db.create(3, "b1", "beard", st + timedelta(hours=1), st + timedelta(hours=1, minutes=30), n))


class FakeSession(BaseSession):
    def __init__(self):
        super().__init__()
        self.calls = []
        self.mid = 100

    async def close(self):
        pass

    async def stream_content(self, *a, **k):
        yield b""

    async def make_request(self, bot, method, timeout=None):
        self.calls.append(method)
        if isinstance(method, (SendMessage, EditMessageText)):
            self.mid += 1
            return Message(message_id=self.mid, date=datetime.now(),
                           chat=Chat(id=method.chat_id or 1, type="private"), text=method.text)
        return True


CLIENT = User(id=111, is_bot=False, first_name="Іван", username="ivan")
ADMIN = User(id=999, is_bot=False, first_name="Власник")


class FlowTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dp = B.setup(os.path.join(self.tmp, "t.db"), "999")
        self.session = FakeSession()
        self.bot = Bot("42:TEST", session=self.session,
                       default=DefaultBotProperties(parse_mode="HTML"))
        self.uid = 0
        # «Зараз» — понеділок 9 листопада 2026, 09:00
        self.p = mock.patch.object(B, "now", lambda: datetime(2026, 11, 9, 9, 0))
        self.p.start()

    async def asyncTearDown(self):
        self.p.stop()

    async def send(self, user, text=None, contact=None):
        self.uid += 1
        msg = Message(message_id=self.uid, date=datetime.now(), chat=Chat(id=user.id, type="private"),
                      from_user=user, text=text, contact=contact)
        self.session.calls.clear()
        await self.dp.feed_update(self.bot, Update(update_id=self.uid, message=msg))
        return self.session.calls

    async def click(self, user, data):
        self.uid += 1
        msg = Message(message_id=1, date=datetime.now(), chat=Chat(id=user.id, type="private"), text="x")
        cb = CallbackQuery(id=str(self.uid), from_user=user, chat_instance="c", message=msg, data=data)
        self.session.calls.clear()
        await self.dp.feed_update(self.bot, Update(update_id=self.uid, callback_query=cb))
        return self.session.calls

    @staticmethod
    def texts(calls):
        return [c.text for c in calls if isinstance(c, (SendMessage, EditMessageText))]

    @staticmethod
    def buttons(calls):
        out = []
        for c in calls:
            m = getattr(c, "reply_markup", None)
            if m is not None and hasattr(m, "inline_keyboard"):
                out += [b.callback_data for row in m.inline_keyboard for b in row]
        return out

    async def test_full_booking_flow(self):
        calls = await self.send(CLIENT, "/start")
        self.assertIn("Barber Studio", self.texts(calls)[0])

        calls = await self.send(CLIENT, B.BTN_BOOK)
        self.assertIn("svc:cut", self.buttons(calls))

        calls = await self.click(CLIENT, "svc:cut")
        self.assertIn("brb:any", self.buttons(calls))

        calls = await self.click(CLIENT, "brb:b1")
        days = [b for b in self.buttons(calls) if b.startswith("day:")]
        self.assertEqual(days[0], "day:2026-11-09")
        self.assertNotIn("day:2026-11-15", days)  # неділя — вихідний

        calls = await self.click(CLIENT, "day:2026-11-09")
        times = [b for b in self.buttons(calls) if b.startswith("tm:")]
        self.assertEqual(times[0], "tm:10:00")  # 09:00 + 60 хв

        calls = await self.click(CLIENT, "tm:10:00")
        self.assertTrue(any("номер телефону" in t for t in self.texts(calls)))

        calls = await self.send(CLIENT, "abc")
        self.assertIn("Не схоже", self.texts(calls)[0])

        calls = await self.send(CLIENT, contact=Contact(phone_number="380671234567", first_name="Іван"))
        self.assertIn("confirm", self.buttons(calls))

        calls = await self.click(CLIENT, "confirm")
        texts = self.texts(calls)
        self.assertIn("Ви записані", texts[0])
        admin_msgs = [c for c in calls if isinstance(c, SendMessage) and c.chat_id == 999]
        self.assertEqual(len(admin_msgs), 1)
        self.assertIn("+380671234567", admin_msgs[0].text)
        self.assertIn("10:00", admin_msgs[0].text)

        # Слот 10:00 і 10:30 у b1 тепер зайняті
        await self.click(CLIENT, "svc:cut")
        await self.click(CLIENT, "brb:b1")
        calls = await self.click(CLIENT, "day:2026-11-09")
        times = [b for b in self.buttons(calls) if b.startswith("tm:")]
        self.assertNotIn("tm:10:00", times)
        self.assertNotIn("tm:10:30", times)
        self.assertIn("tm:11:00", times)

        # Другий раз телефон не питають
        calls = await self.click(CLIENT, "tm:11:00")
        self.assertIn("confirm", self.buttons(calls))

        # Адмін бачить записи на сьогодні
        calls = await self.send(ADMIN, "/today")
        self.assertIn("10:00", self.texts(calls)[0])
        # Клієнт не бачить адмін-команд
        calls = await self.send(CLIENT, "/today")
        self.assertEqual(self.texts(calls), [])

        # Мої записи + скасування
        calls = await self.send(CLIENT, B.BTN_MY)
        cancel = [b for b in self.buttons(calls) if b.startswith("uc:")][0]
        calls = await self.click(CLIENT, cancel)
        self.assertIn("скасовано", self.texts(calls)[0])
        self.assertTrue(any(isinstance(c, SendMessage) and c.chat_id == 999 for c in calls))

    async def test_race_same_slot(self):
        other = User(id=222, is_bot=False, first_name="Петро")
        for u, phone in ((CLIENT, "0671111111"), (other, "0672222222")):
            await self.send(u, B.BTN_BOOK)
            await self.click(u, "svc:cut")
            await self.click(u, "brb:b1")
            await self.click(u, "day:2026-11-09")
            await self.click(u, "tm:12:00")
            await self.send(u, phone)
        await self.click(CLIENT, "confirm")
        calls = await self.click(other, "confirm")
        alerts = [c for c in calls if isinstance(c, AnswerCallbackQuery) and c.text]
        self.assertIn("щойно зайняли", alerts[0].text)

    async def test_any_barber_uses_second(self):
        for i, u in enumerate((CLIENT, User(id=333, is_bot=False, first_name="Ігор"))):
            await self.send(u, B.BTN_BOOK)
            await self.click(u, "svc:beard")
            await self.click(u, "brb:any")
            await self.click(u, "day:2026-11-09")
            await self.click(u, "tm:15:00")
            await self.send(u, f"067000000{i}")
            calls = await self.click(u, "confirm")
            self.assertIn("Ви записані", self.texts(calls)[0])
        rows = B.db.between(datetime(2026, 11, 9), datetime(2026, 11, 10))
        self.assertEqual(sorted(r["barber_id"] for r in rows), ["b1", "b2"])

    async def test_admin_cancel_notifies_client(self):
        await self.send(CLIENT, B.BTN_BOOK)
        await self.click(CLIENT, "svc:cut")
        await self.click(CLIENT, "brb:b2")
        await self.click(CLIENT, "day:2026-11-10")
        await self.click(CLIENT, "tm:14:00")
        await self.send(CLIENT, "0671234567")
        calls = await self.click(CLIENT, "confirm")
        ac = [b for b in self.buttons(calls) if b.startswith("ac:")][0]
        self.assertEqual(await self.click(CLIENT, ac) and None, None)  # клієнт не може
        self.assertEqual(B.db.get(int(ac[3:]))["status"], "active")
        calls = await self.click(ADMIN, ac)
        self.assertEqual(B.db.get(int(ac[3:]))["status"], "cancelled")
        self.assertTrue(any(isinstance(c, SendMessage) and c.chat_id == CLIENT.id for c in calls))

    async def test_reminders(self):
        await self.send(CLIENT, B.BTN_BOOK)
        await self.click(CLIENT, "svc:cut")
        await self.click(CLIENT, "brb:b1")
        await self.click(CLIENT, "day:2026-11-10")
        await self.click(CLIENT, "tm:12:00")   # завтра 12:00 (> 24 год від «зараз»)
        await self.send(CLIENT, "0671234567")
        await self.click(CLIENT, "confirm")

        def at(h, m=0, d=9):
            return mock.patch.object(B, "now", lambda: datetime(2026, 11, d, h, m))

        async def run():
            self.session.calls.clear()
            await B.send_reminders(self.bot)
            return [c for c in self.session.calls if isinstance(c, SendMessage)]

        with at(11, 30):
            self.assertEqual(await run(), [])            # ще більше 24 год
        with at(12, 5):
            sent = await run()
            self.assertEqual(len(sent), 1)
            self.assertIn("завтра", sent[0].text)
            self.assertEqual(await run(), [])            # не дублює
        with at(10, 30, 10):
            sent = await run()
            self.assertEqual(len(sent), 1)
            self.assertIn("сьогодні", sent[0].text)


if __name__ == "__main__":
    unittest.main()
