# Bike demand across time and weather

Harsh Menaria · NYU Information Visualization · Working dashboard prototype

**[Open the interactive Tableau dashboard](https://public.tableau.com/views/BikeDemandacrossTimeandWeather-Prototype/BikedemandPrototype?:showVizHome=no)** · [Tableau Public project page](https://public.tableau.com/app/profile/harsh.menaria/viz/BikeDemandacrossTimeandWeather-Prototype/BikedemandPrototype) · [Download the packaged workbook](menaria_harsh_bike_demand_prototype.twbx?raw=true)

## Run locally

1. Download `menaria_harsh_bike_demand_prototype.twbx` using the link above.
2. Open it in Tableau Desktop or Tableau Public desktop. The workbook was authored in Tableau Desktop 2026.2.2.
3. Select **Bike demand | Prototype**. Its three charts share one embedded Hyper extract containing all 731 daily records. Opening the dashboard requires no external spreadsheet path, Python environment, API key, or data refresh.

The hosted view can be opened without signing in. Use the live dashboard for a browser demo.

## Questions and views

| Research question | Implemented view | Grain and aggregation |
| --- | --- | --- |
| Which months have higher mean daily rentals, and how do 2011 and 2012 compare? | Two yearly lines on fixed January–December calendar positions, with observation markers | AVG(DailyRentals), one mark per observed month/year |
| How do daily rentals vary with temperature, and where do humid days fall? | Daily temperature/rentals scatterplot; humidity on circle size | One mark per exact date, 731 marks in the full-data default |
| Within each weather group, how do working days compare with weekends or holidays? | Paired horizontal bars from a common zero baseline | Six weather/day-type means in the full-data default; observed day counts in hover |

All views use the same daily records. Monthly and group values are **mean rentals per day**, rather than totals. The comparisons describe historical associations; they do not establish causal weather effects or forecast demand.

## Interaction

- **Year, Day type, Weather group:** shared checkbox dropdowns update all three charts. Return each to **(All)** to restore the complete period.
- **Select a weather/day-type bar or its row header:** the monthly chart and daily scatterplot update to those matching days. The source chart keeps its comparison context and emphasizes the selected group.
- **Clear:** click blank space inside the weather/day-type chart. This clears the chart selection while preserving the shared dropdown filters. Tableau's Revert control restores the saved full-data default.
- **Multiple groups:** Command-click on Mac or Ctrl-click on Windows to select additional groups.
- **Hover:** monthly marks show month, original year, mean and n; daily marks show date, rentals, temperature, humidity, weather and day type; group bars show mean and n.

The calendar stays fixed under filtering. Every observed month remains visible as a point, including isolated months. Lines break when consecutive observed months are separated by missing months. No matching days produces a gap, not an invented zero. For example, rain/snow weekends contain only five days across both years; their monthly points occupy the correct February, April, July and October positions.

## Data preparation and provenance

Source: Fanaee-T, H. (2013), *Bike Sharing*, UCI Machine Learning Repository, [doi:10.24432/C5W894](https://doi.org/10.24432/C5W894). Daily Capital Bikeshare records for Washington, DC, January 1, 2011–December 31, 2012. Definitions follow the bundled daily-file Readme.

- One row is one day. All **731 records** remain, with **731 unique consecutive dates**, no missing fields, and **3,292,679 rentals**. No sampling, imputation, aggregation of extract rows, or outlier deletion was performed.
- `Source/day.csv` and `Source/Readme.txt` preserve the supplied bytes. Literal escaped `\r\n` sequences in the handoff were decoded into actual record boundaries.
- `Data/bike_demand.csv` and `Data/bike_demand.xlsx` are typed preparation outputs. The packaged workbook embeds a native **Hyper extract**. Every extracted row and all 14 source fields were compared with the prepared CSV.
- Temperature follows the daily Readme: `temp × 41` °C. Humidity is `hum × 100`, formatted with a literal percent suffix so it is not scaled twice.
- March 10, 2011 retains the recorded **0% humidity** and **623 rentals**. Its tooltip identifies the source anomaly, and a small visible minimum symbol retains the observation.
- Observed weather codes are 1–3: clear/partly cloudy, mist/cloudy, light rain/snow. Code 4 has no daily observations. Day type distinguishes working days from weekends or holidays.

To regenerate only the preparation outputs, install `openpyxl` in Python 3 and run `python Scripts/prepare_data.py`. The final Tableau workbook contains native authoring changes and should be opened directly.

## Encodings and documented changes from the proposal

| Variable and data type | Encoding | Prototype decision |
| --- | --- | --- |
| Month, temporal interval | Fixed continuous calendar x position; separate original year series | Replaces the proposed chronological sequence with aligned seasonal comparison; filtering preserves spacing |
| Daily rentals / mean daily rentals, quantitative ratio | Scatter/line y position; zero-based bar length | Shared 0–10,000 rental bounds; six bar means directly labeled |
| Temperature, quantitative interval | Continuous scatter x position, 0–40 °C | As proposed |
| Humidity, quantitative ratio | Circle size, fixed 0–100 legend, exact percentage in hover | Secondary narrow size range; small visible minimum for the recorded zero. Exact proportional area calibration is not claimed |
| Weather, ordinal categories | Ordered rows and teal lightness | Clear `#6F9E9E`, mist `#3D7A7C`, rain/snow `#155E63`; removed from scatter color |
| Day type, nominal | Paired labeled bar rows | Replaces proposed circle/triangle shapes; working day precedes weekend/holiday |
| Year, nominal comparison | Slate 2011 and teal 2012 lines, compact legend | Makes the between-year comparison explicit |

The monthly display uses `MAKEDATE(2000, [MonthNumber], 1)` only to align the calendar; the original 2011/2012 year remains on Color and in hover. A table calculation detects nonconsecutive observed month numbers within each year and creates separate line segments. It changes drawing continuity without adding or altering daily records.

The approved typography follows the student's latest AMD/NVIDIA dashboard reference: **Georgia 28 pt regular** headline and **Trebuchet MS** supporting text, charts and tooltips. This replaces the proposal's Arial-only styling. Filled scatter circles and paired bars replace the earlier mixed shapes and group dots. Sample sizes stay in hover to keep the dashboard uncluttered.

## Verification and class submission

Native checks covered all three views, all 731 daily marks, each weather/weekend selection, the shared Weekend/holiday filter, the 2012 weekend subset, and the three-day 2012 rain/weekend subset. Monthly tooltips preserve the original year and correct sample size. The humidity legend stays fixed and fits completely inside the dashboard. The saved default has all filters and chart selections cleared.

The two submission images are:

1. [Overview](Screenshots/01_overview.png): native Tableau export, 2880 × 1800.
2. [Linked selection](Screenshots/02_linked_selection.png): actual published dashboard in a fresh browser session, showing selection and hover details.

For a live demo, start with all data, choose Weekend/holiday, compare the three views, restore All, and select the mist/cloudy weekend row. Its 70 matching days update both target views; the missing June 2012 monthly mean remains a clearly explained gap. Then clear the selection.

**Peer feedback remains pending the real in-class session.** Attend and demonstrate the dashboard, then complete `feedback_log.txt` with peer names, main issues raised, and specific planned changes, within one-half page. The current file is a clearly marked template; it is not evidence of attendance or collected feedback.

Full reciprocal brushing, formal accessibility tuning, narrower-screen layouts, and human usability testing remain final-submission work under the supplied rubric.
