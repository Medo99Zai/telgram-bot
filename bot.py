import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. Web Server خفيف لـ Back4App Health Check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. إعدادات البوت والـ Affiliate Link (تم إدراجهم مباشرة)
API_TOKEN = '8930786040:AAFG2ChKQ1zQ-f98StKDAyiaGzwl8Hmko10'
XM_LINK = 'https://affs.click/8Raj3'

bot = telebot.TeleBot(API_TOKEN)

# 3. نصوص الـ Funnel
STEP1_TEXT = (
    "🚀 **Quer ganhar dinheiro enquanto dorme?**\n\n"
    "Chega de trabalhar 8 horas por dia para enriquecer os outros. "
    "Existe uma forma 100% automática de fazer o mercado financeiro trabalhar para você.\n\n"
    "⚠️ **Apenas 10 vagas liberadas para hoje!**\n\n"
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
    "⏱️ **Atenção:** Este link expira em **15 minutos**.\n\n"
    "O sistema está pronto. Comece agora mesmo a copiar os melhores e ative sua nova fonte de renda passiva hoje.\n\n"
    "Clique no botão abaixo para criar sua conta segura e ativar o modo automático: 👇"
)

# 4. Handlers ديال التليغرام (أزرار صغيرة ومرتبة تحت النص)
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
        try:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=STEP2_TEXT,
                                  parse_mode="Markdown",
                                  reply_markup=markup)
        except Exception:
            bot.send_message(chat_id=call.message.chat.id, 
                             text=STEP2_TEXT, 
                             parse_mode="Markdown", 
                             reply_markup=markup)
                              
    elif call.data == "go_3":
        markup = types.InlineKeyboardMarkup()
        btn_final = types.InlineKeyboardButton(text="💰 ATIVAR SISTEMA AUTOMÁTICO", url=XM_LINK)
        markup.add(btn_final)
        try:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=STEP3_TEXT,
                                  parse_mode="Markdown",
                                  reply_markup=markup)
        except Exception:
            bot.send_message(chat_id=call.message.chat.id, 
                             text=STEP3_TEXT, 
                             parse_mode="Markdown", 
                             reply_markup=markup)

# 5. تشغيل السيرفر والبوت بطريقة مستقرة
if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Starting Telegram Bot Polling...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
