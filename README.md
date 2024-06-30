# T2A2-API-Webserver

This is a repository for my API Webserver Project.

## R1. Explain the problem that this app will solve, and explain how this app solves or addresses the problem /6

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

## R2. Describe the way tasks are allocated and tracked in your project /6

For this project, I am using an Agile workflow supplemented by a Trello board as a digital Kanban board (Brede Moe et al., 2014). To do this, I split the overall tasks into smaller tasks and categorised them based on their urgency and impact on other tasks. I entered this information onto my project Trello board, divided my available time and added deadlines to the tasks. I then maintained this Trello board and documented my progress with screenshots at the end of each day. At the beginning of the following day, I reviewed my progress from the prior day, made any neccessary adjustments to the checklist and deadlines and prioritised the next cluster of tasks.

![Initial outline of tasks to complete](docs/1-task-outline.png)
An initial list of the tasks required to complete the project with an estimated urgency assigned.

![Initial Trello Board](docs/agile-1.png)
A screenshot of the initialised Trello board.

![Trello Board screenshot after day 1](docs/agile-2.png)
The Trello board after one day of work.

![Trello Board screenshot after day 2](docs/agile-3.png)
The Trello board after two days of work.

![Trello Board screenshot after day 3](docs/agile-4.png)
The Trello board after three days of work.

![Trello Board screenshot after day 4](docs/agile-5.png)
The Trello board after four days of work. During this day I made some adjustments to the timelines.

![Trello Board screenshot after day 5](docs/agile-6.png)
The Trello board after five days of work. Again, I made some adjustments to the task timelines today after recognising that some of the checklist items were too broad. During this day I initialised the APIs baseline interactions which could be reused in other scopes easily.

![Trello Board screenshot after day 6](docs/agile-7.png)
The Trello board after six days of work. I added a new card to breakdown the task of finishing the API's endpoints.

![Trello Board screenshot after day 7](docs/agile-8.png)
The Trello board after seven days of work.

![Trello Board screenshot after day 8](docs/agile-9.png)
The Trello board after eight days of work.

![Trello Board screenshot after day 9](docs/agile-10.png)
The Trello board after nine days of work. During this day I troubleshooted some errors and progressed code comments but did not finish them. I also adjusted the project management timelines.

![Trello Board screenshot after day 10](docs/agile-11.png)
The Trello board after 10 days of work. After realising that code commenting was taking an extensive time, I decided to answer remaining questions first, as a more important consideration. This sets me up for a smooth final day of work where I only have to finish 2 questions before completing the code comments.

### References

Brede Moe, N., Dingsøyr, T., Dyba, T. (2014) 'Agile Project Management', in Ruhe, G., Wohlin, C. (eds.) _Software Project Management in a Changing World_. Berlin: Springer-Verlag, pp. 277-300.

## R3. List and explain the third-party services, packages and dependencies used in this app /6

### Flask==3.0.3

Flask is a web framework package that provides the tools and templates used to define endpoints, link them to appropriate functions and handle their request bodies, allowing the app to be run on a server. Flask contains methods and decorators which a developer calls in the app's modules to interact with the user's requests, effectively abstracting the routing and connection coding to behind-the-scenes. Built into Flask are error definitions that expand on Pythonic errors and describe the required behaviour for a route or function to work as intended. In addition, Flask contains an errorhandler wrapper that allows a developer to customise the response messages that a user receives for clarity.

### SQLAlchemy==2.0.31

SQLAlchemy is an Object Relational Mapper (ORM) used to generate models which mirror the data structure of a relational database (described in more detail in question 5). Within the app, SQLAlchemy provides Python classes which are used to create inheriting classes which describe the data structures of a connected PostgreSQL database table. Other classes are provided in the package to attribute values including data types and functionality such as default values which are automatically passed to the database if no user input is provided for a particular field.

### marshmallow==3.21.3

Marshmallow is a library which provides methods to convert foreign object types to Python data types. Within the app, marshmallow converts SQLAlchemy objects to Python dictionaries. Marshmallow's provided classes are used to create schema's which, similar to SQLAlchemy models, mirror the data stored in a connected relational database so that attributes and values can be returned as key pairs. These schemas are utilised between the SQLAlchemy requests and returns and the application itself, filtering the user's inputs and responses. For example, marshmallow's built in validators can raise an error if a user enters a string for an email address that does not conclude the "@domain.com" format or if an integer field is passed a string. Similarly, marshmallow schemas filter returned data within the app, removing some fields from the dictionary that is returned to a user such a password value for a GET user request.

#### Flask-JWT-Extended

