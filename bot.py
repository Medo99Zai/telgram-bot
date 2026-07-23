import telebot
from telebot import types

# ✅ L-Token l-Jdid dyalk m-7tout mriql
API_TOKEN = '8930786040:AAHb1Aoj55GpLfzZy2Gn8I4KT62zUIt693o'
bot = telebot.TeleBot(API_TOKEN)

# ⚠️ Hna 7et l-link dyal l-affiliate dyalk d iDrive direct
XM_LINK = "https://affs.click/8Raj3"

# --- LES ÉTAPES D L-FUNNEL (High Conversion) ---

STEP1_TEXT = (
    "🚀 **Quer ganhar dinheiro enquanto dorme?**\n\n"
    "Chega de trabalhar 8 horas por dia para enriquecer os outros. "
    "Existe uma forma 100% automática de fazer o mercado financeiro trabalhar para você.\n\n"
    "Quer ver como funciona em 30 segundos?"
)

STEP2_TEXT = (
    "⚡ **Sem análise. Sem experiência. 1 Clique.**\n\n"
    "Nesta plataforma de elite, você simplesmente **copia automaticamente** as operações dos maiores especialistas do mercado mundial.\n\n"
    "📈 Eles analisam e operam por você.\n"
    "💰 Você recebe os lucros direto na sua conta."
)

STEP3_TEXT = (
    "🔥 **Sua vaga gratuita está liberada!**\n\n"
    "O sistema está pronto. Comece agora mesmo a copiar os melhores e ative sua nova fonte de renda passiva hoje.\n\n"
    "Clique no botão abaixo para criar sua conta segura e ativar o modo automático: 👇"
)

# --- TELEGRAM HANDLERS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="👉 SIM! QUERO VER", callback_data="go_2")
    markup.add(btn)
    bot.send_message(message.chat.id, STEP1_TEXT, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "go_2":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="🚀 QUERO COPIAR AGORA", callback_data="go_3")
        markup.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              text=STEP2_TEXT, 
                              parse_mode="Markdown", 
                              reply_markup=markup)
                              
    elif call.data == "go_3":
        markup = types.InlineKeyboardMarkup()
        btn_final = types.InlineKeyboardButton(text="💰 ATIVAR SISTEMA AUTOMÁTICO", url=XM_LINK)
        markup.add(btn_final)
        bot.edit_message_text(chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              text=STEP3_TEXT, 
                              parse_mode="Markdown", 
                              reply_markup=markup)

if __name__ == '__main__':
    print("Bot is running successfully...")
    bot.infinity_polling()
