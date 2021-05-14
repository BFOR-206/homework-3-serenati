#%% imports 

import re
import pandas as pd
from datetime import datetime
from nltk.corpus import words


#%% read data file

# create empty list for the logs
raw_log = []

# open the file and then read the lines


with open('C:\\Users\\windows 10\\Phyton class/hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    


#%% start creating functions to break the code down


def is_comment_row(row):
    """
    check if row begins with ---
    Parameters
    ----------
    row : string
        row from a chat log.
    Returns
    -------
    True/False.
    """
    is_comment = re.match(r'---', row[0:5])
    
    return is_comment


def is_time_row(row):
    """
    check if the row starts with HH:MM format
    Parameters
    ----------
    row : string
        row from a chat log.
    Returns
    -------
    True/False. - It is actually an re.Match object
    """
    
    is_time = re.search(r'([0-9]{2}):([0-9]{2})', row[0:5])
    
    return is_time


def is_message_row(row):
    """
    Check if row is a user message
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    True/False.
    """
    
    # we are explicitly returning True/False
    
    is_message = re.search(r'<', row[6:7])
    if is_message:
        return True
    else:
        return False


def convert_time():
    """
    Function to convert time from string to hours and minutes
    """
    pass



def extract_username(row):
    """
    Take a known chat row (assumes we already checked it is a chat row)
    find the username and return just that.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    None.
    """
    # print(row)
    username = re.search(r'<.([\w]+)>', row)
    # print(username)

    return username.group(1)


def is_join_quit(row):
    pass



def get_time(row):
    """
    This function will find the hours and minutes in a row.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    This will return the time of day in a string
    formatted as HH:MM.
    """
    result = re.match('[0-9]{2}:[0-9]{2}', row[:6])
    
    
    # group 0 is the whole match
    if result:
        return result.group(0)
    else: 
        # this prevents errors if there is no match
        return None
    
    
def get_date(row):
    """
    
    Parameters
    ----------
    row : str
        Row from the chat that starts with ---.
    Returns
    -------
    Time in the format of 'YYYY-MM-DD' .
    """
    
    # TODO remove this later
    # row = '--- Log opened Tue Sep 20 00:01:49 2016'
    
    date_parts = row.split()    
    
    # join is a function of a string
    # it takes a list of strings and joins them together, 
    # separated by whatever string you specify
    
    raw_date = "-".join([date_parts[7], date_parts[4], date_parts[5]])
    print(raw_date)
    
    formatted_date = datetime.strptime(raw_date, '%Y-%b-%d')
    print(formatted_date)
    return formatted_date



def check_non_english_words(word_counts):
    """
    Pass a dictionary (Python dictionary) with words and their counts.
    Check for each word in the English word list.
    Return the dictionary of non-English words
    
    This method is useful if you use Collections and Counter 
    (like in HW2) to get your word counts.
    
    This solution is based on this:
        https://stackoverflow.com/questions/3420122/filter-dict-to-contain-only-certain-keys
    Parameters
    ----------
    word_counts : dict
        Unique words and their counts
    Returns
    -------
    Filtered dictionary of words not found in English.
    """
    
    word_list = set(words.words())
    # print(word_list)
    
    non_english_keys = set(word_counts.keys()) - word_list
    
    # from the stackoverflow linked above^
    # dict_you_want = { your_key: old_dict[your_key] for your_key in your_keys }
    non_english_counts = { your_key: word_counts[your_key] for your_key in non_english_keys }

    return non_english_counts
    


#%% find comment rows (rows that start with ---)

time_row_list = []
bad_row_list = []
message_row_list = []

for row in raw_log:
    # print(row)
    
    """
    The first row is:
    --- Log opened Tue Sep 20 00:01:49 2016
    
    We want to find rows that match this pattern at the beginning
    
    To look at just the beginning of the string, just view
    the first 5 characters (a string is like a list of characters)
    
    """
    # print("the first 5 chars are", row[0:5])
    if is_comment_row(row):
        print("Found comment row", row)
        # pass
    
    elif is_message_row(row):
        message_row_list.append(row)
    
    # check if the row starts with HH:MM format
    elif is_time_row(row):
        #print("Found row with times ", row)
        time_row_list.append(row)
        

    # show us any rows that do meet these criteria
    # there are 7-8 rows that do not match
    else:
        print("row has no matches", row)
        bad_row_list.append()


#%% we can also do this with pandas apply function

# put the data into a dataframe

hacker_log = pd.DataFrame(raw_log, columns=['raw_log'])
hacker_log['is_message'] = hacker_log['raw_log'].apply(is_message_row)
print(hacker_log)


# subset the data to just those that are messages
# 
chat_rows = hacker_log.loc[hacker_log['is_message'] == True].copy()

#%%% get usernames
# apply the extract username function
chat_rows['username'] = chat_rows['raw_log'].apply(extract_username)

