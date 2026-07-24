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

# 3. النصوص المحفزة، اللي كاتبيع الوهم وتجيب الكليكات بأقوى إيموجيز (Top 1)
STEP1_TEXT = (
    "🚨 **ATENÇÃO ABSOLUTA! ISSO VAI MUDAR SUA VIDA HOJE!** 👑\n\n"
    "Chega de ser escravo do sistema e trabalhar 8 horas por dia para deixar os outros ricos! 🛑💸\n\n"
    "🔥 **Descubra o robô mágico e lendário** que gera milhares de dólares no mercado financeiro enquanto você dorme na sua cama, sem experiência e sem nenhum esforço! 🤖💰\n\n"
    "⚠️ **Vagas limitadas e explosivas:** A porta vai fechar hoje para evitar vazamentos! ⚡\n\n"
    "👇 **Clique no botão abaixo para começar agora:**"
)

STEP2_TEXT = (
    "⚡ **VOCÊ ESTÁ A UM PASSO DA RIQUEZA FÁCIL!** 💎\n\n"
    "O sistema automático mais insano do mercado vai assumir o controle total da sua conta agora. 🚀📈\n\n"
    "💵 Seus lucros vão começar a cair de forma automática e descontrolada a cada hora. 🎰✨\n\n"
    "👇 **Clique no botão para abrir o cofre secreto:**"
)

STEP3_TEXT = (
    "🎯 **PARABÉNS! SUA VAGA DE OURO FOI APROVADA!** 🏆\n\n"
    "⏱️ **ALerta Vermelho:** O sistema vai deletar seu acesso em **10 minutos** por excesso de acessos simultâneos! ⚠️🔥\n\n"
    "🔗 O link oficial e definitivo está pronto. Clique no botão abaixo e ative o modo milionário: 👇"
)

# 4. Handlers ديال التليغرام (إرسال رسالة جديدة بإشعار في كل إطاب)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="🔥 [ QUERO FICAR RICO AGORA! ] 🚀", callback_data="go_2")
    markup.add(btn)
    bot.send_message(message.chat.id, STEP1_TEXT, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "go_2":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="⚡ [ ABRIR O COFINHO SECRETO 💸 ] 🔓", callback_data="go_3")
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
        btn_final = types.InlineKeyboardButton(text="💰 [ ATIVAR SISTEMA MILIONÁRIO 🚀 ] 🏆", url=XM_LINK)
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
