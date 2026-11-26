"""Render submission documents; this script never changes the Tableau workbook.
AI assisted the document formatting and verification; the author should review the reflection.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from xml.sax.saxutils import escape
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Submission';OUT.mkdir(exist_ok=True)
DRAFT=ROOT/'Drafts';DRAFT.mkdir(exist_ok=True)
for name,file in [('Georgia','Georgia.ttf'),('Trebuchet','Trebuchet MS.ttf'),('TrebuchetBold','Trebuchet MS Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
INK=colors.HexColor('#1B2324');TEAL=colors.HexColor('#155E63');MUTED=colors.HexColor('#525D5E')
LIVE='https://public.tableau.com/views/BikeDemandacrossTimeandWeather-Prototype/BikedemandPrototype?:showVizHome=no&:toolbar=yes'
REPO='https://github.com/Hmena01/bike-demand-tableau-prototype'
W,H=letter
BODY=ParagraphStyle('Body',fontName='Trebuchet',fontSize=11,leading=15,textColor=INK,spaceAfter=8)
SMALL=ParagraphStyle('Small',parent=BODY,fontSize=9,leading=12)

def para(c,text,x,y,width=504,style=BODY):
 p=Paragraph(text,style);_,h=p.wrap(width,1000);p.drawOn(c,x,y-h);return y-h-7

def heading(c,text,y):
 c.setFont('TrebuchetBold',12);c.setFillColor(TEAL);c.drawString(54,y,text);return y-17

def footer(c,page=None):
 c.setFillColor(MUTED);c.setFont('Trebuchet',9);c.drawString(54,30,'Harsh Menaria | NYU Information Visualization | Mini-Project 2')
 if page:c.drawRightString(W-54,30,str(page))

# Standalone cover, supplied as the first document in the submission checklist.
c=canvas.Canvas(str(OUT/'Cover_Page.pdf'),pagesize=letter);c.setTitle('Mini-Project 2 — Cover page')
c.setFillColor(TEAL);c.setFont('TrebuchetBold',12);c.drawString(54,728,'MINI-PROJECT 2 · INTERACTIVE DASHBOARD')
c.setFillColor(INK);c.setFont('Georgia',34);c.drawString(54,655,'Bike demand across');c.drawString(54,610,'time and weather')
y=para(c,'Harsh Menaria<br/>NYU · Information Visualization<br/>Final submission · November 25, 2026',54,555,style=BODY)
y=heading(c,'Research question',y-28)
y=para(c,'How do time of year, temperature, weather and day type relate to daily bike-rental demand, and how do the patterns differ between 2011 and 2012?',54,y)
y=heading(c,'Dataset',y-15)
y=para(c,'Capital Bikeshare, Washington, DC · 731 daily records<br/>January 2011–December 2012 · UCI Bike Sharing dataset',54,y)
y=heading(c,'Explore the work',y-15)
y=para(c,f'<link href="{escape(LIVE)}" color="#155E63"><u>Open the interactive Tableau dashboard</u></link><br/><link href="{REPO}" color="#155E63"><u>Open the GitHub repository and viewing guide</u></link>',54,y)
para(c,'Three coordinated views: monthly demand, daily temperature/rentals, and weather/day-type means. The packaged TWBX embeds the data; browser viewing requires no Tableau installation.',54,y-10,style=SMALL)
footer(c);c.showPage();c.save()

# One-page reflection and updated channel justification table.
c=canvas.Canvas(str(OUT/'Reflection.pdf'),pagesize=letter);c.setTitle('Mini-Project 2 — Design reflection')
c.setFillColor(INK);c.setFont('Georgia',23);c.drawString(54,741,'Design reflection')
y=724
sections=[
('Expressiveness and effectiveness','Daily rentals use position in the monthly and daily views, and bar length from zero in the weather view. These channels support quantitative comparison, consistent with Cleveland and McGill’s graphical-perception findings. Year is a nominal comparison: black/orange colors and circle/triangle daily marks distinguish categories rather than implying a numeric amount.'),
('Gestalt grouping and hierarchy','The monthly overview sits above the two detailed comparisons. A compact KPI row uses existing header whitespace to summarize total rentals, average rentals per day and observed dates for the current selection. Proximity groups each title, chart and supporting text, while aligned edges and consistent typography create similarity across views. The four shared filters form one control group. Whitespace and a restrained divider separate the overview from the details without adding heavy boxes.'),
('Size perception and the humidity tradeoff','Stevens’ Law reminds me that perceived magnitude does not grow linearly with physical mark size. Humidity therefore uses three ordered display bands rather than claiming exact proportional area. Maria’s feedback showed that the bands were hard to judge in a dense cloud. The added Humidity band filter lets a reader isolate one band across all views; exact percentages remain in tooltips.'),
('Color meaning, interaction and data-ink ratio','The weather bars now use my original teal, reserving black for the 2011 series. This corrects the semantic collision identified in feedback. Minimal gridlines and selective hover details reduce non-data ink. Selecting a month/year, a daily observation or a weather bar cross-filters the other views. The tradeoff is that sparse selections need explicit observation counts; connecting monthly means does not invent missing values or establish causal weather effects.')]
for title,text in sections:
 y=heading(c,title,y-9);y=para(c,escape(text),54,y,style=ParagraphStyle('Compact',parent=BODY,fontSize=10.2,leading=13.2))
y=heading(c,'Updated channel justification',y-3)
rows=[['Variable / type','Channel and justification'],['Rentals · quantitative','Vertical position or zero-based horizontal length'],['Temperature · quantitative','Continuous horizontal position in °C'],['Month · temporal / ordered','Fixed January–December horizontal position'],['Year · categorical','Black/orange; circle/triangle daily marks'],['Humidity · quantitative; ordered bands','Ordered symbol sizes + band filter; exact % on hover'],['Weather / day type · ordered / categorical','Ordered, labeled weather rows and paired day-type rows']]
style=ParagraphStyle('Cell',parent=SMALL,fontSize=9.1,leading=11)
t=Table([[Paragraph(escape(v),style) for v in row] for row in rows],colWidths=[185,319]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF0F0')),('LINEBELOW',(0,0),(-1,0),.5,TEAL),('BOTTOMPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4)]));_,height=t.wrap(504,1000);t.drawOn(c,54,y-height);y-=height+9
refs='Reference: Cleveland & McGill (1984), doi:10.1080/01621459.1984.10478080; principles named in the course brief. AI assistance supported workbook editing, document formatting and verification; I must review and be able to explain the submitted work.'
y=para(c,escape(refs),54,y,style=ParagraphStyle('Ref',parent=SMALL,fontSize=8.2,leading=10.5));assert y>42,('Reflection overflow',y)
footer(c,1);c.showPage();c.save()

# A clearly marked worksheet, not a fabricated completed usability report.
c=canvas.Canvas(str(DRAFT/'Usability_Test_Report_DRAFT.pdf'),pagesize=letter);c.setTitle('DRAFT — Usability test evidence required')
for page in range(1,4):
 c.setFillColor(INK);c.setFont('Georgia',22);c.drawString(54,740,'Usability test report — DRAFT')
 y=para(c,'In-class peer-review participation is confirmed, with feedback I gave recorded on page 3. Task-level observations of classmates using my dashboard are not yet documented here.',54,713)
 if page==1:
  y=heading(c,'Method and three tasks for each tester',y-12)
  y=para(c,'The tasks below are a proposed protocol for the final revision, not reconstructed records of the class session. Ask two peers to think aloud, record completion, difficulties and comments, and reset the dashboard between testers.',54,y)
  tasks=[('1. Compare years and months','Find the highest monthly mean in 2012, compare it with the same month in 2011, and select that month/year to show its daily records and weather groups.'),('2. Isolate humidity','Use the Humidity band control to show only More humid (>70%) days. Hover a daily point to report its humidity and rentals, and describe what changed in the other views.'),('3. Use a weather selection and reset','With all filters at All, select the light rain/snow weekend bar. Report its mean and observed-day count, describe the linked views, then restore the full dashboard.')]
  for title,body in tasks:y=heading(c,title,y-10);y=para(c,body,54,y)
  y=heading(c,'Observed-day counts are not rental totals',y-12);y=para(c,'The verified rain/weekend reference is 1,815 mean rentals per day across 5 observed days. These are facilitator reference values; they are not participant observations.',54,y)
  y=heading(c,'Required session records',y-12);para(c,'Tester 1 name/date: _________________________________<br/>Tester 2 name/date: _________________________________<br/>Prior Tableau familiarity: ______________________________',54,y)
 elif page==2:
  y=heading(c,'Raw observations — record both peers',y-12)
  for tester in ['Tester 1','Tester 2']:
   y=heading(c,tester,y-10)
   for task in range(1,4):y=para(c,f'Task {task}: completion/time/help ______________________________<br/>Observed actions or difficulty _______________________________<br/>Exact comment (only if recorded) ___________________________',54,y)
 else:
  y=heading(c,'Expert feedback already received',y-12)
  y=para(c,'Maria identified a missing cover page, black weather bars reusing the 2011 color, and humidity sizes that were difficult to distinguish in the dense scatterplot. This is instructor feedback and must remain distinct from the two student testing sessions.',54,y)
  y=heading(c,'Changes made in response',y-10)
  y=para(c,'Added a standalone cover page; restored teal weather bars so black is specific to 2011; added a shared Humidity band filter; expanded cross-filtering so all three views can drive a selection. Earlier and revised screenshots are retained for comparison.',54,y)
  y=heading(c,'Early feedback I gave classmates',y-10)
  y=para(c,'<b>Yinkui Yu:</b> I liked the charts and interactivity; the single biggest improvement would be reducing the amount of scrolling needed to explore the dashboard.',54,y)
  y=para(c,'<b>Will Miller:</b> I recommend bringing the charts into one coordinated dashboard view, because clicking between separate charts makes comparisons and relationships harder to follow.',54,y)
  y=para(c,'I also gave feedback to other students in class, but I do not recall their names well enough to attribute individual comments.',54,y,style=SMALL)
  y=heading(c,'Task-level records still to document',y-10)
  para(c,'The class comments above document feedback I gave on other dashboards. To complete the final usability report, add the names of classmates who used my dashboard, the three tasks each attempted, observed difficulties or comments, and changes tied to those findings. Instructor feedback and automated checks remain separately identified.',54,y,style=SMALL)
 footer(c,page);c.showPage()
c.save()

# Keep Tableau's original PNGs unchanged. Add explanatory vector callouts in a
# separate landscape document so the interaction evidence remains auditable.
FIG_W, FIG_H = 792, 612
c=canvas.Canvas(str(OUT/'Annotated_Screenshots.pdf'),pagesize=(FIG_W,FIG_H))
c.setTitle('Mini-Project 2 — Annotated interaction screenshots')
figures=[
 ('10_kpi_overview.png','1. Final overview with KPIs',
  'Teal weather bars avoid reusing the 2011 color. Black/orange year lines and circle/triangle daily marks retain two cues for year. The KPI row summarizes the current selection; four shared filters sit together in the upper right.',
  [(32,103,926,54),(1000,86,180,54),(1148,535,260,260)]),
 ('11_kpi_humidity_filter.png','2. Isolate a humidity band',
  'Humidity band = More humid (>70%). All three views and the KPI row summarize the same 231 days: 932,656 rentals and a daily mean of 4,037. Fixed size bounds preserve the larger symbols instead of shrinking them after filtering.',
  [(1000,86,180,54),(132,515,650,242)]),
 ('12_kpi_month_selection.png','3. Select a month and year',
  'September 2012 is selected in the monthly view. The daily and weather views use its 30 days. The KPIs show 218,573 rentals and a daily mean of 7,286. Clear the selection in the monthly chart to restore the overview.',
  [(1014,278,20,20),(132,515,650,242),(1148,535,260,260)])]
for index,(filename,title,caption,boxes) in enumerate(figures,1):
 c.setFillColor(INK);c.setFont('Georgia',23);c.drawString(36,578,title)
 image_x,image_y,image_w,image_h=36,112,720,450
 c.drawImage(str(ROOT/'Screenshots'/filename),image_x,image_y,image_w,image_h)
 c.setStrokeColor(TEAL);c.setLineWidth(1.1)
 for bx,by,bw,bh in boxes:
  # Dashboard coordinates are 1440 by 900 with a top-left origin.
  c.roundRect(image_x+bx*.5,image_y+(900-by-bh)*.5,bw*.5,bh*.5,3,stroke=1,fill=0)
 para(c,escape(caption),36,92,width=720,style=SMALL)
 c.setFillColor(MUTED);c.setFont('Trebuchet',8.5)
 c.drawString(36,27,'Harsh Menaria | Native Tableau PNG with separate document annotations')
 c.drawRightString(756,27,str(index));c.showPage()
c.save()
for name,pages in [(OUT/'Cover_Page.pdf',1),(OUT/'Reflection.pdf',1),(DRAFT/'Usability_Test_Report_DRAFT.pdf',3)]:
 d=fitz.open(name);assert len(d)==pages
 assert all(p.get_text().strip() for p in d)
 print(name.relative_to(ROOT),len(d),'page(s)')
