import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime as dt
# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
print(df.head())
df["date"] = pd.to_datetime(df["date"])
df=df.set_index("date")
df.index = pd.to_datetime(df.index)
print(df.head())
# Clean data
df = df.sort_values("value")
print(df.head())

print(df.info())
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)
df = df.loc[((df['value'] >= lower_bound) & (df['value'] <= upper_bound))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(32, 10))
    sns.lineplot(data=df,x=df.index,y="value",legend=False, ci=None, color="red")
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        raise TypeError("The DataFrame index must be a DateTime index.")
    df_bar = df.copy()
    #df_bar= df_bar.reset_index()
    df_bar['year'] = [d.year for d in df_bar.index]
    df_bar['year'] = df_bar['year']
    df_bar['month'] = df_bar.index.month_name()
    df_bar = pd.DataFrame(df_bar.groupby(["year", "month"], sort=False)["value"].mean().round().astype(int))
    df_bar = df_bar.reset_index()
    missing_data = {
        "Years": [2016, 2016, 2016, 2016],
        "Months": ['January', 'February', 'March', 'April'],
        "Average Page Views": [0, 0, 0, 0]
    }

    df_bar = pd.concat([pd.DataFrame(missing_data), df_bar])
    #df_bar = df_bar.pivot_table(index="year", columns="month", values='value',aggfunc="mean")
    print(df_bar.head()) 
    # Draw bar plot

    fig, ax= plt.subplots(figsize=(19.2, 10.8), dpi=100)
    chart = sns.barplot(data=df_bar, x="Years", y="value", hue="Months", palette="tab10")
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90, horizontalalignment='center')
    ax.set_ylabel("Average Page Views")
  
        
    

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig 
    



def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['year']= df_box['year'].astype('int')
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # Draw box plots (using Seaborn)
    
    fig, axes= plt.subplots(ncols=2, figsize=(32, 10), dpi=100)

    
    # Year-wise Box Plot (Trend)
    g = axes[0]
    sns.boxplot(x='year', y='value', data=df_box,hue="year",ax=g)
    g.set_title("Year-wise Box Plot (Trend)")
    g.set_xlabel("Year")
    g.set_ylabel("Page Views")
# Month-wise Box Plot (Seasonality)
    
    # Set month order to start from January
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    c= axes[1]
    sns.boxplot(x='month', y='value', data=df_box, order=month_order,hue="month", ax=c)
    c.set_title("Month-wise Box Plot (Seasonality)")
    c.set_xlabel("Month")
    c.set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
