#Data gathering step: Extracting the data
def get_AB_loans(engine):
    import pandas as pd
    query = '''select t.type, t.operation, t.amount as t_amount, t.balance, t.k_symbol, l.amount as l_amount, l.duration, l.payments, l.status
    from trans t
    left join loan l
    on t.account_id = l.account_id
    where l.status in ('A', 'B');'''
    engine = engine.get_engine(password)
    data = pd.read_sql_query(query, engine)
    return data

def get_loans(engine):
    import pandas as pd
    query = '''select l.loan_id, l.amount, l.duration, l.payments, l.status, d.A2 as District, d.A3 as Region from bank.loan as l
    join bank.account as a
    on l.account_id = a.account_id
    join bank.district as d
    on a.district_id = d.A1;'''
    #engine = engine.get_engine(password)
    data = pd.read_sql_query(query, engine)
    return data

def get_debt(engine):
    import pandas as pd
    query = '''select  d.A3 as Region, d.A2 as District, l.status as Status, sum(l.amount-l.payments) as Debt from bank.loan as l
    join bank.account as a
    on l.account_id = a.account_id
    join bank.district as d
    on a.district_id = d.A1
    group by Region, District, Status
    order by Region, District, Status;'''
    data = pd.read_sql_query(query, engine)
    return data

def cleanOperation(x):
    x = x.lower()
    if 'vyber' in x:
        return "vyber"
    elif 'prevod' in x:
        return "prevod"
    elif 'vklad' in x:
        return 'vklad'
    else:
        return 'unknown'

def cleankSymbol(x):
    if x in ['', ' ']:
        return 'unknown'
    else:
        return x

def cleanDuration(x):
    if x in ['48', '60']:
        return 'other'
    else:
        return str(x)

def preprocess(df):
    df['operation'] = list(map(cleanOperation,df['operation']))
    df['k_symbol'] = list(map(cleankSymbol, df['k_symbol']))
    df = df[~df['k_symbol'].isin(['POJISTINE', 'SANKC. UROK', 'UVER'])]
    df['duration'] = df['duration'].astype('str')
    df['duration'] = list(map(cleanDuration, df['duration']))
    df.reset_index(inplace=True, drop=True)
    return df
