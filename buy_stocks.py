import pandas as pd

def run_model():
    sentiment_data =  pd.read_csv('dataset/sentiment_ticker_by_day.csv')
    ticker_data = pd.read_excel('tickerdata_day_open.xlsx')

    balance = 0
    stocks = { 'PLTR':0,'RKT':0,'ONE':0,'AMC':0,'REAL':0,'SPCE':0,'AMD':0,'DD':0,'GME':0,'TSLA':0,'CRSR':0,'RH':0,'BB':0,'CLOV':0,
    'NOK':0,'AM':0,'WISH':0,'UWMC':0,'BY':0,'MVIS':0,'NIO':0,'APP':0,'SNDL':0,'AAL':0,'TD':0 }
    for i, day in sentiment_data.iterrows():
        if int(day['Day']) in ticker_data.Day.values:
            print('Day', day['Day'])
            for stock in stocks.keys():
                if day[stock] > 0:
                    # buy stock
                    stocks[stock] += 1
                    balance -= ticker_data.loc[ticker_data['Day']==int(day['Day']),stock].values[0]
                elif day[stock] < 0:
                    # sell stock
                    if stocks[stock] > 0:
                        stocks[stock] -= 1
                        balance += ticker_data.loc[ticker_data['Day']==int(day['Day']),stock].values[0]
                # else hold
            print(balance, stocks)
    # Now assume we sell all the stocks on the last day
    last_day = ticker_data.iloc[-1]
    for stock in stocks.keys():
        balance += stocks[stock] * last_day[stock]
    print(balance)
run_model()
