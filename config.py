
subscribe_channel = 'Чтобы пользоваться ботом и строить фабрику необходимо быть подписанным на канал @tegtory'

not_enough_points = 'Не хватает очков'
factory_not_found = 'Фабрика не найдена Попробуйте еще раз'


def factory_image(_type):
    if _type == 'Древесина':
        _type = 'AgACAgIAAxkBAAII3mcj1ngy48AO2ub-tBZS2lBSFv7hAAKE5jEblg8ZSdSU_7oUOcB5AQADAgADeQADNgQ'
    if _type == 'Железо':
        _type = 'AgACAgIAAxkBAAII32cj1utn_1RJAZ1Wz339Udc0KoXNAALS6jEbBlIgSarZTcxZjWiCAQADAgADeQADNgQ'
    if _type == 'Химикаты':
        _type = 'AgACAgIAAxkBAAII4Gcj1xAb22Sh5PKIa9LbRz4AAY8ybQAC0-oxGwZSIEn3Nyyg12JjzwEAAwIAA3kAAzYE'
    if _type == 'Солнечная энергия':
        _type = 'AgACAgIAAxkBAAII4Wcj10BZ0iDWa_rVgNiCXJn8S_ZhAALX6jEbBlIgSUVzf5261ePYAQADAgADeQADNgQ'
    if _type == 'Атомная энергия':
        _type = 'AgACAgIAAxkBAAII4mcj129mnyqxO7eHAAHWobAdZ-Za8gAC2eoxGwZSIElhG4gbE-dRGgEAAwIAA3kAAzYE'
    if _type == 'Звездная энергия':
        _type = 'AgACAgIAAxkBAAII42cj2GN5iNFXq3m1HMmM7lI3QBKhAAKs5DEb0wLRSF37P9zMX_4lAQADAgADdwADNgQ'
    return _type
