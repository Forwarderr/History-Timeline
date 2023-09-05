import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from PIL import Image


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


    data['Beginning'] = data['Start Year'].apply(format_year)
    data['End'] = data['End Year'].apply(format_year)

    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Start Year:Q', axis=alt.Axis(title='Year', format='.0f')),
        x2=alt.X2('End Year:Q'),
        y=alt.Y('Dynasty:N', axis=alt.Axis(title='Dynasty'), sort='x'),  # Sort by Start Year in descending order
        color=alt.Color('Dynasty:N', legend=None),
        tooltip=['Dynasty:N', 'King:N', 'Beginning:N', 'End:N', 'Capital:N', 'Successor:N', 'Achievements:N',
                 'Events:N', 'Occupied Zone:N', 'Wars:N', 'Rituals:N', 'Malpractices:N', 'Employment:N', 'Diets:N']
    ).properties(
        width=900
    ).interactive()  # Make the chart interactive with zooming and panning

    return chart



# Function to display the grouped bar chart for a specific dynasty
def display_grouped_bar_chart(data, selected_dynasty):
    filtered_data = data[data['Dynasty'] == selected_dynasty]
    melted_data = pd.melt(filtered_data, id_vars=['Dynasty'],
                          value_vars=['Economy', 'Political', 'Science', 'Education', 'Craft', 'Humanity', 'Kindness',
                                      'Law', 'Justice', 'Religion'],
                          var_name='Category', value_name='Value')

    grouped_bar_chart = alt.Chart(melted_data).mark_bar().encode(
        x=alt.X('Category:N', axis=alt.Axis(title=' ',labelFontSize=13, labelFontWeight='bold')),
        y=alt.Y('sum(Value):Q', axis=alt.Axis(title=' '), scale=alt.Scale(domain=(1, 10), nice=0)),
        color=alt.Color('Category:N', legend=None),
    ).properties(
        height=500,  # Set the height of the bar chart
        title=f'{selected_dynasty} Stats'
    )

    return grouped_bar_chart


def display_pop_chart(data, selected_dynasty):
    # Load data from the Excel file
    pie_data = data[data['Dynasty'] == selected_dynasty]
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


#Error message
def err(msg:str):
    st.error(msg)


# Load existing data or create a new DataFrame
data = load_data()

# Sidebar for user input with smaller height
st.sidebar.header('Add New Entry')
dynasty = st.sidebar.text_input('Dynasty name:')
king = st.sidebar.text_input("King:")
start_year = st.sidebar.number_input('Start Year:', min_value=-2000, max_value=2000)
end_year = st.sidebar.number_input('End Year:', min_value=-2000, max_value=2000)
capital = st.sidebar.text_input('Capital:')
successor = st.sidebar.text_input('Successor:')
achievement = st.sidebar.text_input('Achievements:')
event = st.sidebar.text_input('Events:')
zone = st.sidebar.text_input('Zone:')
ritual = st.sidebar.text_input('Rituals:')
malpractice= st.sidebar.text_input('Malpractices:')
employment = st.sidebar.text_input('Employment:')
diet = st.sidebar.text_input('Diets:')
wars = st.sidebar.text_input('Major Wars fought:')
humanity = st.sidebar.number_input('Humanity index:', min_value=0, max_value=10)
economy = st.sidebar.number_input('Economy index:', min_value=0, max_value=10)
education = st.sidebar.number_input('Education index:', min_value=0, max_value=10)
science = st.sidebar.number_input('Science index:', min_value=0, max_value=10)
political = st.sidebar.number_input('Political index:', min_value=0, max_value=10)
craft = st.sidebar.number_input('Craft index:', min_value=0, max_value=10)
religion = st.sidebar.number_input('Religion index:', min_value=0, max_value=10)
kindness = st.sidebar.number_input('King\'s kindness index:', min_value=0, max_value=10)
law = st.sidebar.number_input('Law index:', min_value=0, max_value=10)
justice = st.sidebar.number_input('Justice index:', min_value=0, max_value=10)
hindu = st.sidebar.number_input('Hindu Population:', min_value=0)
mus = st.sidebar.number_input('Muslim Population:', min_value=0)
jain = st.sidebar.number_input('Jain Population:', min_value=0)
sikh = st.sidebar.number_input('Sikh Population:', min_value=0)
bud = st.sidebar.number_input('Buddha Population:', min_value=0)
fre = st.sidebar.number_input('French Population:', min_value=0)
bri = st.sidebar.number_input('British Population:', min_value=0)
chri = st.sidebar.number_input('Christian Population', min_value=0)
oth = st.sidebar.number_input('Other Population:', min_value=0)


# Add new entry to the DataFrame and update the Excel file
if st.sidebar.button('Add Entry'):
    if start_year > end_year:
        err('Start Year must be less than or equal to End Year.')
    else:
        if any(value in ["", None] for value in [dynasty, king, capital, successor, achievement, event, zone, wars,
                                                 ritual, malpractice, employment, diet]):
            err('1 or more field left blank')
        else:
            new_entry = {'Dynasty': dynasty, 'King': king, 'Start Year': start_year, 'End Year': end_year,
                         'Capital': capital, 'Successor': successor, 'Achievements': achievement, 'Events': event,
                         'Occupied Zone': zone, 'Wars': wars, 'Humanity': humanity, 'Economy': economy,
                         'Education': education, 'Science': science, 'Political': political, 'Craft': craft,
                         'Hindu': hindu, 'Muslim': mus, 'Jain': jain, 'Buddha': bud, 'Sikh': sikh, 'French': fre,
                         'British': bri, 'Christian': chri, 'Others': oth, 'Rituals': ritual, 'Malpractices': malpractice,
                         'Employment': employment, 'Diets': diet, 'Kindness':kindness, 'Law': law, 'Justice': justice,
                         'Religion': religion}
            new_data = pd.DataFrame(new_entry, index=[0])
            data = pd.concat([data, new_data], ignore_index=True)
            data.to_excel('store.xlsx', index=False, engine='openpyxl')
            st.experimental_rerun()


# Add a search box above the Gantt chart
search_query = st.text_input('Search for Dynasty:')
if search_query:
    data = data[data['Dynasty'].str.contains(search_query, case=False, na=False)]

# Display the Gantt chart with zoom and pan
chart = display_gantt_chart(data)
st.altair_chart(chart, use_container_width=True)
# Allow the user to select a dynasty
selected_dynasty = st.selectbox('Select a Dynasty:', data['Dynasty'].unique())

col1, col2, col3 = st.columns([2, 0.3, 3])

# Display the Gantt chart and the grouped bar chart for the selected dynasty
if selected_dynasty:
    grouped_bar_chart = display_grouped_bar_chart(data, selected_dynasty)
    col1.altair_chart(grouped_bar_chart, use_container_width=True)

    pie_chart = display_pop_chart(data, selected_dynasty)
    col3.plotly_chart(pie_chart, use_container_width=True)
