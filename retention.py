
import pandas as pd

from datetime import timedelta
from datetime import datetime

def cohort_retention(reg_data,
                     auth_data,
                     start_date: str,
                     end_date: str,
                     cohort_type: str,
                     number_of_periods: int,
                     retention_type='classic'):
    """
    Calculate cohort retention rates.

    Parameters
    ----------
    reg_data : pandas.core.frame.DataFrame
        DataFrame containing user registration data, including 'uid' and 'reg_ts' columns.
        'reg_ts' should be in timestamp format.

    auth_data : DataFrame
        DataFrame containing user authentication data, including 'uid' and 'auth_ts' columns.
        'auth_ts' should be in timestamp format.

    start_date : str
        Start date for defining cohorts in 'YYYY-MM-DD' format. Cohorts will be created from this date onwards.

    end_date : str
        End date for defining cohorts in 'YYYY-MM-DD' format. Cohorts will not extend beyond this date.
        Note: The parameter does not affect the number of reported periods, only the number of cohorts.

    cohort_type : str
        Type of cohorts to create. Supported cohort types: 'day', 'week', 'month', 'quarter', 'year'.

    number_of_periods : int
        Number of periods from the cohort registration date to calculate the retention rate.

    retention_type : str, default 'classic'
        Type of retention calculation. Supported options: 'classic' and 'rolling'.

    Returns
    -------
    pandas.core.frame.DataFrame
        A DataFrame containing cohort retention rates.

    DataFrame MetaData:
        result_df.start_date     = start_date
        result_df.end_date       = end_date
        result_df.cohort_type    = cohort_type
        result_df.retention_type = retention_type
    """
    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Define a dictionary to map cohort_types to DateOffsets
    offset_dictionary = {
                            'day'    : pd.DateOffset(days=1),
                            'week'   : pd.DateOffset(weeks=1),
                            'month'  : pd.DateOffset(months=1),
                            'quarter': pd.DateOffset(months=3),
                            'year'   : pd.DateOffset(years=1)}
    
    # Calcute increment depending on cohort_type
    cohort_increment = offset_dictionary[cohort_type]
    
    # Descope data based on start_date, end_date, cohort_type, number_of_periods in order to increase performance
    reg_data_temp = reg_data[(reg_data['reg_ts'] >= start_date) 
                              & (reg_data['reg_ts'] < (end_date 
                                                       + cohort_increment))]
    if retention_type == 'classic':
        auth_data_temp = auth_data[(auth_data['auth_ts'] >= start_date) 
                                    & (auth_data['auth_ts'] < (end_date 
                                                               + cohort_increment * (number_of_periods + 1)))]
    else:
        auth_data_temp = auth_data[(auth_data['auth_ts'] >= start_date)]


    # Initialize an empty data frame to store the retention calculation results
    result_df = pd.DataFrame(columns = ['Cohort', 'Users'] 
                                        + [f'{i}' for i in range(0, number_of_periods + 1)])

    # Initialize parameters                          
    cohort_number = 0                                   
    cohort_start_date = start_date # Initialize start date for the first cohort
    cohort_end_date = start_date   # Initialize end date for the first cohort

    # Cohort loop - create row for each cohort
    while cohort_end_date < end_date:
        
        cohort_retention = []  # Initialize a list which represents a particular cohort

        cohort_start_date = start_date + cohort_increment * cohort_number
        cohort_end_date = start_date + cohort_increment * (cohort_number + 1)

        # Append cohort_start_date as cohort name in DD MMM YY format 
        cohort_retention.append(cohort_start_date.strftime('%d %b %y'))

        # Filter the registration data for the cohort
        cohort_reg_users = reg_data_temp\
                           .query('reg_ts >= @cohort_start_date & reg_ts < @cohort_end_date').uid.unique()
        cohort_size = len(cohort_reg_users)

        # Append cohort size
        cohort_retention.append(cohort_size)

        # Calculate the retention rate for the period [0]
        cohort_retention.append(cohort_size / max(cohort_size, 1))

        # Retention loop - calculate the retention rate for periods [1, number_of_periods]
        period = 1
        while period <= number_of_periods:
            auth_start_date = cohort_start_date + cohort_increment * period
            auth_end_date   = cohort_start_date + cohort_increment * (period + 1)

            # Filter the authentication data for the cohort and period
            if retention_type == 'classic':
                cohort_auth_users = auth_data_temp[(auth_data_temp['uid'].isin(cohort_reg_users))]\
                                        .query('auth_ts >= @auth_start_date & auth_ts < @auth_end_date')\
                                        .uid.unique()
            else:
                cohort_auth_users = auth_data_temp[(auth_data_temp['uid'].isin(cohort_reg_users))]\
                                        .query('auth_ts >= @auth_start_date')\
                                        .uid.unique()

            # Calculate the retention rate
            cohort_retention.append(len(cohort_auth_users) / cohort_size if cohort_size != 0 else 0)
            
            period += 1

        # Append calculated cohort retention row to the data frame
        result_df.loc[cohort_number] = cohort_retention
        cohort_number += 1

    # Calculate 'All Users' row 
    cohort_retention = []
    cohort_retention.append('All Users')
    total_users = result_df.iloc[:,1].sum()
    cohort_retention.append(total_users)
    
    for period in range (2, number_of_periods + 3):
        # valid_rows required to exclude rows where retention rate equals to 0, in order to not influence 'All Users' 
        valid_rows = result_df.iloc[:,period] != 0
        all_users_returned_in_period = result_df.iloc[:,1] @ result_df.iloc[:,period]
        # Exclude from denominator users where correspondent retention rate equals to 0
        total_users_corrected = (valid_rows * result_df.iloc[:, 1]).sum()
        
        # Calculate the retention rate
        cohort_retention.append(all_users_returned_in_period / total_users_corrected if total_users_corrected != 0 else 0)

    # Write All users row to the dataframe
    result_df.loc[cohort_number] = cohort_retention

    # Sort DataFrame by index
    result_df = result_df.sort_index(ascending=False)
    
    # Set related metadata to the DataFrame in order to use it for plotting
    result_df.start_date     = start_date
    result_df.end_date       = end_date
    result_df.cohort_type    = cohort_type
    result_df.retention_type = retention_type

    return result_df