#/usr/local/bin/python3
from bs4 import BeautifulSoup
import requests
from terminaltables import AsciiTable

cash = 100000000
list_of_tickers = ["AMZN", "AAPL", "SNAP", "AMD", "LLY"]

def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)


def list_shares(trades):
    # shares = 0
    sorted_trades = sorted(trades, key=lambda x: x.postdate, reverse=True)
    for trade in sorted_trades:
        print "-----------"
        print "Side: "+str(trade.side)
        print "Ticker: "+trade.symbol
        print "Quantity: "+str(trade.quantity)
        print "Executed price: "+as_currency(trade.price)
        print "Executed Timestamp: "+str(trade.postdate)
        print "Money In/Out: "+as_currency(trade.price*float(trade.quantity.replace(',', '')))
        print "-----------"


def num_shares(trades, symbol):
    shares = 0
    for trade in trades:

        if trade.side == 'BUY' and trade.symbol == symbol:
            shares += int(trade.quantity)
        if trade.side == 'SELL' and trade.symbol == symbol:
            shares -= int(trade.quantity)
    return shares


def sold_shares(trades, symbol):
    shares = 0
    for trade in trades:
        if trade.side == 'SELL' and trade.symbol == symbol:
            shares += int(trade.quantity)
    return shares


def pl(market, the_wap, shares):
    return float((market-the_wap)*int(shares))

def wap(trades, symbol):
    the_wap = 0
    acum = 0
    for trade in trades:
        if trade.side == 'BUY' and trade.symbol == symbol:
            the_wap += int(trade.quantity)*trade.price
            acum += int(trade.quantity)
    if acum > 0:
        return float(the_wap/acum)
    else:
        return float(0.00)


def market(trades, symbol):
    # market price is the latest price you buy or sell, if there's no orders, use the one in yahoo.
    sorted_trades = sorted((t for t in trades if t.symbol == symbol), key=lambda x: x.postdate, reverse=True)
    if len(sorted_trades)>0:
        return float(sorted_trades[0].price)
    else:
        r = requests.get('https://finance.yahoo.com/quote/' + symbol)
        soup = BeautifulSoup(r.content, 'html.parser')
        return float(soup.findAll(match_class(["Trsdu(0.3s)"]))[0].text.replace(',', ''))


def market_ask(symbol):
    r = requests.get('https://finance.yahoo.com/quote/' + symbol)
    soup = BeautifulSoup(r.content, 'html.parser')
    return float(soup.find("td", {"data-test": "ASK-value"}).text.split('x')[0].replace(',',''))

def market_bid(symbol):
    r = requests.get('https://finance.yahoo.com/quote/' + symbol)
    soup = BeautifulSoup(r.content, 'html.parser')
    return float(soup.find("td", {"data-test": "BID-value"}).text.split('x')[0].replace(',',''))


def trade(trades):
    global cash, list_of_tickers
    import datetime
    from order import Order

    print ("available symbols: "+", ".join(list_of_tickers))
    symbol = ""
    the_type = ""
    amount = 0

    while symbol not in list_of_tickers:
        symbol = raw_input("please type a symbol")
    while the_type not in ["BUY", "SELL"]:
        the_type = raw_input("Type of trade(BUY, SELL):")
    while amount <= 0:
        amount = raw_input("number of shares:")

    if the_type == "BUY":
        price = market_ask(symbol)
        confirm = raw_input("Please confirm if you want to buy " + amount + " shares at a price of " + as_currency(price) + " per share. (Y to confirm)")

        if confirm == "Y":
            total = float(amount) * price
            if total <= cash:
                the_order = Order(the_type, symbol, amount, price, datetime.datetime.now())
                cash -= total
                trades.append(the_order)
                return True
            else:
                print "Not enough money."
                return None
        else:
            print "transaction cancelled."
            return None
    else:
        price = market_bid(symbol)
        confirm = raw_input("Please confirm if you want to sell " + amount + " shares at a price of " + as_currency(price) + " per share. (Y to confirm)")
        if confirm == "Y":
            # check if you have enough shares to sell
            if num_shares(trades, symbol) >= int(amount):
                total = float(amount) * price
                cash += total
                the_order = Order(the_type, symbol, amount, price, datetime.datetime.now())
                trades.append(the_order)
                return True
            else:
                print "Not enough shares to sell."
                return None
        else:
            print "transaction cancelled."
            return None


def show_pl(trades):
    global cash, list_of_tickers
    data = []
    data.append(['Ticker', 'Position', 'Market', 'WAP', 'UPL', 'RPL'])
    for the_trade in list_of_tickers:
        ns = num_shares(trades, the_trade)
        ss = sold_shares(trades, the_trade)
        ma = market(trades, the_trade)
        wap_price = wap(trades, the_trade)
        upl = pl(ma, wap_price, ns) # here is not ma, but the price at BUY/SELL of the latest trade | video->17:50
        rpl = pl(ma, wap_price, ss) # here is not ma, but the price at SELL of the latest trade | video->17:50

        data.append([the_trade, ns, as_currency(ma), as_currency(wap_price), as_currency(upl), as_currency(rpl)])
    table = AsciiTable(data)
    print table.table
    print "your cash is "+as_currency(cash)


def main():
    global cash
    res = 0
    trades = list()

    while res != 4:
        res = input("---------------------\n1. Trade\n2. Show Blotter\n3. Show P/L\n4. Quit\n---------------------")
        if res == 1:
            trade(trades)
        if res == 2:
            list_shares(trades)
        if res == 3:
            show_pl(trades)
        if res == 4:
            print "Bye!"


if __name__ == "__main__":
    main()
