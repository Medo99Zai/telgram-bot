import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. إعداد سيرفر Flask لـ Back4App Health Check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. إعدادات البوت والـ Affiliate Link
API_TOKEN = '8930786040:AAFG2ChKQ1zQ-f98StKDAyiaGzwl8Hmko10'
XM_LINK = 'https://affs.click/8Raj3'

bot = telebot.TeleBot(API_TOKEN)

# 3. النصوص الاحترافية والقصير (Pro)
STEP1_TEXT = (
    "⚡ **Acesso Liberado!**\n\n"
    "Você não precisa entender de gráficos para ver resultados no mercado. O sistema executa as operações de forma automatizada.\n\n"
    "👇 Clique abaixo para ver como configurar o seu:"
)

STEP2_TEXT = (
    "📈 **Prático e Direto ao Ponto**\n\n"
    "Basta conectar sua conta para seguir as estratégias validadas. Sem complicações técnicas.\n\n"
    "👇 Toque no botão para ir à etapa final:"
)

STEP3_TEXT = (
    "🎯 **Última Etapa**\n\n"
    "O ambiente de ativação está pronto. Crie sua conta agora و comece a operar de forma automatizada:\n\n"
    "👇 Clique no botão oficial abaixo:"
)

# 4. Handlers ديال التليغرام
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="👉 CONTINUAR", callback_data="go_2")
    markup.add(btn)
    bot.send_message(message.chat.id, STEP1_TEXT, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "go_2":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="🚀 VER PASSO FINAL", callback_data="go_3")
        markup.add(btn)
        
        bot.send_message(chat_id=call.message.chat.id, 
                         text=STEP2_TEXT, 
                         parse_mode="Markdown", 
                         reply_markup=markup)
        
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        except Exception:
            pass
                              
    elif call.data == "go_3":
        markup = types.InlineKeyboardMarkup()
        btn_final = types.InlineKeyboardButton(text="💰 ATIVAR CONTA AGORA", url=XM_LINK)
        markup.add(btn_final)
        
        bot.send_message(chat_id=call.message.chat.id, 
                         text=STEP3_TEXT, 
                         parse_mode="Markdown", 
                         reply_markup=markup)
                         
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        except Exception:
            pass

# 5. التشغيل المتوازي (Flask + Telegram Bot)
if __name__ == '__main__':
    # تشغيل Flask في Background Thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Starting Telegram Bot Polling...")
    # تشغيل البوت الأساسي
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
