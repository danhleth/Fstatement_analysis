from dataclasses import dataclass
from abc import ABC, abstractmethod

from typing import Any
import pandas as pd

@dataclass
class FinancialStatementAnalysis:
    def __init__(self, 
                 ticker_symbol: str,
                 start_year:int, 
                 end_year:int,
                 quarter:int,
                 db_cursor:object):
        self.ticker_symbol = ticker_symbol
        self.start_year = start_year
        self.end_year = end_year
        self.quarter = quarter
        self.df = pd.DataFrame(db_cursor, 
                               columns=['id',
                                        'tickersymbol',
                                        'year',
                                        'quarter',
                                        'code',
                                        'value'])


    ## Required methods
    def get_total_debt(self):
        '''
        Total debt = Short term debt (current liabilities) + Long term debt (non-current liabilities)
        '''
        current_liability_code = 3100
        non_current_liability_code = 3300

        current_liability = self.df[(self.df['code'] == current_liability_code)
                                    & (self.df['year']==self.end_year)
                                    & (self.df['quarter'] == self.quarter)]['value']
        non_current_liability = self.df[(self.df['code'] == non_current_liability_code)
                                        & (self.df['year']==self.end_year)
                                        & (self.df['quarter'] == self.quarter)]['value']
        return float(current_liability+non_current_liability)


    def get_revenue(self):
        '''
        Revenue = Sales
        '''
        revenue_code = 10
        revenue = self.df[(self.df['code'] == revenue_code)
                       & (self.df['year'] == self.end_year)
                       & (self.df['quarter'] == self.quarter)]['value'].values[0]
        return revenue
    
    def get_current_liabilities(self):
        '''
        Current liabilities = Short term debt (current liabilities)
        '''
        current_liability_code = 3100
        current_liability = self.df[(self.df['code'] == current_liability_code)
                                    & (self.df['year']==self.end_year)
                                    & (self.df['quarter'] == self.quarter)]['value']
        return current_liability


    def report(self):
        # print("---Financial Statement Analysis---")
        # print("Ticker symbol: ", self.ticker_symbol)
        # print("Start year: ", self.start_year)
        # print("End year: ", self.end_year)
        # print("Quarter: ", self.quarter)
        # print("----------------------------------")
        print("Acitivity ratios")
        print("Inventory turnover: ", self.inventory_turnover())
        print("Days of inventory on hand: ", self.days_of_inventory_on_hand())
        print("Receivable turnover: ", self.reveivable_turnover())
        print("Days of sales outstanding: ", self.days_of_sales_outstanding())
        print("Payable turnover: ", self.payable_turnover())
        print("Number of days of payables: ", self.num_days_of_payables())
        print("Working capital turnover: ", self.working_capital_turnover())
        print("Fixed asset turnover: ", self.fixed_asset_turnover())
        print("Total Asset turnover: ", self.total_asset_turnover())

    
    ## Activity ratios
    def inventory_turnover(self) -> float:
        '''
        Inventory turnover = COGS / Average inventory
        '''
        cogs_code = 21
        inventory_code = 1400
        cogs = self.df[(self.df['code'] == cogs_code)
                       & (self.df['year'] == self.end_year)
                       & (self.df['quarter'] == self.quarter)]['value'].values[0]

        average_inventory = self.df[(self.df['code']== inventory_code)
                                    & (self.df['year']==self.start_year) | (self.df['year']==self.end_year)
                                    & (self.df['quarter']==self.quarter)]['value'].mean()
        return float(cogs) / average_inventory
    

    def days_of_inventory_on_hand(self) -> float:
        '''
        Days of inventory on hand = number of days in period / Inventory turnover
        '''
        number_of_days_in_period = 365
        inventory_turnover = self.inventory_turnover()
        return number_of_days_in_period / inventory_turnover
    

    def reveivable_turnover(self) -> float:
        '''
        Receivable turnover = Revenue / Average receivables
        '''
        receivable_code = 1300
        revenue = self.get_revenue()
        
        average_receivable = self.df[(self.df['code'] == receivable_code)
                                    & (self.df['year']==self.start_year) | (self.df['year']==self.end_year)
                                    & (self.df['quarter'] == self.quarter)]['value'].mean()
        return float(revenue)/average_receivable
    

    def days_of_sales_outstanding(self) -> float:
        '''
        Days of sales outstanding = number of days in period / Receivable turnover
        '''
        number_of_days_in_period = 365
        receivable_turnover = self.reveivable_turnover()
        return number_of_days_in_period / receivable_turnover
    

    def payable_turnover(self) -> float:
        '''
        Payable turnover = COGS / Average payables
        '''
        cogs_code = 21
        average_trade_payable_code = 3130
        cogs = self.df[(self.df['code'] == cogs_code)
                       & (self.df['year'] == self.end_year)
                       & (self.df['quarter'] == self.quarter)]['value'].values[0]
        average_payables = self.df[(self.df['code'] == average_trade_payable_code)
                                   & (self.df['year']==self.start_year) | (self.df['year']==self.end_year)
                                   & (self.df['quarter'] == self.quarter)]['value'].mean()
        return float(cogs) / average_payables
    

    def num_days_of_payables(self) -> float:
        '''
        Number of days of payables = number of days in period / Payable turnover
        '''
        number_of_days_in_period = 365
        payable_turnover = self.payable_turnover()
        return number_of_days_in_period / payable_turnover
    

    def working_capital_turnover(self) -> float:
        '''
        Working capital turnover = Revenue / Average working capital
        '''
        working_capital_code = 10

        revenue = self.get_revenue()
        average_working_capital = self.df[(self.df['code'] == working_capital_code)
                                          & (self.df['year']==self.start_year) | (self.df['year']==self.end_year)
                                          & (self.df['quarter'] == self.quarter)]['value'].mean()
        return float(revenue)/average_working_capital
    

    def fixed_asset_turnover(self) -> float:
        '''
        Fixed asset turnover = Revenue / Average fixed assets
        '''
        fix_asset_code = 2200
        revenue = self.get_revenue()
        fix_asset = self.df[(self.df['code'] == fix_asset_code)
                            & (self.df['year']==self.start_year) | (self.df['year']==self.end_year)
                            & (self.df['quarter'] == self.quarter)]['value'].mean()
        return float(revenue)/fix_asset
    

    def total_asset_turnover(self) -> float:
        '''
        Asset turnover = Revenue / Average total assets
        '''
        total_asset_code = 2800
        revenue = self.get_revenue()
        total_asset = self.df[(self.df['code'] == total_asset_code)
                              & (self.df['year']==self.start_year) | (self.df['year']==self.end_year)
                              & (self.df['quarter'] == self.quarter)]['value'].mean()
        return float(revenue)/total_asset
    

    ## Liquidity ratios
    def current_ratio(self):
        '''
        Current ratio = Current assets / Current liabilities
        '''
        current_asset_code = 1000

        current_asset = self.df[(self.df['code'] == current_asset_code)
                                & (self.df['year']==self.end_year)
                                & (self.df['quarter'] == self.quarter)]['value']
        
        current_liability =  self.get_current_liabilities()
        return current_asset/current_liability
    

    def quick_ratio(self):
        '''
        Quick ratio = (Cash+Short term investment+Receivables) / Current liabilities
        '''
        cash_code = 1100
        short_term_investment_code = 1200
        cash = self.df[(self.df['code'] == cash_code)
                       & (self.df['year']==self.end_year)
                       & (self.df['quarter'] == self.quarter)]['value']
        short_term_investment = self.df[(self.df['code'] == short_term_investment_code)
                                        & (self.df['year']==self.end_year)
                                        & (self.df['quarter'] == self.quarter)]['value']
        current_liability = self.get_current_liabilities()
        return float(cash+short_term_investment)/current_liability
    
    
    def cash_ratio(self):
        '''
        Cash ratio = (Cash+Short term investment) / Current liabilities
        '''
        cash_code = 1100
        short_term_investment_code = 1200
        cash = self.df[(self.df['code'] == cash_code)
                       & (self.df['year']==self.end_year)
                       & (self.df['quarter'] == self.quarter)]['value']
        short_term_investment = self.df[(self.df['code'] == short_term_investment_code)
                                        & (self.df['year']==self.end_year)
                                        & (self.df['quarter'] == self.quarter)]['value']
        current_liability = self.get_current_liabilities()                
        return float(cash+short_term_investment)/current_liability           

    def cash_conversion_cycle(self):
        '''
        Cash conversion cycle = Days of sales outstanding + Days of inventory on hand - Number of days of payables
        '''
        return self.days_of_sales_outstanding() + self.days_of_inventory_on_hand() - self.num_days_of_payables()


    def debt_to_assets_ratio(self):
        '''
        Debt to assets ratio = Total debt / Total assets
        Total debt = Short term debt (current liabilities) + Long term debt (non-current liabilities)
        '''

        total_asset_code = 2800

        total_debt = self.get_total_debt()
        total_asset = self.df[(self.df['code'] == total_asset_code)
                              & (self.df['year']==self.end_year)
                              & (self.df['quarter'] == self.quarter)]['value']
        
        return total_debt/total_asset


    def debt_to_capital_ratio(self):
        '''
        Debt to capital ratio = Total debt / (Total debt + Total shareholder's equity)
        Total shareholder's equity = Total assets - Total debt
        '''
        total_asset_code = 2800
        total_asset = self.df[(self.df['code'] == total_asset_code)
                              & (self.df['year']==self.end_year)
                              & (self.df['quarter'] == self.quarter)]['value']
        total_debt = self.get_total_debt()


