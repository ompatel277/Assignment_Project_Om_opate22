# Assignment_Project_Om_opate22
PathFinder will help current, former, or even upcoming students in college explore and get detailed maps of specifc career related roles. This app will allow students to filter to a specific career roles and find classes, and clubs that are associated at their school. This app will help students become more prepared for certain roles by exploring classes and clubs related to real-world interests.  



Why these models/fields?
I chose these models because I can get an idea of what the app would look like when the user first sign-up and logs in. I think it will help me add or eliminate possible features.

Your relationship choices (ForeignKey, on_delete rationale),
ForeignKey, unique, and primary key. I am still playing around with these optoins not set and stone yet but will figure out more as I continue the project

Any constraints (unique, ordering),
I did make a unique and ordering but I got that from chatGPT and I do not know what it does fully. I was just experimenting on how things would look. But once again I will figure it out with trial and error throughout the project

How you seeded test data.
I manually added the data from the admin dashboard. I do want to try to do the dummydata once I have everything connected. 

For A4 I added 2 different urls in views. Both display a list of users# Assignment_Project_Om_opate22.
This shows the difference between manually entering HTML and using django's shortcut


Hw 5
For homework 5, I added class based views. A base generic views and list view to the project.
I also refactored the URL structures so it can use  "Included()", and created templated that used {% empty %}. I also wired most of the navigations to specific pages


HW 6
I added a searchable college list, where users can search up specific colleges by state, name, and abbreviation using a listview which is linked to a query. The page also shows aggregations like counting up the total schools in a specific state.  

HW 7
I added css code to make my web app look a bit better and I also added a chart which is not the most useful right now but it is a start. 

HW 8
In my Traject project, the **GET method** is used for retrieving or filtering data — for example, the `college_search_view` allows users to search colleges, and the query appears in the URL (`?q=Illinois`). The **POST method** is used for securely creating or submitting data, such as adding a new major through `add_major_fbv` or `AddMajorCBV`, with CSRF protection enabled.  

A **Function-Based View (FBV)** handles both GET and POST manually inside one function using conditional logic (`if request.method == 'POST'`). In contrast, a **Class-Based View (CBV)** like Django’s `FormView` automatically handles form validation, success redirects, and template rendering in a structured way. Both achieve the same result, but CBVs reduce code repetition and are better suited for reusable, scalable form handling.
