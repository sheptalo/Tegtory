from bot import cur


class GetStockPrice:
    @property
    def get(self):
        cur.execute('SELECT price FROM stock_price')
        price = cur.fetchone()[0]
        print(price)
        return price
