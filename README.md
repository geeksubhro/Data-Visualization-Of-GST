# Visualizing GST Collection Trends in Indian States (FY 2020–2025)

This project analyzes and visualizes Goods and Services Tax (GST) collection data across Indian states from FY 2020–21 to 2024–25 (till November). It uses Python to calculate year-over-year growth percentages and generate comparative horizontal bar charts suitable for reporting and presentations.

---

## 📊 Features

- Reads GST data from a CSV file.
- Cleans column names and filters valid state entries.
- Calculates percentage growth between consecutive fiscal years.
- Sorts data by the most recent year's collection.
- Splits the dataset into two parts for visual clarity.
- Creates horizontal bar charts with:
  - Year-wise bars in color.
  - Growth percentage annotations.
  - Alternating row shading.
  - A4-sized output suitable for printing.
- Saves plots as high-resolution PNG images.

---

## 🗂️ File Structure

```
.
├── script.py                                   # Python script for data analysis and plotting
├── data.csv                                    # CSV file containing GST collection data
├── GST_Collection_A4_Part_1.png                # Output chart for the first half of states
├── GST_Collection_A4_Part_2.png                # Output chart for the second half of states
└── README.md                                   # Project documentation
```

---

## 🧾 Data Format

The input CSV (`data.csv`) should follow this format:

| State      | 2020-21 Cr | 2021-22 Cr | 2022-23 Cr | 2023-24 Cr | 2024-25 Cr |
|------------|------------|------------|------------|------------|-------------|
| StateName1 | 12345      | 13579      | 14600      | 15800      | 12000       |
| ...        | ...        | ...        | ...        | ...        | ...         |

- Column names may include additional text but should contain "Cr" (e.g., `"2020-21 Cr"`).
- The script will automatically strip whitespace and detect valid year columns.

---

## ✅ Requirements

Install Python packages before running:

```bash
pip install pandas matplotlib numpy
```

---

## 🚀 Usage

1. Make sure your CSV file is named `data.csv` and located in the same folder as the script.
2. Run the script:

```bash
python a98f1aab-2fbc-40ed-b6ad-18b2ff433f62.py
```

3. Two PNG images will be generated:
   - `GST_Collection_A4_Part_1.png`
   - `GST_Collection_A4_Part_2.png`

These images represent state-wise GST collection comparisons over time.

---

## 📸 Output Preview

Each chart:
- Compares GST collection over five fiscal years.
- Highlights year-on-year growth percentages as annotations.
- Uses color-coded bars and clean labels.
- Is formatted to A4 portrait size for direct inclusion in reports or presentations.

---

## 📝 License

This project is licensed under the Creative Commons Attribution 4.0 International License. You are free to use, share, and adapt the work with attribution to **Subhrojeet Dutta**. See [LICENSE](LICENSE) for full terms.

---

## 🙌 Acknowledgments

- Data visualization powered by [Matplotlib](https://matplotlib.org/)
- Data processing with [pandas](https://pandas.pydata.org/)