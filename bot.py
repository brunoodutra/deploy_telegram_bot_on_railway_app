#!/usr/bin/env python
# coding: utf-8

# ### Bot Telegran

# In[ ]:


#%% imports and librarys 
#https://api.telegram.org/bot5653024553:AAEoPXvjfmoG8hUKYF50LyxL5DHrzDyTEfQ/getUpdates
import numpy as np
import pandas as pd
import pickle

import random
from datetime import datetime
import pytz

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from telegram import ParseMode


# ### Roleta Game custom function  

# In[ ]:


Group_ID=-1001842984697


# In[ ]:


from Game_Cassino_functions import Scraping_Roleta_Game
Rom1=Scraping_Roleta_Game()
Rom1.login('Roullete1')

Rom2=Scraping_Roleta_Game()
Rom2.login('Roullete2')
#values=Rom1.get_history(10)


# In[ ]:


Room_mobile_link= Rom1.get_room_mobile_link()
Room_desktop_link=Rom1.get_room_desktop_link()
room_name=Rom1.get_room_name()


# ### Pre-processing

# In[ ]:



#%% configuração de data e hora do brasil 
T_br = pytz.timezone('America/Sao_Paulo') 

#%% configuração do tokenizer responsável do pré-processamento das palavras antes de ir pra rede 
 
replace_list = {r"á": 'a',
                r"ê": 'e',
                r"ç": 'c',
                r"â":  'a',
                r"'ve": ' have',
                r"can't": 'can not',
                r"cannot": 'can not',
                r"shan’t": 'shall not',
                r"n't": ' not',
                r"'d": ' would',
                r"'ll": ' will',
                r"'scuse": 'excuse',
                ',': ' ',
                '.': ' ',
                '!': ' ',
                '?': ' ',
                '\s+': ' '}
#%% funções de pré-processamento
def clean_text(text):
    text = text.lower()
    for s in replace_list:
        text = text.replace(s, replace_list[s])
    text = ' '.join(text.split())
    return text


# ### Telegran init 

# In[ ]:


#%% configuração de integração com o telegran 
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# #### Functions to use with telegran API

# #### Command functions

# In[ ]:


#%% funções para leitura de frases e palavras do telegran 

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
from urllib import response


def start(update: Update, context: CallbackContext) -> None:
    global SuperUser
    SuperUser = update.message.from_user
    print(SuperUser.to_json)
     
    """Send a message when the command /start is issued."""
    response="""Oi eu sou o RedBot estou aqui para te indicar os melhores Sinais de Roleta. 
Digite: \n 
/help \n
/ultimo_valor_da_roleta \n
/ultimos_10_valores_da_roleta \n
/qnty_duzia \n
/qnty_coluna \n
para receber opções"""

    update.message.reply_text(response)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(' Sou treinado para informar sinais de Roleta Online com base em sequências de dúzias e colunas. \n'+
                                'Caso queira participar do grupo de sinais mande menssagem para (92)9362-0447')

def qnty_duzia(update: Update, context: CallbackContext) -> None:
    global coluna
    update.message.reply_text(duzia)

def qnty_coluna(update: Update, context: CallbackContext) -> None:
    global coluna
    update.message.reply_text(coluna)

def ultimos_10_valores_da_roleta(update: Update, context: CallbackContext) -> None:
    values=Rom1.get_history(10)
    update.message.reply_text( text='Os últimos números que sairam foram: \n' 
                                              + str(values['number'].values))

def ultimo_valor_da_roleta(update: Update, context: CallbackContext) -> None:
    global Rom1
    values=Rom1.get_history(1)

    response="o ultimo valor sorteado foi: "+str(values.values[0][0])+" "+values.values[0][1]
    
    update.message.reply_text(response)

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


# #### Receive (data, image, menssage, document) Functions 

# In[ ]:


