import logging
import os

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


# ============================================
# SETTINGS
# ============================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

# External news source (not owned by this bot) — plain link, hardcoded.
SITE_URL = "https://www.turkiyetoday.com/"
SITE_NAME = "Türkiye Today"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()
BRAND = "Turkey Guide"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============================================
# HELPERS
# ============================================
def btn(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def site_btn():
    # Plain external link to a third-party news site (opens in Telegram's browser).
    return types.InlineKeyboardButton(
        text=f"📰 Read the news on {SITE_NAME}",
        url=SITE_URL,
    )


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [button for button in row if button is not None]
        if row:
            markup.row(*row)
    return markup


BTN_HEADLINES = ("📋 Today's reads", "headlines")
BTN_MENU = ("🗂 Contents", "menu")


def article_rows():
    return [
        [site_btn()],
        [btn(*BTN_HEADLINES), btn(*BTN_MENU)],
    ]


# ============================================
# SCREEN TEXTS
# ============================================
TEXT_START = (
    f"🇹🇷 <b>Welcome to {BRAND}!</b>\n\n"
    "<i>A small seasonal guide to culture, food and travel in Turkey.</i>\n\n"
    "Each season, a short selection of reads to enjoy right here in the chat.\n\n"
    "To begin, tap <b>Today's reads</b>."
)

TEXT_HEADLINES = (
    "📋 <b>Today's reads</b>\n\n"
    "Three reads picked for today, each available in full in the chat.\n\n"
    "<b>Culture</b> — five museums to see this autumn.\n\n"
    "<b>Food</b> — five classic Turkish dishes.\n\n"
    "<b>Travel</b> — five places for a weekend away.\n\n"
    "Tap a title to open the article."
)

TEXT_CULTURE = (
    "🎨 <b>Five museums to see this autumn</b>\n\n"
    "<b>Istanbul — Topkapı Palace Museum</b>\n"
    "Home to the Ottoman sultans for nearly four centuries: treasury "
    "rooms, sacred relics and courtyards well worth the visit.\n\n"
    "<b>Istanbul — Hagia Sophia</b>\n"
    "A monumental meeting of Byzantine and Ottoman architecture, its "
    "great dome and mosaics witness to centuries of history.\n\n"
    "<b>Ankara — Museum of Anatolian Civilizations</b>\n"
    "Hittite, Phrygian and more — thousands of years of Anatolia's "
    "past brought together under one roof.\n\n"
    "<b>Antakya — Hatay Archaeology Museum</b>\n"
    "Home to one of the world's richest collections of Roman-era "
    "mosaics.\n\n"
    "<b>İzmir — Ephesus</b>\n"
    "The Library of Celsus and the great theatre make this one of the "
    "best-preserved ancient cities in the world.\n\n"
    "<i>Dates and opening hours: please check the museums' official sites.</i>"
)

TEXT_CUISINE = (
    "🍲 <b>Five classic Turkish dishes</b>\n\n"
    "<b>Mantı</b>\n"
    "Small dumplings filled with spiced meat, served under garlicky "
    "yoghurt and a drizzle of butter.\n\n"
    "<b>İskender kebab</b>\n"
    "Thin slices of döner over pide bread, with tomato sauce, melted "
    "butter and yoghurt. A Bursa classic.\n\n"
    "<b>Menemen</b>\n"
    "Eggs gently cooked with tomatoes and peppers — the essential "
    "Turkish breakfast pan.\n\n"
    "<b>Lahmacun</b>\n"
    "Thin dough topped with spiced minced meat; roll it up with lemon "
    "and parsley.\n\n"
    "<b>Baklava</b>\n"
    "Layers of filo with pistachio or walnut and syrup — a masterpiece "
    "of patience.\n\n"
    "<i>Amounts and cooking times can be adjusted to taste.</i>"
)

TEXT_TRAVEL = (
    "🏡 <b>Five places for a weekend away</b>\n\n"
    "<b>Cappadocia (Nevşehir)</b>\n"
    "Fairy chimneys, underground cities and balloon flights. The "
    "autumn light makes the valleys unforgettable.\n\n"
    "<b>Şirince (İzmir)</b>\n"
    "A peaceful hill village of stone houses and vineyards, known for "
    "its local fruit wines.\n\n"
    "<b>Safranbolu (Karabük)</b>\n"
    "A UNESCO-listed town of Ottoman mansions — an open-air museum "
    "with a historic bazaar.\n\n"
    "<b>Amasra (Bartın)</b>\n"
    "A small, charming town on the Black Sea, with a castle, coves and "
    "fish restaurants.\n\n"
    "<b>Assos / Behramkale (Çanakkale)</b>\n"
    "Views over the Aegean from the ancient Temple of Athena, and "
    "quiet stone streets.\n\n"
    "<i>For lodging, midweek booking is recommended.</i>"
)

TEXT_MENU = (
    "🗂 <b>Contents</b>\n\n"
    "From this menu you can:\n\n"
    "• Read <b>today's reads</b> and the articles, right here.\n"
    "• Browse the sections: Culture, Food, Travel.\n"
    "• Check the glossary and frequently asked questions.\n"
    "• Learn more about the project and get in touch."
)

TEXT_GLOSSARY = (
    "📖 <b>Little glossary</b>\n\n"
    "<b>Han</b> — a traditional inn where travellers and traders once "
    "lodged.\n\n"
    "<b>Meydan</b> — a public square, the gathering point of a town.\n\n"
    "<b>Çarşı</b> — a traditional market district; covered or open.\n\n"
    "<b>Konak</b> — a large traditional town mansion, usually two or "
    "three storeys.\n\n"
    "<b>Meze</b> — small shared plates served before the main course.\n\n"
    "<b>Ören yeri</b> — an archaeological site, the ruins of an "
    "ancient settlement."
)

TEXT_FAQ = (
    "❓ <b>Frequently asked questions</b>\n\n"
    "<b>Is this bot official?</b>\n"
    f"No. It's an independent guide, not affiliated with {SITE_NAME} or "
    "any publication. The news button simply links to their public site. "
    "It never asks for passwords, codes or card details.\n\n"
    "<b>How often is it updated?</b>\n"
    "The selection of reads is refreshed each season.\n\n"
    "<b>How do I mute notifications?</b>\n"
    "From the Telegram chat settings you can mute or disable "
    "notifications.\n\n"
    "<b>Can I share an article?</b>\n"
    "Yes. Use Telegram's forward function."
)

TEXT_ABOUT = (
    f"ℹ️ <b>About {BRAND}</b>\n\n"
    f"{BRAND} gathers, each season, a few reads about Turkey: "
    "museums, traditional food and beautiful places to visit.\n\n"
    "The idea is simple: short, pleasant texts to read right in "
    "Telegram, without ads and without rushing.\n\n"
    f"For the latest news, the button links to {SITE_NAME} "
    "(turkiyetoday.com), an independent news site."
)


def contact_text():
    email_line = (
        f"• E-mail: {CONTACT_EMAIL}\n\n"
        if CONTACT_EMAIL
        else "• A contact address will be added soon.\n\n"
    )
    return (
        "✏️ <b>Contact</b>\n\n"
        "For suggestions, corrections or article ideas:\n"
        + email_line
        + "Thank you for every message!"
    )


# ============================================
# SCREENS: callback_data -> (text, buttons)
# ============================================
SCREENS = {
    "headlines": (
        TEXT_HEADLINES,
        [
            [btn("🎨 Culture — autumn museums", "culture")],
            [btn("🍲 Food — classic dishes", "cuisine")],
            [btn("🏡 Travel — five places", "travel")],
            [btn(*BTN_MENU)],
        ],
    ),
    "culture": (TEXT_CULTURE, article_rows()),
    "cuisine": (TEXT_CUISINE, article_rows()),
    "travel": (TEXT_TRAVEL, article_rows()),
    "menu": (
        TEXT_MENU,
        [
            [site_btn()],
            [btn(*BTN_HEADLINES)],
            [btn("📖 Glossary", "glossary"), btn("❓ FAQ", "faq")],
            [btn("✏️ Contact", "contact"), btn("ℹ️ About", "about")],
        ],
    ),
    "glossary": (TEXT_GLOSSARY, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "faq": (TEXT_FAQ, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "contact": (
        contact_text(),
        [[btn(*BTN_MENU), btn("ℹ️ About", "about")]],
    ),
    "about": (
        TEXT_ABOUT,
        [[site_btn()], [btn(*BTN_MENU), btn("✏️ Contact", "contact")]],
    ),
}


# ============================================
# HANDLERS
# ============================================
@bot.message_handler(commands=["start"])
def start(message):
    markup = make_markup([[site_btn()], [btn(*BTN_HEADLINES), btn(*BTN_MENU)]])
    bot.send_message(message.chat.id, TEXT_START, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in SCREENS)
def show_screen(call):
    bot.answer_callback_query(call.id)
    text, rows = SCREENS[call.data]
    markup = make_markup(rows)
    try:
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
    except ApiTelegramException:
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    bot.set_chat_menu_button(menu_button=types.MenuButtonDefault(type="default"))

    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
