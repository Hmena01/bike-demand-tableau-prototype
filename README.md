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
| How do daily rentals vary with temperature, and where do humid days fall? | Daily temperature/rentals scatterplot; year on color and shape, humidity on symbol size | One mark per exact date, 731 marks in the full-data default |
| Within each weather group, how do working days compare with weekends or holidays? | Paired horizontal bars from a common zero baseline | Six weather/day-type means in the full-data default; observed day counts in hover |

All views use the same daily records. Monthly and group values are **mean rentals per day**, rather than totals. The comparisons describe historical associations; they do not establish causal weather effects or forecast demand.

## Interaction

- **Year:** a shared single-select dropdown offers All, 2011, or 2012 to reduce overlap across all three charts. **Day type and Weather group:** shared checkbox dropdowns. Return each filter to **(All)** to restore the complete period.
- **Select a weather/day-type bar or its row header:** the monthly chart and daily scatterplot update to those matching days. The source chart keeps its comparison context and emphasizes the selected group.
- **Clear:** click blank space inside the weather/day-type chart. This clears the chart selection while preserving the shared dropdown filters. Reopening the hosted link restores the saved full-data default.
- **Multiple groups:** Command-click on Mac or Ctrl-click on Windows to select additional groups.
- **Hover:** monthly marks show month, original year, mean and n; daily marks show date, rentals, temperature, humidity, weather and day type; group bars show mean and n.

The calendar stays fixed under filtering. Points represent observed monthly means; lines connect those points within each year, including across months without matching days. A connecting segment does not represent an observed value for an intervening month. No missing month is assigned zero or imputed. For example, rain/snow weekends contain only five days across both years; their points occupy the correct February, April, July and October positions.

“Weekend / holiday” combines Saturdays, Sundays and source-flagged holidays. An independent check of all original dates found 210 weekend days and 21 additional weekday holidays, matching all 231 nonworking records. Rentals count trips across the system, not distinct riders or the number of days. Full-period daily means and sample counts are:

| Weather | Working day: mean (days) | Weekend / holiday: mean (days) |
| --- | ---: | ---: |
| Clear / partly cloudy | 5,024 (307) | 4,587 (156) |
| Mist / cloudy | 4,075 (177) | 3,937 (70) |
| Light rain / snow | 1,800 (16) | 1,815 (5) |

The rain/snow weekend mean rests on just five observations and should not be presented as a reliable weekend effect. Every original `cnt` value also equals `casual + registered`.

## Data preparation and provenance

