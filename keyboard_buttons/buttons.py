from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

currency = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Dollar", callback_data="USD"),],
        [InlineKeyboardButton(text="Euro", callback_data="EUR"),],
        [InlineKeyboardButton(text="Rubl", callback_data="RUB"),],
        [InlineKeyboardButton(text="Yuan", callback_data="CYN"),],
        [InlineKeyboardButton(text="Manat", callback_data="TMT"),],
        [InlineKeyboardButton(text="Dirxam", callback_data="AED"),]
            
    ]
        
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ortga", callback_data="back")]
        
        
    ]
    

)





from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



valyut = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Valyuta")]
    ],
    resize_keyboard=True,
    input_field_placeholder="valyuta tugmasini bosing"
)
