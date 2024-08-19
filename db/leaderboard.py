from bot import cur


class Leaderboard:
    class Money:
        def __str__(self):
            cur.execute('SELECT * FROM Users WHERE id > 5000 ORDER BY money DESC')
            rows = cur.fetchmany(10)
            text = 'Таблица лидеров по деньгам:\n\n'
            place = 1
            for row in rows:
                text += f'{f'place.' if __reward__(place) is None else __reward__(place)} {row[2]}: {row[3]:,}\n'
                place += 1
            return text

        def me(self, iternal_id):
            if iternal_id < 5000:
                return 0
            counter = 1
            cur.execute('SELECT id FROM Users WHERE id > 5000 ORDER BY money DESC')
            rows = cur.fetchall()
            for row in rows:
                if iternal_id == row[0]:
                    return counter
                counter += 1

    class Stolar:
        def __str__(self):
            cur.execute('SELECT * FROM Users WHERE id > 5000 ORDER BY stolar DESC')
            rows = cur.fetchmany(10)
            text = 'Таблица лидеров по столар коинам:\n\n'
            place = 1
            for row in rows:
                text += f'{f'place.' if __reward__(place) is None else __reward__(place)} {row[2]}: {row[6]:,}\n'
                place += 1
            return text

        def me(self, iternal_id):
            if iternal_id < 5000:
                return 0
            counter = 1
            cur.execute('SELECT id FROM Users WHERE id > 5000 ORDER BY stolar DESC')
            rows = cur.fetchall()
            for row in rows:
                if iternal_id == row[0]:
                    return counter
                counter += 1

    class Rating:
        def __str__(self):
            cur.execute('SELECT * FROM Users WHERE id > 5000 ORDER BY rating DESC')
            rows = cur.fetchmany(10)
            text = 'Самый ценные игроки\n\n'
            place = 1
            for row in rows:
                text += f'{f'place.' if __reward__(place) is None else __reward__(place)} {row[2]}: {row[7]:,}\n'
                place += 1
            return text

        def me(self, iternal_id):
            if iternal_id < 5000:
                return 0
            counter = 1
            cur.execute('SELECT id FROM Users WHERE id > 5000 ORDER BY rating DESC')
            rows = cur.fetchall()
            for row in rows:
                if iternal_id == row[0]:
                    return counter
                counter += 1

    class Level:
        def __str__(self):
            cur.execute('SELECT * FROM Factory WHERE owner_id > 5000 ORDER BY lvl DESC')
            rows = cur.fetchmany(10)
            text = '*Лучшие фабрики*\n\n'
            place = 1
            for row in rows:
                text += f'{f'place.' if __reward__(place) is None else __reward__(place)} {row[1]}: {row[2]} уровень {row[3]}\n'
                place += 1
            return text

        def me(self, iternal_id):
            if iternal_id < 5000:
                return 0
            counter = 1
            cur.execute('SELECT owner_id FROM Factory WHERE owner_id > 5000 ORDER BY lvl DESC')
            rows = cur.fetchall()
            for row in rows:
                if iternal_id == row[0]:
                    return counter
                counter += 1

    class Eco:
        def __str__(self):
            cur.execute('SELECT name, ecology FROM Factory WHERE owner_id > 5000 ORDER BY ecology DESC')
            rows = cur.fetchmany(10)
            text = '*Самые чистые фабрики*\n\n'
            place = 1
            for row in rows:
                text += f'{f'place.' if __reward__(place) is None else __reward__(place)} {row[0]}: {row[1]:,} баллов\n'
                place += 1
            return text

        def me(self, iternal_id):
            if iternal_id < 5000:
                return 0
            cur.execute('SELECT owner_id FROM Factory WHERE owner_id > 5000 ORDER BY ecology DESC')
            place = 1
            rows = cur.fetchall()
            for row in rows:
                if iternal_id == row[0]:
                    return place
                place += 1

    class Clan:
        def __init__(self, name):
            self.clan_name = name

        def __str__(self):
            cur.execute(f'SELECT name, money, clan_leader FROM Users WHERE'
                        f' clan_name = %s AND id > 5000 ORDER BY money DESC',
                        (self.clan_name,))
            leaders = cur.fetchall()
            total_money = 0
            text = 'Таблица лидеров объединения\n\n'
            for row in leaders:
                total_money += row[1]
            leaders = leaders[:3]
            place = 1
            for leader in leaders:
                text += __reward__(place)
                text += f' {leader[0]}: {leader[1]:,} {'👑' if leader[2] == 1 else ''}\n'
                place += 1

            text += f'\n💸Баланс объединения {total_money:,}\n\n'
            return text

    def my_place_any(self, iternal_id) -> int:
        if iternal_id < 5000:
            return 0
        places = [self.Money().me(iternal_id),
                  self.Stolar().me(iternal_id),
                  self.Rating().me(iternal_id),
                  self.Level().me(iternal_id)]
        places.sort(reverse=True)
        return places[0]


def __reward__(place):
    if place == 1:
        return '🥇'
    if place == 2:
        return '🥈'
    if place == 3:
        return '🥉'
    return None
