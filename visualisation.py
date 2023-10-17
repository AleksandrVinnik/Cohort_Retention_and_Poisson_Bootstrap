import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns

# Turn off interactive mode to prevent automatic plot display
plt.ioff()

# Default settings for plotting
sns.set(
    font_scale=1,
    style="whitegrid",
    rc={'figure.figsize':(20,10)}
        )


def retention_plot(retention_df, number_of_lines=0):
    """
    Generate line plots and a heatmap to visualize retention rates from a DataFrame calculated by the cohort_retention function.

    Parameters
    ----------
    retention_df : DataFrame
         A DataFrame obtained from the cohort_retention function, containing retention rate data.
        
    number_of_lines : int
        Limits the number of most recent cohorts to be displayed in the line plot. 
        By default, all cohorts are plotted. This parameter does not affect the heatmap.
        
    Returns
    -------
        None.
    """
    # Ensure that number_of_lines falls within the range [1, number of cohorts]
    number_of_lines = max(1, min(number_of_lines, retention_df.shape[0] - 1))
    
    # Prepare plt_df for plotting
    plt_df = retention_df.assign(Cohort_Users=retention_df['Cohort'].astype(str) + ' - ' 
                                 + retention_df['Users'].astype(str)) # Create cohort names
    plt_df = plt_df.set_index('Cohort_Users') # Set Cohort_Users' as the new index
    plt_df = plt_df.iloc[:, 3:] # Drop the 'Cohort', 'Users' and 'Day_0' columns

    # Create a figure and axis for lineplot
    fig, ax = plt.subplots()  
        
    # Create a lineplot for 'All Users'
    sns.lineplot(data=pd.concat([plt_df.iloc[:1], 
                                 plt_df.iloc[-1*number_of_lines:]]).iloc[:1].transpose(), 
                                 dashes=False,   
                                 palette="OrRd", 
                                 ax=ax)
    # Create a lineplot for recent {number_of_lines} cohorts
    sns.lineplot(data=pd.concat([plt_df.iloc[:1], 
                                 plt_df.iloc[:number_of_lines+1]]).iloc[2:].transpose(), 
                                 dashes=False, 
                                 palette="Blues_r", 
                                 ax=ax)

    # Format the lineplot
    ax.lines[0].set_linestyle("--")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))     # Format the y-axis labels as percentages

    footnote_text = '' # Footnote intended to note that not all lines have been displayed on lineplot
    if number_of_lines < retention_df.shape[0]-1:
        footnote_text = f'    *The lineplot displays the recent {number_of_lines} cohorts.'
    
    plt.title(f'{retention_df.cohort_type.capitalize()} cohorts {retention_df.retention_type} ' 
              f'retention for period: '
              f'{retention_df.start_date.strftime("%d %b %y")} - {retention_df.end_date.strftime("%d %b %y")}.'
              f'{footnote_text}') # Create lineplot title
    plt.ylabel("\n\n\n Retention Rate \n")
    plt.legend(title="Cohort and number of users")
    plt.show()
    
    # Create a new figure for the heatmap
    fig, ax = plt.subplots()

    # Create a heatmap
    sns.set(style='ticks', font_scale=0.8)
    sns.heatmap(plt_df, annot=True, fmt=".2%", cmap='Blues', linewidths=0.01, cbar=False)
    # Format the heatmap
    plt.ylabel('Cohort and number of users')
    plt.yticks(rotation=0) # Rotate the y-axis tick labels to be horizontal
    plt.xlabel(f'{retention_df.cohort_type.capitalize()}s after registration')
    plt.show()
    

def annotate_arrow(ax,
                   text: str,
                   xy: tuple,
                   xytext: tuple,
                   color: str):
    """
    Annotate a matplotlib axes with an arrow connecting a text label to a point.

    Parameters:
    -----------
    ax : matplotlib.axes._axes.Axes
        The matplotlib axes to annotate.

    text : str
        The text label to display.

    xy : tuple
        The coordinates of the arrow tip (x, y).

    xytext : tuple
        The annotation text offset (x, y).

    color : str
        The color of the arrow and text.

    Returns:
    --------
    None
    """
    ax.annotate(
        text,
        xy=xy,          # The coordinates of the arrow tip
        xytext=xytext,  # Annotation text offset
        textcoords='offset points',
        horizontalalignment="center",
        color=color,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3", lw=2, color='grey'))


def plot_bootstrap_result(bootstrap_data, 
                          B    : int, 
                          alpha: float):
    """
        Create a distribution plot for the Pandas Series containing Poisson bootstrap results,
        which is calculated by the 'poisson_bootstrap' function.

    Parameters
    ----------
    bootstrap_data : pandas.core.series.Series
         A Pandas Series obtained from the 'cohort_retention' function, representing a specific metric.
        
    B : int
        The number of samples.
        
    alpha : int
        Alpha - significance level.
        Represents the probability of making a Type I error, 
        which is the error of incorrectly rejecting a null hypothesis when it is, in fact, true.
        
    None
    -------

        Distribution plot.
    """
    # Calculate CI
    quantile_l = np.quantile(bootstrap_data, alpha / 2)
    quantile_r = np.quantile(bootstrap_data, 1 - alpha / 2)
    # Illustrate Poisson bootstrap results for ARPU difference between group 'a' and 'b'
    sns.histplot(bootstrap_data)

    # Plot vertical lines for CI and samples mean
    plt.axvline(bootstrap_data.mean(), ls='--', lw=1.3, c='red')
    plt.axvline(quantile_l, ls='--', lw=1.3, c='black')
    plt.axvline(quantile_r, ls='--', lw=1.3, c='black')
    plt.title(f"Distribution of the {bootstrap_data.name.replace('_', ' ')} between group 'a' and 'b', "
                +f"along with {1-alpha:.1%} CI and sample mean difference based on {B:,} Poisson bootstrap samples")
    plt.show()