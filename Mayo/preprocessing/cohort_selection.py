import pandas as pd
import numpy as np
import pickle as pkl
import os
import sys
import shutil
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
print('all imported')
sys.stdout.flush()


def cohort_selction(df):
    """
    df : transfer_locations file - contains one transfer withint hospital per row - one hospitalization spans multiple rows but share the same PATIENT_DK, ADMIT_DTM, and DISCHARGE_DTM
    """
    df = df.dropna(subset=['DISCHARGE_DTM']) #sometimes discharge time is not recorded properly
    df = df.drop_duplicates(subset=['PATIENT_DK', 'ADIMT_DTM'])
    print('Unique hospitalizations:\t', len(df))
    df['ADMISSION_DTM'] = pd.to_datetime(df.ADMISSION_DTM, errors='coerce')
    df['DISCHARGE_DTM'] = pd.to_datetime(df.DISCHARGE_DTM, errors='coerce')
    def to_days(x,y):
        if pd.isnull(x)==False:
            return (x-y).days

    df['Days in hospital']  = df.apply(lambda row : to_days(row['DISCHARGE_DTM'], row['ADMISSION_DTM']), axis = 1)
    df = df.loc[df['Days in hospital']>2]
    print('Unique hospitalizations longer than 2 days:\t', len(df))

    return df