# """THIS PYHTON CODE PERFORMS A SALES ANALYSIS ON A MERGED TWELVE MONTHS DATA FOR THE YEAR 2019
# """

# """ IMPORTING THE NECESSARY LIBRARY
# "
import os.path
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
import urllib.request
import csv

#""" This function parses the website, download
#    and return the dataset in CSV format"""
def get_data(base_url):
    data = urllib.request.urlopen(base_url)
    all_data = pd.read_csv(data)
    all_data = all_data.dropna(how='all')
    all_data = all_data.to_csv("all_data.csv", index= False)
    return all_data


#"""This function open, read and return the content of the downloaeded dataset"""
def read_data():
    file_name = "all_data.csv"
    file = open(file_name)
    contents = csv.reader(file)
    return contents


#""" This function makes a connection to the SQLITE3 
#""" database and create a table called Sales"""
def create_table():
    connection = sqlite3.connect('Sales.db')
    cursor = connection.cursor()
    create_table ='''CREATE TABLE IF NOT EXISTS Sales( 
                        Order_id int, 
                        Product text, 
                        Quantity_ordered int, 
                        Price_each int,
                        Order_date int, 
                        Purchase Address text);
                    '''
    cursor.execute(create_table)
    connection.commit()
    connection.close()

#""" This function inserts the contents of the CSV data into the database""" 
def insert_data():
    connection = sqlite3.connect('Sales.db')
    cursor = connection.cursor()
    insert_records = "INSERT INTO Sales (Order_id, Product, Quantity_ordered, Price_each,Order_date, Purchase) VALUES(?, ?, ?, ?, ?, ?)"
    contents = read_data()
    cursor.executemany(insert_records, contents)
    connection.commit()
    connection.close()

#This function converts the SQLITE3 table into a Dataframe using pandas"""
def data_frame():
    connection = sqlite3.connect('Sales.db')
    cursor = connection.cursor()
    all_data = pd.read_sql_query("SELECT * from Sales", connection) 
    # """ Getting rid of text in order date column
    all_data.columns = all_data.iloc[0]
    all_data = all_data.iloc[1:].reset_index(drop=True)
    all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
    # """Changing columns type to easy-to-work-with ones
    all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
    all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
    # """ Adding a month column
    all_data['Month'] = all_data['Order Date'].str[0:2]
    all_data['Month'] = all_data['Month'].astype('int32')
    all_data.head()
    return all_data
    cursor.execute()
    connection.commit()

# """ Creating a function that adds a City column to the database
    
def get_city(address):
    return address.split(",")[1].strip(" ")
def get_state(address):
    return address.split(",")[2].split(" ")[1]




            # """  DATA MANAGEMENT AND ANALYSIS USING PANDAS
             # """

# """ What was the best month for sales?
#     How much was earned that month?
# """
def best_month(all_data):
    all_data['City'] = all_data['Purchase Address'].apply(
        lambda x: f"{get_city(x)}  ({get_state(x)})")
    all_data.head()

    all_data['Sales'] = all_data['Quantity Ordered'].astype(
        'int') * all_data['Price Each'].astype('float')
    all_data.groupby(['Month']).sum()

    # """ Plotting the results
    months = range(1, 13)
    #print(months)

    plt.bar(months, all_data.groupby(['Month']).sum()['Sales'])
    plt.xticks(months)
    plt.ylabel('Sales in USD ($)')
    plt.xlabel('Month number')
    if os.path.isfile('month-sales.pdf'):
        print("File exist")
    else:
        plt.savefig('month-sales.pdf')
        
# """ What city sold the most product?
# """
def most_product(all_data):
    all_data.groupby(['City']).sum()

    # """ Plotting results
    keys = [city for city, df in all_data.groupby(['City'])]

    plt.bar(keys, all_data.groupby(['City']).sum()['Sales'])
    plt.ylabel('Sales in USD ($)')
    plt.xlabel('Month number')
    plt.xticks(keys, rotation='vertical', size=8)
    if os.path.isfile('city-sales.pdf'):
        print("File exist")
    else:
        plt.savefig('city-sales.pdf')


# """ What time should we display advertisements to maximize likelihood of customer's buying product?
# """"
def advert_time(all_data):
    # """ First adding an hour and a minute columns
    all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
    all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute
    all_data['Count'] = 1
    all_data.head()

    keys = [pair for pair, df in all_data.groupby(['Hour'])]

    # """Plotting results
    plt.plot(keys, all_data.groupby(['Hour']).count()['Count'])
    plt.xticks(keys)
    plt.grid()
    if os.path.isfile('count.pdf'):
        print("File exist")
    else:
        plt.savefig('count.pdf')


# """ What products are most often sold together?
# """
def complement_goods(all_data):
    df = all_data[all_data['Order ID'].duplicated(keep=False)]

    df['Grouped'] = df.groupby('Order ID')[
                               'Product'].transform(lambda x: ','.join(x))
    df2 = df[['Order ID', 'Grouped']].drop_duplicates()

    count = Counter()

    for row in df2['Grouped']:
        row_list = row.split(',')
        count.update(Counter(combinations(row_list, 2)))

    #Results will be returned in a dictionary format
    for key,value in count.most_common(10):
        print(key, value)
    
    if os.path.isfile('excelreport.xlsx'):
        print("File exist")
    else:
        df2.to_excel('excelreport.xlsx')


    if os.path.isfile('csvreport.csv'):
        print("File exist")
    else:
        df2.to_csv('csvreport.csv')


# """What product sold the most? Why do you think it sold the most?
# """
def most_sold(all_data):
    product_group = all_data.groupby('Product')
    quantity_ordered = product_group.sum()['Quantity Ordered']

    keys = [pair for pair, df in product_group]
    plt.bar(keys, quantity_ordered)
    plt.xticks(keys, rotation='vertical', size=8)
    if os.path.isfile('prodtype.pdf'):
        print("File exist")
    else:
        plt.savefig('prodtype.pdf')

    prices = all_data.groupby('Product').mean()['Price Each']

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.bar(keys, quantity_ordered, color='g')
    ax2.plot(keys, prices, color='b')

    ax1.set_xlabel('Product Name')
    ax1.set_ylabel('Quantity Ordered', color='g')
    ax2.set_ylabel('Price ($)', color='b')
    ax1.set_xticklabels(keys, rotation='vertical', size=8)
    fig.show()




def main():
    url = "https://raw.githubusercontent.com/KeithGalli/Pandas-Data-Science-Tasks/master/SalesAnalysis/Output/all_data.csv"
    get_data(url)
    create_table()
    insert_data()
    all_data = data_frame()
    best_month(all_data)
    most_product(all_data)
    advert_time(all_data)
    complement_goods(all_data)
    most_sold(all_data)
    
if __name__ == "__main__":
  main()

