from bot import TeleBot
from tic_tac_toe import TicTacToe
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.tic_tac_toe_handlers.choose_dimension import *

def choose_mode(teleBot: TeleBot, query_id: int, chat_id: int, message_id: int, username: str, chat_type: str): 
	msg_id = (chat_id, message_id)

	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='Single Player', callback_data='single'),
		InlineKeyboardButton(text='Duo Player', callback_data='duo'),
  		InlineKeyboardButton(text='Triple Player', callback_data='triple')]
	])
 
	teleBot.bot.editMessageText(msg_id, 'Pilih Mode:')
	teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=buttons)

def get_choose_mode_handler(jumlah_player: int):
	def handler(teleBot: TeleBot, query_id, chat_id, message_id, username, chat_type):
		# teleBot.bot.answerCallbackQuery(query_id, text='Mode: ' + str(jumlah_player) + ' player')
		game: TicTacToe = TicTacToe.load(message_id)
		msg_id = (chat_id, message_id)
  
		# Jika dichat pribadi maka fitur multiplayer akan nonaktif
		if (jumlah_player == 2 or jumlah_player == 3) and chat_type == 'private':
			teleBot.bot.answerCallbackQuery(query_id, text='Permainan multiplayer hanya untuk grup')
			return
		if jumlah_player == 1:
			game.set_symbol_player_count(1)
			game.save()
			size_buttons(teleBot, query_id, chat_id, message_id, username, chat_type)
		if jumlah_player == 2 and chat_type == "group":
			game.set_symbol_player_count(2)
			game.save()
			teleBot.bot.editMessageText(msg_id, 'Tag lawan Anda!')
			teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=None)
		if jumlah_player == 3 and chat_type == "group":
			game.set_symbol_player_count(3)
			game.save()
			teleBot.bot.editMessageText(msg_id, 'Menunggu pemain ketiga untuk bergabung...', 
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Bergabung', callback_data='join')]]))
            # Menghapus tombol mode setelah memulai permainan
			teleBot.bot.editMessageReplyMarkup(msg_id, reply_markup=None)
	return handler