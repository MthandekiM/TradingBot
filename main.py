import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Simulate historical price data
data = {
    'Date': pd.date_range('2021-01-01', periods=100),
    'Price': np.random.rand(100) * 100 + 100
}

# Create dataframe from the data
df = pd.DataFrame(data)


# Calculate the moving averages
def calculate_moving_averages(df, short_window, long_window):
    df['Short_MA'] = df['Price'].rolling(window=short_window).mean()
    df['Long_MA'] = df['Price'].rolling(window=long_window).mean()


# Define trading signal based on moving averages
def generate_signals(df):
    signals = []
    position = 0  # 1 for long, -1 for short, 0 for neutral

    for i, row in df.iterrows():
        if row['Short_MA'] > row['Long_MA'] and position != 1:
            signals.append(1)  # Go Long
            position = 1
        elif row['Short_MA'] < row['Long_MA'] and position != -1:
            signals.append(-1)  # Go Short
            position = -1
        else:
            signals.append(0)  # Stay Neutral
    return signals


# Simulate trading based on signals
def simulate_trading(df, signals):
    df['Signal'] = signals
    df['Position'] = df['Signal'].diff()
    df['Portfolio'] = df['Position'] * df['Price'].shift(-1)  # Buy/Sell the next day's open


# Set short and long moving average window sizes
short_window = 10
long_window = 50

# Calculate moving averages
calculate_moving_averages(df, short_window, long_window)

# Generate trading signals
signals = generate_signals(df)

# Simulate trading
simulate_trading(df, signals)

# Create a line chart
fig, ax = plt.subplots(figsize=(10, 6))  # Corrected 'figSize' to 'figsize'
ax.plot(df['Date'], df['Price'], label='Price', linewidth=2)
ax.plot(df['Date'], df['Short_MA'], label=f'Short_MA ({short_window}) days')
ax.plot(df['Date'], df['Long_MA'], label=f'Long_MA ({long_window}) days')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Price and moving averages')
ax.legend()

# Add buying and selling buttons
axcolor = 'lightgoldenrodyellow'
ax_buy = plt.axes([0.8, 0.01, 0.1, 0.03], facecolor=axcolor)
ax_sell = plt.axes([0.8, 0.06, 0.1, 0.03], facecolor=axcolor)
button_buy = Button(ax_buy, 'Buy')
button_sell = Button(ax_sell, 'Sell')

buy_dates = []
sell_dates = []


# Creating Buy & Sell event handler functions
def on_buy(event):
    buy_dates.append(ax.get_xlim()[0])
    ax.vlines(buy_dates, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], colors='g', linestyles='dotted')
    plt.draw()


def on_sell(event):
    sell_dates.append(ax.get_xlim()[0])
    ax.vlines(sell_dates, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], colors='r', linestyles='dotted')
    plt.draw()


button_buy.on_clicked(on_buy)
button_sell.on_clicked(on_sell)

plt.show()
