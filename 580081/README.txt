A companion dataset for the paper "Social sensing of urban land use based on analysis of Twitter users' mobility patterns". This dataset contains five files and one dictionary. All identification of Twitter users were removed to protect the privacy of users.

D1_twitter_pr.csv 
------------------
Data to reproduce the land use uncertainty figure 1 (a) and the preferential return of Twitter users figure 2 (a & b). Eight comma separated columns as follows: longitude (lon) and latitude (lat) of clusters of tweets, rank of the cluster based on the number of tweets (rank), number of tweets within the cluster(count), the active time period of the clusters in days (activetime_days), land use uncertainty expressed as the percentage of tweet that belong to the major land use parcel relative to the total number of tweets in the cluster (purity), the dominant land use type in the cluster using the simplified activity code from 1 to 12 (activity), area of the cluster in square kilometers (area_km2). 


D2_survey_pr.csv
----------------
Data to reproduce the preferential return of travel survey individuals figure 2 (c & d). The data is a subset of the Travel Tracker Survey - CMAP for more details refer to (http://www.cmap.illinois.gov/data/transportation/travel-tracker-survey). Eight comma separated columns as follows: surveyed household id (SAMPN), surveyed individual id (PERNO), day of the survey (DAYNO), trip purpose in the original travel survey classification (TPURP), activity duration in minutes (ACTDUR).


D3_macro_signatures.csv
-----------------------
Data to reproduce figure 4 (a & b). Each row represents a tweet and there are six comma separated columns as follows: longitude of a tweet (lon), latitude of a tweet (lat), date of the tweet (date), land use of the nearest land use parcel to the tweet (luse), hour of the day starting with 0 for midnight (hour), day of the week starting with 1 for Sunday (dow). Land use attributes were extracted from the CMAP land use inventory (http://www.cmap.illinois.gov/data/land-use/inventory).


D4_clusters_signatures.csv
--------------------------
Data to reproduce figure 5. Each row represents a unique cluster of tweets with twenty-five comma separated columns as follows: Column (h0) to (h23) are the number of tweets during the hour of the day relative to the total number of tweets, where (h0) is midnight 12:00 am. Column (land use) is the dominant land use types of the cluster using the simplified activity code 1 to 12. 


D5_clusters_per_user.csv
------------------------
Data to reproduce figure 1 (b). Each row represents a unique Twitter user with thirteen comma separated columns showing the number of identified clusters grouped by the simplified twelve classes land use in addition to the total. 

survey.dict
-----------
A dictionary to translate from the original CMAP Travel Tracker Survey ( 23 classes) to the simplified 12 classes used in this study.  



