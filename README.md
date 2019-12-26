# ichingdb
Interactive I Ching website created with Django and MySQL.

See a live example of this code, running at: https://ichingdb.pythonanywhere.com/ichingdb/

From the about page on that website:

I have found the I Ching to be an invaluable source of wisdom and insight. I hope this tool will help make it more accessible to others.

This is a minimal prototype of a new "I Ching engine". Just ask a question (or append the first and last hexagram numbers to the URL, such as 12/1/) and it will assemble a complex reading for you.

The front-end website is deliberately minimal, showing only the core functionality. This will be customised in the future.

The purpose of this website is to exhibit the functionality of the back-end engine, which is a relational database (MySQL) with a schema that encodes the structure of the I Ching and the associated text fragments.

This enables one to perform complex readings of the I Ching with ease. SQL queries pull together all the associated text fragments, which are then formatted into a 'reading' using Django to interface with the web.

The prototype has no user-access controls, hence on this demo website updating and deleting are disabled.

All randomly generated readings remain part of the archive and can be referred back to later, however there is no identifying information stored along with them.

Licensing:

This work (excluding the text fragments) is unlicensed and free to use and adapt in any way you see fit.

This approach is simple, flexible, customisable and open source. I hope it will evolve from these humble beginnings.

Some of the text fragments included in the database were scraped from The Gnostic Book of Changes (http://jamesdekorne.com/GBCh/I%20Ching_dl.pdf). There is no copyright declaration with these.

Most were scraped from the website I Ching: Mothering Change (http://inthefamilyway.org/iching/), which is based on the work of Steven Karcher (https://ichinglivingchange.org/). These are copyrighted.

Note: I have used Steven Karcher's book "Total I Ching: Myths For Change" (https://www.amazon.com/Total-I-Ching-Myths-Change/dp/074993980X/) for many years. I include this text as a sign of respect for his work and out of a desire to provide the best I Ching access to the general public. I only scraped a minimal amount of text and hope there are no copyright issues. If so the text and links can easily be swapped for another set.

Enjoy! :)
