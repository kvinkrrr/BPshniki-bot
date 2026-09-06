import logging
import random
from aiogram.filters import CommandStart
from aiogram.types import (
    ChatJoinRequest)
from aiogram import Router, F
from aiogram.types import (Message, MessageEntity)
from aiogram.types import FSInputFile
from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


GROUP_AD = -1002855315839
GROUP_ID = -1001870935202
BOT_TOKEN = "8064135284:AAFrlUp07n7oyuwwRmhbltJzxIvAQ-Xc1zk"
router = Router()

group_to_user = {}

# ID сообщения пользователя -> ID сообщения в группе
user_to_group = {}

class SendMessage(StatesGroup):
    waiting_for_message = State()

@router.message(Command("send"))
async def send_command(message:Message, state: FSMContext):
    caption = "-У тебя возникла проблема 💎?\nМы её постараемся решить 🚀. Опиши свою проблему, "\
              "а также свой @username для того, чтобы мы могли с тобой связаться 👇.\n"\
              "После того, как придет сообщение от админа группы - свайпни влево для ответа🔜.\n\n"\
              "Нажми /start, чтобы вернутся обратно в меню\n"

    emojis = [
        ("💎", "5344002312039862645"),
        ("🚀", "5345973749273356952"),
        ("👇", "5256258204651785650"),
        ("🔜", "5442990914391791134")
    ]

    entities = []

    # Добавляем Premium Emoji
    for emoji, emoji_id in emojis:
        pos = caption.find(emoji)

        entities.append(
            MessageEntity(
                type="custom_emoji",
                offset=len(
                    caption[:pos].encode("utf-16-le")
                ) // 2,
                length=len(
                    emoji.encode("utf-16-le")
                ) // 2,
                custom_emoji_id=emoji_id
            )
        )

    await message.answer_photo(
        photo=FSInputFile("sva.jpg"),
        caption=caption,
        caption_entities=entities)



    await state.set_state(
        SendMessage.waiting_for_message
    )

# =========================
# ОТПРАВКА СООБЩЕНИЯ В ГРУППУ
# =========================

@router.message(SendMessage.waiting_for_message)
async def process_message(
    message: types.Message,
    state: FSMContext,
    bot: Bot
):

    try:

        # Копируем сообщение пользователя в группу
        sent = await bot.copy_message(
            chat_id=GROUP_AD,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )

        # Связываем сообщение в группе с пользователем
        group_to_user[sent.message_id] = message.from_user.id

        # Связываем сообщение пользователя с сообщением группы
        user_to_group[message.message_id] = sent.message_id

        await message.answer(
            "✅ Сообщение отправлено!\n"
            "Если хочешь ответить на сообщение от админа, то свайпни влево для ответа\n\n"
            "Нажми /start, чтобы вернутся обратно в меню\n"
        )

    except Exception as e:

        await message.answer(
            f"❌ Ошибка:\n{e}"
        )

    finally:

        await state.clear()

# ==================================================
# ОТВЕТ УЧАСТНИКА ГРУППЫ
# ==================================================

@router.message(
    lambda message:
    message.chat.id == GROUP_AD
    and message.reply_to_message is not None
)
async def group_reply(message: types.Message, bot: Bot):

    replied_message_id = (
        message.reply_to_message.message_id
    )

    # Ищем пользователя, которому принадлежит
    # сообщение, на которое ответили
    user_id = group_to_user.get(
        replied_message_id
    )

    if not user_id:
        return

    try:

        # Отправляем ответ пользователю
        sent = await bot.copy_message(
            chat_id=user_id,
            from_chat_id=GROUP_AD,
            message_id=message.message_id
        )

        # Теперь сообщение пользователя в личке
        # связано с сообщением в группе
        user_to_group[sent.message_id] = (
            message.message_id
        )

    except Exception as e:

        print(
            f"Ошибка отправки ответа: {e}\n\n"
            "Нажми /start, чтобы вернутся обратно в меню\n"
        )

# ==================================================
# ОТВЕТ ПОЛЬЗОВАТЕЛЯ НА СООБЩЕНИЕ ИЗ ГРУППЫ
# ==================================================

@router.message(
    lambda message:
    message.chat.id != GROUP_AD
    and message.reply_to_message is not None
)
async def user_reply(message: types.Message, bot: Bot):

    replied_message_id = (
        message.reply_to_message.message_id
    )

    # Находим сообщение в группе,
    # которому соответствует сообщение в личке
    group_message_id = user_to_group.get(
        replied_message_id
    )

    if not group_message_id:
        return

    try:

        # Копируем ответ пользователя в группу
        sent = await bot.copy_message(
            chat_id=GROUP_AD,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_parameters=types.ReplyParameters(
                message_id=group_message_id
            )
        )

        # Связываем новое сообщение в группе
        # с пользователем
        group_to_user[sent.message_id] = (
            message.from_user.id
        )

    except Exception as e:

        print(
            f"Ошибка отправки ответа: {e}\n\n"
            "Нажми /start, чтобы вернутся обратно в меню\n"
        )

# ==========================================
# ПРОВЕРОЧНЫЕ ТЕКСТЫ
# ==========================================

