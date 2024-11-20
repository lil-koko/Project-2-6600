import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Set Seaborn style and color palette
sns.set_style("whitegrid")
sns.set_palette("Set2")


def load_data():
    df = pd.read_csv(
        r'C:\Users\NJ\Desktop\Streamlit\Price_Agriculture_commodities_Week.csv')
    return df


df = load_data()
df['Date'] = pd.to_datetime(df['Date'])
st.title('Price of Agricultural Commodities in India')

# Interactive Element: Select Commodity
st.subheader('Average Modal Price Over Time for Selected Commodity')
commodities = df['Commodity'].unique()
selected_commodity = st.selectbox('Select Commodity', commodities)

# Filter data based on selected commodity
commodity_data = df[df['Commodity'] == selected_commodity]

# Interactive Element: Date Range Selection
st.subheader('Filter Data by Date Range (27th July - 2nd August)')
start_date = st.date_input('Start Date', df['Date'].min())
end_date = st.date_input('End Date', df['Date'].max())

# Filter data based on date range
date_mask = (commodity_data['Date'] >= pd.to_datetime(start_date)) & (
    commodity_data['Date'] <= pd.to_datetime(end_date))
date_filtered_data = commodity_data.loc[date_mask]

# Visualization 1: Average Modal Price Over Time
avg_price_over_time = date_filtered_data.groupby(
    'Date')['Modal_Price'].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.lineplot(x='Date', y='Modal_Price', data=avg_price_over_time,
             ax=ax1, color='blue', marker='o')
ax1.set_xlabel('Date')
ax1.set_ylabel('Average Modal Price')
plt.xticks(rotation=45)
st.pyplot(fig1)

# Visualization 2: Top 10 Markets by Average Modal Price
st.subheader('Top 10 Markets by Average Modal Price for Selected Commodity')
avg_price_by_market = date_filtered_data.groupby(
    'Market')['Modal_Price'].mean().reset_index()
top10_markets = avg_price_by_market.nlargest(10, 'Modal_Price')

fig2, ax2 = plt.subplots()
sns.barplot(x='Modal_Price', y='Market',
            data=top10_markets, ax=ax2, palette='coolwarm')
ax2.set_xlabel('Average Modal Price')
ax2.set_ylabel('Market')
st.pyplot(fig2)

# Visualization 3: Distribution of Modal Prices
st.subheader('Distribution of Modal Prices for Selected Commodity')
fig3, ax3 = plt.subplots()
sns.histplot(date_filtered_data['Modal_Price'],
             bins=20, kde=True, ax=ax3, color='green')
ax3.set_xlabel('Modal Price')
ax3.set_ylabel('Frequency')
st.pyplot(fig3)

# Visualization 4: Average Modal Price by State
st.subheader('Average Modal Price by State for Selected Commodity')
avg_price_by_state = date_filtered_data.groupby(
    'State')['Modal_Price'].mean().reset_index()

fig4, ax4 = plt.subplots(figsize=(10, 8))
sns.barplot(x='Modal_Price', y='State', data=avg_price_by_state.sort_values(
    'Modal_Price', ascending=False), ax=ax4, palette='Spectral')
ax4.set_xlabel('Average Modal Price')
ax4.set_ylabel('State')
st.pyplot(fig4)

# Interactive Element: Compare Prices Across States
st.subheader('Compare Average Modal Price Across Selected States')
states = df['State'].unique()
selected_states = st.multiselect('Select States', states)

if selected_states:
    state_filtered_data = date_filtered_data[date_filtered_data['State'].isin(
        selected_states)]
    avg_price_by_state = state_filtered_data.groupby(
        ['Date', 'State'])['Modal_Price'].mean().reset_index()

    fig5, ax5 = plt.subplots()

    sns.lineplot(x='Date', y='Modal_Price', hue='State',
                 data=avg_price_by_state, ax=ax5, palette='tab10')

    ax5.set_xlabel('Date')
    ax5.set_ylabel('Average Modal Price')

    # Rotate x-axis labels
    plt.xticks(rotation=45)

    # Set major locator and formatter for dates
    ax5.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax5.legend(loc='upper right')

    # Adjust layout to prevent clipping of tick-labels
    plt.tight_layout()

    st.pyplot(fig5)
else:
    st.write('Please select at least one state to display the comparison chart.')
