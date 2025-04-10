import telebot
from ai_engine import generate_analysis
from sofascore import search_team_id, fetch_team_data

bot = telebot.TeleBot("7521045784:AAG2g-MkQfKg8gkOYPpa1kD5m_Pi8kpvVo8")

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Salam! Komanda adını göndər, sənə bütün analizləri və məlumatları çatdırım.")

@bot.message_handler(func=lambda m: True)
def handle_team_query(message):
    team_name = message.text.strip()
    bot.send_message(message.chat.id, f"🔍 Komanda axtarılır...")

    team_id = search_team_id(team_name)
    if not team_id:
        bot.send_message(message.chat.id, "❌ Komanda tapılmadı və ya düzgün tanınmadı.")
        return

    stats = fetch_team_data(team_id)
    analysis = generate_analysis(team_name, stats)
    bot.send_message(message.chat.id, analysis)

bot.polling()