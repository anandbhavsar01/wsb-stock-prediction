import pandas as pd
import numpy as np

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
    weight_dict   = dict()
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
                weight_dict[int(day['Day'])]  = holding_dict[int(day['Day'])]/holding_dict[int(day['Day'])].sum(axis =1).values[0]
            print(equity, stocks)
    #print(equity) 
    return equity_dict,holding_dict, weight_dict


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
                    stocks[stock] += 1
                elif day[stock] < 0:
                    # sell stock
                    if stocks[stock] > day[stock]:
                        stocks[stock] -= 1
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


#sell_at_end_model(stocks, sentiment_data, ticker_data)


def get_trading_return_with_strategy(stocks,trading_decision,ticker_data):
    
    equity_dict,holding_dict, weight_dict  = equity_model(stocks, trading_decision.fillna(0), ticker_data)
    equity_df  = pd.DataFrame(equity_dict, index = ['Portfolio Value']).T
    weight_df  = pd.concat(holding_dict)

    equal_weight  = 1/len(weight_df.columns)
    equal_weight_df = pd.DataFrame(data = equal_weight, index = weight_df.index, columns = weight_df.columns)
    weight_df   = pd.concat(weight_dict)
    weight_df.iloc[0,:] = equal_weight

# compare the returns
    weight_df             = weight_df.reset_index().drop(columns = 'level_1')
    weight_df             = weight_df.rename(columns = {'level_0': 'Day'})
    weight_df             = weight_df.set_index('Day')

    equal_weight_df             = equal_weight_df.reset_index()
    equal_weight_df             = equal_weight_df.rename(columns = {'level_0': 'Day'})
    equal_weight_df             = equal_weight_df.set_index('Day')

    ticker_data_idx       = ticker_data.set_index('Day')


    open2open_ret             = ticker_data_idx.diff(1)/ticker_data_idx
    ret_template              = pd.DataFrame(index = open2open_ret.index, columns = open2open_ret.columns )
    ret_template_weights      = ret_template.fillna(weight_df  ).fillna(method = 'ffill')
    ret_template_equal_weights   = ret_template.fillna(equal_weight_df  ).fillna(method = 'ffill')
    strategy_ret      = (open2open_ret * ret_template_weights).sum(axis =1)
    benchmark_ret      = (open2open_ret * ret_template_equal_weights).sum(axis =1)
    combined_ret       = pd.concat([strategy_ret , benchmark_ret],axis =1)
    combined_ret.columns = ['strategy','benchmark']
    ticker_data_time = pd.read_excel('tickerdata_day_open_LX.xlsx').Day
    combined_ret.index =ticker_data_time
    return weight_df, strategy_ret, combined_ret

stocks = { 'PLTR':0,'RKT':0,'ONE':0,'AMC':0,'REAL':0,'SPCE':0,'AMD':0,'DD':0,'GME':0,'TSLA':0,'CRSR':0,'RH':0,'BB':0,'CLOV':0,
    'NOK':0,'AM':0,'WISH':0,'UWMC':0,'BY':0,'MVIS':0,'NIO':0,'APP':0,'SNDL':0,'AAL':0,'TD':0 }
sentiment_data =  pd.read_csv('dataset/sentiment_ticker_by_day_sum.csv')
ticker_data = pd.read_excel('tickerdata_day_open.xlsx')
#sell_at_end_model(stocks, sentiment_data, ticker_data)
sentiment_data =  pd.read_csv('dataset/sentiment_ticker_by_day_sum.csv').set_index('Day').shift(1)
sentiment_data['Day']  = sentiment_data.index
weight_df, strategy_ret, combined_ret  = get_trading_return_with_strategy(stocks, sentiment_data.fillna(0),ticker_data)

decision_tree_decision    = pd.read_csv('./Dataset/wsb_reddit_returns_sign_timestamp_final.csv').set_index('index')

decision_tree_decision['Ticker']      = decision_tree_decision .apply(lambda x:x.Ticker.replace("{'",'').replace("'}",'').replace("', '",' '),axis =1)

VADER_sentiment = pd.read_csv('text_and_label.csv', index_col =0)
VADER_sentiment.index.name ='index'
matched_df   = pd.merge(VADER_sentiment, decision_tree_decision, left_index = True, right_index= True)
matched_df   = matched_df.set_index('timestamp_x')
matched_df.index  = pd.to_datetime(matched_df.index).floor('D')

decision_df   = pd.DataFrame(index = matched_df.index,columns = ticker_data.columns[1:])
for i in range(len(matched_df['Ticker'])):
    ticker_list  = matched_df['Ticker'].iloc[i].split(' ')
    time          =  matched_df.index[i]
    for ticker in ticker_list:
        decision      = matched_df.index[i][]
        decision_df.iloc[time][ticker]   = decision
        
        
def get_decision_from_ml(mloutput):
    
