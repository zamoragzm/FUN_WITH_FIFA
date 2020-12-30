import pandas as pd
import numpy as np

def load_and_process(url_or_path_to_csv_file):


    def general_position (row):
        if row['BestPosition'] == 'ST' or row['BestPosition'] == 'CF' or row['BestPosition'] == 'RW' or row['BestPosition'] == 'LW':
            return 'Forward'
        elif row['BestPosition'] == 'CB' or row['BestPosition'] == 'RB' or row['BestPosition'] == 'LB' or row['BestPosition'] == 'RWB' or row['BestPosition'] == 'LWB':
            return 'Defender'
        elif row['BestPosition'] == 'GK':
            return 'Goalkeeper'
        return 'Midfielder'

    def heightToCen (row):
        h = (row['Height'].split("'"))
        meters = (int(h[0])*12 + int(h[1])) * 0.0254
        return int(meters*100)


    # Method Chain 1 (Load data and deal with missing data)

    df1 = ( pd.read_csv(url_or_path_to_csv_file)
           .drop(['ID','Photo', 'Flag','Potential','Club Logo','Special', 'International Reputation','Body Type',
                 'Real Face','Joined','Loaned From','Contract Valid Until','Position','Best Overall Rating',
                  'Release Clause','Marking','Value','Wage','Work Rate'], axis=1)
           .rename(columns={'Preferred Foot': 'PreferredFoot','Weak Foot': 'WeakFoot','Jersey Number': 'JerseyNumber',
                          'Best Position': 'BestPosition'})
           .dropna()
           .astype(dtype = int, errors = 'ignore')
           .reset_index(drop=True)
    )

    # Method Chain 2 (Create new columns, drop others, and do processing)

    df2 = (df1
           .assign(GeneralPosition = df1.apply(lambda row: general_position(row), axis=1).values)
            .assign(HeightInCm = df1.apply(lambda row: heightToCen(row), axis=1).values)
           .drop(df1[df1.Overall < 75].index)
           .sort_values(by='Overall', ascending=False)
           .drop(['Height'],axis=1)
           .reset_index(drop=True)
    )

    return df2