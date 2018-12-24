/* Welcome to the SQL mini project. For this project, you will use
Springboard' online SQL platform, which you can log into through the
following link:

https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

Note that, if you need to, you can also download these tables locally.

In the mini project, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */



/* Q1: Some of the facilities charge a fee to members, but some do not.
Please list the names of the facilities that do. */

SELECT name
FROM country_club.Facilities
WHERE membercost >0

/* Q2: How many facilities do not charge a fee to members? */

There are 4 facilities that do not charge a fee to members
SELECT COUNT( * ) 
FROM country_club.Facilities
WHERE membercost =0

/* Q3: How can you produce a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost?
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

SELECT facid, name, membercost, monthlymaintenance
FROM country_club.Facilities
WHERE membercost < 0.20 * monthlymaintenance
AND membercost >0;

/* Q4: How can you retrieve the details of facilities with ID 1 and 5?
Write the query without using the OR operator. */

SELECT * 
FROM country_club.Facilities
WHERE facid
IN ( 1, 5 ) 

/* Q5: How can you produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100? Return the name and monthly maintenance of the facilities
in question. */

SELECT name, monthlymaintenance, 
CASE WHEN monthlymaintenance >100
THEN  'Expensive'
ELSE  'Cheap'
END AS Category
FROM country_club.Facilities

/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Do not use the LIMIT clause for your solution. */

select 
firstname,surname
from country_club.Members where joindate in (select max(joindate) from country_club.Members)
union
select 
firstname,surname
from country_club.Members where joindate in (select min(joindate) from country_club.Members);

/* Q7: How can you produce a list of all members who have used a tennis court?
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

SELECT DISTINCT f.name, CONCAT( m.firstname,  " ", m.surname ) AS Name
FROM country_club.Bookings b
LEFT JOIN country_club.Members m ON b.memid = m.memid
LEFT JOIN country_club.Facilities f ON b.facid = f.facid
WHERE b.facid
IN ( 0, 1 ) 
ORDER BY Name

/* Q8: How can you produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30? Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

SELECT DISTINCT f.name AS Facility_Name, CONCAT( m.firstname,  ' ', m.surname ) AS Member_Name, 
CASE WHEN m.memid =0
THEN b.slots * f.guestcost
ELSE b.slots * f.membercost
END AS Total_Cost
FROM country_club.Members m
JOIN country_club.Bookings b ON m.memid = b.memid
JOIN country_club.Facilities f ON b.facid = f.facid
WHERE (
b.starttime >=  '2012-09-14'
AND b.starttime <  '2012-09-15'
)
AND (
b.slots * f.guestcost >30
OR b.slots * f.membercost >30
)
ORDER BY Total_Cost DESC 

/* Q9: This time, produce the same result as in Q8, but using a subquery. */
SELECT DISTINCT f.name AS Facility_Name, c.Name, c.Total_Cost
FROM country_club.Facilities f
JOIN (
SELECT f1.facid, CONCAT( m1.FirstName,  ' ', m1.Surname ) AS Name, 
CASE WHEN m1.memid =0
THEN b1.slots * f1.guestcost
ELSE b1.slots * f1.membercost
END AS Total_Cost, b1.starttime
FROM country_club.Members m1
JOIN country_club.Bookings b1 ON m1.memid = b1.memid
JOIN country_club.Facilities f1 ON b1.facid = f1.facid
)c ON f.facid = c.facid
WHERE (
c.starttime >=  '2012-09-14'
AND c.starttime <  '2012-09-15'
)
AND c.Total_Cost >30
ORDER BY c.Total_Cost DESC 


/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

SELECT DISTINCT f.name AS Facility_Name, SUM( 
CASE WHEN m.memid =0
THEN b.slots * f.guestcost
ELSE b.slots * f.membercost
END ) AS Total_Revenue
FROM country_club.Members m
JOIN country_club.Bookings b ON m.memid = b.memid
JOIN country_club.Facilities f ON b.facid = f.facid
GROUP BY f.name
HAVING Total_Revenue <1000
ORDER BY Total_Revenue DESC 
