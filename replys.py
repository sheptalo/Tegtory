from aiogram.types import LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

working_on_kb = [
    [InlineKeyboardButton(text='Разрабатывается', callback_data='working_on')]
]
working_on = InlineKeyboardMarkup(inline_keyboard=working_on_kb)

menu_kb = [
    [
        KeyboardButton(text="Фабрика"),
        KeyboardButton(text='Город'),
        KeyboardButton(text='Помощь')
    ],
    [
        KeyboardButton(text='Объединение'),
        KeyboardButton(text='Мини игры')
    ]
]
menu_reply = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=menu_kb)

mini_gms = [
    [
        KeyboardButton(text='Инспекция'),
        KeyboardButton(text='Биржа')
    ],
    [
        KeyboardButton(text='Меню')
    ]
]
mini_game_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=mini_gms)

rinok_kb = [
    [
        InlineKeyboardButton(text='Продать на @tegtoryshop', callback_data='sellonrinok'),
        InlineKeyboardButton(text='Купить', callback_data='buy_stolar_coin')
    ],
    [
        InlineKeyboardButton(text='Купить 10x', callback_data='buy_stolar_coin_10x'),
        InlineKeyboardButton(text='Купить 100x', callback_data='buy_stolar_coin_100x')
    ],
    [InlineKeyboardButton(text='Обратно', callback_data='city')]
]
rinok_markup = InlineKeyboardMarkup(inline_keyboard=rinok_kb)

clan_kb = [
    [InlineKeyboardButton(text='лидирующие обьединения', callback_data='clan_leaderboard')],
    [
        InlineKeyboardButton(text='Уровень', callback_data='factory_leaderboard'),
        InlineKeyboardButton(text='Экология', callback_data='eco_leaderboard')
    ],
    [
        InlineKeyboardButton(text='Денежная', callback_data='leaderboard'),
        InlineKeyboardButton(text='Столар', callback_data='stolar_leaderboard')],
    [InlineKeyboardButton(text='Рейтинг', callback_data='rating_leaderboard')],
    [
        InlineKeyboardButton(text='прошлые сезоны', callback_data='old_leaderboard'),
        InlineKeyboardButton(text='В город', callback_data='city')
    ]
]
leaderboard_inline = InlineKeyboardMarkup(inline_keyboard=clan_kb)

shop_kb = [
    [InlineKeyboardButton(text='Титулы', callback_data='титулы')],
    [
        InlineKeyboardButton(text='Донат', callback_data='донат'),
        InlineKeyboardButton(text='Лотерея', callback_data='лотерея')
    ],
    # [InlineKeyboardButton(text='Имущество', callback_data='имущество')],
    [InlineKeyboardButton(text='В город', callback_data='city')]
]
shop_reply = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=shop_kb)

factory_kb = [
    [
        InlineKeyboardButton(text='Работать', callback_data='work'),
        InlineKeyboardButton(text="Запустить фабрику", callback_data='start_factory')],
    [
        InlineKeyboardButton(text="Улучшение", callback_data='upgrade_factory'),
        InlineKeyboardButton(text='Работники', callback_data='workers'), ],
    [
        InlineKeyboardButton(text='Налоги', callback_data='tax'),
        InlineKeyboardButton(text='Я', callback_data='profile')
    ],
    [
        InlineKeyboardButton(text='Экология', callback_data='ecology_factory')
    ]
]
factory_reply = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=factory_kb)

hire_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Нанять', callback_data='hire_worker')],
    [InlineKeyboardButton(text='Обратно', callback_data='back_factory')]])

upgrade_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='улучшить', callback_data='upgrade_factory_conf')],
    [InlineKeyboardButton(text='Обратно', callback_data='back_factory')]])

subscribed_channel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Готово', callback_data='subscribe')],])

tax_markup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Оплатить налоги', callback_data='pay_tax')],
                     [InlineKeyboardButton(text='Обратно', callback_data='back_factory')]])

