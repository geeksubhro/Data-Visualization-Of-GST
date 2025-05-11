import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# === Feature Flags ===
ENABLE_SPLIT_PLOTS = True
ENABLE_COMPARISON_PLOTS = True
ENABLE_GROWTH_CALCULATION = True

# === Sorting Options ===
# Options: None, "A-Z", "Z-A", "Low-High", "High-Low"
SORTING_MODE = "A-Z"

def safe_print(msg):
    print(f"[INFO] {msg}")

# === Load Data ===
try:
    df = pd.read_csv("data.csv")
    safe_print("CSV file loaded successfully.")
except FileNotFoundError:
    safe_print("Error: 'data.csv' not found. Please ensure the file exists in the working directory.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    safe_print("Error: 'data.csv' is empty.")
    sys.exit(1)
except Exception as e:
    safe_print(f"Error loading 'data.csv': {e}")
    sys.exit(1)

# === Clean Columns ===
try:
    df.columns = df.columns.str.strip()
    if 'State' not in df.columns:
        safe_print("Error: 'State' column not found in the data.")
        sys.exit(1)
    df = df.dropna(subset=['State'])
except Exception as e:
    safe_print(f"Error processing columns: {e}")
    sys.exit(1)

# === Identify Year Columns ===
try:
    year_columns = [col for col in df.columns if 'Cr' in col]
    years = [col.split()[0] for col in year_columns]
    if len(year_columns) < 2:
        safe_print("Error: At least two year columns with 'Cr' in their name are required.")
        sys.exit(1)
except Exception as e:
    safe_print(f"Error extracting year columns: {e}")
    sys.exit(1)

# === Sanitize and Convert Numeric Columns ===
try:
    for col in year_columns:
        df[col] = df[col].astype(str).str.replace(',', '').str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
except Exception as e:
    safe_print(f"Error cleaning numeric columns: {e}")
    sys.exit(1)

# === Compute Growth Rates ===
if ENABLE_GROWTH_CALCULATION:
    try:
        for i in range(1, len(year_columns)):
            prev = year_columns[i - 1]
            curr = year_columns[i]
            df[f'{years[i-1]} to {years[i]} (%)'] = ((df[curr] - df[prev]) / df[prev]) * 100
        safe_print("Growth percentage columns calculated successfully.")
    except Exception as e:
        safe_print(f"Error calculating growth rates: {e}")
        sys.exit(1)

# === Apply Sorting if Needed ===
if SORTING_MODE:
    try:
        if SORTING_MODE == "A-Z":
            df = df.sort_values(by="State", ascending=False).reset_index(drop=True)
            safe_print("Data sorted alphabetically (A-Z).")
        elif SORTING_MODE == "Z-A":
            df = df.sort_values(by="State", ascending=True).reset_index(drop=True)
            safe_print("Data sorted reverse alphabetically (Z-A).")
        elif SORTING_MODE in ["Low-High", "High-Low"]:
            sort_column = year_columns[-1]
            df[sort_column] = pd.to_numeric(df[sort_column], errors='coerce')  # Ensure numeric
            ascending = SORTING_MODE == "Low-High"
            df = df.sort_values(by=sort_column, ascending=ascending).reset_index(drop=True)
            if ascending:
                safe_print(f"Data sorted by '{sort_column}' from Lowest to Highest.")
            else:
                safe_print(f"Data sorted by '{sort_column}' from Highest to Lowest.")
        else:
            safe_print(f"Invalid SORTING_MODE: '{SORTING_MODE}'. No sorting applied.")
    except Exception as e:
        safe_print(f"Error during sorting: {e}")
        sys.exit(1)

# === Create Output Folders ===
split_dir = "Split_Plots"
comparison_dir = "Comparison_Plots"

for folder in [split_dir, comparison_dir]:
    try:
        os.makedirs(folder, exist_ok=True)
        safe_print(f"Output folder '{folder}' is ready.")
    except Exception as e:
        safe_print(f"Error creating folder '{folder}': {e}")
        sys.exit(1)

# === Split Plot Function ===
def plot_split(df_part, index):
    try:
        plt.figure(figsize=(8.27, 11.69))
        y_pos = np.arange(len(df_part))
        bar_width = 0.13
        gap = 0.015
        colors = ['lightgreen', 'royalblue', 'orange', 'orchid', 'salmon']

        for i, year in enumerate(year_columns):
            plt.barh(y_pos + (i - 2) * (bar_width + gap), df_part[year], height=bar_width,
                     label=years[i], color=colors[i % len(colors)], edgecolor='black')

        for y in y_pos:
            if y % 2 == 0:
                plt.axhspan(y - 0.5, y + 0.5, color='whitesmoke', zorder=0)

        if ENABLE_GROWTH_CALCULATION:
            for i in range(1, len(year_columns)):
                curr_year = year_columns[i]
                label = f'{years[i-1]} to {years[i]} (%)'
                for j in range(len(df_part)):
                    growth = df_part.iloc[j][label]
                    if pd.notnull(growth):
                        xpos = df_part.iloc[j][curr_year] * 1.01 + 500
                        ypos = j + (i - 2) * (bar_width + gap)
                        plt.text(xpos, ypos, f'{growth:+.1f}%', va='center', ha='left', fontsize=6,
                                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        plt.yticks(y_pos, df_part['State'], fontsize=7)
        plt.xlabel("GST Collection (in Crores)", fontsize=11)
        plt.ylabel("State", fontsize=11)
        plt.title(f"GST Collection by State - Part {index+1}", fontsize=12, weight='bold')
        plt.legend(loc='lower right', fontsize=7)
        plt.figtext(0.5, 0.01, "Figures show GST collection and growth rates.", ha='center', fontsize=8)
        plt.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        filename = os.path.join(split_dir, f"GST_Split_Part_{index+1}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        safe_print(f"Saved split plot: {filename}")
    except Exception as e:
        safe_print(f"Error creating split plot part {index+1}: {e}")

# === Run Split Plots ===
if ENABLE_SPLIT_PLOTS:
    try:
        mid = len(df) // 2 + len(df) % 2
        for idx, part in enumerate([df.iloc[:mid], df.iloc[mid:]]):
            plot_split(part, idx)
    except Exception as e:
        safe_print(f"Error during split plotting: {e}")

# === Comparison Plot Function ===
def plot_comparison(prev_col, curr_col, growth_col, i):
    try:
        plt.figure(figsize=(8.27, 11.69))
        y_pos = np.arange(len(df))
        bar_width = 0.35

        plt.barh(y_pos - bar_width/2, df[prev_col], height=bar_width,
                 label=prev_col.split()[0], color='skyblue', edgecolor='black')
        plt.barh(y_pos + bar_width/2, df[curr_col], height=bar_width,
                 label=curr_col.split()[0], color='lightcoral', edgecolor='black')

        for y in y_pos:
            if y % 2 == 0:
                plt.axhspan(y - 0.5, y + 0.5, color='whitesmoke', zorder=0)

        if ENABLE_GROWTH_CALCULATION:
            for j in range(len(df)):
                growth = df.iloc[j][growth_col]
                if pd.notnull(growth):
                    xpos = df.iloc[j][curr_col] * 1.01 + 500
                    ypos = j
                    plt.text(xpos, ypos, f'{growth:+.1f}%', va='center', ha='left', fontsize=6,
                             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        plt.yticks(y_pos, df['State'], fontsize=7)
        plt.xlabel("GST Collection (in Crores)", fontsize=11)
        plt.title(f"{prev_col.split()[0]} vs {curr_col.split()[0]} GST Comparison", fontsize=12, weight='bold')
        plt.legend(loc='lower right', fontsize=7)
        plt.figtext(0.5, 0.01, "Figures show GST collection and year-over-year change.", ha='center', fontsize=8)
        plt.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        filename = os.path.join(comparison_dir, f"{prev_col.split()[0]}_vs_{curr_col.split()[0]}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        safe_print(f"Saved comparison plot: {filename}")
    except Exception as e:
        safe_print(f"Error creating comparison plot ({prev_col} vs {curr_col}): {e}")

# === Run Comparison Plots ===
if ENABLE_COMPARISON_PLOTS:
    try:
        for i in range(1, len(year_columns)):
            plot_comparison(year_columns[i-1], year_columns[i], f'{years[i-1]} to {years[i]} (%)', i)
    except Exception as e:
        safe_print(f"Error during comparison plotting: {e}")
