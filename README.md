# AI Usage and Impact on Students and Professionals

An end-to-end data exploration, cleaning and visualization project, finished as an interactive Streamlit dashboard.

**Live app:** https://aiusage.streamlit.app

---

## 1. Project overview

This project is the VizLab assignment: 20 tasks that take a real, messy dataset from first look to a deployed web app. The dataset records how students and professionals use AI tools and how they rate the impact on their productivity.

The work is split into four parts, matching the assignment:

| Part | Tasks | What it covers |
|------|-------|----------------|
| A. Get to know your data | 1-5 | Previewing, types, summary statistics, extreme rows |
| B. Clean it | 6-10 | Missing values, duplicates, wrong values, outliers |
| C. Visualize | 11-16 | Histogram, count plot, box plot, scatter, bar chart, heatmap |
| D. Tell the story and share it | 17-20 | Polished chart, findings, Streamlit app, deployment |

## 2. Dataset

- **Source:** Kaggle, `eishatuzzuhra/ai-usage-and-impact-on-students-and-professionals`
- **File:** `AI_Usage_and_Impact_on_Students_and_Professionals.csv`
- **Size:** 300 rows and 19 columns (before cleaning)
- **Groups:** 158 students and 142 professionals

### Columns

| Column | Description |
|--------|-------------|
| `User_ID` | Respondent identifier |
| `Age`, `Gender`, `Country` | Demographics |
| `User_Type` | Student or Professional |
| `Education_Level`, `Profession` | Background |
| `Monthly_Income` | Income in dollars |
| `AI_Tool` | Main AI tool used (ChatGPT, Claude, Gemini, Copilot, etc.) |
| `AI_Purpose`, `Tasks_Performed` | What the tool is used for |
| `AI_Usage_Hours_Per_Day` | Hours of AI use per day |
| `Monthly_AI_Cost` | Money spent on AI per month |
| `Productivity_Score` | Self-rated productivity (main number column, 1-10) |
| `Accuracy_Rating`, `Satisfaction_Score` | Ratings of the AI tool |
| `Time_Saved_Hours_Per_Week` | Weekly hours saved by AI |
| `Work_or_Study_Hours_Per_Day` | Daily work or study hours |
| `Would_Recommend` | Yes, No or Maybe |

**Main number column:** `Productivity_Score`.

## 3. Data quality problems found

The raw data is deliberately messy. The main issues:

- **Numbers stored as text.** Values such as `2 hrs`, `8.4 hrs`, `36 yrs` and `$0` sit in columns that should be numeric, so most columns loaded as `object`.
- **Inconsistent categories.** Gender appeared as `Male`, `male`, `M` and `FEMALE`; countries as `United States`, `United States of America` and `U.K.`; tools as `ChatGPT` and `Chat GPT`, `Gemini` and `Google Gemini`.
- **Missing values** in every column except `User_ID` and `User_Type`, from 1.7% (`Would_Recommend`) up to 7.7% (`Age`).
- **Duplicate rows:** 12.
- **Impossible values:** ages up to 97 and AI usage of up to 23 hours per day.
- **Mixed languages** in the `Profession` and `Tasks_Performed` text (some entries are in Portuguese or French).

## 4. Cleaning decisions

| Step | Decision | Reason |
|------|----------|--------|
| Text standardization | Title-cased and mapped variants (`M`/`F` to Male/Female, USA variants to United States, `Chat GPT` to ChatGPT, `Copilot` to Microsoft Copilot, `Gemini` to Google Gemini) | One real category should not be split into several |
| Text to numbers | Stripped units and symbols, converted with `pd.to_numeric(errors="coerce")` | Needed for statistics and charts |
| Missing numeric values | Filled with the median | Robust to outliers and skew |
| Missing categorical values | Filled with the mode | Keeps standard groups intact |
| Duplicates | 12 exact duplicates removed | Duplicates count the same respondent twice and bias averages |
| Impossible ages (over 80) | 2 values replaced with the median age | Not realistic for the survey population |
| Impossible usage (over 16 hours/day) | 1 value replaced with the median | More hours than is plausible alongside work or study |
| IQR outliers in `Productivity_Score` | 3 found (bounds 0.7 to 9.5), all kept | They are valid scores on a 1-10 scale, not errors |

After cleaning, no missing values remain.

## 5. Visualizations

| # | Chart | Question answered |
|---|-------|-------------------|
| 11 | Histogram with mean and median lines | Is productivity balanced or skewed? |
| 12 | Count plot of `AI_Tool` | Which tools are most used? |
| 13 | Box plot of productivity by `User_Type` | Do students and professionals differ? |
| 14 | Scatter plot of time saved vs productivity, coloured by `User_Type` | Do the two move together? |
| 15 | Bar chart of average productivity by `AI_Tool` (no time column exists) | Which tool users score highest? |
| 16 | Correlation heatmap of numeric columns | Which two columns are most strongly related? |
| 17 | Improved box plot: ordered groups, median labels, single colour family, descriptive title | A chart ready to present |

## 6. The Streamlit app

Live at **https://aiusage.streamlit.app**

**Features**

- **Filters (sidebar):** User type and AI tool multi-selects
- **Key numbers (`st.metric`):** number of users, average productivity score, average hours saved per week
- **Charts:** average productivity by AI tool, productivity by user type (box plot), and productivity vs time saved with a trend line
- **Bonus:** a "Download clean data" button that exports the currently filtered rows as CSV

All figures update as the filters change.

## 7. Repository structure

```
.
├── VizLab_AI_Usage_Completed.ipynb   # Full notebook: all 20 tasks
├── app.py                            # Streamlit dashboard
├── clean_data.csv                    # Cleaned dataset used by the app
├── requirements.txt                  # App dependencies
└── README.md
```

## 8. Run it yourself

**Notebook (Google Colab)**

1. Upload `VizLab_AI_Usage_Completed.ipynb` to Colab.
2. Run all cells. The dataset is downloaded automatically with `kagglehub`.
3. Task 19 writes `app.py`, `clean_data.csv` and `requirements.txt`.

**App locally**

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

**Deploy on Streamlit Community Cloud**

1. Push `app.py`, `clean_data.csv` and `requirements.txt` to a public GitHub repo.
2. Go to https://share.streamlit.io, choose Create app, select the repo, branch `main` and main file `app.py`.
3. Under Advanced settings, set the custom subdomain to `aiusage` to get https://aiusage.streamlit.app.

## 9. Tech stack

- Python 3
- pandas and NumPy for cleaning and analysis
- Matplotlib and Seaborn for notebook charts
- Plotly for the interactive app charts
- Streamlit for the dashboard
- kagglehub for loading the data
- Google Colab and Streamlit Community Cloud for running and hosting

## 10. Limitations

- **Small sample:** 300 rows (288 after removing duplicates), so group differences should be read cautiously.
- **Self-reported data:** productivity, accuracy and satisfaction are opinions, not measurements.
- **Imputation:** median and mode filling keeps every row but reduces natural variation and can hide real differences.
- **Correlation is not causation:** a link between time saved and productivity does not show that one causes the other.

## 11. Credits

- Dataset: `eishatuzzuhra` on Kaggle
- Assignment: VizLab, 20 Tasks for Your Dataset
