# Program to collect error in a Python code and send to a DB
# Written by Ezgi DEMIR, PhD. Industrial Engineering

import sqlite3 as sql
from pylint import epylint
import datetime as dateee
import getpass
import platform
#import re

#gathering error as a dictionary
def error(string,filename):
    # Data Filtering for Undesired Spaces and End of Lines
    string=string.strip(' ')
    string=string.replace('\n','')
    string=string.split(' ')
    
    error_dict={}
    # Obtaining the Index Number Containing Keyword 'error' for Array Manipulation
    for i in range(len(string)):
        if string[i]=='error':
            break

    # Parsing Errors with Respect to the Given Criteria
    error_dict['Filename']=filename
    error_dict['Hostname']=platform.node()
    error_dict['Username']=getpass.getuser()
    error_dict['Date']=dateee.datetime.now().strftime('%Y-%m-%d')
    error_dict['Time']=dateee.datetime.now().strftime('%H:%M:%S')
    error_dict['Row']=string[i-1]
    error_dict['Error Code']=string[i+1]
    error_dict['Error Type']=string[i+2]
    error_dict['Description']=' '.join(string[i+3:])
    
    return error_dict

# Linting Errors 
def define_error(filename):
    options = '--errors-only'  # all messages will be shown
    pylint_stdout, pylint_stderr = epylint.py_run(filename+ ' ' + options, return_std=True)
    #db_dict={} #Creating an Open Dictionary
    
    #Finding the keyword 'error'
    #keyword=re.compile('error')
    
    #obtaining the index numbers of string list containing the keywords
    #index=[]
    
    #Filtering process of pylint stdout
    explanation=pylint_stdout.getvalue()
    explanation=explanation.replace('(','')
    explanation=explanation.replace(')','')
    explanation=explanation.replace(':',' ')
    explanation=explanation.replace('  ',' ')
    explanation=explanation.replace(',','')   
    
    #Splitting the sentence into a list of string arrays
    s2=explanation.split()    
    s2=explanation.split(filename)    
    
    #Filtering Result List
    s2=s2[1:]
    
    return s2

# Gathering all the Errors into a List of Dictionaries
def list_to_dict(array,filename):
    err_list=[]
    for i in range(len(array)):
        err_list.append(error(array[i],filename))
    return err_list


#dictionary to SQLite DB
def to_database(error_dictionary):
    conn=sql.connect('errorinpython.db')
    c=conn.cursor()
   
    d1=error_dictionary['Filename']
    d2=error_dictionary['Hostname']
    d3=error_dictionary['Username']
    d4=error_dictionary['Date']
    d5=error_dictionary['Time']
    d6=error_dictionary['Row']
    d7=error_dictionary['Error Code']
    d8=error_dictionary['Error Type']
    d9=error_dictionary['Description']
    
    c.execute("CREATE TABLE IF NOT EXISTS [error]([id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,[Filename] TEXT NULL,[Hostname] TEXT NULL,[Username] TEXT NULL,[Date] TEXT NULL,[Time] TEXT NULL,[Row] TEXT NULL,[Error Code] TEXT NULL,[General Error Type] TEXT NULL,[Explanation] TEXT NULL)") #Creating DB
    c.execute("INSERT INTO error('Filename','Hostname','Username','Date','Time','Row','Error Code','General Error Type','Explanation') VALUES (?,?,?,?,?,?,?,?,?)",(d1,d2,d3,d4,d5,d6,d7,d8,d9)) #Inserting to DB     
   
    conn.commit()
    c.close()
    conn.close()


#Function calls
#result=define_error('ornekhata_1.py')
#errors=list_to_dict(result,'ornekhata_1.py')

# Sending Errors to DB with any Dictionary Elements of Error Lists
#for i in range(len(errors)):
    #to_database(errors[i])
       






