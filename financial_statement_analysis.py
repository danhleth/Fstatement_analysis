from dataclasses import dataclass
from abc import ABC, abstractmethod

from typing import Any
from decimal import Decimal
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
    def __query_average_by_code(self,code):
        # average_total_assets = self.df[(self.df['quarter'] == self.quarter)
        #                                & (self.df['year'] == self.start_year) | (self.df['year']==self.end_year)
        #                                & (self.df['code']==code)]
        average_total_assets = self.df.query(f"code == {code} \
                                            & (year == {self.start_year} | year == {self.end_year}) \
                                            & quarter == {self.quarter}")
        
        average_total_assets = average_total_assets['value'].mean()
        return Decimal(average_total_assets)
    


    def __query_value_by_code(self, code):
        value = self.df.query(f"code == {code} & year == {self.end_year} & quarter == {self.quarter}")['value'].values[0]
        return Decimal(value)


    def get_average_total_assets(self):
        total_assets_code = 2800
        average_total_assets = self.__query_average_by_code(total_assets_code)
        return average_total_assets
    

    def get_average_total_equity(self):
        total_equity_code = 4100
        average_total_equity = self.__query_average_by_code(total_equity_code)
        return average_total_equity
    

    def get_net_income(self):
        net_income_code = 70
        net_income = self.__query_value_by_code(net_income_code)
        return net_income

    def get_total_debt(self):
        '''
        Total debt = Short term debt (current liabilities) + Long term debt (non-current liabilities)
        '''
        # current_liability_code = 3100
        # non_current_liability_code = 3300

        # current_liability = self.__query_value_by_code(current_liability_code)
        # non_current_liability = self.__query_value_by_code(non_current_liability_code)
        
        # total_debt = float(current_liability+non_current_liability)
        total_debt_code = 3000
        total_debt = self.__query_value_by_code(total_debt_code)
        
        return total_debt


    def get_revenue(self):
        '''
        Revenue = Sales
        '''
        revenue_code = 20
        revenue = self.__query_value_by_code(revenue_code)
        return revenue
    

    def get_current_liabilities(self):
        '''
        Current liabilities = Short term debt (current liabilities)
        '''
        current_liability_code = 3100
        current_liability = self.__query_value_by_code(current_liability_code)
        return current_liability


    def __repr__(self):
        content = f'''
        # Financial Statement Analysis 
        Ticker symbol:  {self.ticker_symbol} 
        Start year:  {self.start_year} 
        End year:  {self.end_year} 
        Quarter:  {self.quarter}

        ### Acitivity ratios 
        Inventory turnover:  {self.inventory_turnover()}
        Days of inventory on hand:  {self.days_of_inventory_on_hand()}
        Receivable turnover:  {self.reveivable_turnover()}
        Days of sales outstanding:  {self.days_of_sales_outstanding()}
        Payable turnover:  {self.payable_turnover()}
        Number of days of payables:  {self.num_days_of_payables()}
        Working capital turnover: {self.working_capital_turnover()}
        Fixed asset turnover:  {self.fixed_asset_turnover()}
        Total Asset turnover:  {self.total_asset_turnover()}

        ### Liquidity ratios
        Current ratio: {self.current_ratio()}
        Quick ratio: {self.quick_ratio()}
        Cash ratio: {self.cash_ratio()}
        Cash conversion cycle: {self.cash_conversion_cycle()}

        ### Solvecy ratios
        Debt to assets ratio: {self.debt_to_assets_ratio()}
        Debt to capital ratio: {self.debt_to_capital_ratio()}
        Debt to equity ratio: {self.debt_to_equity_ratio()}
        Financial Leverate ratio: {self.financial_leverager_ratio()}
        Debt to EBITDA: {self.debt_to_ebitda()}
        Interest coverage: {self.interest_coverage()}

        ### Profitability Ratios
        Gross profit margin: {self.gross_profit_margin()}
        Operating profit margin: {self.operating_profit_margin()}
        Pretax margin: {self.pretax_margin()}
        Net profit margin: {self.net_profit_margin()}
        Operating ROA: {self.operating_roa()}
        ROA: {self.roa()}
        ROE: {self.roe()}
        '''
        return content
    
    def to_csv(self, filename='default_log.csv'):
        data = {"Inventory": self.inventory_turnover(),
                "Days of inventory on hand": self.days_of_inventory_on_hand(),
                "Receivable turnover": self.reveivable_turnover(),
                "Days of sales outstanding": self.days_of_sales_outstanding(),
                "Payable turnover": self.payable_turnover(),
                "Number of days of payables": self.num_days_of_payables(),
                "Working capital turnover": self.working_capital_turnover(),
                "Fixed asset turnover": self.fixed_asset_turnover(),
                "Total Asset turnover": self.total_asset_turnover(),
                "Current ratio": self.current_ratio(),
                "Quick ratio": self.quick_ratio(),
                "Cash ratio": self.cash_ratio(),
                "Cash conversion cycle": self.cash_conversion_cycle(),
                "Debt to assets ratio": self.debt_to_assets_ratio(),
                "Debt to capital ratio": self.debt_to_capital_ratio(),
                "Debt to equity ratio": self.debt_to_equity_ratio(),
                "Financial Leverate ratio": self.financial_leverager_ratio(),
                "Debt to EBITDA": self.debt_to_ebitda(),
                "Interest coverage": self.interest_coverage(),
                "Gross profit margin": self.gross_profit_margin(),
                "Operating profit margin": self.operating_profit_margin(),
                "Pretax margin": self.pretax_margin(),
                "Net profit margin": self.net_profit_margin(),
                "Operating ROA": self.operating_roa(),
                "ROA": self.roa(),
                "ROE": self.roe(),
                }
        df = pd.DataFrame(data, index=[0])
        df.to_csv(filename, index=False)


    def to_txt(self, filename="default_log.txt"):
        with open(filename, 'w') as f:
            f.write(self.__repr__())

    
    #########
    ###### Activity ratios
    ###
    def inventory_turnover(self) -> float:
        '''
        Inventory turnover = COGS / Average inventory
        '''
        cogs_code = 21
        inventory_code = 1400
        cogs = self.__query_value_by_code(cogs_code)
        average_inventory = self.__query_average_by_code(inventory_code)
        return cogs / average_inventory
    

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
        receivable_code = 1310
        revenue = self.get_revenue()
        
        average_receivable = self.__query_average_by_code(receivable_code)
        return revenue/average_receivable
    

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
        cogs = self.__query_value_by_code(cogs_code)
        average_payables = self.__query_average_by_code(average_trade_payable_code)
        return cogs / average_payables
    

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
        Working capital = Current assets - Current liabilities
        '''
        working_capital_code = 10
        current_assets_code = 1000
        current_liabilities_code = 3100

        revenue = self.get_revenue()
        average_working_capital = self.__query_average_by_code(current_assets_code) - self.__query_average_by_code(current_liabilities_code)
        return revenue/average_working_capital
    

    def fixed_asset_turnover(self) -> float:
        '''
        Fixed asset turnover = Revenue / Average fixed assets
        '''
        fix_asset_code = 2200
        revenue = self.get_revenue()
        avg_fix_asset = self.__query_average_by_code(fix_asset_code)
        return revenue/avg_fix_asset
    

    def total_asset_turnover(self) -> float:
        '''
        Asset turnover = Revenue / Average total assets
        '''
        revenue = self.get_revenue()
        average_total_assets = self.get_average_total_assets()
        return revenue/average_total_assets
    

    #########
    ###### Liquidity ratios
    ###
    def current_ratio(self):
        '''
        Current ratio = Current assets / Current liabilities
        '''
        current_asset_code = 1000

        current_asset = self.__query_value_by_code(current_asset_code)
        
        current_liability =  self.get_current_liabilities()
        return current_asset/current_liability
    

    def quick_ratio(self):
        '''
        Quick ratio = (Cash+Short term investment+Receivables) / Current liabilities
        '''
        cash_code = 1100
        short_term_investment_code = 1200
        current_account_receivable_code =1300
        cash = self.__query_value_by_code(cash_code)

        short_term_investment = self.__query_value_by_code(short_term_investment_code)
        current_liability = self.get_current_liabilities()
        current_account_receivable = self.__query_value_by_code(current_account_receivable_code)

        return (cash+short_term_investment+current_account_receivable)/current_liability
    
    
    def cash_ratio(self):
        '''
        Cash ratio = (Cash+Short term investment) / Current liabilities
        '''
        cash_code = 1100
        short_term_investment_code = 1200
        cash = self.__query_value_by_code(cash_code)
        short_term_investment = self.__query_value_by_code(short_term_investment_code)
        current_liability = self.get_current_liabilities()                
        return (cash+short_term_investment)/current_liability           


    def cash_conversion_cycle(self):
        '''
        Cash conversion cycle = Days of sales outstanding + Days of inventory on hand - Number of days of payables
        '''
        return self.days_of_sales_outstanding() + self.days_of_inventory_on_hand() - self.num_days_of_payables()


    #########
    ###### Solvency Ratio
    ###
    def debt_to_assets_ratio(self):
        '''
        Debt to assets ratio = Total debt / Total assets
        Total debt = Short term debt (current liabilities) + Long term debt (non-current liabilities)
        '''

        total_asset_code = 2800

        total_debt = self.get_total_debt()
        total_asset = self.__query_value_by_code(total_asset_code)
        
        return total_debt/total_asset


    def debt_to_capital_ratio(self):
        '''
        Debt to capital ratio = Total debt / (Total debt + Total shareholder's equity)
        '''
        shareholder_equity_code = 4100
        total_debt = self.get_total_debt()
        shareholder_equity = self.__query_value_by_code(shareholder_equity_code)
        return total_debt/(total_debt+shareholder_equity)
        


    def debt_to_equity_ratio(self):
        '''
        Debt to equity ratio = Total debt / Total shareholder's equity
        '''
        shareholder_equity_code = 4100
        shareholder_equity = self.__query_value_by_code(shareholder_equity_code)
        total_debt = self.get_total_debt()

        return total_debt/shareholder_equity
    

    def financial_leverager_ratio(self):
        '''
        Financial leverage ratio = Average total assets / Average total equity
        '''
        average_total_assets = self.get_average_total_assets()
        average_total_equity = self.get_average_total_equity()
        return average_total_assets/average_total_equity
    

    def debt_to_ebitda(self):
        '''
        Debt to EBITDA = Total or net debt / EBITDA
        EBITDA = Operating Profit + Depreciation & Amortization
        EBITDA = EBT(60) + Interest Expense (32)
        '''
        total_debt = self.get_total_debt()
        net_profit_code = 60
        depreciation_n_amortization_code = 111
        interest_expesen_code = 33

        ebitda = self.__query_value_by_code(net_profit_code) \
                + self.__query_value_by_code(depreciation_n_amortization_code) \
                + self.__query_value_by_code(33)


        
        return total_debt / ebitda

    
    def interest_coverage(self):
        '''
        Interest Coverage = EBIT / Interest payments
        EBIT = Operating Profit - Interest Expense
        '''
        net_profit_code = 60
        interest_expense_code = 33
        interest_expense = self.__query_value_by_code(interest_expense_code)

        ebit = self.__query_value_by_code(net_profit_code) + interest_expense

        return ebit/interest_expense
        

    #########
    ###### Profitability Ratios
    ###
    def gross_profit_margin(self):
        '''
        Gross profit margin = Gross profit / revenue
        '''
        gross_profit_code = 30
        gross_profit = self.__query_value_by_code(gross_profit_code)
        revenue = self.get_revenue()
        return (gross_profit) / revenue
    

    def operating_profit_margin(self):
        '''
        Operating Profit Margin = Operating Income / Revenue
        Operating Income = Gross Profit - Selling Expenses - General and Administrative Expenses
        '''
        gross_profit_code = 30
        selling_expense_code = 35
        general_n_admin_expense_code = 36
        operating_income = self.__query_value_by_code(gross_profit_code) \
                            - self.__query_value_by_code(selling_expense_code) \
                            - self.__query_value_by_code(general_n_admin_expense_code)
        
        revenue = self.get_revenue()
        return operating_income/revenue
    

    def pretax_margin(self):
        '''
        Pretax margin = EBT(earning before tax but after interest) / revenue
        '''
        net_profit_before_tax_code = 60
        net_profit_before_tax = self.__query_value_by_code(net_profit_before_tax_code)
        revenue = self.get_revenue()

        return net_profit_before_tax / revenue
    

    def net_profit_margin(self):
        '''
        Net profit margin = net income / revenue
        '''
        net_income = self.get_net_income()
        
        revenue = self.get_revenue()
        return (net_income) / revenue
    

    def operating_roa(self):
        '''
        Operating ROA = Operating income / Average total assets
        '''
        operating_income_code = 40
        operating_income = self.__query_value_by_code(operating_income_code)
        avg_total_assets = self.get_average_total_assets()
        return operating_income / avg_total_assets
    

    def roa(self):
        '''
        ROA = Net income / Average total assets
        '''
        net_income = self.get_net_income()
        avg_total_assets = self.get_average_total_assets()
        return net_income/avg_total_assets
    

    def roe(self):
        '''
        ROE = Net income / Average total equity
        '''
        net_income = self.get_net_income()
        avg_total_equity = self.get_average_total_equity()
        return net_income/avg_total_equity