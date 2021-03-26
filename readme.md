Summary
I am working on a python project that analyzes my portfolio, gives me a facility to aggregate on different attributes and levels of my portfolio like sector and funds. It also shows me the risk numbers at these aggregated levels.
 For example, let say we have a hypothetical portfolio of 5 stocks and 5 ETFs:
     
Stocks:                   
AAPL 	    10		    
ABNB	    20		    
AMZN	    2		    
TSLA	    10			
UBER	    20			


ETFs

ARKK	   20                 

VOO		    5

SPY		    5

SRET       10

XLK		    3

Step 1
This program loops through all the 10 symbols, if it finds an ETF then it goes a level down, finds top holdings, and aggregates it with the list of stocks that this portfolio consists of. For example, ARKK contains some parts of AAPL, so the total of AAPL stock that this portfolio has is:

Total quantity AAPL = 10 AAPL + 20 ARKK * Weight of AAPL in this ETF
                                   = 10 + 20 * 0.10 = 10 + 2 = 12

This way it keeps expanding the ETF and keeps adding to AAPL

Step2:
It aggregates the output of Step 1 and finds the market value of each stock using quantity * price then sorts the portfolio by the decreasing market value and save it as a CSV file
