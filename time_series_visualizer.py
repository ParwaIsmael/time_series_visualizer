import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Use Pandas to import the data from "fcc-forum-pageviews.csv". Set the index to the date column.
df = pd.read_csv('fcc-forum-pageviews.csv')
df.set_index('date', inplace=True)

# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.
df_bottom = df['value'].quantile(0.025)
df_top = df['value'].quantile(0.975)
df_cleaned = df[(df['value'] >= df_bottom) & (df['value'] <= df_top)]

# Create a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png". The title should be Daily freeCodeCamp Forum Page Views 5/2016-12/2019. The label on the x axis should be Date and the label on the y axis should be Page Views.
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_cleaned.index, df_cleaned['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019.')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    fig.savefig('line_plot.png')
    return fig

# Create a draw_bar_plot function that draws a bar chart similar to "examples/Figure_2.png". It should show average daily page views for each month grouped by year. The legend should show month labels and have a title of Months. On the chart, the label on the x axis should be Years and the label on the y axis should be Average Page Views.
def draw_bar_plot():
    
    # Prepare data for bar plot
    df_bar=df.copy()
    df_bar.index=pd.to_datetime(df_bar.index)
    df_bar['year']=df_bar.index.year
    df_bar['month']=df_bar.index.month_name()

    # group the data
    df_grouped = df_bar.groupby(['year', 'month']).mean().unstack()

    # sort months correctly
    months_order=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_grouped.columns = df_grouped.columns.get_level_values(1)
    df_grouped= df_grouped[months_order]

    # Plotting
    fig = df_grouped.plot(kind='bar', figsize=(15, 5)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()
    
    fig.savefig('bar_plot.png')
    return fig


# Create a draw_box_plot function that uses Seaborn to draw two adjacent box plots similar to "examples/Figure_3.png". These box plots should show how the values are distributed within a given year or month and how it compares over time. The title of the first chart should be Year-wise Box Plot (Trend) and the title of the second chart should be Month-wise Box Plot (Seasonality). Make sure the month labels on bottom start at Jan and the x and y axis are labeled correctly. The boilerplate includes commands to prepare the data.
def draw_box_plot():
    df_box= df.copy()
    df_box.reset_index(inplace=True)
    df_box['date']=pd.to_datetime(df_box['date'])
    df_box['year']=df_box['date'].dt.year
    df_box['month']=df_box['date'].dt.strftime('%b')
    df_box['month_num']=df_box['date'].dt.month

    # Sort months
    df_box = df_box.sort_values('month_num')
    
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True)

    # Draw box plots
    fig, axes= plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel("Page Views")

    sns.boxplot(data=df_box, x='month', y='value', ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page View')

    fig.tight_layout()
    fig.savefig('box_plot.png')
    return fig


