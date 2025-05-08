import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# Load data
df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()
df = df.dropna(subset=['State'])

# Extract year columns
year_columns = [col for col in df.columns if 'Cr' in col]
years = [col.split()[0] for col in year_columns]

# Calculate growth percentages between consecutive years
for i in range(1, len(year_columns)):
    prev = year_columns[i - 1]
    curr = year_columns[i]
    df[f'{years[i-1]} to {years[i]} (%)'] = ((df[curr] - df[prev]) / df[prev]) * 100

# Sort by most recent year
latest_year_col = year_columns[-1]
df = df.sort_values(by=latest_year_col, ascending=True).reset_index(drop=True)

# Split into two halves
half = math.ceil(len(df) / 2)
dfs = [df.iloc[:half], df.iloc[half:]]

# Colors
colors = ['lightgreen', 'royalblue', 'orange', 'orchid', 'salmon']

# Function to plot and save each half
def plot_half(df_part, index):
    plt.figure(figsize=(8.27, 11.69))  # A4 portrait
    y_pos = np.arange(len(df_part))
    bar_width = 0.13
    gap = 0.015  # spacing between stacked bars

    # Plot bars for each year
    for i, year in enumerate(year_columns):
        plt.barh(y_pos + (i - 2) * (bar_width + gap), df_part[year], height=bar_width,
                 label=years[i], color=colors[i], edgecolor='black')

    # Alternate row shading for better readability
    for y in y_pos:
        if y % 2 == 0:
            plt.axhspan(y - 0.5, y + 0.5, color='whitesmoke', zorder=0)

    # Annotate with growth percentages
    for i in range(1, len(year_columns)):
        curr_year = year_columns[i]
        prev_year = year_columns[i - 1]
        growth_label = f'{years[i-1]} to {years[i]} (%)'
        for j in range(len(df_part)):
            growth = df_part.iloc[j][growth_label]
            if pd.notnull(growth):
                bar_value = df_part.iloc[j][curr_year]
                xpos = bar_value + bar_value * 0.01 + 500
                ypos = j + (i - 2) * (bar_width + gap)
                plt.text(xpos, ypos, f'{growth:+.1f}%', va='center', ha='left', fontsize=6,
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

    # Axis and title
    plt.yticks(y_pos, df_part['State'], fontsize=7)
    plt.xlabel("GST Collection (in Crores)", fontsize=11)
    plt.ylabel("State", fontsize=11)
    plt.title(f"State-wise GST Collection (FY 2020-21 to 2024-25 till Nov) - Part {index+1}",
              fontsize=12, weight='bold')

    # Legend in bottom right
    plt.legend(loc='lower right', fontsize=7, frameon=True)

    # Caption and layout
    plt.figtext(0.5, 0.01,
                "Figures show GST collection (in ₹ Cr) and year-over-year growth percentages.",
                wrap=True, horizontalalignment='center', fontsize=8)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    path = f"GST_Collection_A4_Part_{index+1}.png"
    plt.savefig(path, dpi=300)
    plt.close()
    return path

# Generate plots
output_paths = [plot_half(dfs[i], i) for i in range(1, -1, -1)]
output_paths