VERIFICATION_TEXTS = [
    "K7#mP2@xL9",
    "vQ4!zN8$Rt",
    "A9@kL3#pX7",
    "m2$Wq8!Hb5",
    "Z6&nR1@tK9",
    "pL8#X2!vM4",
    "Q5@dS9$kN2",
    "xR7!bC3#Y8",
    "H4$wP9@mK6",
    "nT2#qV7!Ls",
    "B8@rF5$zX1",
    "kM3!Q7#pR9",
    "W6$xN2@hL8",
    "cP9#vK4!mT7",
    "R1@zH8$qF5",
]


# ==========================================
# ИНИЦИАЛИЗАЦИЯ
# ==========================================

logging.basicConfig(level=logging.INFO)




# ==========================================
# ЗАЯВКИ, ОЖИДАЮЩИЕ ВЕРИФИКАЦИИ
# ==========================================

# Формат:
#
# pending_requests[user_id] = {
#     "chat_id": ID группы,
#     "verification": "текст"
# }

pending_requests = {}


# ==========================================
# /START
# ==========================================

@router.message(Command("start"))
async def start_handler(message: Message):
    caption="💎 🚀 👇🔜 😳 👅 😭\n\n"\
            "Мы рады видеть тебя в нашей боте-верификаторе, чтобы вступить в группу БПшники - подай заявку 💀:\n"\
            "https://t.me/bpshniki - ссылка на группу БПшники\n\n"\
            "Если ты подал заявку на вступление в группу, "\
            "дождись сообщения с проверочным текстом 🔫.\n\nЕсли у тебя возникла проблема - отправь команду /send"
    emojis = [
        ("💎", "5282759888034878668"),
        ("🚀", "5285448181079891664"),
        ("👇", "5285346828441640817"),
        ("🔜", "5283084836670563301"),
        ("😳", "5285152605725545670"),
        ("👅", "5285226311659313403"),
        ("😭", "5282901892538589652"),
        ("💀", "5256258204651785650"),
        ("🔫", "5341429493485574514")
    ]

    entities = []

    # Добавляем Premium Emoji
    for emoji, emoji_id in emojis:
        pos = caption.find(emoji)

        entities.append(
            MessageEntity(
                type="custom_emoji",
                offset=len(
                    caption[:pos].encode("utf-16-le")
                ) // 2,
                length=len(
                    emoji.encode("utf-16-le")
                ) // 2,
                custom_emoji_id=emoji_id
            )
        )
    await message.answer_photo(
        photo=FSInputFile("bp.jpg"),
        caption=caption,
        caption_entities=entities

    )


# ==========================================
# НОВАЯ ЗАЯВКА НА ВСТУПЛЕНИЕ
# ==========================================

@router.chat_join_request()
async def join_request_handler(request: ChatJoinRequest, bot:Bot):

    # Проверяем нужную группу
    if request.chat.id != GROUP_ID:
        return

    user_id = request.from_user.id

    # Выбираем случайный проверочный текст
    verification_text = random.choice(VERIFICATION_TEXTS)

    # Сохраняем заявку
    pending_requests[user_id] = {
        "chat_id": request.chat.id,
        "verification": verification_text
    }

    # Отправляем проверку
    await bot.send_message(
        chat_id=request.user_chat_id,
        text=(
            "🔐 <b>Проверка на человека!</b>\n\n"
            "Чтобы подтвердить, что ты реальный пользователь, "
            "скопируй проверочный текст ниже и отправь его "
            "мне обычным сообщением.\n\n"

            f"<code>{verification_text}</code>\n\n"

            "⚠️ Отправь текст точно так же, как он указан выше."
        ),
        parse_mode="HTML"
    )

    logging.info(
        f"Пользователь {user_id} получил проверку: "
        f"{verification_text}"
    )


# ==========================================
# ПРОВЕРКА ОТВЕТА ПОЛЬЗОВАТЕЛЯ
# ==========================================

@router.message(F.text)
async def verification_answer(message: Message, bot:Bot):

    user_id = message.from_user.id

    # Проверяем, есть ли у пользователя активная заявка
    if user_id not in pending_requests:
        return

    request_data = pending_requests[user_id]

    correct_text = request_data["verification"]

    # ======================================
    # ПРАВИЛЬНЫЙ ОТВЕТ
    # ======================================

    if message.text == correct_text:

        try:

            # Принимаем заявку
            await bot.approve_chat_join_request(
                chat_id=request_data["chat_id"],
                user_id=user_id
            )

            # Удаляем данные о заявке
            del pending_requests[user_id]

            # Сообщаем пользователю
            await message.answer(
                "✅ <b>Верификация пройдена!</b>\n\n"
                "Твоя заявка одобрена.\n"
                "Добро пожаловать в группу БПшники! Приятного общения 🎉",
                parse_mode="HTML"
            )

            logging.info(
                f"Пользователь {user_id} успешно прошёл "
                f"верификацию."
            )

        except Exception as e:

            logging.error(
                f"Ошибка при принятии заявки "
                f"{user_id}: {e}"
            )

            await message.answer(
                "❌ Произошла ошибка при принятии заявки.\n"
                "Попробуй отправить текст ещё раз."
            )

    # ======================================
    # НЕПРАВИЛЬНЫЙ ОТВЕТ
    # ======================================

    else:

        await message.answer(
            "❌ <b>Неверный проверочный текст.</b>\n\n"
            "Скопируй текст из предыдущего сообщения "
            "и отправь его без изменений.",
            parse_mode="HTML"
        )