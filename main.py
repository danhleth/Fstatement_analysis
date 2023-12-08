import psycopg2
import pandas as pd
from financial_statement_analysis import FinancialStatementAnalysis
db_name = "algotradeDB"
host = "api.algotrade.vn"
user = "intern_re@d_only"
port = 5432
password = "@@@@@@@@@@@@"



def main():
    conn = psycopg2.connect(database=db_name, 
                            user=user, 
                            password=password, 
                            host=host, 
                            port=port)

    cur = conn.cursor()

    query = '''SELECT * FROM financial.info i 
                WHERE i.tickersymbol = 'MWG'
                AND i.year >= 2021
    '''
    cur.execute(query)
    data = cur.fetchall()

    analyst = FinancialStatementAnalysis(ticker_symbol="MWG",
                                         start_year=2021,
                                         end_year=2022,
                                         quarter=0,
                                         db_cursor=data)


    analyst.report()

if __name__=="__main__":
    main()