# okta-certifinder

A simple selenium project that takes in a .csv file [firstname,lastname,link-to-credly-user-profile] (column headers) with respective data
and returns a csv export file [export_okta_certification_dates_[todays-date].csv]
with the consultants issue and expiration date as well as a marker for which okta certificate paths are expired.

Since okta consultants have 2 certification paths, if the consultant has taken only one of the paths, it will only display 1 line.
if they've taken both exam paths, it will show each line respectively.
if they've taken only the architect exam, they should only have one line.

if they are not okta architects - a consultant must take a recertification exam once every 2 years.
these recertification exams are significantly less challenging and less expensive than taking a full-term exam again.
this means that receritifications and now allowing your certifications to expire is very important to all parties. 

okta ceritifications paths:
1. okta professional -> okta administrator -> okta consultant -> okta architecture
2. okta developer ----------------------------------------------^

the two okta certification paths merge at the architect level.
