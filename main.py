import psycopg2
import pandas as pd
from financial_statement_analysis import InforBaseCompany
from argparse import ArgumentParser
db_name = "algotradeDB"
host = "api.algotrade.vn"
user = "intern_re@d_only"
port = 5432
password = "DDDDDDD"



def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--symbol", type=str, default="VNM")
    arg_parser.add_argument("--start_year", type=int, default=2021)
    arg_parser.add_argument("--end_year", type=int, default=2022)
    arg_parser.add_argument("--quarter", type=int, default=0)
    args = arg_parser.parse_args()


    conn = psycopg2.connect(database=db_name, 
                            user=user, 
                            password=password, 
                            host=host, 
                            port=port)

    cur = conn.cursor()

    query = f'''SELECT * FROM financial.info i 
                WHERE i.tickersymbol = '{args.symbol}'
                AND i.year >= 2021
    '''
    cur.execute(query)
    data = cur.fetchall()

    analyst = InforBaseCompany(ticker_symbol=args.symbol,
                                         start_year=args.start_year,
                                         end_year=args.end_year,
                                         quarter=args.quarter,
                                         db_cursor=data)


    print(analyst)
    # analyst.to_txt()
    # analyst.to_csv()
   

if __name__=="__main__":
    main()