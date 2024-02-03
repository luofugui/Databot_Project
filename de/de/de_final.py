from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

def load_and_process_data():
    # Replace this with your actual data loading logic
    df = pd.read_parquet("sea_of_thieves.parquet")
    df['date_time'] = df['timestamp_created'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%m/%d/%y'))
    df['date_time'] = pd.to_datetime(df['date_time'], format='%m/%d/%y')
    return df

def create_plot(df, time_range_selection, grouping_selection, start_date, end_date):
    if time_range_selection == "DateRange":
        mask = (df['date_time'] >= pd.to_datetime(start_date, format='%Y-%m-%d')) & \
               (df['date_time'] <= pd.to_datetime(end_date, format='%m/%d/%y'))  # Adjusted format here
        df = df.loc[mask]

    if grouping_selection == "Month":
        df['year_month'] = df['date_time'].dt.to_period('M')
        grouped_counts = df.groupby('year_month')['voted_up'].value_counts().unstack()
        grouped_counts = grouped_counts.reset_index()
        grouped_counts['year_month'] = grouped_counts['year_month'].dt.strftime('%b %Y')

        positive_counts = grouped_counts[True]
        negative_counts = -grouped_counts[False]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=grouped_counts['year_month'],
            y=positive_counts,
            name='Positive',
            marker_color='turquoise'
        ))

        fig.add_trace(go.Bar(
            x=grouped_counts['year_month'],
            y=negative_counts,
            name='Negative',
            marker_color='salmon'
        ))

        fig.update_layout(
            title='Positive and Negative Counts by Month',
            xaxis_title='Month',
            yaxis_title='Count',
            barmode='relative'
        )

    elif grouping_selection == "Day":
        grouped_counts = df.groupby('date_time')['voted_up'].value_counts().unstack()
        grouped_counts = grouped_counts.reset_index()

        positive_counts = grouped_counts[True]
        negative_counts = -grouped_counts[False]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=grouped_counts['date_time'],
            y=positive_counts,
            name='Positive',
            marker_color='turquoise'
        ))

        fig.add_trace(go.Bar(
            x=grouped_counts['date_time'],
            y=negative_counts,
            name='Negative',
            marker_color='salmon'
        ))

        fig.update_layout(
            title='Positive and Negative Counts by Day',
            xaxis_title='Day',
            yaxis_title='Count',
            barmode='relative'
        )

    return fig

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    grouping_selection = request.form.get('grouping_selection')
    start_date = request.form.get('start_date')
    end_date = '12/31/23'  # Static end date for example

    df = load_and_process_data()
    fig = create_plot(df, "DateRange", grouping_selection, start_date, end_date)

    plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    return render_template('plot.html', plot_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)