def menssagem(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global T_br, datetime, user ,ID
    datetime= datetime.now(T_br)
    user = update.message.from_user
    ID = update.message.chat_id
    print(user.to_json)
    nome=user.first_name
    
    print(user.first_name,user.last_name,'está conversando com o RedBot')
    #update.message.reply_text(resposta)
    
    msg=update.message.text
    msg=msg.lower()

    #resp=read_text(clean_text(msg))
    if msg=='ok' or msg=='tudo bem' or msg=='certo' or msg=='ta bom' or msg=='blz' or msg=='show' or msg=='oks' or msg=='ta':
        pass
    elif msg=='oi':
        resposta=("oi "+ nome +", fique atento que logo mais mando alguns sinais")
    #elif msg=='hora':
    #    print(msg)
    #    #resposta=respondebot(msg,nome,datetime.hour)
    #    resposta=datetime.hour
    #    print(resposta)
    #    update.message.reply_text(resposta)
    else:
        pass
        #update.message.reply_text('aguarde que estou analizando a mesa e logo mais mando um sinal')

def image_handler(update, context):
    update.message.reply_text("Imagem Recebida")
    group_id = update.message.media_group_id

    if group_id is None:
        file = context.bot.getFile(update.message.photo[0].file_id)
        print ("file_id: " + str(update.message.photo[0].file_id))
        file.download('saved_image.jpg')

def document_handler(update, context):
    update.message.reply_text("Documento Recebido")
    
    group_id = update.message.media_group_id
    
    if group_id is None:
        file = context.bot.getFile(update.message.document.file_id)
        print ("file_id: " + str(update.message.document.file_id))
        file.download('arquivo_recebido.xlsx')


# In[ ]:


""" if values['number'][0] >=1 and values['number'][0] <=12:
        duzia[0]+=1
        duzia[1]=0
        duzia[2]=0
        print('Duzia 1 ++',duzia)

    elif values['number'][0] >=13 and values['number'][0] <=24:
        duzia[0]=0
        duzia[1]+=1
        duzia[2]=0
        print('Duzia 2 ++',duzia)

    elif values['number'][0] >=25 and values['number'][0] <=36:
        duzia[0]=0
        duzia[1]=0
        duzia[2]+=1
        print('Duzia 3 ++',duzia)
"""

"""
if values['number'][0] != values['number'][1] and values['number'][1] != values['number'][2]:
            if values['number'][0:1].between(0,12):
                duzia[0]=values['number'][0:5].between(0,12).value_counts().values[0]
                duzia[1]=0
                duzia[2]=0

            elif values['number'][0:1].between(13,24):    
                duzia[0]=0
                duzia[1]=values['number'][0:5].between(13,24).value_counts().values[0]
                duzia[2]=0

            elif values['number'][0:1].between(25,36): 
                duzia[0]=0
                duzia[1]=0   
                duzia[2]=values['number'][0:5].between(25,36).value_counts().values[0]
                
            print('Duzias',duzia)
        else:
            duzia[0]=0
            duzia[1]=0
            duzia[2]=0
"""


# ### Strategys

# In[ ]:


def duzia_strategy(context):
    global status, values1, values, num_repetido, last_numbers
    global duzia, Entrada_status_duzia, duzia_do_sinal, duzia_Entrada, duzia_list, Martingale_duzia, bot_chat_id_duzia
    global coluna, Entrada_status_coluna, coluna_do_sinal, coluna_Entrada ,coluna_list, Martingale_duzia_coluna, numbers_in_column, bot_chat_id_coluna
    
    if Entrada_status_duzia==2 and (duzia[0]>=5 or duzia[1]>=5 or duzia[2]>=5):
        print('Martingale_duzia')
        Martingale_duzia=duzia[duzia_do_sinal]

    if Entrada_status_duzia==1 and (duzia[0]<3 and duzia[1]<3 and duzia[2]<3):
        print('Sinal Cancelado')
        #context.bot.send_message(chat_id=Group_ID, text='❌❌❌ SINAL DE MESA CANCELADO ❌❌❌ ')
        context.bot.deleteMessage (message_id = bot_chat_id_duzia.message_id,
                                        chat_id = Group_ID)
        Entrada_status_duzia=0

    if Entrada_status_duzia==0 and (duzia[0]==3 or duzia[1]==3 or duzia[2]==3):
        print('Espera Sinal')
        
        max_value = max(duzia)
        duzia_do_sinal = duzia.index(max_value)
        
        duzia_Entrada=[]
        for i in duzia_list:
            if i != (duzia_do_sinal+1):
                duzia_Entrada.append(i)
        
        last_numbers=Rom1.get_history(4)
        bot_chat_id_duzia = context.bot.send_message(chat_id=Group_ID, text='🚨 ANALISANDO MESA 🚨 \n'+ '\n'+
                                                                '🏦 Mesa: '+room_name+'\n \n'
                                                                '🧠 Estratégia: apostar na '+str(duzia_Entrada[0])+'º e na '+str(duzia_Entrada[1]) +'º duzia \n \n'+
                                                                """🗣 Cobrir o ZERO (0) com 2 % da banca"""+'\n \n'+
                                                                '🚦 Últimos números que sairam: \n \n' 
                                                                 + str(last_numbers['number'].values) +'\n \n'+
                                                                 "🔗 LINKS: <a href='"+Room_mobile_link+"'>📱Celular</a> <a href='"+Room_desktop_link+"'>💻Computador</a> ",parse_mode=ParseMode.HTML)  
                                                               
        Entrada_status_duzia=1


    elif Entrada_status_duzia==1 and (duzia[0]==4 or duzia[1]==4 or duzia[2]==4):
        print('Confirma Sinal')

        last_numbers=Rom1.get_history(4)
        bot_chat_id_duzia=context.bot.send_message(chat_id=Group_ID, text='☑️ ENTRADA CONFIRMADA!!! ☑️ \n'+ '\n'+
                                                                '🏦 Mesa: '+room_name+'\n \n'
                                                                '🧠 Estratégia: apostar na '+str(duzia_Entrada[0])+'º e na '+str(duzia_Entrada[1]) +'º duzia \n \n'+
                                                                """🗣 Cobrir o ZERO (0) com 2 % da banca"""+'\n \n'+
                                                                '🚦 Últimos números que sairam: \n \n' 
                                                                 + str(last_numbers['number'].values) +'\n \n'+
                                                                 "🔗 LINKS: <a href='"+Room_mobile_link+"'>📱Celular</a> <a href='"+Room_desktop_link+"'>💻Computador</a> ",parse_mode=ParseMode.HTML)    
        Entrada_status_duzia=2

    if Entrada_status_duzia==2 and ((duzia[duzia_Entrada[0]-1]>0 or duzia[duzia_Entrada[1]-1]>0) or values['number'][0]==0):
         print('Ganho do Sinal')
         print(duzia)
         print(duzia_Entrada)
         
         if Martingale_duzia>1:
            last_numbers=Rom1.get_history(((Martingale_duzia + num_repetido) - 3))
            context.bot.send_message(chat_id=Group_ID, text='✅ RED BOT ACERTOU ✅🚀🚀 \n'+
                                                                'Os Útilmos Números Sorteados foram: '+str(last_numbers['number'].values), reply_to_message_id=bot_chat_id_duzia.message_id)
         else:
            context.bot.send_message(chat_id=Group_ID, text='✅ RED BOT ACERTOU ✅🚀🚀 \n'+
                                                                'O Útilmo Número Sorteado foi: '+str(str(values['number'][0])), reply_to_message_id=bot_chat_id_duzia.message_id)
         Entrada_status_duzia=0
         Martingale_duzia=0
         num_repetido=0

    elif Entrada_status_duzia==2 and(duzia[0]>=7 or duzia[1]>=7 or duzia[2]>=7):
        print('Derrota do Sinal')
        context.bot.send_message(chat_id=Group_ID, text='❌ O Robô Errou ❌', reply_to_message_id=bot_chat_id_duzia.message_id)
        Entrada_status_duzia=0
        Martingale_duzia=0
        num_repetido=0


# In[ ]:


def coluna_strategy(context):
    
    global status, values1, values, bot_chat_id, num_repetido, last_numbers
    global duzia, Entrada_status_duzia, duzia_do_sinal, duzia_Entrada, duzia_list, Martingale_duzia, bot_chat_id_coluna_duzia
    global coluna, Entrada_status_coluna, coluna_do_sinal, coluna_Entrada ,coluna_list, Martingale_coluna, numbers_in_column, bot_chat_id_coluna
    
    if Entrada_status_coluna==2 and (coluna[0]>=5 or coluna[1]>=5 or coluna[2]>=5):
        print('Martingale_coluna')
        Martingale_coluna=coluna[coluna_do_sinal]

    if Entrada_status_coluna==1 and (coluna[0]<3 and coluna[1]<3 and coluna[2]<3):
        print('Sinal Cancelado')
        #context.bot.send_message(chat_id=Group_ID, text='❌❌❌ SINAL DE MESA CANCELADO ❌❌❌ ')
        context.bot.deleteMessage (message_id = bot_chat_id_coluna.message_id,
                                        chat_id = Group_ID)
        Entrada_status_coluna=0

    if Entrada_status_coluna==0 and (coluna[0]==3 or coluna[1]==3 or coluna[2]==3):
        print('Espera Sinal')
        
        max_value = max(coluna)
        coluna_do_sinal = coluna.index(max_value)
        
        coluna_Entrada=[]
        for i in coluna_list:
            if i != (coluna_do_sinal+1):
                coluna_Entrada.append(i)
        
        last_numbers=Rom1.get_history(4)
        bot_chat_id_coluna = context.bot.send_message(chat_id=Group_ID, text='🚨 ANALISANDO MESA 🚨 \n'+ '\n'+
                                                                '🏦 Mesa: '+room_name+'\n \n'
                                                                '🧠 Estratégia: apostar na '+str(coluna_Entrada[0])+'º e na '+str(coluna_Entrada[1]) +'º coluna \n \n'+
                                                                """🗣 Cobrir o ZERO (0) com 2 % da banca"""+'\n \n'+
                                                                '🚦 Últimos números que sairam: \n \n' 
                                                                 + str(last_numbers['number'].values) +'\n \n'+
                                                                 "🔗 LINKS: <a href='"+Room_mobile_link+"'>📱Celular</a> <a href='"+Room_desktop_link+"'>💻Computador</a> ",parse_mode=ParseMode.HTML)  
                                                               
        Entrada_status_coluna=1


    elif Entrada_status_coluna==1 and (coluna[0]==4 or coluna[1]==4 or coluna[2]==4):
        print('Confirma Sinal')

        last_numbers=Rom1.get_history(4)
        bot_chat_id_coluna=context.bot.send_message(chat_id=Group_ID, text='☑️ ENTRADA CONFIRMADA!!! ☑️ \n'+ '\n'+
                                                                '🏦 Mesa: '+room_name+'\n \n'
                                                                '🧠 Estratégia: apostar na '+str(coluna_Entrada[0])+'º e na '+str(coluna_Entrada[1]) +'º coluna \n \n'+
                                                                """🗣 Cobrir o ZERO (0) com 2 % da banca"""+'\n \n'+
                                                                '🚦 Últimos números que sairam: \n \n' 
                                                                 + str(last_numbers['number'].values) +'\n \n'+
                                                                 "🔗 LINKS: <a href='"+Room_mobile_link+"'>📱Celular</a> <a href='"+Room_desktop_link+"'>💻Computador</a> ",parse_mode=ParseMode.HTML)    
        Entrada_status_coluna=2

    if Entrada_status_coluna==2 and ((coluna[coluna_Entrada[0]-1]>0 or coluna[coluna_Entrada[1]-1]>0) or values['number'][0]==0):
         print('Ganho do Sinal')
         print(coluna)
         print(coluna_Entrada)
         
         if Martingale_coluna>1:
            last_numbers=Rom1.get_history(((Martingale_coluna + num_repetido) - 3))
            context.bot.send_message(chat_id=Group_ID, text='✅ RED BOT ACERTOU ✅🚀🚀 \n'+
                                                                'Os Útilmos Números Sorteados foram: '+str(last_numbers['number'].values), reply_to_message_id=bot_chat_id_coluna.message_id)
         else:
            context.bot.send_message(chat_id=Group_ID, text='✅ RED BOT ACERTOU ✅🚀🚀 \n'+
                                                                'O Útilmo Número Sorteado foi: '+str(str(values['number'][0])), reply_to_message_id=bot_chat_id_coluna.message_id)
         Entrada_status_coluna=0
         Martingale_coluna=0
         num_repetido=0

    elif Entrada_status_coluna==2 and(coluna[0]>=7 or coluna[1]>=7 or coluna[2]>=7):
        print('Derrota do Sinal')
        context.bot.send_message(chat_id=Group_ID, text='❌ O Robô Errou ❌'
                                                    + '🚦 Últimos números que sairam: \n \n' 
                                                    + str(last_numbers['number'].values) +'\n \n', reply_to_message_id=bot_chat_id_coluna.message_id)
        Entrada_status_coluna=0
        Martingale_coluna=0
        num_repetido=0


# #### Signal functions

# In[ ]:


#global status, duzia, chat_id, duzia_list, Martingale, coluna, coluna_list, numbers_in_column

def callback_auto_message(context):   
    global status, values1, values, num_repetido
    global duzia, Entrada_status_duzia, duzia_do_sinal, duzia_Entrada, duzia_list, Martingale_duzia, bot_chat_id_duzia
    global coluna, Entrada_status_coluna, coluna_do_sinal, coluna_Entrada ,coluna_list, Martingale_coluna, numbers_in_column, bot_chat_id_coluna
    if status == 0:
        print('boas vindas')
        context.bot.send_message(chat_id=Group_ID, text='Olá estou começanco a análise da Mesa '+room_name)
        status=1 # status que indica o funcionamento da análise
        Entrada_status_duzia=0
        Entrada_status_coluna=0
        values1=Rom1.get_history(10)
    
    values=Rom1.get_history(10)

    if values1['number'][0]==values['number'][0]:
        num_repetido+=1
    else:
        if Martingale_coluna < 1:
            num_repetido=0
        # --------Verifica a ocorrencia de duzias--------------------------------------------------------------------------------------------
        if values['number'][0] >=1 and values['number'][0] <=12:
            duzia[0]+=1
            duzia[1]=0
            duzia[2]=0
            print('Duzia 1 ++',duzia)

        elif values['number'][0] >=13 and values['number'][0] <=24:
            duzia[0]=0
            duzia[1]+=1
            duzia[2]=0
            print('Duzia 2 ++',duzia)

        elif values['number'][0] >=25 and values['number'][0] <=36:
            duzia[0]=0
            duzia[1]=0
            duzia[2]+=1
            print('Duzia 3 ++',duzia)
        # --------Verifica a ocorrencia de zeros--------------------------------------------------------------------------------------------
        elif (Entrada_status_duzia==0 or Entrada_status_duzia==1)  and values['number'][0] == 0:
            duzia[0]=0
            duzia[1]=0
            duzia[2]=0
        elif Entrada_status_duzia == 2 and values['number'][0] == 0:
            duzia[duzia_do_sinal]+=1

        # --------Verifica a ocorrencia de colunas--------------------------------------------------------------------------------------------
        if values['number'][0] in numbers_in_column[1]:
            coluna[0]+=1
            coluna[1]=0
            coluna[2]=0
            print('Coluna 1 ++',coluna)

        elif values['number'][0] in numbers_in_column[2]:
            coluna[0]=0
            coluna[1]+=1
            coluna[2]=0
            print('Coluna 2 ++',coluna)

        elif values['number'][0] in numbers_in_column[3]:
            coluna[0]=0
            coluna[1]=0
            coluna[2]+=1
            print('Coluna 3 ++',coluna)
        # --------Verifica a ocorrencia de zeros--------------------------------------------------------------------------------------------
        elif (Entrada_status_coluna==0 or Entrada_status_coluna==1)  and values['number'][0] == 0:
            coluna[0]=0
            coluna[1]=0
            coluna[2]=0
        elif Entrada_status_coluna == 2 and values['number'][0] == 0:
            coluna[coluna_do_sinal]+=1

    #----------------------------------------------------------------------------------------------------    
            
    values1 = values 

   # lógia para contagem de dúzias ----------------------------------------------------------------------
    duzia_strategy(context)
    # lógia para contagem de colunas ----------------------------------------------------------------------
    coluna_strategy(context)


# In[ ]:


def start_analysis(update, context):
    global status, values1, values, num_repetido
    global duzia, Entrada_status_duzia, duzia_do_sinal, duzia_Entrada, duzia_list, Martingale_duzia, bot_chat_id_duzia
    global coluna, Entrada_status_coluna, coluna_do_sinal, coluna_Entrada ,coluna_list, Martingale_coluna, numbers_in_column, bot_chat_id_coluna
    
    #-----variáveis globais das duzias--------------------------------------------
    duzia_list=range(1,4)
    duzia=[0,0,0]
    Martingale_duzia=0

    #------variáveis globais das colunas------------------------------------------
    coluna=[0,0,0]
    coluna_list=range(1,4)
    Martingale_coluna=0
    numbers_in_column={1: [1], 2: [2], 3: [3]}
    for i in numbers_in_column:
        for j in range(1,12):
            numbers_in_column[i].append(numbers_in_column[i][-1]+3)
    #-------------------------------------------------------
    num_repetido=0
    status=0
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(callback_auto_message, 30, context=chat_id, name=str(chat_id))
    # context.job_queue.run_once(callback_auto_message, 3600, context=chat_id)
    # context.job_queue.run_daily(callback_auto_message, time=datetime.time(hour=9, minute=22), days=(0, 1, 2, 3, 4, 5, 6), context=chat_id, name=str(chat_id))

def stop_analysis(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=Group_ID, text='Stopping automatic messages!')
    job = context.job_queue.get_jobs_by_name(str(chat_id))
    job[0].schedule_removal()


# #### Telegrans's Main function

# In[ ]:


#%% Função principal responsável por chamar as funções intermediárias de funcionamento do chatboot
#from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.triggers.cron import CronTrigger
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5653024553:AAEoPXvjfmoG8hUKYF50LyxL5DHrzDyTEfQ")
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("ultimo_valor_da_roleta", ultimo_valor_da_roleta))
    dispatcher.add_handler(CommandHandler("ultimos_10_valores_da_roleta", ultimos_10_valores_da_roleta))
    dispatcher.add_handler(CommandHandler("qnty_duzia", qnty_duzia))
    dispatcher.add_handler(CommandHandler("qnty_coluna", qnty_coluna))



    #updater.dispatcher.add_handler(CommandHandler('notify', daily_job, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("start_analysis", start_analysis))
    dispatcher.add_handler(CommandHandler("stop_analysis", stop_analysis))


    updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, document_handler))


    # handler responsável por verificar menssagens aplicar filtros de texto e encaminhar para a função "menssagem"
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, menssagem)) 

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    

if __name__ == '__main__':
    main()


# In[ ]:




