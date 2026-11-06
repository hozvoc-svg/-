"""Telegram-бот запису в барбершоп. Запуск: python bot.py"""
import asyncio
import html
import logging
import os
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup)

import config as C
from db import DB, FMT
from slots import free_starts, human_day

TZ = ZoneInfo(C.TIMEZONE)
SERVICES = {s["id"]: s for s in C.SERVICES}
BARBERS = {b["id"]: b for b in C.BARBERS}
ANY = "any"

BTN_BOOK = "✂️ Записатися"
BTN_MY = "📋 Мої записи"
BTN_PRICES = "💈 Послуги і ціни"
BTN_CONTACTS = "📍 Контакти"

router = Router()
db: DB  # ініціалізується в main()
ADMIN_IDS: set[int] = set()


class Booking(StatesGroup):
    phone = State()


def now() -> datetime:
    return datetime.now(TZ).replace(tzinfo=None, second=0, microsecond=0)


def esc(value) -> str:
    return html.escape(str(value or ""))


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text=BTN_BOOK)],
        [KeyboardButton(text=BTN_MY), KeyboardButton(text=BTN_PRICES)],
        [KeyboardButton(text=BTN_CONTACTS)],
    ])


def kb(rows) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t, callback_data=d) for t, d in row] for row in rows])


def chunk(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


# ---------- доступний час ----------

def barbers_for(barber_id: str) -> list[str]:
    return list(BARBERS) if barber_id == ANY else [barber_id]


def free_times(day, service_id: str, barber_id: str) -> dict[datetime, list[str]]:
    """{час: [вільні майстри]} для дня."""
    minutes = SERVICES[service_id]["minutes"]
    hours = C.WORK_HOURS.get(day.weekday())
    result: dict[datetime, list[str]] = {}
    for b in barbers_for(barber_id):
        for t in free_starts(day, hours, minutes, db.busy(b, day.isoformat()), now(),
                             C.SLOT_STEP_MIN, C.MIN_LEAD_MIN):
            result.setdefault(t, []).append(b)
    return dict(sorted(result.items()))


def open_days(service_id: str, barber_id: str):
    today = now().date()
    days = (today + timedelta(days=i) for i in range(C.DAYS_AHEAD))
    return [d for d in days if free_times(d, service_id, barber_id)]


# ---------- тексти ----------

def booking_text(row, for_admin=False) -> str:
    start = datetime.strptime(row["start"], FMT)
    s = SERVICES.get(row["service_id"], {"name": row["service_id"], "price": "?"})
    barber = BARBERS.get(row["barber_id"], {"name": row["barber_id"]})["name"]
    lines = [
        f"🗓 <b>{human_day(start.date(), now().date())}, {start:%H:%M}</b>",
        f"✂️ {esc(s['name'])} — {s['price']} грн",
        f"💈 Майстер: {esc(barber)}",
    ]
    if for_admin:
        who = esc(row["user_name"])
        if row["username"]:
            who += f" (@{esc(row['username'])})"
        lines += [f"👤 {who}", f"📞 {esc(row['phone'])}"]
    return "\n".join(lines)


def prices_text() -> str:
    lines = [f"💈 <b>Послуги {esc(C.BUSINESS_NAME)}</b>\n"]
    for s in C.SERVICES:
        lines.append(f"• {esc(s['name'])} — <b>{s['price']} грн</b> ({s['minutes']} хв)")
    return "\n".join(lines)


def contacts_text() -> str:
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    sched = "\n".join(
        f"{days[i]}: {h[0]}–{h[1]}" if h else f"{days[i]}: вихідний"
        for i, h in sorted(C.WORK_HOURS.items()))
    parts = [f"📍 <b>{esc(C.BUSINESS_NAME)}</b>", esc(C.ADDRESS), f"📞 {esc(C.PHONE)}"]
    if C.MAP_URL:
        parts.append(f'<a href="{esc(C.MAP_URL)}">Відкрити на карті</a>')
    if C.INSTAGRAM:
        parts.append(f'<a href="{esc(C.INSTAGRAM)}">Instagram</a>')
    return "\n".join(parts) + f"\n\n🕒 <b>Графік</b>\n{sched}"


# ---------- клієнт: меню ----------

@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    db.upsert_user(msg.from_user.id, msg.from_user.full_name, msg.from_user.username)
    await msg.answer(C.GREETING, reply_markup=main_menu())


@router.message(Command("myid"))
async def my_id(msg: Message):
    await msg.answer(f"Ваш Telegram ID: <code>{msg.from_user.id}</code>")


@router.message(F.text == BTN_PRICES)
async def prices(msg: Message):
    await msg.answer(prices_text())


@router.message(F.text == BTN_CONTACTS)
async def contacts(msg: Message):
    await msg.answer(contacts_text(), disable_web_page_preview=True)


@router.message(F.text == BTN_MY)
async def my_bookings(msg: Message):
    rows = db.user_upcoming(msg.from_user.id, now())
    if not rows:
        await msg.answer("У вас немає майбутніх записів.", reply_markup=kb([[(BTN_BOOK, "book")]]))
        return
    for r in rows:
        await msg.answer(booking_text(r), reply_markup=kb([[("❌ Скасувати запис", f"uc:{r['id']}")]]))


# ---------- клієнт: запис ----------

def services_kb():
    rows = [[(f"{s['name']} · {s['price']} грн", f"svc:{s['id']}")] for s in C.SERVICES]
    return kb(rows)


@router.message(F.text == BTN_BOOK)
async def book(msg: Message, state: FSMContext):
    await state.clear()
    db.upsert_user(msg.from_user.id, msg.from_user.full_name, msg.from_user.username)
    await msg.answer("Оберіть послугу:", reply_markup=services_kb())


@router.callback_query(F.data == "book")
async def book_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer("Оберіть послугу:", reply_markup=services_kb())
    await cb.answer()


async def show_barbers(cb: CallbackQuery, state: FSMContext):
    if len(BARBERS) == 1:
        await state.update_data(barber=next(iter(BARBERS)))
        return await show_days(cb, state)
    rows = [[("🎲 Будь-який вільний майстер", f"brb:{ANY}")]]
    rows += chunk([(b["name"], f"brb:{b['id']}") for b in C.BARBERS], 2)
    rows.append([("⬅️ Назад", "back:svc")])
    await cb.message.edit_text("Оберіть майстра:", reply_markup=kb(rows))


async def show_days(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    days = open_days(data["service"], data["barber"])
    back = "back:brb" if len(BARBERS) > 1 else "back:svc"
    if not days:
        await cb.message.edit_text("На найближчі дні вільного часу немає 😔\n"
                                   f"Зателефонуйте нам: {esc(C.PHONE)}",
                                   reply_markup=kb([[("⬅️ Назад", back)]]))
        return
    today = now().date()
    rows = chunk([(human_day(d, today), f"day:{d.isoformat()}") for d in days], 2)
    rows.append([("⬅️ Назад", back)])
    await cb.message.edit_text("Оберіть день:", reply_markup=kb(rows))


async def show_times(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    day = datetime.strptime(data["day"], "%Y-%m-%d").date()
    times = free_times(day, data["service"], data["barber"])
    if not times:
        await cb.answer("Цей день уже зайнятий, оберіть інший", show_alert=True)
        return await show_days(cb, state)
    rows = chunk([(f"{t:%H:%M}", f"tm:{t:%H:%M}") for t in times], 4)
    rows.append([("⬅️ Назад", "back:day")])
    await cb.message.edit_text(f"{human_day(day, now().date())}. Оберіть час:", reply_markup=kb(rows))


def summary(data) -> str:
    s = SERVICES[data["service"]]
    day = datetime.strptime(data["day"], "%Y-%m-%d").date()
    barber = "будь-який вільний" if data["barber"] == ANY else BARBERS[data["barber"]]["name"]
    return ("Перевірте, будь ласка:\n\n"
            f"✂️ {esc(s['name'])} — {s['price']} грн\n"
            f"💈 Майстер: {esc(barber)}\n"
            f"🗓 <b>{human_day(day, now().date())}, {data['time']}</b>")


CONFIRM_KB = kb([[("✅ Підтвердити", "confirm")], [("⬅️ Змінити час", "back:time")]])


@router.callback_query(F.data.startswith("svc:"))
async def pick_service(cb: CallbackQuery, state: FSMContext):
    sid = cb.data[4:]
    if sid not in SERVICES:
        return await cb.answer()
    await state.update_data(service=sid)
    await show_barbers(cb, state)
    await cb.answer()


@router.callback_query(F.data.startswith("brb:"))
async def pick_barber(cb: CallbackQuery, state: FSMContext):
    bid = cb.data[4:]
    if bid != ANY and bid not in BARBERS:
        return await cb.answer()
    await state.update_data(barber=bid)
    await show_days(cb, state)
    await cb.answer()


@router.callback_query(F.data.startswith("day:"))
async def pick_day(cb: CallbackQuery, state: FSMContext):
    await state.update_data(day=cb.data[4:])
    await show_times(cb, state)
    await cb.answer()


@router.callback_query(F.data.startswith("tm:"))
async def pick_time(cb: CallbackQuery, state: FSMContext):
    await state.update_data(time=cb.data[3:])
    data = await state.get_data()
    if "service" not in data or "day" not in data:
        await cb.answer("Почніть запис спочатку", show_alert=True)
        return
    user = db.get_user(cb.from_user.id)
    if user and user["phone"]:
        await cb.message.edit_text(summary(data), reply_markup=CONFIRM_KB)
    else:
        await state.set_state(Booking.phone)
        await cb.message.edit_text(summary(data))
        await cb.message.answer(
            "Залиште номер телефону, щоб майстер міг з вами зв'язатися.\n"
            "Натисніть кнопку нижче або напишіть номер.",
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
                [KeyboardButton(text="📱 Надіслати мій номер", request_contact=True)]]))
    await cb.answer()


@router.message(Booking.phone)
async def got_phone(msg: Message, state: FSMContext):
    phone = msg.contact.phone_number if msg.contact else (msg.text or "")
    digits = re.sub(r"\D", "", phone)
    if not 10 <= len(digits) <= 15:
        await msg.answer("Не схоже на номер телефону 🤔 Спробуйте ще раз, наприклад: 0671234567")
        return
    if not phone.startswith("+") and len(digits) == 10 and digits.startswith("0"):
        phone = "+38" + digits
    elif not phone.startswith("+"):
        phone = "+" + digits
    db.upsert_user(msg.from_user.id, msg.from_user.full_name, msg.from_user.username)
    db.set_phone(msg.from_user.id, phone)
    await state.set_state(None)
    await msg.answer("Дякую! 👍", reply_markup=main_menu())
    await msg.answer(summary(await state.get_data()), reply_markup=CONFIRM_KB)


@router.callback_query(F.data.startswith("back:"))
async def go_back(cb: CallbackQuery, state: FSMContext):
    step = cb.data[5:]
    data = await state.get_data()
    if step == "svc" or "service" not in data:
        await cb.message.edit_text("Оберіть послугу:", reply_markup=services_kb())
    elif step == "brb":
        await show_barbers(cb, state)
    elif step == "day" or "day" not in data:
        await show_days(cb, state)
    else:
        await show_times(cb, state)
    await cb.answer()


@router.callback_query(F.data == "confirm")
async def confirm(cb: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if not {"service", "barber", "day", "time"} <= data.keys():
        await cb.answer("Почніть запис спочатку", show_alert=True)
        return
    start = datetime.strptime(f"{data['day']} {data['time']}", FMT)
    end = start + timedelta(minutes=SERVICES[data["service"]]["minutes"])
    booking_id = None
    if start >= now():
        n = now()
        # Нагадування, час яких уже минув, не надсилаємо.
        reminded = sum(1 for h in C.REMIND_HOURS if start - n <= timedelta(hours=h))
        for b in barbers_for(data["barber"]):
            booking_id = db.create(cb.from_user.id, b, data["service"], start, end, n, reminded)
            if booking_id:
                break
    if not booking_id:
        await cb.answer("Ой, цей час щойно зайняли. Оберіть інший 🙏", show_alert=True)
        return await show_times(cb, state)

    await state.clear()
    row = db.get(booking_id)
    await cb.message.edit_text("✅ <b>Ви записані!</b>\n\n" + booking_text(row) +
                               f"\n\n📍 {esc(C.ADDRESS)}\nНагадаємо напередодні. До зустрічі!")
    await cb.answer("Готово!")
    await notify_staff(bot, row, "🆕 <b>Новий запис</b>")


# ---------- скасування ----------

@router.callback_query(F.data.startswith("uc:"))
async def user_cancel(cb: CallbackQuery, bot: Bot):
    row = db.get(int(cb.data[3:]))
    if not row or row["user_id"] != cb.from_user.id or not db.cancel(row["id"]):
        await cb.answer("Запис не знайдено або вже скасовано", show_alert=True)
        return
    await cb.message.edit_text("❌ Запис скасовано.\n\n" + booking_text(row))
    await cb.answer()
    await notify_staff(bot, row, "❌ <b>Клієнт скасував запис</b>", with_button=False)


@router.callback_query(F.data.startswith("ac:"))
async def admin_cancel(cb: CallbackQuery, bot: Bot):
    if cb.from_user.id not in ADMIN_IDS:
        return await cb.answer("Недостатньо прав", show_alert=True)
    row = db.get(int(cb.data[3:]))
    if not row or not db.cancel(row["id"]):
        return await cb.answer("Запис уже скасовано", show_alert=True)
    await cb.message.edit_text("❌ <b>Скасовано адміністратором</b>\n\n" + booking_text(row, True))
    await cb.answer()
    await safe_send(bot, row["user_id"],
                    "На жаль, ваш запис скасовано барбершопом 😔\n\n" + booking_text(row) +
                    f"\n\nОберіть інший час або зателефонуйте: {esc(C.PHONE)}",
                    reply_markup=kb([[(BTN_BOOK, "book")]]))


# ---------- адмін ----------

def staff_ids(row) -> set[int]:
    ids = set(ADMIN_IDS)
    tg = BARBERS.get(row["barber_id"], {}).get("tg_id")
    if tg:
        ids.add(int(tg))
    return ids


async def safe_send(bot: Bot, chat_id: int, text: str, **kw):
    try:
        await bot.send_message(chat_id, text, **kw)
    except Exception as e:  # клієнт заблокував бота тощо
        logging.warning("send to %s failed: %s", chat_id, e)


async def notify_staff(bot: Bot, row, title: str, with_button=True):
    markup = kb([[("❌ Скасувати", f"ac:{row['id']}")]]) if with_button else None
    for chat_id in staff_ids(row):
        await safe_send(bot, chat_id, f"{title}\n\n{booking_text(row, True)}", reply_markup=markup)


async def list_period(msg: Message, start: datetime, days: int, title: str):
    if msg.from_user.id not in ADMIN_IDS:
        return
    rows = db.between(start, start + timedelta(days=days))
    if not rows:
        await msg.answer(f"{title}: записів немає.")
        return
    parts = [f"<b>{title}</b> — {len(rows)} записів\n"]
    for r in rows:
        st = datetime.strptime(r["start"], FMT)
        s = SERVICES.get(r["service_id"], {"name": r["service_id"]})
        barber = BARBERS.get(r["barber_id"], {"name": r["barber_id"]})["name"]
        day = f"{human_day(st.date())} " if days > 1 else ""
        parts.append(f"{day}<b>{st:%H:%M}</b> · {esc(barber)} · {esc(s['name'])}\n"
                     f"   👤 {esc(r['user_name'])} 📞 {esc(r['phone'])}")
    await msg.answer("\n".join(parts))


def day_start(offset=0) -> datetime:
    return datetime.combine(now().date() + timedelta(days=offset), datetime.min.time())


@router.message(Command("today"))
async def adm_today(msg: Message):
    await list_period(msg, day_start(), 1, "Сьогодні")


@router.message(Command("tomorrow"))
async def adm_tomorrow(msg: Message):
    await list_period(msg, day_start(1), 1, "Завтра")


@router.message(Command("week"))
async def adm_week(msg: Message):
    await list_period(msg, day_start(), 7, "Найближчі 7 днів")


@router.message(Command("stats"))
async def adm_stats(msg: Message):
    if msg.from_user.id not in ADMIN_IDS:
        return
    s = db.stats(now() - timedelta(days=30))
    await msg.answer(f"📊 За 30 днів через бота: <b>{s['n']}</b> записів, "
                     f"<b>{s['clients']}</b> клієнтів.")


@router.message(Command("help"))
async def help_cmd(msg: Message):
    text = "Натисніть «✂️ Записатися», щоб обрати послугу й час."
    if msg.from_user.id in ADMIN_IDS:
        text += ("\n\n<b>Команди адміністратора</b>\n/today — записи на сьогодні\n"
                 "/tomorrow — на завтра\n/week — на тиждень\n/stats — статистика за 30 днів")
    await msg.answer(text, reply_markup=main_menu())


@router.message()
async def fallback(msg: Message):
    await msg.answer("Оберіть дію в меню нижче 👇", reply_markup=main_menu())


# ---------- нагадування ----------

async def send_reminders(bot: Bot):
    hours = sorted(C.REMIND_HOURS, reverse=True)  # напр. (24, 2)
    n = now()
    for r in db.between(n, n + timedelta(hours=hours[0])):
        st = datetime.strptime(r["start"], FMT)
        due = sum(1 for h in hours if st - n <= timedelta(hours=h))
        if due > r["reminded"]:
            db.set_reminded(r["id"], due)
            when = "сьогодні" if st.date() == n.date() else "завтра"
            await safe_send(bot, r["user_id"],
                            f"⏰ Нагадуємо: {when} о <b>{st:%H:%M}</b> вас чекають у "
                            f"{esc(C.BUSINESS_NAME)}!\n\n{booking_text(r)}\n\n📍 {esc(C.ADDRESS)}",
                            reply_markup=kb([[("❌ Не зможу прийти", f"uc:{r['id']}")]]))


async def reminders(bot: Bot):
    while True:
        try:
            await send_reminders(bot)
        except Exception:
            logging.exception("reminder loop")
        await asyncio.sleep(60)


# ---------- запуск ----------

def load_env(path=".env"):
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def setup(db_path: str, admin_ids: str) -> Dispatcher:
    global db
    db = DB(db_path)
    ADMIN_IDS.clear()
    ADMIN_IDS.update(int(x) for x in re.findall(r"\d+", admin_ids or ""))
    global _dp
    if _dp is None:
        _dp = Dispatcher()
        _dp.include_router(router)
    return _dp


_dp: Dispatcher | None = None


async def main():
    logging.basicConfig(level=logging.INFO)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    load_env()
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise SystemExit("Вкажіть BOT_TOKEN у файлі .env (див. README.md)")
    dp = setup(os.environ.get("DB_PATH", "bookings.db"), os.environ.get("ADMIN_IDS", ""))
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.create_task(reminders(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
