import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Load Data ---
df = pd.read_json('StreamingHistory.json')
df['endTime'] = pd.to_datetime(df['endTime'])
df['month_str'] = df['endTime'].dt.strftime('%b %Y')
df['month'] = df['endTime'].dt.to_period('M')

# --- Page Title ---
st.title('Spotify Listening Dashboard')

# --- Dropdown ---
artists = ['All'] + sorted(df['artistName'].unique().tolist())
selected_artist = st.selectbox('Select an Artist', artists)

# --- Filter ---
if selected_artist == 'All':
    filtered = df
else:
    filtered = df[df['artistName'] == selected_artist]

# --- Summary Stats ---
total_listens = len(filtered)
most_active_month = filtered.groupby('month_str')['trackName'].count().idxmax()
most_played_track = filtered.groupby('trackName')['trackName'].count().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric('Total Listens', total_listens)
col2.metric('Most Active Month', most_active_month)
col3.metric('Most Played Track', most_played_track)

# --- Chart ---
monthly = filtered.groupby('month_str')['trackName'].count()

fig, ax = plt.subplots(figsize=(12, 4))
monthly.plot(kind='bar', ax=ax, color='purple', edgecolor='blue')
ax.set_title(f'Monthly Listens — {selected_artist}')
ax.set_xlabel('Month')
ax.set_ylabel('Total Listens')
plt.tight_layout()

st.pyplot(fig)