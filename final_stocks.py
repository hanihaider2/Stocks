import pandas as pd
import matplotlib.pyplot as plt


class Stocks:
    '''
    Attributes: 
    stocks_ filename: this will have all the data for the stock which we want the data to be presented 
    major_index :
    This will have the file **(please add info for it i don't know have what will the data have )
    Methods :
    1)	Summary 
    2)	Rasing error
    3)	Graphs
    4)	Moving average
    5)	Comparing stocks summary
    6)	Comparing stocks graph
    '''

    def __init__(self, stocks_filename: str, stocks_filename2=None):
        '''
        Constructor: creates an new instance for stock
        parameter :
        Self -- the current object 
        stocks _filename:string -- the data for the stocks 
        return None 
        '''
        # add code to raise error
        self.stocks_filename = stocks_filename
        self.stocks_filename2 = stocks_filename2
        try:
            self.stock_file = pd.read_csv(stocks_filename)
            if self.stocks_filename2 != None:
                self.stock_file2 = pd.read_csv(stocks_filename2)

        except:
            raise FileNotFoundError("file is not present")

        for i in range(len(stocks_filename)):
            if stocks_filename[i] == ".":
                if stocks_filename[i + 1] != "c" and stocks_filename[i + 2] != "s" and stocks_filename[i + 3] != "v":
                    raise ValueError("please enter valid filename ")

    def rasing_error(self, filename):
        '''
        parameter:
        self -- the current object 
        his will raise any error, this method will
        be called in all the method or that we can raise error
        '''
        whole_file = open(filename, 'r').readlines()
        line = whole_file[0]
        line = line.rstrip("\n")
        line = line.split(",")
        if line[0].lower() != "date":
            raise ValueError("header is wrong ")  # be more clean
        elif line[1].lower() != "open":
            raise ValueError("header is wrong ")
        elif line[2].lower() != "high":
            raise ValueError("header is wrong ")
        elif line[3].lower() != "low":
            raise ValueError("header is wrong ")
        elif line[4].lower() != "close":
            raise ValueError("header is wrong ")
        elif line[5].lower() != "adj close":
            raise ValueError("header is wrong ")
        elif line[6].lower() != "volume":
            raise ValueError("header is wrong ")

    def name(self):
        '''
        parameter:
        self -- the current object 
        return two list with data for the data frame 
        '''
        max_value = self.stock_file.loc[self.stock_file['Close'].idxmax()]
        min_value = self.stock_file.loc[self.stock_file['Close'].idxmin()]
        self.stock_file["Largest percent"] = (
            (self.stock_file["Close"] - self.stock_file["Open"]) / self.stock_file["Close"]) * 100
        max_percentage = self.stock_file.loc[self.stock_file['Largest percent'].idxmax(
        )]
        min_percentage = self.stock_file.loc[self.stock_file['Largest percent'].idxmin(
        )]
        first_list = [max_value["Close"], min_value["Close"],
                      max_percentage["Close"], min_percentage["Close"]]
        second_list = [max_value["Date"], min_value["Date"],
                       max_percentage["Date"], min_percentage["Date"]]

        return first_list, second_list

    def summary(self):
        '''
        Method:summary: gets the complete summary of stocks 
        Parameter:
        Self-- the current object:
        Returns the complete summary which will have stock price and date, where 
        it was  highest stock, lowest stock, largest moving up in a single day
        % and largest moving downward in a single day by %
        '''
        
        self.rasing_error(self.stocks_filename)

        value1, value2 = self.name()

        summary = {'summary': ["Price", "Date"], 'Highest High': [value1[0], value2[0]],
                   'Lowest Low': [value1[1], value2[1]],
                   'Largest Move Up in a single day %': [value1[2], value2[2]],
                   'Largest Move Downward in a single day%': [value1[3], value2[3]],
                   }

        df = pd.DataFrame(summary, columns=['summary', 'Highest High', 'Lowest Low',
                                            'Largest Move Up in a single day %', 'Largest Move Downward in a single day%'])

        return df.style.set_properties(**{'text-align': 'center'}).hide_index()

    def read_file(self):
        '''
        parameter:read bothe csv files for graphs 
        self -- the current object 
        his will raise any error, this method will
        return None
        '''
        self.csv_file = pd.read_csv(self.stocks_filename)
        if self.stocks_filename2 != None:
            self.rasing_error(self.stocks_filename2)
            df2 = pd.read_csv(self.stocks_filename2)
            self.df_compare = self.csv_file[['Date', 'Adj Close']]
            self.df2_compare = df2[['Date', 'Adj Close']]

    # Transform the input file
    def transform(self):
        '''
        this function drops columns not needed and relabels
        the column names it also calculates the 50 and 200 day moving average'''
        # Eliminating columns and renaming
        self.read_file()
        self.result = self.csv_file.drop(
            columns=["Open", "High", "Volume", "Low", "Close"])
        self.result.columns = ['Date', 'Price']

        # Moving Average
        self.result['50-day MA'] = self.result.Price.rolling(
            window=50).mean()
        self.result['200-day MA'] = self.result.Price.rolling(
            window=200).mean()

        # Setting/formatting x, y axis and title
        self.result.Date = pd.to_datetime(self.result.Date)

    # draw plot
    def show_plot(self):
        '''creates the axis titles and graph features '''
        self.result.plot(x="Date")
        plt.ylabel('Price (USD)')
        plt.title(" Stock Price: 2016 - 2021")
        plt.show()

    def graph(self):
        '''
        parameter:call the fuction and make the graph plot 
        self -- the current object 
        retrun None 
        '''
        
        self.transform()
        self.show_plot()

    def transform_data(self):
        '''
        method -- transform_data:picks up the closing price and merges it 
        return the merged data 
        '''
        
        output1 = pd.merge(
            self.df_compare, self.df2_compare, on='Date', how='inner')
        output1.columns = ['Date', self.stocks_filename, self.stocks_filename2]

        output1.Date = pd.to_datetime(output1.Date)
        return output1

    def stock_comparison_graph(self):
        '''
        Method -- comparing_stocks_graphs 

        Self -- the current object 

        Returns a line graph of the stock prices
        '''
        
        output1 = self.transform_data()
        output1.plot(x="Date")
        plt.title("Closing Prices", fontsize=16)
        plt.ylabel('Price(USD)', fontsize=14)
        plt.xlabel('Year', fontsize=14)
        plt.show()

    def stock(self):
        '''
        Method : stock
        Self—current object:

        Returns two list which ahas information for data frame 


        '''

        max_value = self.stock_file.loc[self.stock_file['Close'].idxmax()]
        min_value = self.stock_file.loc[self.stock_file['Close'].idxmin()]

        max_value1 = self.stock_file2.loc[self.stock_file2['Close'].idxmax()]
        min_value1 = self.stock_file2.loc[self.stock_file2['Close'].idxmin()]

        self.stock_file["Largest percent"] = (
            (self.stock_file["Close"] - self.stock_file["Open"]) / self.stock_file["Close"]) * 100
        self.stock_file2["Largest percent"] = (
            (self.stock_file2["Close"] - self.stock_file2["Open"]) / self.stock_file2["Close"]) * 100

        percentage = self.stock_file.loc[self.stock_file['Largest percent'].idxmax(
        )]
        percentage1 = self.stock_file2.loc[self.stock_file2['Largest percent'].idxmax(
        )]

        list1 = [max_value["Close"], min_value["Close"], percentage["Close"]]
        list2 = [max_value1["Close"],
                 min_value1["Close"], percentage1["Close"]]
        return list1, list2

    def comparing_summary(self):
        '''
        Method : summary: get the complete summary after comapring 2 stocks

        Self—current object:

        Returns the complete summary of 2 stocks which has the highest stock, lowest stock and percentage change

        Raise error if one of the data sets is not entered
        '''

        self.rasing_error(self.stocks_filename)

        value1, value2 = self.stock()

        summary = {'summary': [self.stocks_filename, self.stocks_filename2], 'Highest High': [value1[0], value2[0]],
                   'Lowest Low': [value1[1], value2[1]], 'Percentage Change': [value1[2], value2[2]]}

        df = pd.DataFrame(summary, columns=[
                          'summary', 'Highest High', 'Lowest Low', 'Percentage Change'])

        return df.style.set_properties(**{'text-align': 'center'}).hide_index()