Source: Fanaee-T, H. (2013), *Bike Sharing*, UCI Machine Learning Repository, [doi:10.24432/C5W894](https://doi.org/10.24432/C5W894). Daily Capital Bikeshare records for Washington, DC, January 1, 2011–December 31, 2012. Definitions follow the bundled daily-file Readme.

- One row is one day. All **731 records** remain, with **731 unique consecutive dates**, no missing fields, and **3,292,679 rentals**. No sampling, imputation, aggregation of extract rows, or outlier deletion was performed.
- `Source/day.csv` and `Source/Readme.txt` preserve the supplied bytes. The source uses standard CRLF line endings, which are handled by the CSV reader.
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
| Humidity, quantitative ratio, grouped into ordered bands | Three ordered symbol sizes: Drier (<50%), Moderate (50–70%), More humid (>70%); exact percentage in hover | Replaces the subtle continuous size scale with readable bands and a visible minimum. These display thresholds are not scientific classifications. Size indicates order, not proportional area; Tableau omits absent bands from the filtered legend |
| Weather, ordinal categories | Ordered, labeled rows | Each weather/day-type combination keeps one solid tungsten `#333333` mean bar. Weather is identified by row position and text, with no color subdivision |
| Day type, nominal | Paired labeled bar rows | Replaces proposed circle/triangle shapes; working day precedes weekend/holiday |
| Year, nominal comparison | Tungsten `#333333` for 2011; orange/vermilion `#D55E00` for 2012 | One monthly line per year; circles for 2011 and triangles for 2012 in the scatterplot. A single colored year key and the shared Year filter support comparison |

The monthly display uses `MAKEDATE(2000, [MonthNumber], 1)` only to align the calendar; the original 2011/2012 year remains on Color and in hover. The earlier line-segment table calculation has been removed from the Marks card so sparse selections retain connected observed-month lines. No daily record changes. The scatter view is 310 pixels high, increased from 250, with the monthly panel shortened to make room.

The approved typography follows the student's latest AMD/NVIDIA dashboard reference: **Georgia 28 pt regular** headline and **Trebuchet MS** supporting text, charts and tooltips. This replaces the proposal's Arial-only styling. The scatterplot now uses hollow circles and triangles for the two years, with restrained sizes and no point labels. The weather chart retains the original six paired horizontal mean bars; it is not split into year segments. Sample sizes stay in hover to keep the dashboard uncluttered.

## Feedback received and changes already implemented

Raz and Maria (instructors) said the sequential colors were not distinct enough and the monthly chart needed a clearer distinction between the two years. I already acted on this feedback during the prototype stage because it mainly concerned small color and shape changes:

- 2011 is tungsten black and 2012 is orange/vermilion in the monthly chart and scatterplot. The orange comes from the [Okabe–Ito Color Universal Design palette](https://jfly.uni-koeln.de/color/). The scatterplot also distinguishes years with circles and triangles.
- The monthly chart keeps exactly one line per year. Selecting one year reduces overlap in all three views.
- The weather chart preserves one mean bar per weather/day-type row. All six bars are solid tungsten black, with the same 0–10,000 scale and values placed in readable space after the bars. No year contributions are stacked together.
- The scatterplot has one native linear fit per year, without confidence bands. These describe associations within the displayed observations, not causal effects or forecasts. Sparse selections have very few observations, so fitted lines should be treated cautiously.
- I inspected a grayscale conversion of the revised native export. The year lines retain different lightness, and the scatterplot keeps its different shapes. This is a visual diagnostic, not a claim of complete accessibility or human usability testing. The specified solid year colors have contrast ratios of 12.63:1 and 3.87:1 against white; symbol transparency and antialiasing affect displayed contrast.

The completed [feedback log](feedback_log.txt) identifies who gave feedback, the main issues, changes already made, and remaining checks for the final. Instructor feedback is identified accurately; it is not described as feedback from student peers.

## Verification and screenshots

Native checks covered the full-data overview, the shared 2011 and 2012 filter, and the linked five-day rain/weekend selection. All six full-period weather means match the original source; the 2011 and 2012 means were checked independently as well. The original embedded Hyper data remains unchanged. The hosted revision loads in a fresh anonymous browser, and its rain/weekend tooltip shows a mean of 1,815 across 5 observed days.

Use these two revised images for the current submission:

1. [Revised overview](Screenshots/03_revised_overview.png): native Tableau export, 2880 × 1800.
2. [Revised linked selection](Screenshots/04_revised_linked_selection.png): the published dashboard with the five-day rain/weekend selection and actual tooltip.

The [grayscale diagnostic](Screenshots/05_grayscale_check.png) is derived from the native revised overview. It documents the visual check and is not a replacement for the interactive dashboard.

The earlier [overview](Screenshots/01_overview.png) and [linked selection](Screenshots/02_linked_selection.png) are retained unchanged as the prototype before this feedback response. They document progress and should not be mistaken for the current design.

For a live demo, start with all data, select a single year to demonstrate the reduction in overlap, restore All, and select the light rain/snow weekend bar. The monthly chart and scatterplot update to the five matching days. Hover the bar to show its mean and observed-day count. Click blank plot space in the weather chart to clear the selection while preserving dropdown filters.

Submit the repository/dashboard link, the two revised screenshots, and the completed feedback log. Full reciprocal brushing, formal accessibility tuning, narrower-screen layouts, and human usability testing remain final-submission work under the supplied rubric.
