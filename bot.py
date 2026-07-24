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

# 2. إعدادات البوت والـ Affiliate Link
API_TOKEN = '8930786040:AAFG2ChKQ1zQ-f98StKDAyiaGzwl8Hmko10'
XM_LINK = 'https://affs.click/8Raj3'

bot = telebot.TeleBot(API_TOKEN)

# 3. نصوص الفانل بالبرتغالية (تتناسب مع الترافيك البرازيلي)
STEP1_TEXT = (
    "🚨 **ATENÇÃO: Vagas extremamente limitadas para hoje!**\n\n"
    "Trabalhar 8 horas por dia para enriquecer os outros já era.\n\n"
    "Agora, existe um sistema 100% automático que faz o mercado financeiro trabalhar para você enquanto dorme, sem precisar de experiência ou análises complexas.\n\n"
    "🔥 **Aviso:** Abrimos **apenas 10 vagas hoje** para evitar sobrecarga no servidor, e sua vaga pode expirar.\n\n"
    "Quer ver como funciona em 30 segundos antes que feche? 👇"
)

STEP2_TEXT = (
    "⚡ **Passo 2: Simplicidade Absoluta (Zero Experiência)**\n\n"
    "Você não precisa entender nada de trading! Neste sistema, você simplesmente **copia automaticamente** as operações dos maiores especialistas.\n\n"
    "📈 Eles analisam e operam.\n"
    "💰 Os lucros vão direto para a sua conta.\n\n"
    "Pronto para garantir sua vaga final? 👇"
)

STEP3_TEXT = (
    "🔥 **Parabéns! Sua vaga foi aprovada temporariamente.**\n\n"
    "⏱️ **Atenção:** O sistema vai fechar o acesso em **15 minutos** devido à alta demanda.\n\n"
    "Seu link direto está pronto. Clique no botão abaixo para criar sua conta e ativar o sistema automático agora mesmo: 👇"
)

# 4. Handlers ديال التليغرام (إرسال رسالة جديدة بإشعار في كل إطاب)
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
        btn_final = types.InlineKeyboardButton(text="💰 ATIVAR SISTEMA AUTOMÁTICO", url=XM_LINK)
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

# 5. تشغيل السيرفر والبوت
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
