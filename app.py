import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go


# Function to load data from the Excel file or create a new one if it doesn't exist
def load_data():
    try:
        data = pd.read_excel('store.xlsx', engine='openpyxl')
    except FileNotFoundError:
        data = pd.DataFrame(
            columns=['Dynasty', 'Start Year', 'End Year', 'Capital', 'Successor', 'Economy', 'Political', 'Science',
                     'Education'])
        data.to_excel('store.xlsx', index=False, engine='openpyxl')
    return data


im = Image.open("timeline.ico")


st.set_page_config(
    page_title="History Timeline",
    page_icon=im,
    layout="wide",
    initial_sidebar_state="auto",
)


st.markdown('''
    <style>
    footer {visibility : hidden;}
    header {visibility : hidden;}
    </style>
''', unsafe_allow_html=True)


# Function to display the Altair Gantt chart
def display_gantt_chart(data):
    def format_year(year):
        modYear = ''
        if year < 0:
            modYear = f"{abs(year)} BC"
        elif year == 0:
            modYear = year
        else:
            modYear = f"{year} AD"

        return modYear

    data.loc[:, 'Beginning'] = data['Start Year'].apply(format_year)
    data.loc[:, 'End'] = data['End Year'].apply(format_year)

    max_end_years = data.groupby('Dynasty')['End Year'].max().reset_index()
    data = data.merge(max_end_years, on='Dynasty', suffixes=('', '_max'))

    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Start Year:Q', axis=alt.Axis(title='Year', format='.2f'),
                scale=alt.Scale(domain=[data['Start Year'].min(), data['End Year'].max()])),
        x2=alt.X2('End Year:Q'),
        y=alt.Y('Dynasty:N', axis=alt.Axis(title='Dynasty'),
                sort=alt.SortField(field='End Year_max', order='ascending')),
        color=alt.Color('King:N', legend=None),
        tooltip=['Dynasty:N', 'King:N', 'Beginning:N', 'End:N']
    ).properties(
        width=900
    ).interactive()  # Make the chart interactive with zooming and panning

    return chart


def display_table(data):

    def format_year(year):
        modYear = ''
        if year < 0:
            modYear = f"{abs(year)} BC"
        elif year == 0:
            modYear = year
        else:
            modYear = f"{year} AD"

        return modYear

    data.loc[:, 'Beginning'] = data['Start Year'].apply(format_year)
    data.loc[:, 'End'] = data['End Year'].apply(format_year)

    headerColor = 'black'
    rowColor = 'white'
    rowSeparatorColor = 'rgba(0, 0, 0, 0.2)'  # Color for row separators

    # Extract the columns you want to display
    columns_to_display = ['Dynasty', 'King', 'Beginning', 'End', 'Capital', 'Successor', 'Achievements',
                 'Events', 'Occupied Zone', 'Wars', 'Rituals', 'Malpractices', 'Employment', 'Diets',
                 'Inventions', 'Architecture', 'Advancement', 'Tribes']

    # Create a list of dictionaries, one for each row
    table_data = []

    for col in columns_to_display:
        table_data.append({'Attribute': col, 'Value': data[col].values[0]})

    # Create a list of values for the first and second columns separately
    attribute_column = [data['Attribute'] for data in table_data]
    value_column = [data['Value'] for data in table_data]

    # Increase the cell height and add CSS styling to align them in the center
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>Attribute</b>', '<b>Value</b>'],
            line_color='white',  # Header border color
            fill_color=headerColor,  # Header background color
            align=['center', 'center'],  # Align both header columns to the center
            font=dict(color='white', size=14)  # Header font color and size
        ),
        cells=dict(
            values=[['<b>' + str(attribute) + '</b>' for attribute in attribute_column], ['<b>' + str(value) + '</b>' for value in value_column]],
            line_color=rowSeparatorColor,  # Row separator color
            fill_color=[rowColor, rowColor] * len(table_data),  # Cell background color
            align=['center', 'center'],  # Align both cell columns to the center
            font=dict(color='black', size=14),  # Cell font color and size
        ))
    ])

    # Update layout for better appearance
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),  # Adjust margins
        height = 750
    )
    return fig


# Function to display the grouped bar chart for a specific dynasty
def display_grouped_bar_chart(data, selected_dynasty):
    filtered_data = data[data['King'] == selected_dynasty]
    melted_data = pd.melt(filtered_data, id_vars=['Dynasty'],
                          value_vars=['Economy', 'Political', 'Science', 'Education', 'Craft', 'Humanity', 'Kindness',
                                      'Law', 'Justice', 'Religion'],
                          var_name='Category', value_name='Value')

    grouped_bar_chart = alt.Chart(melted_data).mark_bar().encode(
        x=alt.X('Category:N', axis=alt.Axis(title=' ', labelFontSize=13, labelFontWeight='bold')),
        y=alt.Y('sum(Value):Q', axis=alt.Axis(title=' '), scale=alt.Scale(domain=(1, 10), nice=0)),
        color=alt.Color('Category:N', legend=None),
    ).properties(
        height=500,  # Set the height of the bar chart
        title=f'{selected_dynasty} Stats'
    )

    return grouped_bar_chart


def display_pop_chart(data, selected_dynasty):
    # Load data from the Excel file
    pie_data = data[data['King'] == selected_dynasty]
    # Extract values for the Pie Chart
    hindu_value = pie_data['Hindu'].iloc[0]
    muslim_value = pie_data['Muslim'].iloc[0]
    jain_value = pie_data['Jain'].iloc[0]
    buddha_value = pie_data['Buddha'].iloc[0]
    sikh_value = pie_data['Sikh'].iloc[0]
    french_value = pie_data['French'].iloc[0]
    british_value = pie_data['British'].iloc[0]
    chri_value = pie_data['Christian'].iloc[0]
    other_value = pie_data['Others'].iloc[0]
    fig = px.pie(values=[hindu_value, muslim_value, jain_value, buddha_value, sikh_value, french_value, british_value,
                         other_value, chri_value],
                 names=['Hindu', 'Muslim', 'Jain', 'Buddha', 'Sikh', 'French', 'British', 'Others', 'Christian'],
                 title=f'{selected_dynasty} Population')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


# Main Streamlit app
st.markdown("<h1 style='text-align: center;'>History Timeline</h1>", unsafe_allow_html=True)


# Error message
def err(msg: str):
    st.error(msg)


# Load existing data or create a new DataFrame
data = load_data()

# Add a search box above the Gantt chart
search_query = st.text_input('Search for Dynasty:')
if search_query:
    data = data[data['Dynasty'].str.contains(search_query, case=False, na=False)]

# Display the Gantt chart with zoom and pan
chart = display_gantt_chart(data)
st.altair_chart(chart, use_container_width=True)


# Allow the user to select a dynasty
selected_dynasty = st.selectbox('Select a Dynasty:', [None] + list(data['King'].unique()))

if selected_dynasty:
    data = data[data['King'].str.contains(selected_dynasty, case=False, na=False)]
    table = display_table(data)
    st.plotly_chart(table, use_container_width=True)

col1, col2, col3 = st.columns([2.5, 0.1, 3])

# Display the Gantt chart and the grouped bar chart for the selected dynasty
if selected_dynasty:
    grouped_bar_chart = display_grouped_bar_chart(data, selected_dynasty)
    col1.altair_chart(grouped_bar_chart, use_container_width=True)

    pie_chart = display_pop_chart(data, selected_dynasty)
    col3.plotly_chart(pie_chart, use_container_width=True)