lottery_kb = [
    [InlineKeyboardButton(text='Купить бронзовый билет', callback_data='bronze_ticket')],
    [InlineKeyboardButton(text='Купить Серебряный билет', callback_data='serebro_ticket')],
    [InlineKeyboardButton(text='Купить золотой билет', callback_data='gold_ticket')],
    [InlineKeyboardButton(text='Купить Столар билет', callback_data='stolar_ticket')],
    [InlineKeyboardButton(text='Обратно', callback_data='back_shop')],

]
lottery_markup = InlineKeyboardMarkup(inline_keyboard=lottery_kb)

old_seasons_kb = [
    [InlineKeyboardButton(text='Сезон pre-alpha', callback_data='pre_apha_season')],
    [InlineKeyboardButton(text='Сезон alpha', callback_data='alpha_season')],
    [InlineKeyboardButton(text='Обратно', callback_data='old_leaderboard')]
]
old_seasons_markup = InlineKeyboardMarkup(inline_keyboard=old_seasons_kb)

property_kb = [
    [
        InlineKeyboardButton(text='Дома', callback_data='дом'),
        InlineKeyboardButton(text='Машины', callback_data='машина'),
        InlineKeyboardButton(text='Вещи', callback_data='Вещи')
    ],
    [InlineKeyboardButton(text='Обратно', callback_data='back_shop')]
]
property_reply = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=property_kb)

title_shop_kb = [
    [
        InlineKeyboardButton(text='Богач', callback_data='buy_title:Богач'),
        InlineKeyboardButton(text='Магнат', callback_data='buy_title:Магнат')
    ],
    [
        InlineKeyboardButton(text='Один из лучших', callback_data='buy_title:Один_из_лучших')
    ],
    [
        InlineKeyboardButton(text='Эколог', callback_data='buy_title:Эколог'),
        InlineKeyboardButton(text='Хранитель', callback_data='buy_title:Хранитель')
    ],
    [InlineKeyboardButton(text='Обратно', callback_data='back_shop')]
]
titles_shop_markup = InlineKeyboardMarkup(inline_keyboard=title_shop_kb)

title_error = [
    [InlineKeyboardButton(text='Обратно', callback_data='титулы')],
]
title_error_markup = InlineKeyboardMarkup(inline_keyboard=title_error)

prices = [LabeledPrice(label='100000 очков', amount=8500)]

market_kb = [
    [
        InlineKeyboardButton(text='Продать', callback_data='sell_on_market')
    ],
    [
        InlineKeyboardButton(text='Обратно', callback_data='city')
    ]
]
market_markup = InlineKeyboardMarkup(inline_keyboard=market_kb)

back_shop_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обратно', callback_data='back_shop')]])

ecology_kb = [
    [InlineKeyboardButton(text='Уменьшить выбросы +1 1050', callback_data='ecology:1')],
    [InlineKeyboardButton(text='покупка фильтров +2 2050', callback_data='ecology:2'),],
    [InlineKeyboardButton(text='рециркуляции воды +5 5050', callback_data='ecology:5')],
    [InlineKeyboardButton(text='энергоэффективные технологии +10 1050', callback_data='ecology:10')],
    [InlineKeyboardButton(text='Обратно', callback_data='back_factory')]
]
ecology_markup = InlineKeyboardMarkup(inline_keyboard=ecology_kb)

city_kb = [
    [
        InlineKeyboardButton(text='Магазин', callback_data='shop'),
        InlineKeyboardButton(text='Зал славы', callback_data='leaderboard')
    ],
    [
        InlineKeyboardButton(text='Рынок', callback_data='рынок'),
        InlineKeyboardButton(text='Маркет', callback_data='маркет')
    ]
]
city_markup = InlineKeyboardMarkup(inline_keyboard=city_kb)

lottery_back_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обратно', callback_data='Лотерея')]
])

back_city = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Обратно', callback_data='city')]])


back_factory = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обратно', callback_data='back_factory')]])

create_factory_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать фабрику', callback_data='create_factory')]])