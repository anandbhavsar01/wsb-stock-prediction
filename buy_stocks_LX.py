import pandas as pd


def equity_model_ts(stocks, sentiment_data, ticker_data):
    sentiment  = sentiment_data
    equity_dict = dict()
    holding_dict  = dict()
    for day in sentiment_data.index:
            print('Day', day)
            equity = 0
            for stock in stocks.keys():
                if sentiment.loc[day,stock] > 0:
                    # buy stock
                    stocks[stock] += sentiment.loc[day,stock]
                elif sentiment.loc[day,stock] < 0:
                    # sell stock
                    if stocks[stock] > sentiment.loc[day,stock]:
                        stocks[stock] -= sentiment.loc[day,stock]
                    else:
                        stocks[stock] = 0
                equity += stocks[stock] * ticker_data.loc[ticker_data['Day']==sentiment.loc[day]].values[0]
                # else hold
                equity_dict[day] = equity
                holding_dict[day] = stocks
            print(equity, stocks)
    print(equity) 
    return equity_dict,holding_dict


def equity_model(stocks, sentiment_data, ticker_data):
    equity_dict = dict()
    holding_dict  = dict()
    for i, day in sentiment_data.iterrows():
        print(int(day['Day']))
        if int(day['Day']) in ticker_data.Day.values:
            print(int(day['Day']) in ticker_data.Day.values)
            print('Day', day['Day'])
            equity = 0
            for stock in stocks.keys():
                if day[stock] > 0:
                    # buy stock
                    stocks[stock] += day[stock]
                elif day[stock] < 0:
                    # sell stock
                    if stocks[stock] > day[stock]:
                        stocks[stock] -= day[stock]
                    else:
                        stocks[stock] = 0
                equity += stocks[stock] * ticker_data.loc[ticker_data['Day']==int(day['Day']),stock].values[0]
                # else hold
                equity_dict[int(day['Day'])] = equity
                holding_dict[int(day['Day'])] = pd.DataFrame(stocks, index = [int(day['Day'])])
            print(equity, stocks)
    #print(equity) 
    return equity_dict,holding_dict


def equity_model_oneshare(stocks, sentiment_data, ticker_data):
    equity_dict = dict()
    holding_dict  = dict()
    for i, day in sentiment_data.iterrows():
        print(int(day['Day']))
        if int(day['Day']) in ticker_data.Day.values:
            print(int(day['Day']) in ticker_data.Day.values)
            print('Day', day['Day'])
            equity = 0
            for stock in stocks.keys():
                if day[stock] > 0:
                    # buy stock
                    stocks[stock] += day[stock]
                elif day[stock] < 0:
                    # sell stock
                    if stocks[stock] > day[stock]:
                        stocks[stock] -= day[stock]
                    else:
                        stocks[stock] = 0
                equity += stocks[stock] * ticker_data.loc[ticker_data['Day']==int(day['Day']),stock].values[0]
                # else hold
                equity_dict[int(day['Day'])] = equity
                holding_dict[int(day['Day'])] = pd.DataFrame(stocks, index = [int(day['Day'])])
            print(equity, stocks)
    #print(equity) 
    return equity_dict,holding_dict


def sell_at_end_model(stocks, sentiment_data, ticker_data):
    balance = 0
    for i, day in sentiment_data.iterrows():
        if int(day['Day']) in ticker_data.Day.values:
            print('Day', day['Day'])
            for stock in stocks.keys():
                if day[stock] > 0:
                    # buy stock
                    stocks[stock] += day[stock]
                    balance -= day[stock] * ticker_data.loc[ticker_data['Day']==int(day['Day']),stock].values[0]
                elif day[stock] < 0:
                    # sell stock
                    if stocks[stock] > day[stock]:
                        stocks[stock] -= day[stock]
                        balance += day[stock] * ticker_data.loc[ticker_data['Day']==int(day['Day']),stock].values[0]
                    else:
                        balance += stocks[stock] * ticker_data.loc[ticker_data['Day']==int(day['Day']),stock].values[0]
                        stocks[stock] = 0
                # else hold
            print(balance, stocks)
    # Now assume we sell all the stocks on the last day
    last_day = ticker_data.iloc[-1]
    for stock in stocks.keys():
        balance += stocks[stock] * last_day[stock]
    print(balance)

stocks = { 'PLTR':0,'RKT':0,'ONE':0,'AMC':0,'REAL':0,'SPCE':0,'AMD':0,'DD':0,'GME':0,'TSLA':0,'CRSR':0,'RH':0,'BB':0,'CLOV':0,
    'NOK':0,'AM':0,'WISH':0,'UWMC':0,'BY':0,'MVIS':0,'NIO':0,'APP':0,'SNDL':0,'AAL':0,'TD':0 }
sentiment_data =  pd.read_csv('dataset/sentiment_ticker_by_day_sum.csv')
ticker_data = pd.read_excel('tickerdata_day_open.xlsx')
#sell_at_end_model(stocks, sentiment_data, ticker_data)
sentiment_data =  pd.read_csv('dataset/sentiment_ticker_by_day_sum.csv').set_index('Day').shift(1)
sentiment_data['Day']  = sentiment_data.index
#sell_at_end_model(stocks, sentiment_data, ticker_data)
equity_dict,holding_dict  = equity_model(stocks, sentiment_data.fillna(0), ticker_data)
equity_df  = pd.DataFrame(equity_dict, index = ['Portfolio Value']).T
holding_df  = pd.concat(holding_dict)


ticker_data = pd.read_excel('tickerdata_day_open_LX.xlsx')
#sell_at_end_model(stocks, sentiment_data, ticker_data)
sentiment_data =  pd.read_csv('dataset/sentiment_by_ticker_sum.csv').shift(1)
equity_dict,holding_dict  = equity_model_ts(stocks, sentiment_data.fillna(0), ticker_data)
