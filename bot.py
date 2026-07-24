import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. Flask setup for Back4App
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running on high conversion mode!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Security Setup
# Khassk t-revoki l-token l-qdime f @BotFather w tzid jdid f l-Environment Variables dyal Back4App b smiyt TELEGRAM_TOKEN
API_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8930786040:AAFG2ChKQ1zQ-f98StKDAyiaGzwl8Hmko10") 
AFFILIATE_LINK = 'https://affs.click'

bot = telebot.TeleBot(API_TOKEN)

# 3. Copywriting ghadi ykhlli l-nas f Brasil fihom l-foudoul (Curiosity Hook)
STEP1_TEXT = (
    "⚡ **Oportunidade Única de Renda Automática!**\n\n"
    "Cansado de passar horas analisando gráficos ou perdendo dinheiro? Descubra como o nosso sistema inteligente faz todo o trabalho pesado por você.\n\n"
    "🔥 100% no piloto automático.\n"
    "🔥 Sem precisar de experiência prévia.\n\n"
    "👇 **Toque no botão abaixo para ver como funciona:**"
)

STEP2_TEXT = (
    "🤖 **Tecnologia de Cópia Avançada**\n\n"
    "O nosso sistema replica em tempo real as operações dos traders mais lucrativos do mercado financeiro direto na sua conta.\n\n"
    "📈 Quando eles lucram, você lucra também, sem precisar fazer nada.\n"
    "⏱️ A configuração inicial leva menos de 2 minutos.\n\n"
    "👇 **Clique abaixo para ir para o passo final e ativar:**"
)

STEP3_TEXT = (
    "🎯 **Seu Acesso Gratuito Está Liberado!**\n\n"
    "Para ativar o sistema automático na sua conta agora mesmo, siga os passos:\n\n"
    "1️⃣ Clique no botão oficial abaixo para abrir sua conta de negociação.\n"
    "2️⃣ Faça a ativação da sua conta com o saldo mínimo de operação.\n"
    "3️⃣ Conecte ao nosso sistema automático e comece a rodar.\n\n"
    "🚨 *Nota: As vagas gratuitas com taxa zero são extremamente limitadas hoje.*"
)

# 4. Handlers
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
        
        bot.send_message(chat_id=call.message.chat.id, text=STEP2_TEXT, parse_mode="Markdown", reply_markup=markup)
        
        # إزالة الزر السابق لمنع التكرار
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        except Exception:
            pass
                              
    elif call.data == "go_3":
        markup = types.InlineKeyboardMarkup()
        btn_final = types.InlineKeyboardButton(text="💰 ATIVAR SISTEMA AGORA", url=AFFILIATE_LINK)
        markup.add(btn_final)
        
        bot.send_message(chat_id=call.message.chat.id, text=STEP3_TEXT, parse_mode="Markdown", reply_markup=markup)
                         
        try:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        except Exception:
            pass

# 5. Production Loop
if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Bot is polling successfully...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            pass
