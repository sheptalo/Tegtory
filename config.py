# region text

subscribe_channel = ('Чтобы пользоваться ботом и строить фабрику необходимо быть подписанным на офф канал бота '
                     '@tegtory')

not_enough_points = 'Не хватает очков'


factory_not_finded = 'Фабрика не найдена Попробуйте еще раз'

# endregion

wood = 'pictures/wood/factory_bg1.jfif'

coal = 'pictures/iron/Iron.jpg'

electro = 'pictures/electro/solar_panel.jpg'

nuclear_energy = 'pictures/nuclear_electro/nuclear_bg1.jpg'

star_factory = 'pictures/star_factory/star_factory.jpg'

chimicats = 'pictures/chimcats/chimicats.webp'


factory_types = ['Древесина', 'Железо', 'Химикаты', 'Солнечная энергия' 'Атомная энергия']


def type_func(_type):
    if _type == 'Древесина':
        _type = wood
    if _type == 'Железо':
        _type = coal
    if _type == 'Химикаты':
        _type = chimicats
    if _type == 'Солнечная энергия':
        _type = electro
    if _type == 'Атомная энергия':
        _type = nuclear_energy
    if _type == 'Звездная энергия':
        _type = star_factory
    return _type
