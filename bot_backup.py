import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# ============================================================
# KONFIGURASI
# ============================================================

# JANGAN taruh token asli di GitHub.
# Masukkan token baru hasil regenerate dari BotFather.
BOT_TOKEN = "8863344516:AAEAQMZrC_629QKB6WGGiru17bnCMsKmqNA"

# ID akun Telegram yang diperbolehkan menggunakan bot
ALLOWED_USER_ID = 7998043167


# ============================================================
# DAFTAR GROUP
# ============================================================

GROUP_IDS = [
    -5533715902,        # HORAS711 BANDAR TOGEL
    -1003769469405,     # PREDIKSI TERJITU
    -1004486299973,     # AGENT MAXWIN
    -1003878958758,     # BANDAR HORAS711 GACOR
    -1004498060497,     # BANDAR ONLINE HORAS711
    -1004330340321,     # SITUS HORAS GACOR
    -5056875719,        # BO TERBESAR DAN TERPERCAYA
    -1003907654922,     # HORAS MEDAN 711
    -1003943297366,     # LINK_AKTIF_HORAS
    -1004403252038,     # PROMO HORAS711
]


# ============================================================
# TOMBOL POSTING
# ============================================================

KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "⚜️ DAFTAR HORAS711 DISINI ⚜️",
            url="https://lenke.digital/horas711"
        )
    ],
    [
        InlineKeyboardButton(
            "🌐 CARI HORAS711 DI TEMUKAN KITA 🌐",
            url="https://temukankita.id/search?query=horas711"
        )
    ],
    [
        InlineKeyboardButton(
            "🔰 INSTAGRAM 🔰",
            url="https://www.instagram.com/horas711_gacor/"
        ),
        InlineKeyboardButton(
            "🔰 TELEGRAM 🔰",
            url="https://t.me/Horas711Mdn"
        )
    ],
    [
        InlineKeyboardButton(
            "💰 PREDIKSI TOGEL 💰",
            url="https://lenke.digital/Myprediksi"
        ),
        InlineKeyboardButton(
            "💰 RTP SLOT TERGACOR 💰",
            url="https://hsllink.com/RtpHoras711"
        )
    ],
    [
        InlineKeyboardButton(
            "💠 LIVECHAT HORAS711 💠",
            url="https://secure.livechatenterprise.com/customer/action/open_chat?license_id=19110693"
        )
    ],
    [
        InlineKeyboardButton(
            "🪆 DOWNLOAD APLIKASI HORAS711 🪆",
            url="https://hsllink.com/HORAS711_APK"
        )
    ]
])


# ============================================================
# CEK USER
# ============================================================

def is_allowed(update: Update) -> bool:
    """Memastikan hanya user yang diizinkan yang dapat memakai bot."""

    if not update.effective_user:
        return False

    return update.effective_user.id == ALLOWED_USER_ID


# ============================================================
# /START
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_allowed(update):
        if update.message:
            await update.message.reply_text(
                "⛔ Anda tidak memiliki akses ke bot ini."
            )
        return

    total_groups = len(GROUP_IDS)

    await update.message.reply_text(
        f"🤖 AUTO POST BOT\n\n"
        f"Bot siap digunakan.\n\n"
        f"📢 Target posting: {total_groups} group\n\n"
        f"📸 Kirim FOTO + CAPTION ke chat ini."
    )


# ============================================================
# POSTING FOTO
# ============================================================

async def handle_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_allowed(update):
        if update.message:
            await update.message.reply_text(
                "⛔ Anda tidak memiliki akses ke bot ini."
            )
        return

    if not update.message or not update.message.photo:
        return

    photo = update.message.photo[-1]

    caption = update.message.caption or ""

    total_groups = len(GROUP_IDS)

    success = 0
    failed = 0

    status_message = await update.message.reply_text(
        f"⏳ Mengirim posting ke {total_groups} group..."
    )

    for group_id in GROUP_IDS:

        try:
            await context.bot.send_photo(
                chat_id=group_id,
                photo=photo.file_id,
                caption=caption,
                reply_markup=KEYBOARD
            )

            success += 1

            print(
                f"✅ Berhasil mengirim ke {group_id}"
            )

        except Exception as e:

            failed += 1

            print(
                f"❌ Gagal mengirim ke {group_id}: {e}"
            )

        # Jeda antar pengiriman
        await asyncio.sleep(0.5)

    await status_message.edit_text(
        f"✅ POSTING SELESAI\n\n"
        f"📢 Total group : {total_groups}\n"
        f"✅ Berhasil    : {success}/{total_groups}\n"
        f"❌ Gagal       : {failed}/{total_groups}"
    )


# ============================================================
# PESAN TEKS
# ============================================================

async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_allowed(update):
        if update.message:
            await update.message.reply_text(
                "⛔ Anda tidak memiliki akses ke bot ini."
            )
        return

    total_groups = len(GROUP_IDS)

    await update.message.reply_text(
        f"📸 Silakan kirim FOTO beserta caption.\n\n"
        f"Bot akan mengirimnya ke {total_groups} group."
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    print(
        f"❌ ERROR BOT: {context.error}"
    )


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():

    if not BOT_TOKEN or BOT_TOKEN == "MASUKKAN_TOKEN_BOT_BARU_DI_SINI":

        print(
            "❌ ERROR: Token bot belum dimasukkan!"
        )

        return

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Command /start
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # Foto + caption
    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo
        )
    )

    # Pesan teks biasa
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    # Error handler
    application.add_error_handler(
        error_handler
    )

    print("===================================")
    print("          AUTO POST BOT")
    print("===================================")
    print("✅ BOT BERHASIL DIJALANKAN")
    print(f"📢 TARGET : {len(GROUP_IDS)} GROUP")
    print("📸 Menunggu posting...")
    print("===================================")

    application.run_polling()


# ============================================================
# JALANKAN BOT
# ============================================================

if __name__ == "__main__":
    main()