## PDD
I got the PDD finalised and submitted this week. Writing the content in
markdown and only using Word at the end to format it worked well and is
probably the approach I'll take for the final report. Using markdown had a
number of benefits including version control alongside the codebase and a
simple syntax that allowed me avoid messing with formatting, fonts and sizing
until the content was written. The final PDF is in the
`docs/Project-Definition-Doc directory`.

## Database
The rest of the FYP work this week was focused on getting a database set up
to store the results of the classifier into. I decided to go with Postgres
SQL because it's a highly performant SQL database that follows a lot of
standards and I had read good things about it online for a while reading up
to this. The database design is simple enough that pretty much any of the
main DBMSs out there would have sufficed so it seemed like a good opportunity
to get more familiar with another DBMS.

My rusty SQL skills along with my unfamiliarity of Postgres SQL meant the
set-up took longer than expected. I used a Docker container to run it locally
to avoid having to install the database onto my own laptop. I used the
psycopg2 Python package to connect the classifier to the database. The
initial table design can be seen in `database/create-table.sql` but I expect
it to be improved over time (adding constraints etc.).

I left the pipeline run for a few minutes and then viewed the contents of
the database (below). All the Tweets we received during that time passed
through the pipeline successfully and were stored in the database. This is
the first time we've successfully run the entire first half of the pipeline
together and is a good milestone of progress.

```
postgres=# SELECT * FROM sentiment;
      tweet_id      | sentiment |      timestamp      | viewpoint
--------------------+-----------+---------------------+-----------
 927184935055691776 | t         | 2017-11-05 14:44:49 | f
 927185122549469186 | t         | 2017-11-05 14:45:34 | f
 927185254263197697 | f         | 2017-11-05 14:46:05 | t
 927185268800712704 | t         | 2017-11-05 14:46:09 | f
 927185767423717379 | f         | 2017-11-05 14:48:07 | t
 927185882213507073 | t         | 2017-11-05 14:48:35 | t
 927186030578585604 | f         | 2017-11-05 14:49:10 | t
 927186037222334464 | t         | 2017-11-05 14:49:12 | f
 927186071716327424 | f         | 2017-11-05 14:49:20 | t
 927186328273539074 | t         | 2017-11-05 14:50:21 | f
 927186344954290177 | t         | 2017-11-05 14:50:25 | f
 927186396594556929 | t         | 2017-11-05 14:50:37 | f
 927186668280573952 | f         | 2017-11-05 14:51:42 | f
 927186728531656705 | t         | 2017-11-05 14:51:57 | f
 927186773469523969 | t         | 2017-11-05 14:52:07 | t
 927187014570692609 | t         | 2017-11-05 14:53:05 | f
(16 rows)
```
