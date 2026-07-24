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

# 3. نصوص محفزة باعتدال، بروفيسيونال، وكتجيب الكليكات بنكهة واقعية
STEP1_TEXT = (
    "⚡ **Oportunidade Única no Mercado!**\n\n"
    "Cansado de trocar seu tempo por pouco dinheiro? Descubra como o sistema automatizado faz o trabalho pesado por você no mercado financeiro.\n\n"
    "🔥 Sem precisar de experiência prévia ou análises chatas.\n\n"
    "👇 **Toque no botão abaixo para ver os detalhes:**"
)

STEP2_TEXT = (
    "📈 **Praticidade e Resultados Reais**\n\n"
    "O robô executa as estratégias validadas diretamente na sua conta, de forma 100% automática.\n\n"
    "⏱️ O processo leva menos de um minuto para configurar.\n\n"
    "👇 **Clique para avançar para a última etapa:**"
)

STEP3_TEXT = (
    "🎯 **Tudo Pronto para Começar!**\n\n"
    "O seu acesso exclusivo está liberado. Crie sua conta agora e ative o sistema automático:\n\n"
    "👇 **Clique no botão oficial abaixo:**"
)

# 4. Handlers ديال التليغرام (إرسال رسالة جديدة بإشعار في كل إطاب)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="👉 QUERO VER COMO FUNCIONA", callback_data="go_2")
    markup.add(btn)
    bot.send_message(message.chat.id, STEP1_TEXT, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "go_2":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="🚀 VER ETAPA FINAL", callback_data="go_3")
        markup.add(btn)
        
        # إرسال ميساج جديد مع Notification جديدة
        bot.send_message(chat_id=call.message.chat.id, 
                         text=STEP2_TEXT, 
                         parse_mode="Markdown", 
                         reply_markup=markup)
        
        # إزالة الزر القديم
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        except Exception:
            pass
                              
    elif call.data == "go_3":
        markup = types.InlineKeyboardMarkup()
        btn_final = types.InlineKeyboardButton(text="💰 ATIVAR SISTEMA AGORA", url=XM_LINK)
        markup.add(btn_final)
        
        # إرسال الميساج النهائي برابط الإفلييت
        bot.send_message(chat_id=call.message.chat.id, 
                         text=STEP3_TEXT, 
                         parse_mode="Markdown", 
                         reply_markup=markup)
                         
        # إزالة الأزرار القديمة
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        except Exception:
            pass

# 5. التشغيل المتوازي السريع
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
