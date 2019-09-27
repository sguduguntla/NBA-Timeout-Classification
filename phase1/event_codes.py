import pandas as pd

def get_event_codes():
    """ Gets dictionary of Event_Msg_Type mapping to Event_Msg_Description. """
    
    df = pd.read_csv('data/EventCodesNBA.csv')

    event_codes = {}
    for index, row in df.drop_duplicates(subset ="Event_Msg_Type").iterrows():
        message_type = row['Event_Msg_Type']
        event_codes[message_type] = row["Event_Msg_Type_Description"].strip()

    return event_codes