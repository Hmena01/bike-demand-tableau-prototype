"""Preserve the handoff; prepare typed daily records and independent controls."""
from pathlib import Path
import csv, io, json, hashlib
from collections import Counter, defaultdict
from datetime import date, timedelta
from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
original = (ROOT / 'Source/day.csv').read_bytes()
# The downloaded handoff serialized its line endings as literal backslash text.
text = original.decode('utf-8-sig').replace('\\r\\n', '\n')
raw = list(csv.DictReader(io.StringIO(text)))
assert len(raw) == 731
assert all(all(v != '' for v in row.values()) for row in raw)
weather = {1: 'Clear / partly cloudy', 2: 'Mist / cloudy', 3: 'Light rain / snow'}
rows = []
for r in raw:
    d = date.fromisoformat(r['dteday'])
    rows.append(dict(Date=d, Month=date(d.year,d.month,1), Year=str(d.year),
        MonthNumber=d.month, TemperatureC=float(r['temp'])*41,
        HumidityPct=float(r['hum'])*100, DailyRentals=int(r['cnt']),
        Weather=weather[int(r['weathersit'])], WeatherCode=int(r['weathersit']),
        DayType='Working day' if r['workingday']=='1' else 'Weekend / holiday',
        HumidityNote='Source records 0% humidity; retained as reported' if float(r['hum'])==0 else 'Recorded daily humidity',
        RecordID=int(r['instant']), CasualRentals=int(r['casual']), RegisteredRentals=int(r['registered'])))
dates = [r['Date'] for r in rows]
assert dates == [date(2011,1,1)+timedelta(days=i) for i in range(731)]
assert len(set(r['RecordID'] for r in rows)) == 731
assert all(r['CasualRentals']+r['RegisteredRentals']==r['DailyRentals'] for r in rows)
assert sum(r['DailyRentals'] for r in rows)==3292679
assert Counter(r['WeatherCode'] for r in rows)=={1:463,2:247,3:21}
with (ROOT/'Data/bike_demand.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
wb=Workbook();ws=wb.active;ws.title='Daily'
ws.append(list(rows[0]))
for r in rows:ws.append(list(r.values()))
for row in ws.iter_rows(min_row=2):
    row[0].number_format='yyyy-mm-dd';row[1].number_format='yyyy-mm'
ws.freeze_panes='A2';wb.save(ROOT/'Data/bike_demand.xlsx')
def summary(records):
    return dict(days=len(records),rentals=sum(r['DailyRentals'] for r in records),
        mean=sum(r['DailyRentals'] for r in records)/len(records) if records else None)
audit=dict(source_sha256=hashlib.sha256(original).hexdigest(), rows=731,
    missing_values=0,duplicate_dates=0,aggregation='Unweighted mean across daily records',
    scope=summary(rows),year={y:summary([r for r in rows if r['Year']==y]) for y in ['2011','2012']},
    zero_humidity=[{**r,'Date':str(r['Date']),'Month':str(r['Month'])} for r in rows if r['HumidityPct']==0],
    groups={f'{w} | {d}':summary([r for r in rows if r['Weather']==w and r['DayType']==d]) for w in weather.values() for d in ['Working day','Weekend / holiday']},
    monthly={str(m):summary([r for r in rows if r['Month']==m]) for m in sorted(set(r['Month'] for r in rows))},
    notes=['Literal escaped line endings decoded; original handoff bytes preserved.',
        'Daily Readme conversion: temp * 41 degrees Celsius; hum * 100 percent.',
        'All daily records retained. No imputation or outlier deletion.',
        'Weather groups ordered by source codes 1, 2, 3. Code 4 has no daily observations.',
        'Year stored as a nominal comparison label; MonthNumber gives chronological Jan-Dec order.'])
(ROOT/'Verification/data_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps(audit['scope']));print(audit['groups'])
