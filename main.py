import psycopg2
import pandas as pd
from financial_statement_analysis import FinancialStatementAnalysis
db_name = "algotradeDB"
host = "api.algotrade.vn"
user = "intern_read_only"
port = 5432
password = "Bingo@0711"



def main():
    ticker_symbol = "MWG"

    conn = psycopg2.connect(database=db_name, 
                            user=user, 
                            password=password, 
                            host=host, 
                            port=port)

    cur = conn.cursor()

    query = f'''SELECT * FROM financial.info i 
                WHERE i.tickersymbol = '{ticker_symbol}'
                AND i.year >= 2021
    '''
    cur.execute(query)
    data = cur.fetchall()

    analyst = FinancialStatementAnalysis(ticker_symbol=ticker_symbol,
                                         start_year=2021,
                                         end_year=2022,
                                         quarter=0,
                                         db_cursor=data)


    # print(analyst)
    analyst.to_txt()
    analyst.to_csv()
   

if __name__=="__main__":
    main()