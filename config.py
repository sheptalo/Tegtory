
subscribe_channel = 'Чтобы пользоваться ботом и строить фабрику необходимо быть подписанным на канал @tegtory'

not_enough_points = 'Не хватает очков'
url = ''

factory_not_found: str = 'Фабрика не найдена Попробуйте еще раз'


def factory_image(_type):
    if _type == 'Древесина':
        _type = url + 'pictures/wood/factory_bg1.jfif'
    if _type == 'Железо':
        _type = url + 'pictures/iron/Iron.jpg'
    if _type == 'Химикаты':
        _type = url + 'pictures/chimcats/chimicats.webp'
    if _type == 'Солнечная энергия':
        _type = url + 'pictures/electro/solar_panel.jpg'
    if _type == 'Атомная энергия':
        _type = url + 'pictures/nuclear_electro/nuclear_bg1.jpg'
    if _type == 'Звездная энергия':
        _type = url + 'pictures/star_factory/star_factory.jpg'
    return _type
