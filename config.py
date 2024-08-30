
subscribe_channel = ('Чтобы пользоваться ботом и строить фабрику необходимо быть подписанным на офф канал бота '
                     '@tegtory')

not_enough_points = 'Не хватает очков'


factory_not_found: str = 'Фабрика не найдена Попробуйте еще раз'


def factory_image(_type):
    if _type == 'Древесина':
        _type = 'pictures/wood/factory_bg1.jfif'
    if _type == 'Железо':
        _type = 'pictures/iron/Iron.jpg'
    if _type == 'Химикаты':
        _type = 'pictures/chimcats/chimicats.webp'
    if _type == 'Солнечная энергия':
        _type = 'pictures/electro/solar_panel.jpg'
    if _type == 'Атомная энергия':
        _type = 'pictures/nuclear_electro/nuclear_bg1.jpg'
    if _type == 'Звездная энергия':
        _type = 'pictures/star_factory/star_factory.jpg'
    return _type
