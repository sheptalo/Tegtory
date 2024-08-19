# def leaderboard_for_all(): TODO
#     cl.execute('SELECT * from Clans WHERE clan_name != ?', ('0',))
#     clans = cl.fetchall()
#     clan_data = []
#     for rate in clans:
#         cl.execute('SELECT user_id from Clans WHERE clan_name = ?', (rate[0],))
#         users = cl.fetchall()
#         users_data = list()
#         for _id in users:
#             cursor.execute('SELECT * from Users WHERE id = ?', (_id[0],))
#             a = get_title(_id[0])
#             cannot_be_inLeader = False
#             for title in a:
#                 if title != 'Разработчик':
#                     pass
#                 else:
#                     cannot_be_inLeader = True
#                 if title == 'Тестер':
#                     cannot_be_inLeader = True
#
#             if cannot_be_inLeader:
#                 continue
#             users_data.append(cursor.fetchone())
#
#         sorted_arrays = sorted(users_data, key=lambda x: x[2], reverse=True)
#         total_money = 0
#         for money in sorted_arrays:
#             total_money += money[2]
#         if total_money < 50000:
#             continue
#         ready_for_leaderboard = [rate[0], total_money]
#         clan_data.append(ready_for_leaderboard)
#
#     leaderboard_array = []
#     for item in clan_data:
#         if item not in leaderboard_array:
#             leaderboard_array.append(item)
#
#     place = 1
#     text = '🏆 *Самые богатые обьединения* 🏆 \n'
#     for item in leaderboard_array:
#         if place == 1:
#             text += '🥇'
#         if place == 2:
#             text += '🥈'
#         if place == 3:
#             text += '🥉'
#         text += f'{place}. *Название*: {item[0].replace('_', ' ')}\n*Баланс* {item[1]:,} \n \n'
#         place += 1
#     connection.close()
#     clan.close()
#     return text
#
# def find_factory_fight(par):
#     connection = sqlite3.connect('/data/my_database.db')
#     cursor = connection.cursor()
#     a = []
#     cursor.execute('SELECT lvl FROM Factory WHERE owner_id = ?', (par,))
#     a.append(cursor.fetchone()[0])
#     cursor.execute('SELECT workers FROM Factory WHERE owner_id = ?', (par,))
#     a.append(cursor.fetchone()[0])
#     connection.close()
#     create_user_in_management(par)
#     create_user_in_stanki(par)
#     manag = sqlite3.connect('/data/management.db')
#     manag_cr = manag.cursor()
#
#     manag_cr.execute('SELECT lvl,quality FROM Management WHERE user_id = ?', (par,))
#     try:
#         b = manag_cr.fetchone()
#         for i in b:
#             a.append(i)
#     except:
#         create_user_in_management(par)
#
#     manag.close()
#     for stanki in get_stanki(par):
#         a.append(stanki)
#     return a
