class AppException(Exception):
    message = ""

    def __init__(self, message=""):
        if message:
            self.message = message


class NotEnoughPointsException(AppException):
    message = "Недостаточно очков"


class TaxException(AppException):
    message = "Выплатите Налоги чтобы продолжить"


class DuringWorkException(AppException):
    message = "Невозможно выполнить действие во время работы"
