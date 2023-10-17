import pandas as pd
import numpy as np

def poisson_bootstrap(ab_test_data, B):
    """
    Perform Poisson bootstrap sampling for an A/B test.

    Parameters
    ----------
    ab_test_data : pandas.core.frame.DataFrame
        A DataFrame containing two columns:
        - 'testgroup' with possible values 'a' or 'b'.
        - 'revenue' representing revenue values.

    B : int
        The number of bootstrap samples to generate.

    Returns
    -------
    pandas.core.frame.DataFrame
        A DataFrame with B rows, each describing an individual sample. The columns include:
        - 'revenue_a': Total revenue for group 'a'.
        - 'count_users_a': Count of users in group 'a'.
        - 'count_paying_users_a': Count of paying users in group 'a'.
        - 'revenue_b': Total revenue for group 'b'.
        - 'count_users_b': Count of users in group 'b'.
        - 'count_paying_users_b': Count of paying users in group 'b'.
        - 'ARPU_difference': Difference in Average Revenue Per User (ARPU) between groups 'a' and 'b'.
        - 'ARPPU_difference': Difference in Average Revenue Per Paying User (ARPPU) between groups 'a' and 'b'.
        - 'CR_difference': Difference in Conversion Rate (CR) between groups 'a' and 'b'.
    """
    a_result = np.array([[0, 0, 0]] * B)  # Initialize a group result array
    b_result = np.array([[0, 0, 0]] * B)  # Initialize b group result array
    # Iterate by ab_test_data rows
    for idx, row in ab_test_data.iterrows():
        # Generate Poisson distribution
        weights = np.random.poisson(1, B)
        # Calculate samples for row
        if row['testgroup'] == 'a':
            a_result[:, 0] += weights *  row['revenue']      # Revenue
            a_result[:, 1] += weights                        # Count users
            a_result[:, 2] += weights * (row['revenue'] > 0) # Count paying users 
        else:
            b_result[:, 0] += weights *  row['revenue']      # Revenue
            b_result[:, 1] += weights                        # Count users
            b_result[:, 2] += weights * (row['revenue'] > 0) # Count paying users 
    
    # Combine a_result and b_result horizontally
    ab_result = np.hstack((a_result, b_result))
    
    # Convert the combined NumPy array to a pandas DataFrame
    result_df = pd.DataFrame(ab_result, columns=[
        'revenue_a', 'count_users_a', 'count_paying_users_a',
        'revenue_b', 'count_users_b', 'count_paying_users_b'])
    # Calculate KPIs difference  between groups
    result_df['ARPU_difference'] = ((result_df['revenue_b'] / result_df['count_users_b']) 
                                    - (result_df['revenue_a'] / result_df['count_users_a']))
    
    result_df['ARPPU_difference'] = ((result_df['revenue_b'] / result_df['count_paying_users_b']) 
                                     - (result_df['revenue_a'] / result_df['count_paying_users_a']))
        
    result_df['CR_difference'] = ((result_df['count_paying_users_b'] / result_df['count_users_b']) 
                                  - (result_df['count_paying_users_a'] / result_df['count_users_a']))
    return result_df

def bootstrap_result_check(bootstrap_data, 
                           alpha: float):
    """
    Check if 0 belongs to the confidence interval of bootstrap data.

    Parameters:
    -----------
    bootstrap_data : pandas.core.series.Series
        An array of bootstrapped data for hypothesis testing.

    alpha : float
        The significance level for hypothesis testing, representing the probability of making a Type I error.

    Returns:
    --------
    None
    """
    # Check if 0 belongs to the confidence interval
    quantile_l = np.quantile(bootstrap_data, alpha / 2)
    quantile_r = np.quantile(bootstrap_data, 1 - alpha / 2)
    print(f"Sample mean difference: {bootstrap_data.mean():.3f}")
    print(f"{1-alpha:.1%} Confidence Interval ({quantile_l:.3f}, {quantile_r:.3f})")
    if quantile_l <= 0 <= quantile_r:
        print(f"0 belongs to the {100*(1-alpha)}% confidence interval. There is no basis to reject H0.")
    else:
        print(f"0 does not belong to the {100*(1-alpha)}% confidence interval. Rejecting H0.")