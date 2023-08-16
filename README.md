# ams_proj_1

AMS Project 1 for QA

## Installation

This is assuming you have a MySQL database located conforming to this URI: mysql+pymysql://root:@localhost:3306/flask_test

If you do not have this, you can change the URI in the __init__.py file to match your database.

```bash
git clone https://github.com/jamesbryer/ams_proj_1.git
cd ams_proj_1
pip3 install -r requirements.txt
python3 create.py
python3 app.py

```

## Project Requirements

### 1. Pages

#### 1.1 The MVP (minimum viable product) describes the requirement for these pages

- Home page
- Product Listing page
- Category page
- Cart page
- Checkout page
- Payment page
- Contact Us page
- About Us page

#### 1.2 The MVP also describes the requirement for these compments

- A kanban board detailing the tasks for the project
- A git repository

### 2. User Stories

#### Using the MVP as my guide, I devised the following user stories

- As a user, I can see a list of products with their image, price, and description on the products page
- As a user, I can click on a product to see more information about it
- As a user, I can see products separated by category
- As a user, I can see a description of the system on the home page
- As a user, I can add products to a cart
- As a user, I can see the products in my cart
- As a user, I can remove products from my cart
- As a user, I can update the quanitity of products in my cart
- As a user, I can see the total price of the products in my cart
- As a user, I can navigate between pages easily
- As a user, I can see a contact us page
- As a user, I can see an about us page
- As a user, I can see a checkout page and add my delivery address via this page
- As a user, I can see a payment page and add my payment details via this page
- As a user, I can see a confirmation page and see a summary of my order
- As a user, I can see my order history with a description of the order
- As a user, I can place an order

### 3. Acceptance Criteria

#### Using the user stories as my guide, I devised the following acceptance criteria

- The products page should show a list of products with their image, price, and description
- The products page should have a link to the product page
- The product page should show the product's image, price, and description
- The product page should have a link to the products page
- The products page should show products separated by category
- The home page should show a description of the system
- The cart page should show the products in the cart
- The cart page should show the total price of the products in the cart
- The cart page should have a link to the products page
- The cart page should have a link to the checkout page
- The checkout page should show the delivery address form
- The checkout page should have a link to the cart page
- The checkout page should have a link to the payment page
- The payment page should show the payment details form
- The payment page should have a link to the checkout page
- The payment page should have a link to the confirmation page
- The confirmation page should show a summary of the order
- The confirmation page should have a link to the products page
- The confirmation page should have a link to the order history page
- The order history page should show a list of orders with a description of the order

### 4. Database Design

#### I devised the following database design, using the principals of relational databases and normalisation

![Database Design](/application/static/images/database_design.png)

### 5. Development Methodology

#### Scrum

While this is an individual project, so scrum is not technically necessary (or strictly possible), I decided to use scrum as my development methodology. I did this due to its iterative nature, which I felt would be useful for this project. I also felt that it would be useful to practice using scrum in a project, as it is important to be able to use it in a team environment.

#### Kanban Board

I used a kanban board via Jira to track my progress through the project. I used the MVP as a guide for the tasks I needed to complete, and I added tasks as I went along. I also used the kanban board to track my progress through the project, and I used it to keep track of what I needed to do next. Some of the difficulties I found were my development process didn't nessesarily fit into the scrum methodology, as I was working alone. I also found it difficult to estimate the time it would take to complete tasks, as I was very new to much of the technology (Flask in particular) having only learned it over the previous week. I also found it difficult tto analyse exactly which tasks to add in which sprint. As I am so new to Flask, I wasn't 100% sure the order in which to complete tasks, leading to a reevaluation of the tasks in each sprint.

#### Sprint Reports

Burnup Chart:
![Kanban Board](/application/static/images/jira_burnup.png)

Sprint 1:
During the first sprint, I planned the project and set up the Jira kanban board. I also designed the database and created the models to implement this. I generated the product backlog during this period, for each user-story. However, I found that I needed to be more granular with the issues on the board and so ended up changing my approach. I began implementation and got the product pages, the navbar, the cart, and the login system completed during this sprint.

Sprint 2:
During the second sprint, I continued the project by completing the checkout system and allowing a user to complete an order from start to finish. I also added some of the more static pages such as the about page and the home page content. I added the order history page, and the contact us page. I added the input validation on all forms to prevent errors occuring. Lastly, on the development side, I added the redirection from pages if the user shouldn't be able to access them, for example, if they are not logged in they cannot access the cart page and if their cart is empty they cannot access the checkout page. Lastly, I created the test suite to fully test the application. I have a test coverage of 95% and I am happy with the tests I have written, although a higher coverage would be ideal, a lot of the missed coverage is in areas that are difficult to test.

#### Test Coverage

Using Pytest and coverage I was able to pass all my tests and achieve a test coverage of 95%.

![Test Coverage](/application/static/images/test_coverage.png)
![Test Passing](/application/static/images/test_pass.png)

#### Git

I used git to track my progress through the project. I used branches to develop features and then merged them into the main branch when they were complete.

#### Jenkins

I implemented a Jenkings freestlye project linked to my GitHub repository which automatically tests and runs the application when run. Ideally, I would have liked to implement a webhook to automatically run the tests when a push is made to the repository, however, I was unable to do this due to my development on a local environment rather than a cloud environment.

![Jenkins](/application/static/images/jenkins_pass.png)
