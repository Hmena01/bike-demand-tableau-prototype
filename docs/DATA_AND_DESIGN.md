# Data, design and verification notes

[Back to the project and interaction guide](../README.md) · [Open the live dashboard](https://public.tableau.com/views/BikeDemandacrossTimeandWeather-Prototype/BikedemandPrototype?:showVizHome=no)

These notes document the dataset, calculations and design decisions behind the final dashboard revision. For instructions on viewing and interacting with it, start with the project README.

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

| Variable and data type | Encoding | Final decision |
| --- | --- | --- |
| Month, temporal interval | Fixed continuous calendar x position; separate original year series | Replaces the proposed chronological sequence with aligned seasonal comparison; filtering preserves spacing |
| Daily rentals / mean daily rentals, quantitative ratio | Scatter/line y position; zero-based bar length | Monthly/scatter rental axes fixed at 0–10,000; bar axis fixed at 0–12,000 to leave space for values after bars, including the maximum observed daily count of 8,714 |
| Temperature, quantitative interval | Continuous scatter x position, 0–40 °C | As proposed |
| Humidity, quantitative ratio, grouped into ordered bands | Three ordered symbol sizes: Drier (<50%), Moderate (50–70%), More humid (>70%); exact percentage in hover | Replaces the subtle continuous size scale with readable bands and a visible minimum. These display thresholds are not scientific classifications. Size indicates order, not proportional area. The size calculation assigns ranks 1, 2 and 3, with a fixed size range so filtering cannot resize a band. The native text key names all three bands |
| Weather, ordinal categories | Ordered, labeled rows | Each weather/day-type combination keeps one solid teal `#155E63` mean bar. Weather is identified by row position and text, with no color subdivision |
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

Year, Day type, Weather group and Humidity band filters apply to all three charts. Each chart can also drive a cross-filter: a monthly point passes its original Year and MonthNumber to the daily and weather views; a daily symbol passes its exact date to the monthly and weather views; a weather/day-type bar passes those categories to monthly and daily views. Clearing a selection in its source chart restores the target views within the other active selections and shared filters. Tooltips provide precise values and observed-day counts for aggregated marks. Conflicting selections can produce no matching records; clear the source selections and set all four dropdowns to All to reset. Tableau Public Revert restores the published starting state.

All three charts are sources of selection actions, each with the other two charts as targets. The year key is a text guide; the Year dropdown provides filtering. Native workbook animations are enabled at Fast (0.30 seconds), Simultaneous. Filtered-out groups with no observed days are not invented zero-rental bars.

The scatterplot includes a native linear fit for each visible year, without confidence bands. These are descriptive associations, not causal effects or forecasts. Fits based on sparse selections should be treated cautiously.

## Color and grayscale check

2011 uses tungsten `#333333`; 2012 uses orange/vermilion `#D55E00`, from the [Okabe–Ito Color Universal Design palette](https://jfly.uni-koeln.de/color/). The scatterplot also uses circles and triangles. The weather bars are uniformly teal; this separates their meaning from the black 2011 series. Their color does not encode year.

A [final grayscale conversion](../Screenshots/09_final_grayscale_check.png) of the final native overview was visually inspected; the [prototype check](../Screenshots/05_grayscale_check.png) is preserved. The year lines retain different lightness and the daily points retain their shapes. The specified solid year colors have contrast ratios of 12.63:1 and 3.87:1 against white; symbol transparency and antialiasing affect displayed contrast. This check does not establish complete accessibility or replace testing with viewers.

## Verification and feedback response

Native checks covered the full-data overview, humidity filtering, a September 2012 monthly selection, an exact-date daily selection, and the weather-bar selection. All six full-period weather means match the original source. The original embedded Hyper data remains unchanged.

Independent humidity-band counts are **146 Drier**, **354 Moderate**, and **231 More humid** (total 731). September 2012 contains 30 days with a mean of 7,285.77 rentals. Selecting September 15, 2012 leaves one date and 8,714 rentals in both target summaries. These are automated/data verification values, not peer-testing observations.

The published prototype was previously checked in a fresh anonymous browser session. Its Year filter and rain/weekend tooltip matched these source values:

| Year filter | Rain/weekend mean rentals per day | Observed days |
| --- | ---: | ---: |
| All | 1,815 | 5 |
| 2011 | 711 | 2 |
| 2012 | 2,552 | 3 |

Selecting the rain/weekend bar updated both target charts. Clicking blank plot space cleared the selection. The revised value labels were checked at the dashboard's intended desktop width.

Raz and Maria's feedback and the color/shape changes already made are recorded in the [feedback log](../feedback_log.txt). Earlier screenshots remain available alongside the revised screenshots in the [project README](../README.md#screenshots-and-feedback).

The final revision adds a cover page, restores teal weather bars, adds the shared humidity filter with stable sizes, and completes cross-filtering from each view. A one-page reflection and three annotated screenshots accompany the workbook. [In-class feedback I gave](CLASS_FEEDBACK_GIVEN.md) is documented, including the comments on Yinkui Yu and Will Miller. The three-page draft also includes this class participation; task-level observations of two classmates using my dashboard still need to be recorded for the final usability report. A separate narrower-screen layout and comprehensive assistive-technology testing have not been completed.

## My own reflection and further analytical work

This direction comes from my own reflection on the project's purpose, separately from Raz and Maria's color and year-distinction feedback. I noticed that I can do more with the data to develop one clearer overall insight across the views.

Further aggregation is feasible with the existing records. The prepared data already includes year, month, weather, day type and separate casual/registered rental counts. These support grouped daily averages and a rider-type breakdown without adding another dataset. An independent calculation from the original daily CSV gives:

| Year | Observed days | Mean rentals per day |
| --- | ---: | ---: |
| 2011 | 365 | 3,405.76 |
| 2012 | 366 | 5,599.93 |

Mean daily rentals increased **64.4%** between the two years. This is a possible central finding for further analysis: connect the views around demand growth, then examine how the descriptive patterns differ by month, weather, day type and rider type. Using daily means accounts for the different number of days in each year; grouped comparisons should retain their observed-day counts.

If another source adds useful context, [UCI also provides hourly records for 2011–2012](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset), and [Capital Bikeshare publishes trip-history data](https://capitalbikeshare.com/system-data). Those records could be aggregated to a suitable comparison level after checking date coverage, definitions and data grain. They add detail from which summaries can be calculated; another dataset is not required simply to aggregate the current records.

These are planned analytical improvements. No additional source or rider-type dashboard has been implemented as part of this feasibility check. The final corrections above address usability and encoding feedback; these analytical extensions remain future work.

The final published workbook was downloaded independently and checked for the restored teal, fixed humidity size bounds, cleared action filters and an unchanged Hyper extract hash. The fixed-size bounds use Tableau’s [native size range controls](https://help.tableau.com/current/pro/desktop/en-us/viewparts_marks_markproperties.htm).

Final anonymous browser checks passed for the default overview, the More humid filter, monthly selection, exact-date daily selection, weather selection, selection clearing and tooltips. Checked values include clear/working mean 5,024 (307 days), More humid clear/working mean 5,116, September 2012 clear/working mean 7,617, the selected September 15 daily/monthly count 8,714, and rain/weekend mean 1,815 (5 days). These checks confirm the shipped interactions; they are not human usability observations.
