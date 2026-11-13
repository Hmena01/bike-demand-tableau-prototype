# Data, design and verification notes

[Back to the project and interaction guide](../README.md) · [Open the live dashboard](https://public.tableau.com/views/BikeDemandacrossTimeandWeather-Prototype/BikedemandPrototype?:showVizHome=no)

These notes document the dataset, calculations and design decisions behind the working prototype. For instructions on viewing and interacting with it, start with the project README.

## Source and preparation

Source: Fanaee-T, H. (2013), *Bike Sharing*, UCI Machine Learning Repository, [doi:10.24432/C5W894](https://doi.org/10.24432/C5W894). Daily Capital Bikeshare records for Washington, DC, January 1, 2011–December 31, 2012. Definitions follow the bundled daily-file Readme.

- One row is one day. All **731 records** remain, with **731 unique consecutive dates**, no missing fields, and **3,292,679 rentals**. No sampling, imputation, aggregation of extract rows, or outlier deletion was performed.
- [`Source/day.csv`](../Source/day.csv) and [`Source/Readme.txt`](../Source/Readme.txt) preserve the supplied bytes. The source uses standard CRLF line endings, which are handled by the CSV reader.
- [`Data/bike_demand.csv`](../Data/bike_demand.csv) and [`Data/bike_demand.xlsx`](../Data/bike_demand.xlsx) are typed preparation outputs. The packaged workbook embeds a native **Hyper extract**. Every extracted row and all 14 prepared fields were compared with the prepared CSV.
- Temperature follows the daily Readme: `temp × 41` °C. Humidity is `hum × 100`, formatted with a literal percent suffix so it is not scaled twice.
- March 10, 2011 retains the recorded **0% humidity** and **623 rentals**. Its tooltip identifies the source anomaly, and a small visible minimum symbol retains the observation.
- Observed weather codes are 1–3: clear/partly cloudy, mist/cloudy, light rain/snow. Code 4 has no daily observations. Day type distinguishes working days from weekends or holidays.

To regenerate only the preparation outputs, install `openpyxl` in Python 3 and run `python Scripts/prepare_data.py`. The final Tableau workbook contains native authoring changes and should be opened directly.

## Data types used in the project

Q means quantitative (a numeric amount), O means ordinal (an ordered category), and N means nominal (a category).

| Field | Type | Use |
| --- | --- | --- |
| Daily rentals | Q, ratio | Daily points, monthly means and weather/day-type means |
| Temperature | Q, interval | Scatterplot horizontal position in °C |
| Humidity | Q, ratio; grouped into O display bands | Ordered symbol sizes; exact percent in the tooltip |
| Month | Ordered calendar/time field | January–December horizontal position |
| Weather group | O, increasing severity | Clear, mist/cloudy, then light rain/snow rows |
| Day type | N | Working day or weekend/holiday rows and filter |
| Year | N for the two-year comparison | 2011/2012 color, scatterplot shape and shared filter |

## Encodings and changes from the proposal

| Variable and data type | Encoding | Prototype decision |
| --- | --- | --- |
| Month, temporal interval | Fixed continuous calendar x position; separate original year series | Replaces the proposed chronological sequence with aligned seasonal comparison; filtering preserves spacing |
| Daily rentals / mean daily rentals, quantitative ratio | Scatter/line y position; zero-based bar length | Shared 0–10,000 rental bounds; six bar means directly labeled |
| Temperature, quantitative interval | Continuous scatter x position, 0–40 °C | As proposed |
| Humidity, quantitative ratio, grouped into ordered bands | Three ordered symbol sizes: Drier (<50%), Moderate (50–70%), More humid (>70%); exact percentage in hover | Replaces the subtle continuous size scale with readable bands and a visible minimum. These display thresholds are not scientific classifications. Size indicates order, not proportional area; Tableau omits absent bands from the filtered legend |
| Weather, ordinal categories | Ordered, labeled rows | Each weather/day-type combination keeps one solid tungsten `#333333` mean bar. Weather is identified by row position and text, with no color subdivision |
| Day type, nominal | Paired labeled bar rows | Replaces proposed circle/triangle shapes; working day precedes weekend/holiday |
| Year, nominal comparison | Tungsten `#333333` for 2011; orange/vermilion `#D55E00` for 2012 | One monthly line per year; circles for 2011 and triangles for 2012 in the scatterplot. A single colored year key and the shared Year filter support comparison |

The monthly display uses `MAKEDATE(2000, [MonthNumber], 1)` only to align the calendar; the original 2011/2012 year remains the identifier for each colored series. The line connects observed monthly means within each year, including sparse selections; the daily records are unchanged. The scatter view is 310 pixels high, increased from 250, with the monthly panel shortened to make room.

The revised typography uses **Georgia 28 pt regular** headline and **Trebuchet MS** supporting text, charts and tooltips. This replaces the proposal's Arial-only styling. The scatterplot now uses hollow circles and triangles for the two years, with restrained sizes and no point labels. The weather chart retains the original six paired horizontal mean bars; it is not split into year segments. Sample sizes stay in hover to keep the dashboard uncluttered.

## Reading filtered and sparse selections

The calendar stays fixed under filtering. Points represent observed monthly means; lines connect those points within each year, including across months without matching days. A connecting segment does not represent an observed value for an intervening month. No missing month is assigned zero or imputed. For example, rain/snow weekends contain only five days across both years; their points occupy the correct February, April, July and October positions.

“Weekend / holiday” combines Saturdays, Sundays and source-flagged holidays. An independent check of all original dates found 210 weekend days and 21 additional weekday holidays, matching all 231 nonworking records. Rentals count trips across the system, not distinct riders or the number of days. Full-period daily means and sample counts are:

| Weather | Working day: mean (days) | Weekend / holiday: mean (days) |
| --- | ---: | ---: |
| Clear / partly cloudy | 5,024 (307) | 4,587 (156) |
| Mist / cloudy | 4,075 (177) | 3,937 (70) |
| Light rain / snow | 1,800 (16) | 1,815 (5) |

The rain/snow weekend mean rests on just five observations and should not be presented as a reliable weekend effect. Every original `cnt` value also equals `casual + registered`.

## Implemented interactions

Year, Day type and Weather group filters apply to all three charts. Selecting a weather/day-type bar filters the monthly and daily views to matching records; the weather chart retains the comparison rows and dims the other bars. Clearing that selection restores the target views within the current dropdown filters. Tooltips provide precise values and observed-day counts for aggregated marks.

The weather chart is the source of the cross-view selection action. The year key is a text guide; the Year dropdown provides filtering. Full reciprocal brushing remains final-submission work.

The scatterplot includes a native linear fit for each visible year, without confidence bands. These are descriptive associations, not causal effects or forecasts. Fits based on sparse selections should be treated cautiously.

## Color and grayscale check

2011 uses tungsten `#333333`; 2012 uses orange/vermilion `#D55E00`, from the [Okabe–Ito Color Universal Design palette](https://jfly.uni-koeln.de/color/). The scatterplot also uses circles and triangles. The weather bars are uniformly tungsten; their color does not encode year.

A [grayscale conversion](../Screenshots/05_grayscale_check.png) of the revised native overview was visually inspected. The year lines retain different lightness and the daily points retain their shapes. The specified solid year colors have contrast ratios of 12.63:1 and 3.87:1 against white; symbol transparency and antialiasing affect displayed contrast. This check does not establish complete accessibility or replace testing with viewers.

## Verification and feedback response

Native checks covered the full-data overview, the shared 2011 and 2012 filter, and the linked five-day rain/weekend selection. All six full-period weather means match the original source. The original embedded Hyper data remains unchanged.

The published revision loaded in a fresh anonymous browser session. Its Year filter and rain/weekend tooltip were checked against the source:

| Year filter | Rain/weekend mean rentals per day | Observed days |
| --- | ---: | ---: |
| All | 1,815 | 5 |
| 2011 | 711 | 2 |
| 2012 | 2,552 | 3 |

Selecting the rain/weekend bar updated both target charts. Clicking blank plot space cleared the selection. The revised value labels were checked at the dashboard's intended desktop width.

Raz and Maria's feedback and the color/shape changes already made are recorded in the [feedback log](../feedback_log.txt). Earlier screenshots remain available alongside the revised screenshots in the [project README](../README.md#screenshots-and-feedback).

Full reciprocal brushing, formal accessibility tuning, narrower-screen layouts and human usability testing remain final-submission work under the supplied rubric.

## My own reflection and plan for version 3

This direction comes from my own reflection on the project's purpose, separately from Raz and Maria's color and year-distinction feedback. I noticed that I can do more with the data to develop one clearer overall insight across the views.

Further aggregation is feasible with the existing records. The prepared data already includes year, month, weather, day type and separate casual/registered rental counts. These support grouped daily averages and a rider-type breakdown without adding another dataset. An independent calculation from the original daily CSV gives:

| Year | Observed days | Mean rentals per day |
| --- | ---: | ---: |
| 2011 | 365 | 3,405.76 |
| 2012 | 366 | 5,599.93 |

Mean daily rentals increased **64.4%** between the two years. This is a possible central finding for version 3: connect the views around demand growth, then examine how the descriptive patterns differ by month, weather, day type and rider type. Using daily means accounts for the different number of days in each year; grouped comparisons should retain their observed-day counts.

If another source adds useful context, [UCI also provides hourly records for 2011–2012](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset), and [Capital Bikeshare publishes trip-history data](https://capitalbikeshare.com/system-data). Those records could be aggregated to a suitable comparison level after checking date coverage, definitions and data grain. They add detail from which summaries can be calculated; another dataset is not required simply to aggregate the current records.

These are planned analytical improvements. No additional source or version-3 dashboard has been implemented as part of this feasibility check.
