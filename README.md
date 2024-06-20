# T2A2-API-Webserver

This is a repository for my API Webserver Project.

## R1. Explain the problem that this app will solve, and explain how this app solves or addresses the problem

When running a service that involves looking after children, such as an after school care or class, it is vital that teachers and parents can contact eachother timely and easily. Children may become unwell or injured, or parents might simply want to stay informed about what activities their child is completing. However, a child's living situation or contact can change week-to-week or on certain days and it is difficult for businesses to have real-time knowledge on this information. For example, a child may have their parent pick them up on a Wednesday whilst a grandparent may pick them up on a Thursday.For these reasons, it is beneficial to have a centralised database that can ease teacher communication with parents and deliver up-to-date information to both sides.

Currently, there exist many popular apps and services for childcare businesses such as [OWNA](https://www.owna.com.au/features/childcare-communication-app.aspx) and [Xap](https://xap.net.au/childcare-parent-engagement-app-software/) which enable messaging and posts between staff and parents as well as contact information services. These apps are effective tools, however, aside from reduced functionality free versions, these products are also expensive. OWNA charges [$99 per month](https://www.owna.com.au/pricing.aspx) whilst Xap charges [$149 per month](https://xap.net.au/pricing/) to use their services. In addition, these services are delivered as complete applications, meaning they cannot be integrated into a separate website or service and also establishing product dependence from businesses.

Finally, data privacy is a serious concern for small businesses who are typically preoccupied with day-to-day operations. For this reason, the API collects and stores a minimal data about children and carers alike.

This API incorporates multiple measures to solve these issues. Functionally, the API allows businesses to securely store minimalistic but essential data about the children in their care and their contacts' information. A teacher user is able to access a child's designated carer so they can contact the appropriate person. The API also features a comment functionality that allows a teacher to post about children for records purposes and to communicate with parents. From the parent's side, parents receive a user account which allows them to add multiple contacts and designate who is the active carer on a particular day. Because the circumstances around contacting a carer change, a parent can also control whether an active contact should be overriden from receiving sensitive communications. Also, comments about a child can only be accessed from a user account meaning that temporary contacts cannot and do not have to engage with them.

This API provides a free alternative to expensive competitors and, being published as source code, allows businesses to integrate it into their own websites as well.

#### References

[Xplor Education expensive reviews](https://www.getapp.com/education-childcare-software/a/xplor/pricing/)

[OWNA features](https://www.owna.com.au/features/childcare-communication-app.aspx)

[Xap features](https://xap.net.au/childcare-parent-engagement-app-software/)

[OWNA pricing](https://www.owna.com.au/pricing.aspx)

[Xap pricing](https://xap.net.au/pricing/)

## R2. Describe the way tasks are allocated and tracked in your project

For this project, I am using an Agile workflow supplemented by a Trello board as a digital Kanban board (Brede Moe et al., 2014). To do this, I split the overall tasks into smaller tasks and categorised them based on their urgency and impact on other tasks. I entered this information onto my project Trello board, divided my available time and added deadlines to the tasks. I then maintained this Trello board and documented my progress with screenshots at the end of each day. At the beginning of the following day, I reviewed my progress from the prior day, made any neccessary adjustments to the checklist and deadlines and prioritised the next cluster of tasks.

![Initial outline of tasks to complete](docs/1-task-outline.png)
An initial list of the tasks required to complete the project with an estimated urgency assigned.

![Initial Trello Board](docs/agile-1.png)
A screenshot of the initialised Trello board.

![Initial Trello Board](docs/agile-2.png)
The Trello board after one day of work.

![Initial Trello Board](docs/agile-3.png)
The Trello board after two days of work.

![Initial Trello Board](docs/agile-4.png)
The Trello board after three days of work.

### References

Brede Moe, N., Dingsøyr, T., Dyba, T. (2014) 'Agile Project Management', in Ruhe, G., Wohlin, C. (eds.) _Software Project Management in a Changing World_. Berlin: Springer-Verlag, pp. 277-300.

## R6. Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design

### This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase

![ERD Diagram](docs/API-ERD-V1.0.png)
The ERD Diagram for this API, created using Crow's Foot Notation (Abba, 2022). The entities recorded in the API's database are Users, Children, Comments, Teachers, Contacts, Groups and Attendances.

Users are the central entity in the database as they grant parents, admin and teachers the ability to interact with the API. The User table's primary key is an ID and each instance also stores an email, password, first name and two booleans describing the type of account. Only the user's first name is stored in an effort to preserve privacy. The first name is required to identify a user's comment. When interacting with the API, users must first log in and receive a JWT which will then grant them access to different route functionality based on their admin and teacher status.

Before normalisation, Users would store child_ids, contact_ids and comment_ids as a single user is responsible for creating these values. These values are, instead, linked via foreign key.

Children are the next most prominent entity that is tracked and child tuples take their registering user's user_id as a foreign key. A user can register as many children as neccessary so it is a one-to-many relationship. Child tuples contain their first name and last name as well. Because children must be registered by their parents, teacher users cannot register children.

Without normalisation, a child instance would contain their listed contacts, however, because multiple children from the same family can share a contact, it makes sense to register contacts separately and link the two entities in a join table. Similarly, comments are about children so in a non-normalised table, this data would be stored with a child. Instead, tracking comments independently allows increased functionality and less duplication.

Comments are tuples that take a user_id and a child_id as foreign keys. The user_id links the user who is writing the comment with the message whilst the child_id links the comment to its subject, an individual child. Teachers and non-teachers can make comments but, parents can only read and write comments about children they have registered. Comments track the date they were created as well as an urgency rating. The urgency rating is chosen from "urgent", "positive" and "neutral". The urgency rating is included to allow for increased front end posibilities such as a user automatically receiving emails or notifications containing urgent comments.

Contacts are registered by parents and linked to the user that registered them. Contacts are entered with a name, a phone number, an optional email address and an emergency contact boolean. The emergency contact boolean allows emergency requests to skip a contact if they are not designated as appropriate for certain messages. For example, a child's grandparent may be their contact for pick-up information but a parent may want behavioural-based communications to be sent directly to themselves. In these circumstances, teachers or admin can access the appropriate contacts that have been designated by a user.

The Teachers table records a teacher's first name and their email. Groups are entities that describe the information of a class or lesson. Groups require one or more teacher_id values and contain the name of a group and the day it gathers. The day data being stored in groups allows for groups that share the same name meeting on different days of the week as well as describing altered groups based on the day such as a 3-year-old class being merged with a 4-year-old class only on Thursdays. Knowing their child's group allows a parent to access contact information for the teachers that are responsible for the group.

Attendances describe the days that a child attends child care, what group they are in and who their contact is for that day. Attendances take a child_id, group_id and contact_id as foreign keys. Attendances link all of this information so that a parent can specify different contacts for their children on different days. From the teacher's side, they can make API requests for the child's contact information on a given day.

Attendances are a join table created to enforce data normalisation. Attendance data could be noted in a child's tuple but it is not a complete piece of information without including the group that the child is a part of, something that would be recorded many times across children. For this reason, their attendance must be linked with a group_id that links the name of the group, its teacher and what day the group meets. All of this data, in combination with a designated contact for a particular day, uniquely describes which child attends what group on which day as well as who their primary contact is for that attendance.

### References

Abba, I (2022) _[Crow's Foot Notation – Relationship Symbols And How to Read Diagrams](https://www.freecodecamp.org/news/crows-foot-notation-relationship-symbols-and-how-to-read-diagrams/)_, FreeCodeCamp website, accessed 19 June 2024.

## R8. Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint

* HTTP verb
* Path or route
* Any required body or header data
* Response

### Users

GET User

* GET
* /Users OR /Users/<int:id>
* JWT_Token where is_admin == True
* Response: user_id, email, first_name, is_admin, is_teacher, 200/400, 401

CREATE User

* POST
* /Users
* Body: email, password, first_name
* Response: Success: user created, 200/400

UPDATE User

* PATCH
* /Users/<int:id>
* JWT_Token JWT_Token where is_admin == True or get_JWT_identity == user.id
* Body: email or password
* Response: {Success: user updated, changed_field: new_value}, 200, 400, 401

DELETE User

* DELETE
* /Users/<int:id>
* JWT_Token JWT_Token where is_admin == True
* Response: Success: user deleted, 200/400, 401

### Children

GET Child/Children

* GET
* /Children OR /Children/<int:id>
* JWT_Token where is_admin == True, is_teacher == False or children.user_id == get_JWT_identity
* Response: first_name, last_name, 200/400, 401

CREATE Child

* POST
* /Children
* JWT_Token where is_admin == True, is_teacher == False
* Body: first_name, last_name
* Response: {Success: child registered, first_name, last_name}, 200/400, 401

DELETE Child

* DELETE
* /Children/<int:id>
* JWT_Token where is_admin == True, or children.user_id == get_JWT_identity
* Response: {Success: child deleted}

UPDATE Child

* PUT
* /children/<int:id>
* JWT_Token where is_admin == True, or children.user_id == get_JWT_identity
* Response: {Success: data updated, field_updated: value}, 200/400, 401

### Comments

GET Comments

* GET
* /children/<int:id>/comments
* JWT_Token where is_admin == True, is_teacher == True or children.user_id == get_JWT_identity
* Response: date_created, urgency, children.first_name, children.last_name, message, 200/400, 401

CREATE Comment

* POST
* /children/<int:id>/comments
* JWT_Token where is_admin == True, is_teacher == True or children.user_id == get_JWT_identity
* Response: {Success: comment posted, date_created, urgency, children.first_name, children.last_name, message}, 200/400, 401

DELETE Comment

* DELETE
* /children/<int:id>/comments
* JWT_Token where is_admin == True, or children.user_id == get_JWT_identity, or comment.user_id == get_JWT_identity
* Response: {Success: comment deleted}, 200/400, 401

UPDATE Comment

* PATCH
* /children/<int:id>/comments
* JWT_Token where is_admin == True, or children.user_id == get_JWT_identity, or comment.user_id == get_JWT_identity
* Body: comment_id
* Response: {Success: comment updated, field_updated: new_value}, 200/400, 401

### Teachers

GET Teacher

* GET
* /teachers or teachers/<int:id>
* JWT_Token where is_admin == True, is_teacher == True
* Response: {teacher_id, first_name, email}, 200/400, 401

CREATE Teacher

* PUT
* /teachers
* JWT_Token where is_admin == True
* Body: {first_name, email}
* Response: {teacher_id, first_name, email}, 200/400, 401

* is_admin == True

UPDATE Teacher

* PATCH
* /teachers/<int:id>
* JWT_Token where is_admin == True
* Body: first_name or email
* Response: {Success: teacher updated, updated_field: new_value}, 200/400, 401

DELETE Teacher

* DELETE
* /teachers/<int:id>
* JWT_Token where is_admin == True
* Response: {Success: teacher deleted}, 200/400, 401

### Contacts

GET Contact

* GET
* /contacts/<int:id>
* JWT_Token where is_admin == True, is_teacher == True or contact.user_id == get_JWT_identity
* Response: contact_id, first_name, ph_number, emergency_cont, email, 200/400, 401

CREATE Contact

* POST
* /contacts
* JWT_Token where is_admin == True, is_teacher == False
* Body: first_name, ph_number, emergency_cont, email (optional)
* Response: {Success: contact registered, first_name, ph_number, emergency_cont, email}, 200/400, 401

UPDATE Contact

* PATCH
* /contacts/<int:id>
* JWT_Token where is_admin == True, or contact.user_id == get_JWT_identity
* Body: updated_field: new_value
* Response: {Success: contact updated, field_updated: new_value}, 200/400, 401

DELETE Contact

* DELETE
* /contacts/<int:id>
* JWT_Token where is_admin == True, or contact.user_id == get_JWT_identity
* Response: {Success: contact deleted}, 200/400, 401

### Groups

GET Group

* GET
* /groups or groups/<int:id>
* JWT_Token
* Response: {name, teacher_id, day, teacher.first_name, teacher.email}, 200/400, 401

CREATE Group

* PUT
* /groups
* JWT_Token where is_admin == True
* Body: {name, teacher_id, day}
* Response: {Success: group created, {name, teacher_id, day}}, 200/400, 401

UPDATE Group

* PATCH
* /groups/<int:id>
* JWT_Token where is_admin == True
* Body: {field_update: new_value}
* Response: {Success: group updated, updated_field: new_value}, 200/400, 401

DELETE Teacher

* DELETE
* /groups/<int:id>
* JWT_Token where is_admin == True
* Response: {Success: group deleted}, 200/400, 401

### Attendances

GET Attendance

* GET
* /children/attendances/<int:id>
* JWT_Token where is_admin == True, is_teacher == True or children.user_id == get_JWT_identity
* Response: {children.first_name, children.last_name}, {group.name, group.day}, {contact.first_name, contact.ph_number, contact.emergency_cont, contact.email}, 200/400, 401

CREATE Attendance

* POST
* /children/attendances
* JWT_Token where is_admin == True, is_teacher == False
* Body: child_id, group_id, contact_id
* Response: {Success: attendance registered, {children.first_name, children.last_name}, {group.name, group.day}, {contact.first_name, contact.ph_number, contact.emergency_cont, contact.email}}, 200/400, 401

UPDATE Attendance

* PATCH
* /children/attendances/<int:id>
* JWT_Token where is_admin == True, or child.user_id == get_JWT_identity
* Body: updated_field: new_value
* Response: {Success: contact updated, field_updated: new_value}, 200/400, 401

DELETE Attendance

* DELETE
* /children/attendances/<int:id>
* JWT_Token where is_admin == True, or child.user_id == get_JWT_identity
* Response: {Success: attendance deleted}, 200/400, 401
