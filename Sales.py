import sqlite3
import csv


def read_data():
    file_name = "all_data.csv"
    file = open(file_name)
    contents = csv.reader(file)
    return contents


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

def insert_data():
    connection = sqlite3.connect('Sales.db')
    cursor = connection.cursor()
    insert_records = "INSERT INTO Sales (Order_id, Product, Quantity_ordered, Price_each,Order_date, Purchase) VALUES(?, ?, ?, ?, ?, ?)"
    contents = read_data()
    cursor.executemany(insert_records, contents)
    connection.commit()
    connection.close()



def main():
    create_table()
    insert_data()
    
if __name__ == "__main__":
  main()