Flask-JWT-Extended is a pip package used to generate JWTs (JSON Web Tokens). JWTs are generated strings which contain data in three parts: the header, payload and signature. The header is the section of a JWT that describes which algorithm the token was generated with whilst the payload describes values included in the token such as how long the token should be considered validated and any optional data included in a key pair. The signature confirms which system issued the token and considers a secret key, passed when generating the key, the values in the payload and the formatting described in the header. Whilst data in a JWT's header and payload can be deciphered, the secret key is not revealed in the token itself meaning that a duplicate signature cannot be forged and proving the token came from a trusted source. In this app, Flask-JWT-Extended generates tokens when users log in and authenticates them when requests are made to the various endpoints, ensuring users can only access appropriate resources.

#### bcrypt==4.1.3

Bcrypt is a dependency within the app used to hash user passwords so that they can be stored in the database in a non-plain text format. Within the app, a bcrypt instance is first initialised which containts various methods for creating and interpreting hashed passwords. Hashing generates a fixed length but unpredictable string which masks the input string. The returned hash can be recreated using the same hashing function on the same input string but, because hashed values are always the same length, an infinite number of strings can generate the same hashed value. To login in this app and generate a JWT, a user passes a request containing a password string, it is then passed through the hashing method and compared to the stored, already-hashed password recorded and compared. If they have equal values, the user is returned a JWT.

### psycopg2-binary==2.9.9

Pyscopg2-binary is utilised in the app for connecting the application to a local PostgreSQL database. Psycopg2 creates the route string which is passed to Flask that designates which socket the database will be hosted at and includes the app's PostgreSQL authentication for exchanges with the database including user name and password. Psycopg2 is responsible for actually sending the data, generated using SQLAlchemy, to the database.

### python-dotenv==1.0.1

Python-dotenv allows the application to access data stored in ".env" files. In this app, the JWT secret key value is stored in the env file so that it can remain hidden and generated locally when the app is cloned. It also stores the psycopg routing string to hide it from users.

## R4. Explain the benefits and drawbacks of this app’s underlying database system /6

This app uses a PostgreSQL (Postgres) database, connected via psycopg2 to store data in a relational manner. PostgreSQL is a robust, open-source database that is freely accessible on all major operating systems. This is a key benefit for this application as it means that users can initialise this API on their systems without assuming overhead costs altering their hardware or gaining access to the prescribed database software.

In addition, when choosing a database for this application, PostgreSQL is a favourable choice due to its prominence in back-end development. Flask, SQLAlchemy and psycopg2 are highly developed packages which work seamlessly with Postgres databases. These packages were key to the app's development. To initialise this API, users simply have to install the app's dependencies, create a PostgreSQL database, link it to the app and run Flask. The default install of Postgres contains all neccessary features required.

PostgreSQL is also ACID (Atomicity, Consistency, Isolation, Durability) compliant meaning that connection errors will not corrupt the database records as they existed (PostgreSQL Documentation, n.d.). ACID compliance is key for APIs where users may lose connectivity with the database due to servers failing.

One drawback of using PostgreSQL for this app's database is that Postgres databases cannot be stored on the cloud. Postgres does not contain functionality to host databases on the cloud and, instead, a service such as Google's "Cloud SQL" by would be required for online storage. Notably, these services can mirror the functionality of a local Postgres database and could be utilised without much configuration required if the app's database needed to be stored remotely (Google Cloud, 2024).

Another main drawback of Postgres is its speed and resource intensiveness. If this app were adopted and scaled widely, it would require a relatively powerful server to host it with good performance. By extension, query speeds will likely be slower than if the app were built on, key competitor, MySQL, a persistent critique of Postgres (Amazon Web Services, 2024).

Notably, using an ORM mitigates some of the traditional drawbacks of Postgres such as its strict semantics and difficult syntax. This app's endpoints and error handling attempts to mitigate the confusing elements of querying and recording data to a Postgres database. Similarly, using the models and endpoints within this app may make it easier to migrate data if the database used needed to be moved, a typical challenge of Postgres (Hanlon et al., 2011).

### References

