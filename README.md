# lockdown-airquality-impact
Observed air quality measurements in Frankfurt am Main, DE area.

The German government's decision to declare a curfew on the 22th March (20th March, Bavaria) 
to further reduce people's transmission rate seems to be supported by 
local air quality measurements which serve as a proxy for activity and mobility.

- Data was retrieved from [Hessisches Landesamt für Naturschutz, Umwelt und Geologie](https://www.hlnug.de/messwerte/luft/recherche-1).
- Goal was to investigate whether COVID-19's induced limitation of movement was visible through air quality measurements.
- Plot below shows the latest week (un until the 17th of March) as a red line. Previous weeks are plotted as darker with increasing recency.
![Recent Air Quality Measurements, Frankfurt, per Week](https://raw.githubusercontent.com/DarioHett/lockdown-airquality-impact/master/output.png "Air Quality Frankfurt")
- Plot below shows a rough Gaussian Process fit. The model does not work well, yet some structure can be picked up such as bi-periodic days and Sunday drawdowns.
The latest observations still seem on the upper end, yet weather is a complex phenomenon and this could as well be caused by a lack of wind. 
Fitting larger models or incorporating variables such as Temperature and Wind speed (both in the data) was not feasible due to ressource constraints.
![Gaussian Process](https://raw.githubusercontent.com/DarioHett/lockdown-airquality-impact/master/gp.png)

