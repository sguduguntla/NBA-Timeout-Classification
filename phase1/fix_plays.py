import pandas as pd
from event_codes import get_event_codes

def main():
    df = pd.read_csv('data/PlayByPlayNBA.csv')
    gl = pd.read_csv('data/GameLineupNBA.csv')

    event_codes, action_types = get_event_codes()

    i = 0
    for index, row in df.iterrows():
        if i > 0:
            person1 = row["Person1"].strip()
            temp = gl.loc[gl["Person_id"] == person1]
            team = temp["Team_id"].tolist()
            if len(team) > 0:
                df.at[index, "Team_id"] = team[0]

            print(df.at[index, "Team_id"])
        i += 1
    
    df.to_csv("data/UpdatedPlayByPlayNBA.csv")
    
if __name__ == '__main__':
    main()