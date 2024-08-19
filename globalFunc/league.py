from bot import cur, con


def league():
    cur.execute('UPDATE Users SET league = ? WHERE money < 10000', ('Деревянная лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=10000 AND money < 25000',
                ('Каменная лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=25000 AND money < 50000',
                ('Медная лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=50000 AND money < 100000',
                ('Бронзовая лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=100000 AND money < 1000000',
                ('Серебряная лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=1000000 AND money < 100000000',
                ('Золотая лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=10000000 AND money < 1000000000',
                ('Обсидиановая лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=100000000 AND money < 10000000000',
                ('Сапфировая лига',))
    cur.execute('UPDATE Users SET league = ? WHERE money >=1000000000 AND money < 100000000000',
                ('Бриллиантовая лига',))
    cur.execute('UPDATE Users SET league = ? WHERE stolar >=5 AND money > 100000000', ('Лига столар',))

    con.commit()