Amazon Web Services (2024) _[What is SQL?](https://aws.amazon.com/what-is/sql/)_, AWS website, accessed 29 June 2024.

Google Cloud (2024) _[Cloud SQL for PostgreSQL features](https://cloud.google.com/sql/docs/postgres/features)_, Google Cloud website, accessed 29 June 2024.

Hanlon, M., Dooley, R., Mock, S., Dahan, M., Nuthulapati, P. & Hurley, P. (2011). _Benefits of NoSQL databases for portals & science gateways_. DOI:[10.1145/2016741.2016780](https://doi.org/10.1145/2016741.2016780).

PostgreSQL Documentation (n.d.) _[About](https://www.postgresql.org/about)_, PostgreSQL website, accessed 29 June 2024.

## R5. Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app /6

Object relational models (ORMs) are software packages that ease the conversion of code from one coding language into another language to interact with a relational database. In this application, SQLAlchemy is used to convert Python code to SQL for interaction with a PostgreSQL database. Using SQLAlchemy classes, the app contains models to create Pythonic objects that mirror entities stored in a connected relational database. This allows for object-oriented programming on the Pythonic side (Abba, 2022). Returned objects from the database are then interacted-with and sometimes altered, reformatted into SQL and sent for long-term storage in the connected database. Long-term storage is a particular advantage granted by ORMs and database storage as, otherwise, a Python application may not be able to preserve state between the app being started, closed and reopened (GeeksforGeeks, 2024).

The app uses SQLAlchemy's provided classes and methods to mirror the entities in a connected database. The following is an example of the "User" model built to interact with a "users" table in a connected relational database:

```Python
    class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(200))
    password: Mapped[Optional[str]] = mapped_column(String(200))
    first_name: Mapped[str] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")
    is_teacher: Mapped[bool] = mapped_column(Boolean(), server_default="false")

    children: Mapped[List["Child"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

```

Each model in the app uses an SQLAlchemy instance, "db", that contains SQLAlchemy's methods for converting Pythonic data structures to SQL formatting. The User class uses these to describe each attribute stored in the "users" table and its data quality. In the above model, id is an integer that represents the primary key for "user" instances, email, password and first_name are all strings with a maximum length of 200 and is_admin and is_teacher are boolean values. As seen above, the model can also describe default values so that, if the model is used to record an instance in the database and no value is provided for the attribute, the default is used. The attributes "children", "comments" and "contacts" all represent seperate entities that are linked with the "users" table via foreign key. The ORM associates these foreign tables with the "User" model so that joined results can be returned when the Python application communicates with the database.

Another key feature of the ORM is its ability to craft complex SQL queries using simple Pythonic code.

```Python
        stmt = db.select(User).where(User.id == request.json["user_id"])
        user = db.session.scalar(stmt)
```

The stmt variable uses SQLAlchemy's methods (called from the db object) to generate a query statement. The statement generates a query requesting each of the values noted in the "User" and specifies the condition that the "id" value must equal the "user_id" value passed in a request body. The generated statement is this:

```SQL
    SELECT users.id, users.email, users.password, users.first_name, users.is_admin, users.is_teacher 
    FROM users 
    WHERE users.id = :id_1
```

This statement is then passed to the database using the db.session.scalar() method which returns any matched instances as a scalar object. These scalars can then be interacted with in the application.

Vitally, ORMs allow for simplified interaction between distinct coding languages such as Python and SQL. In this application, SQLAlchemy facilitates the conversion of Python data structures to SQL formatted code and objects. Without an ORM, the app would require its own unique code for mirroring the data structures in the connection database for any communication between the software. In addition, the ORMs robust structure and formatting provides some security measures as the SQL statement generation is abstracted away from the app's modules (GeeksforGeeks, 2024).

### References

Abba, I. V. (2022) _[What is an ORM – The Meaning of Object Relational Mapping Database Tools](https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/)_, FreeCodeCamp website, accessed 29 June 2024.

GeeksforGeeks (2024) _[What is Object-Relational Mapping (ORM) in DBMS?](https://www.geeksforgeeks.org/what-is-object-relational-mapping-orm-in-dbms/)_, GeeksforGeeks website, accessed 29 June 2024.

## R6. Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design /12

### This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase

![ERD Diagram](docs/API-ERD-V1.0.png)
The ERD Diagram for this API, created using Crow's Foot Notation (Abba, 2022). The entities recorded in the API's database are Users, Children, Comments, Teachers, Contacts, Groups and Attendances.

![Updated ERD Diagram](docs/API-ERD-V1.1.png)
Updated diagram to include "comment_edited" and "date_edited" value.

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

## R7. Explain the implemented models and their relationships, including how the relationships aid the database implementation

### This should focus on the database implementation AFTER coding has begun, eg. during the project development phase /6

* Provides a BRIEF description about the project’s models and their relationships, and includes BRIEF information about how the relationships of the models interact with other models, and includes information about the queries that could be used to access data using the models’ relationships and includes appropriate code examples supporting the descriptions.

User is the core model of this app and facilitates a user's interaction with the app. The user entity describes a unique account which has an email and password and carries an individual's privileges in the boolean values is_admin and is_teacher. These values are queried throughout the application to grant or bar access to instances that were not linked to the user's profile such as registered children or contacts. In addition, a user's id value is passed when registering a child, comment or contact instance as well for further privilege checks.

```Python
user_type = user_status(user_id)

if user_type == "Parent":
        stmt = db.select(Child).where(Child.user_id == user_id)
        registered_children = db.session.scalars(stmt).all()
        return ChildSchema(many=True).dump(registered_children)
```

In this code extract from the "get_children" function, the "user_status" function accepts the user's id value (as passed via their JWT) and returns a description of their user type and privileges. This is then referred to later to designate which SQL query is sent to the database. If the user is a "Parent", the database is queried for any child instances where the child's user_id value matches the requesting user's id. Any returned results are then returned to the user. Alternatively, when requesting a single child's data, if the child's user_id does not match the user's id, they are returned a 403 unauthorised HTTP error. Meanwhile, someone with a "True" is_admin value can access both. In other interactions, these values function differently. A parent can only post comments linked to their own registered children but a teacher account or admin can post comments linked to any child.

Child instances are the next most significant entity and provide foreign keys for comments and attendances. Comments take user_id and child_id as foreign keys to describe which child is being commented on and by who.

The user_id, child_id and comment models' relationship is leveraged when requesting a singular comment:

```Python
    stmt = db.select(Comment).where(Comment.child_id == id, Comment.comment_id == id2)
```

In this line, the database is queried for comments where the child_id value matches an id value submitted via the URI, essentially requesting a particular child's comments. The specific comment is then targeted via a URI input id2 which is compared to the comment's own primary key.

```Python
    comment_dict["user"]["id"] == user_id

```

Later in the same endpoint function, this line checks if the person who posted the returned comment is the user requesting the comment. If the user is not and admin, teacher or the user who posted the comment, the comment is not returned. These three models combine for specific and secure queries.

Users also register contacts who represent a child's point of contact for a particular day. Contacts take the a user_id foreign key which links a registered contact to a user. When a user attempts to interact with a contact, their id is compared to the user_id attribute of the contact.

The other models are the teacher and group entities which represent a teacher and their contact information and a class, it's name, teacher and meeting day respectively. When registering a group the admin user must provide a teacher id to link a teacher's name and their email to a group. This allows users to query to who their child's class' point of contact is.

All models contribute to the attendances entity which describes a child, which class they attend and who their contact is on that day. A join table, the attendance model links a child instance (including it's registering user), a group instance (including its respective teacher), and a contact (also linking its registering user). By querying an attendance, a teacher is able to find out who a child's contact is for the day, if they are an emergency contact, which group the child is attending and who the group's teacher is. At a different endpoint, a parent is able to query their registered child, see a list of their registered attendances and confirm who their contact is set as on each day.

## R8. Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint /6

* Identifies ALL of the application’s API endpoints, including (for each identified endpoint) the HTTP verb, route path, and any required body or header data, and includes examples of what each identified endpoint will return on success AND failure of that endpoint operation

* HTTP verb
* Path or route
* Any required body or header data
* Response

### Users

#### LOGIN User

* POST
* /users/login
* Required header: None
* Required body: email, password
* Successful response: {"token": token_value}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401
    4. {"Error": "Incorrect email or password"}, 401

![Successful user login](docs/endpoint-ss/1-login-user-success.png)
A successful POST login request.

![Unsuccessful user login](docs/endpoint-ss/1-login-user-unsuccess.png)
An unsuccessful POST login request.

#### GET Users

* GET
* /users
* Required header: authorised JWT, user must be an admin
* Required body: None
* Successful response: {["users": user_data]}, 200 - a list of all users and their data including registered children, contacts and attendances
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful users request](docs/endpoint-ss/2-get-users-success.png)
A successful GET users request.

![Unsuccessful users request](docs/endpoint-ss/2-get-users-unsuccess.png)
An unsuccessful GET users request.

#### GET User

* GET
* /users/int
* Required header: authorised JWT, user must be an admin or the user id must match the JWT id
* Required body: None
* Successful response: {user attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET user](docs/endpoint-ss/2a-get-user-success.png)
A successful GET user request.

![Unsuccessful GET user](docs/endpoint-ss/2a-get-user-success.png)
An unsuccessful GET user request.

#### CREATE User as Admin

* POST
* /users/admin
* Required header: authorised JWT, user must be an admin
* Required body: first_name, email, password, is_admin boolean, is_teacher boolean
* Successful response: {"Success": registered user data}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Email already registered. Please provide a unique email address"}, 400
    3. {"Error": "Request is missing field: 'field_name'"}, 400
    4. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    5. {"Error": "first_name: ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces]"}, 400
    6. {"msg": "Token has expired}, 401

![Successful admin user post](docs/endpoint-ss/3-post-users-admin-success.png)
A successful admin POST user request.

![Unsuccessful admin user post](docs/endpoint-ss/3-post-users-admin-unsuccess.png)
An unsuccessful admin POST user request.

#### CREATE User without authorisation

* POST
* /users
* Required header: None
* Required body: first_name, email
* Successful response: {"Success": registered user data, fields submitted}, 200
* Unsuccessful responses:
    1. {"Error": "Email already registered. Please provide a unique email address"}, 400
    2. {"Error": "Request is missing field: 'field_name'"}, 400
    3. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    4. {"Error": "first_name: ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces]"}, 400
    5. {"msg": "Token has expired}, 401

![Successful unauthorised user post](docs/endpoint-ss/4-post-user-success.png)
A successful unauthorised POST user request.

![Unsuccessful unauthorised user post](docs/endpoint-ss/4-post-user-unsuccess.png)
An unsuccessful unauthorised POST user request.

#### PATCH User

* PATCH
* /users/int
* Required header: authorised JWT, user must be an admin or the user id must match the JWT id
* Required body: one of first_name, email or password. If admin is_admin boolean, is_teacher boolean optional
* Successful response: {"Updated fields": { attribute: updated_value}}, 200
  * if password updated: "password": "Password successfully updated"
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Email already registered. Please provide a unique email address"}, 400
    3. {"Error": "Please provide at least one value to update"}, 400
    4. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    5. {"Error": "No resource found"}, 404
    6. {"msg": "Token has expired}, 401

![Successful user PATCH](docs/endpoint-ss/5-patch-user-success.png)
A successful user PATCH request.

![Unsuccessful user PATCH](docs/endpoint-ss/5-patch-user-unsuccess.png)
An usuccessful user PATCH request.

#### DELETE User

* DELETE
* /users/int
* Required header: authorised JWT, user must be an admin
* Required body: None
* Successful response: {"Success": "User registration deleted"}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful DELETE user](docs/endpoint-ss/6-delete-user-success.png)
A successful DELETE user request.

![Unsuccessful DELETE user](docs/endpoint-ss/6-delete-user-unsuccess.png)
An unsuccessful DELETE user request.

### Children

#### GET Children

* GET
* /children
* Required header: authorised JWT
* Required body: None
* Successful response: {[{child: child_data}, {child2: child2_data}]}, 200 - if the user is an admin, all child instances returned, if the user is a parent, only children whose user_id equals the JWT id are returned.
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful children request](docs/endpoint-ss/7-get-children-success.png)
A successful GET children request.

![Unsuccessful children request](docs/endpoint-ss/7-get-children-unsuccess.png)
An unsuccessful GET children request.

#### GET Child

* GET
* /children/int
* Required header: authorised JWT, user must be an admin or the child's user_id must match the JWT id
* Required body: None
* Successful response: {child attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET user](docs/endpoint-ss/8-get-child-success.png)
A successful GET child request.

![Unsuccessful GET user](docs/endpoint-ss/8-get-child-unsuccess.png)
An unsuccessful GET child request.

#### POST Child

* POST
* /children
* Required header: authorised JWT, user must be an admin or a parent
* Required body: "first_name", "last_name". If admin, a user_id must be provided. If parent, user_id is automatically set to JWT id value
* Successful response: {"Success": registered child data}, 201
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "This child is already registered to this user"}, 400
    3. {"Error": "Request is missing field: 'field_name'"}, 400
    4. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    5. {"Error": "first/last_name: ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces]"}, 400
    6. {"msg": "Token has expired}, 401

![Successful admin child post](docs/endpoint-ss/9-post-child-success.png)
A successful admin POST child request.

![Unsuccessful admin child post](docs/endpoint-ss/9-post-child-unsuccess.png)
An unsuccessful admin POST child request.

#### PATCH Child

* PATCH
* /children/int
* Required header: authorised JWT, user must be an admin or the child's user_id must match the JWT id
* Required body: one of first_name or last_name.
* Successful response: {"Updated fields": { attribute: updated_value}}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Please provide at least one value to update"}, 400
    3. {"Error": "first/last_name: ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces]"}, 400
    4. {"Error": "No resource found"}, 404
    5. {"msg": "Token has expired}, 401

![Successful child PATCH](docs/endpoint-ss/10-patch-child-success.png)
A successful child PATCH request.

![Unsuccessful child PATCH](docs/endpoint-ss/10-patch-child-unsuccess.png)
An unsuccessful child PATCH request.

#### DELETE Child

* DELETE
* /children/int
* Required header: authorised JWT, user must be an admin
* Required body: None
* Successful response: {"Success": "Child registration deleted"}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful DELETE child](docs/endpoint-ss/11-delete-child-success.png)
A successful DELETE child request.

![Unsuccessful DELETE child](docs/endpoint-ss/11-delete-child-unsuccess.png)
An unsuccessful DELETE child request.

### Comments

#### GET Comments

* GET
* /children/int/comments
* Required header: authorised JWT, user must be an admin or teacher or child user_id must match JWT id
* Required body: None
* Successful response: [{child_attributes: values, comments: [{comment_attributes : attribute_values}]}], 200 - a child and a list of all their comments and their data
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET child's comments request](docs/endpoint-ss/12-get-child-comments-success.png)
A successful GET child's comments request.

![Unsuccessful GET child's comments request](docs/endpoint-ss/12-get-child-comments-unsuccess.png)
An unsuccessful GET child's comments request.

#### GET Comment

* GET
* /children/int/comments/int
* Required header: authorised JWT, user must be an admin or the child's user_id must match the JWT id
* Required body: None
* Successful response: {comment_attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET comment](docs/endpoint-ss/13-get-child-comment-success.png)
A successful GET comment request.

![Unsuccessful GET comment](docs/endpoint-ss/13-get-child-comment-unsuccess.png)
An unsuccessful GET comment request.

#### POST Comment

* POST
* /children/id/comments
* Required header: authorised JWT, user must be an admin or teacher or child user_id must match JWT id
* Required body: "message", "urgency", "child_id" is passed in URI
* Successful response: {"Success": registered comment data}, 201
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Request is missing field: 'field_name'"}, 400
    3. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    4. {"Error": "message": ["Comments need to be at least 3 characters long"]}, 400
    5. {"msg": "Token has expired}, 401

![Successful comment post](docs/endpoint-ss/14-post-child-comment-success.png)
A successful POST comment request.

![Unsuccessful comment post](docs/endpoint-ss/14-post-child-comment-unsuccess.png)
An unsuccessful POST comment request.

#### PATCH Comment

* PATCH
* /children/int/comments/int
* Required header: authorised JWT, user's JWT -d must match comment's user_id
* Required body: one of "message" or "urgency".
* Successful response: {comment_attributes: comment_fields}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Please provide at least one value to update"}, 400
    3. {"Error": "urgency: ["Must be one of urgent, positive, neutral."]}, 400
    4. {"Error": "No resource found"}, 404
    5. {"msg": "Token has expired}, 401

![Successful comment PATCH](docs/endpoint-ss/15-patch-comment-success.png)
A successful comment PATCH request.

![Unsuccessful comment PATCH](docs/endpoint-ss/15-patch-comment-unsuccess.png)
An unsuccessful comment PATCH request.

#### DELETE Comment

* DELETE
* /children/int/comments/int
* Required header: authorised JWT, user must be an admin or comment user_id must match JWT id
* Required body: None
* Successful response: {"Success": "Comment deleted"}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful DELETE comment](docs/endpoint-ss/16-delete-comment-success.png)
A successful DELETE comment request.

![Unsuccessful DELETE comment](docs/endpoint-ss/11-delete-comment-unsuccess.png)
An unsuccessful DELETE comment request.

### Attendances

#### GET Attendances

* GET
* /children/int/attendances
* Required header: authorised JWT, user must be an admin or teacher or child user_id must match JWT id
* Required body: None
* Successful response: [{attendance_attributes: values}], 200 - a list containing all of a child's attendances and their attributes
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET child's attendances request](docs/endpoint-ss/17-get-attendances-success.png)
A successful GET child's attendances request.

![Unsuccessful GET child's attendances request](docs/endpoint-ss/17-get-attendances-unsuccess.png)
An unsuccessful GET child's attendances request.

#### GET Attendance

* GET
* /children/int/attendances/int
* Required header: authorised JWT, user must be an admin or teacher or child user_id must match JWT id
* Required body: None
* Successful response: {attendance_attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET attendance](docs/endpoint-ss/18-get-attendance-success.png)
A successful GET attendance request.

![Unsuccessful GET attendance](docs/endpoint-ss/18-get-attendance-unsuccess.png)
An unsuccessful GET attendance request.

#### CREATE Attendance

* POST
* /children/id/attendances
* Required header: authorised JWT, user must be an admin or child user_id must match JWT id
* Required body: "group_id", "contact_id", "child_id" is passed in URI
* Successful response: {"Success": registered comment data}, 201
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    3. {"Error": "Please enter a contact_id registered to your account"}, 400
    4. {"msg": "Token has expired}, 401
    5. {"Error": "Child attendance is already registered for that group"}, 400
    6. {"Error": "One of the provided values does not exist. Please ensure both values in the request body are accurate"}, 400

![Successful attendance post](docs/endpoint-ss/19-post-attendance-success.png)
A successful POST attendance request.

![Unsuccessful attendance post](docs/endpoint-ss/19-post-attendance-unsuccess.png)
An unsuccessful POST attendance request.

#### PATCH Attendance

* PATCH
* /children/int/attendances/int
* Required header: authorised JWT, user must be an admin or child user_id must match JWT id
* Required body: one of "group_id" or "contact_id".
* Successful response: {attendance_attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Please provide at least one value to update"}, 400
    3. {"Error": "No resource found"}, 404
    4. {"msg": "Token has expired}, 401
    5. {"Error": "One of the provided values does not exist. Please ensure both values in the request body are accurate"}, 400

![Successful attendance PATCH](docs/endpoint-ss/20-patch-attendance-success.png)
A successful attendance PATCH request.

![Unsuccessful attendance PATCH](docs/endpoint-ss/20-patch-attendance-unsuccess.png)
An unsuccessful attendance PATCH request.

DELETE Attendance

#### DELETE Attendance

* DELETE
* /children/int/attendances/int
* Required header: authorised JWT, user must be an admin or child user_id must match JWT id
* Required body: None
* Successful response: {"Success": "Attendance deleted"}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful DELETE comment](docs/endpoint-ss/21-delete-attendance-success.png)
A successful DELETE attendance request.

![Unsuccessful DELETE attendance](docs/endpoint-ss/21-delete-attendance-unsuccess.png)
An unsuccessful DELETE attendance request.

### Teachers

#### GET Teachers

* GET
* /teachers
* Required header: authorised JWT, user must be an admin
* Required body: None
* Successful response: [{teacher_attributes: values}], 200 - a list containing all teacher instances and their attributes
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"msg": "Token has expired}, 401

![Successful teachers request](docs/endpoint-ss/22-get-teachers-success.png)
A successful GET teachers request.

![Unsuccessful teachers request](docs/endpoint-ss/22-get-teachers-unsuccess.png)
An unsuccessful GET teachers request.

#### GET Teacher

* GET
* /teachers/int
* Required header: authorised JWT, user must be an admin
* Required body: None
* Successful response: {teacher_attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET teacher](docs/endpoint-ss/23-get-teacher-success.png)
A successful GET teacher request.

![Unsuccessful GET teacher](docs/endpoint-ss/23-get-teacher-unsuccess.png)
An unsuccessful GET teacher request.

#### POST Teacher

* POST
* /teachers
* Required header: authorised JWT, user must be an admin
* Required body: "first_name" and "email" values
* Successful response: {"Success": {teacher_attributes: values}}, 201
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "A teacher is already registered with this email"}, 400
    3. {"Error": "Request is missing field: 'field_name'"}, 400
    4. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    5. {"Error": "first_name": ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces"]}, 400
    6. {"msg": "Token has expired}, 401

![Successful teacher post](docs/endpoint-ss/24-post-teacher-success.png)
A successful teacher POST request.

![Unsuccessful teacher post](docs/endpoint-ss/24-post-teacher-unsuccess.png)
An unsuccessful teacher POST request.

#### PATCH Teacher

* PATCH
* /teachers/int
* Required header: authorised JWT, user must be an admin
* Required body: one of "first_name" or "email".
* Successful response: {"Updated fields": { attribute: updated_value}}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Please provide at least one value to update"}, 400
    3. {"Error": "first/last_name: ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces]"}, 400
    4. {"Error": "No resource found"}, 404
    5. {"msg": "Token has expired}, 401
    6. {"Error": "A teacher is already registered with this email"}, 400

![Successful teacher PATCH](docs/endpoint-ss/25-patch-teacher-success.png)
A successful teacher PATCH request.

![Unsuccessful teacher PATCH](docs/endpoint-ss/25-patch-teacher-unsuccess.png)
An unsuccessful teacher PATCH request.

#### DELETE Teacher

* DELETE
* /teachers/int
* Required header: authorised JWT, user must be an admin
* Required body: None
* Successful response: {"Success": "Teacher registration deleted"}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful DELETE teacher](docs/endpoint-ss/26-delete-teacher-success.png)
A successful DELETE child request.

![Unsuccessful DELETE teacher](docs/endpoint-ss/26-delete-teacher-unsuccess.png)
An unsuccessful DELETE teacher request.

### Groups

#### GET Groups

* GET
* /groups
* Required header: authorised JWT
* Required body: None
* Successful response: [{group_attributes: values}], 200 - a list containing all group instances and their attributes
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"msg": "Token has expired}, 401

![Successful GET groups request](docs/endpoint-ss/27-get-groups-success.png)
A successful GET groups request.

![Unsuccessful GET groups request](docs/endpoint-ss/27-get-groups-unsuccess.png)
An unsuccessful GET groups request.

#### GET Group

* GET
* /groups/int
* Required header: authorised JWT
* Required body: None
* Successful response: {group_attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET group](docs/endpoint-ss/28-get-group-success.png)
A successful GET group request.

![Unsuccessful GET group](docs/endpoint-ss/23-get-group-unsuccess.png)
An unsuccessful GET group request.

#### POST Group

* POST
* /teachers
* Required header: authorised JWT, user must be an admin
* Required body: "group_name", "day" and "teacher_id" values
* Successful response: {"Success": {group_attributes: values}}, 201
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "A group is already registered with this name and day"}, 400
    3. {"Error": "Request is missing field: 'field_name'"}, 400
    4. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    5. {"Error": "group_name": ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces"]}, 400
    6. {"Error": "day": ["Must be one of: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."]}, 400
    7. {"msg": "Token has expired}, 401

![Successful group post](docs/endpoint-ss/29-post-post-success.png)
A successful group POST request.

![Unsuccessful group post](docs/endpoint-ss/29-post-group-unsuccess.png)
An unsuccessful group POST request.

#### PATCH Group

* PATCH
* /groups/int
* Required header: authorised JWT, user must be an admin
* Required body: one of "group_name", "day" and "teacher_id" values
* Successful response: {"Updated fields": { attribute: updated_value}}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "Please provide at least one value to update"}, 400
    3. {"Error": "A group is already registered with this name and day"}, 400
    4. {"Error": "group_name": ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces"]}, 400
    5. {"Error": "day": ["Must be one of: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."]}, 400
    6. {"Error": "No resource found"}, 404
    7. {"msg": "Token has expired}, 401

![Successful group PATCH](docs/endpoint-ss/30-patch-group-success.png)
A successful group PATCH request.

![Unsuccessful group PATCH](docs/endpoint-ss/30-patch-group-unsuccess.png)
An unsuccessful group PATCH request.

#### DELETE Group

* DELETE
* /teachers/int
* Required header: authorised JWT, user must be an admin
* Required body: None
* Successful response: {"Success": "Group registration deleted"}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401
* NOTE: Deleting a teacher will delete any linked groups. Please update groups linked to a teacher before deleting a teacher if you want to preserve attendances and groups.

![Successful DELETE group](docs/endpoint-ss/31-delete-group-success.png)
A successful DELETE group request.

![Unsuccessful DELETE group](docs/endpoint-ss/31-delete-group-unsuccess.png)
An unsuccessful DELETE group request.

### Contacts

#### GET Contacts

* GET
* /contacts
* Required header: authorised JWT, user must be a parent or admin
* Required body: None
* Successful response: [{contact_attributes: values}], 200 - if the user is a parent, a list containing all contacts with a user_id value matching the JWT id, if the user is an admin, all registered contacts are returned
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"msg": "Token has expired}, 401

![Successful GET contacts request](docs/endpoint-ss/32-get-contacts-success.png)
A successful GET contacts request.

![Unsuccessful GET contacts request](docs/endpoint-ss/32-get-contacts-unsuccess.png)
An unsuccessful GET contacts request.

#### GET Contact

* GET
* /contacts/int
* Required header: authorised JWT, user must be an admin or the contact's user_id must match the JWT id
* Required body: None
* Successful response: {contact attributes: values}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful GET group](docs/endpoint-ss/33-get-contact-success.png)
A successful GET contact request.

![Unsuccessful GET contact](docs/endpoint-ss/33-get-contact-unsuccess.png)
An unsuccessful GET contact request.

#### POST Contact

* POST
* /contacts
* Required header: authorised JWT, user must be an admin or a parent
* Required body: "first_name", "emergency_contact", "ph_number". "email" value is optional. If admin, a user_id must be provided. If parent, user_id is automatically set to JWT id value
* Successful response: {"Success": registered contact}, 201
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "A contact is already registered with this phone number"}, 400
    3. {"Error": "Request is missing field: 'field_name'"}, 400
    4. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    5. {"Error": "first_name: ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces]"}, 400
    6. {"Error": {"ph_number": ["Phone numbers must be 10 characters"]}}, 400
    7. {"msg": "Token has expired}, 401

![Successful contact post](docs/endpoint-ss/34-post-contact-success.png)
A successful POST contact request.

![Unsuccessful contact post](docs/endpoint-ss/34-post-contact-unsuccess.png)
An unsuccessful POST contact request.

#### PATCH Contact

* PATCH
* /contacts/int
* Required header: authorised JWT, user must be an admin or the contact's user_id must match the JWT id
* Required body: one of "first_name", "emergency_contact", "ph_number" or "email".
* Successful response: {"Updated fields": { attribute: updated_value}}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "A contact is already registered with this phone number"}, 400
    3. {"Error": "Request is missing field: 'field_name'"}, 400
    4. {"Error": "attribute: ["Not a valid attribute_name]"}, 400
    5. {"Error": "first_name: ["Names must not contain numbers or special characters besides hyphens, apostrophes and spaces]"}, 400
    6. {"Error": {"ph_number": ["Phone numbers must be 10 characters"]}}, 400
    7. {"msg": "Token has expired}, 401
    8. {"Error": "Please provide at least one value to update"}, 400

![Successful contact PATCH](docs/endpoint-ss/35-patch-contact-success.png)
A successful contact PATCH request.

![Unsuccessful contact PATCH](docs/endpoint-ss/35-patch-contact-unsuccess.png)
An unsuccessful contact PATCH request.

#### DELETE Contact

* DELETE
* /contacts/int
* Required header: authorised JWT, user must be an admin or contact's "user_id" must match JWT id
* Required body: None
* Successful response: {"Success": "Contact registration deleted"}, 200
* Unsuccessful responses:
    1. {"Error": "You are not authorised to access this resource"}, 403
    2. {"Error": "No resource found"}, 404
    3. {"msg": "Token has expired}, 401

![Successful DELETE contact](docs/endpoint-ss/36-delete-contact-success.png)
A successful DELETE contact request.

![Unsuccessful DELETE contact](docs/endpoint-ss/36-delete-contact-unsuccess.png)
An unsuccessful DELETE contact request.

## Additional Notes

Code comment is formatted according to the Pep 8 style guide and Pep 257 docstring conventions.

### References

Coghlan, A., Rossum, G. v., Warsaw, B.  (2013) _[PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)_, Python.org website, accessed 29 June 2024.

Goodger, D. Rossum, G. v.  (2001) _[PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)_, Python.org website, accessed 29 June 2024.
