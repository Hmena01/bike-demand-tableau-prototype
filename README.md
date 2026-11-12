# Bike demand across time and weather

**Harsh Menaria · NYU Information Visualization · Project 2 prototype**

How do time of year, temperature, weather and day type relate to bike-rental demand? This interactive Tableau dashboard explores **731 days of Capital Bikeshare rentals in Washington, DC, during 2011–2012**, through three connected views.

## View the dashboard

### [Open the live interactive dashboard →](https://public.tableau.com/views/BikeDemandacrossTimeandWeather-Prototype/BikedemandPrototype?:showVizHome=no&:toolbar=yes)

**View it in your browser. No Tableau installation, account or sign-in is needed.** GitHub displays the documentation and screenshots; the filters, selections and tooltips work on Tableau Public.

Use a desktop or laptop for the full layout. If an edge is hidden, use Tableau's **Full Screen** control below the dashboard or zoom your browser out.

[![Current dashboard overview: monthly demand, daily temperature/rentals scatterplot and weather/day-type bars](Screenshots/03_revised_overview.png)](https://public.tableau.com/views/BikeDemandacrossTimeandWeather-Prototype/BikedemandPrototype?:showVizHome=no&:toolbar=yes)

*Current overview. Select the preview above to open the live dashboard.*

## Try it in one minute

1. Open the live dashboard and start with all three filters set to **(All)**.
2. Change **Year** to **2012** in the upper right. All three charts update; the scatterplot shows only orange triangles, making individual days easier to inspect.
3. Hover over a daily point to see its date, rentals, temperature, humidity, weather and day type.
4. Return **Year** to **(All)**, then click the **Weekend / holiday** bar under **Light rain / snow**. The monthly chart and scatterplot update to the **five matching days**. Hover over the bar to see **1,815 mean rentals per day** and **5 observed days**.
5. Click empty plot space inside the weather chart to clear the selection. The other views return to the data allowed by your dropdown filters.

## What the interactions do

| Control or gesture | How to use it | What changes |
| --- | --- | --- |
| **Year** | Choose **2011**, **2012** or **(All)** | Filters all three charts; a single year reduces overlap |
| **Day type** | Use the checkboxes to select working days and/or weekends/holidays | Filters all three charts |
| **Weather group** | Use the checkboxes to select clear, mist/cloudy and/or light rain/snow days | Filters all three charts |
| **Select a weather bar** | Click one of the six horizontal bars | Filters the monthly chart and scatterplot to that weather/day-type group; the weather chart keeps its comparison rows and dims the other bars |
| **Clear a bar selection** | Click blank plot space inside the weather chart | Removes the chart selection while keeping your dropdown filters |
| **Hover over a mark** | Pause over a line point, daily symbol or bar | Shows exact values; monthly points and bars also show how many days contribute to their mean |

The dropdown filters work together. **To reset everything:** clear any weather-bar selection, then set Year, Day type and Weather group to **(All)**. The year key explains the colors and shapes; use the **Year dropdown** to filter.

## How to read the three views

| View | What each mark represents | What to compare |
| --- | --- | --- |
| **Monthly demand** | One month's **mean rentals per day**, with one line per year | Seasonal patterns and the difference between 2011 and 2012 |
| **Daily rentals and temperature** | One day: temperature on the horizontal axis and rentals on the vertical axis | Temperature/demand patterns; larger symbols indicate a higher humidity band |
| **Rentals by weather and day type** | **Mean rentals per day** for one weather/day-type group | Working days versus weekends/holidays within each weather group |

**2011 = tungsten black; 2012 = orange.** The scatterplot also uses **circles for 2011** and **triangles for 2012**. Weather bars are uniformly black; their color does not represent a year. The Year filter controls which years contribute to those means.

Monthly lines connect observed means, including across months without matching days; a gap is never treated as zero. “Observed days” is the sample count behind an average, not the number of rentals. The rain/weekend example has only five days, so it should not be treated as a reliable general weekend effect. Trendlines describe associations rather than causes or forecasts.

## Screenshots and feedback

The two current submission images are the [revised overview](Screenshots/03_revised_overview.png) and [revised linked selection](Screenshots/04_revised_linked_selection.png).

![Published dashboard after selecting the rain/snow weekend bar: both target charts update and the tooltip shows 1,815 mean rentals across 5 days](Screenshots/04_revised_linked_selection.png)

**Feedback already addressed:** Raz and Maria said the colors and the distinction between years needed to be clearer. The prototype now uses orange/black year colors, circle/triangle scatter marks, a shared Year filter and readable black weather bars. The [completed feedback log](feedback_log.txt) records their comments, the changes already made and the planned final checks.

<details>
<summary>View the grayscale check</summary>

This diagnostic was derived from the revised native Tableau export and visually inspected. The year lines retain different lightness and the scatterplot retains different shapes.

![Grayscale diagnostic of the revised dashboard](Screenshots/05_grayscale_check.png)

</details>

<details>
<summary>View the earlier prototype screenshots — preserved before the feedback changes</summary>

These earlier images document progress. The revised screenshots above show the current design.

![Earlier prototype overview](Screenshots/01_overview.png)

![Earlier prototype linked selection](Screenshots/02_linked_selection.png)

</details>

## Open the workbook locally

For viewing, the browser link above is enough. To inspect or edit the native workbook:

1. [Download the packaged Tableau workbook](https://github.com/Hmena01/bike-demand-tableau-prototype/raw/refs/heads/main/menaria_harsh_bike_demand_prototype.twbx).
2. Open the downloaded `.twbx` in Tableau Desktop or Tableau Public desktop. It was authored in **Tableau Desktop 2026.2.2**; use that version or a compatible newer version.
3. Select the **Bike demand | Prototype** dashboard tab.

All 731 daily records are embedded in the workbook. No external spreadsheet connection, Python setup, API key or data refresh is needed to open it. GitHub cannot run the `.twbx` as an interactive dashboard.

## Data and project documentation

Source: Fanaee-T, H. (2013), *Bike Sharing*, [UCI Machine Learning Repository](https://doi.org/10.24432/C5W894). The original daily records are preserved; no days were sampled, deleted or imputed.

| Resource | Contents |
| --- | --- |
| [Data, design and verification notes](docs/DATA_AND_DESIGN.md) | Research encodings, Q/O/N field types, calculations, source checks and limitations |
| [Original source data](Source/) | Supplied daily CSV and dataset Readme |
| [Prepared data](Data/) | Typed CSV and Excel files |
| [Feedback log](feedback_log.txt) | Raz and Maria's feedback and the response |

This is a working prototype for class feedback. Full reciprocal brushing, formal accessibility tuning and human usability testing remain final-submission work.
