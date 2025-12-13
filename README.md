A full-stack web application built using Django, Django REST Framework, SQLite, and a Bootstrap-based single-page frontend.
This project is developed as part of the TDD Kata: Sweet Shop Management System, focusing on Test-Driven Development, clean code, API development, and responsible AI usage.
1. Project Overview:-

The Sweet Shop Management System is a web application that allows users to:

# User Features:-

1. Register and log in using JWT authentication.

2. View all available sweets.

3. Search sweets by name, category, and price range.

4. Purchase sweets (quantity decreases automatically).

5. View updated stock in real-time.

# Technical Highlights:-

1. Fully developed using Test-Driven Development (TDD).

2. RESTful backend with secure JWT-based authentication.

3. Single frontend page using Bootstrap + vanilla JavaScript.

4. SQLite used as the database.

5. Clean, modular Django REST API architecture.

 # Project Structure
sweetshop/
│
├── backend/
│   ├── sweetshop/        # Django project
│   ├── api/              # App (models, views, serializers, tests)
│   ├── db.sqlite3
│   ├── requirements.txt
│
├── frontend/
│   ├── index.html        # Single-page UI
│   ├── script.js         # API logic (Fetch API)
│   ├── styles.css
│   └── screenshots/
│
└── README.md

# AI Tools Used:-
During the development of this Sweet Shop Management System, I used the following AI tools:

ChatGPT (OpenAI) – for coding guidance, architectural support, debugging help, and explanation of errors.

GitHub Copilot – for real-time code suggestions inside VS Code.
ChatGPT

I # used ChatGPT to:-

. Clarify concepts related to Django REST Framework and JWT authentication.

. Understand the best structure for models, serializers, and API endpoints.

. Generate boilerplate code such as initial serializers, views, and test templates.

. Get suggestions when I encountered issues or errors during implementation.

. Help draft the project README, especially the explanation and setup sections.

# GitHub Copilot:-

. I used GitHub Copilot to:

. Autocomplete repetitive code like CRUD methods, imports, and serializers.

. Suggest improvements while writing view logic and validation.

. Generate small utility functions and test case structures.

![image alt](https://github.com/Anish-Thakur291/Kata_sweet_shop/blob/74bc3e2a216e2c1caf203a6805ecf478f6e063e1/sweet01.png)

# A test report:-

Found 24 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
test_purchase_not_enough_stock (api.tests.PurchaseRestockTests.test_purchase_not_enough_stock) ... ok
test_purchase_success (api.tests.PurchaseRestockTests.test_purchase_success) ... ok
test_restock_admin_success (api.tests.PurchaseRestockTests.test_restock_admin_success) ... ok
test_restock_regular_user_forbidden (api.tests.PurchaseRestockTests.test_restock_regular_user_forbidden) ... ok
test_create_sweet_admin (api.tests.SweetAPITests.test_create_sweet_admin) ... ok
test_create_sweet_regular_user_forbidden (api.tests.SweetAPITests.test_create_sweet_regular_user_forbidden) ... ok
test_create_sweet_unauthenticated (api.tests.SweetAPITests.test_create_sweet_unauthenticated) ... ok
test_delete_sweet_admin_success (api.tests.SweetAPITests.test_delete_sweet_admin_success) ... ok
test_delete_sweet_regular_user_forbidden (api.tests.SweetAPITests.test_delete_sweet_regular_user_forbidden) ... ok
test_delete_sweet_unauthenticated (api.tests.SweetAPITests.test_delete_sweet_unauthenticated) ... ok
test_list_sweets_authenticated (api.tests.SweetAPITests.test_list_sweets_authenticated) ... ok
test_list_sweets_unauthenticated (api.tests.SweetAPITests.test_list_sweets_unauthenticated) ... ok
test_update_sweet_admin (api.tests.SweetAPITests.test_update_sweet_admin) ... ok
test_update_sweet_regular_user_forbidden (api.tests.SweetAPITests.test_update_sweet_regular_user_forbidden) ... ok
test_update_sweet_unauthenticated (api.tests.SweetAPITests.test_update_sweet_unauthenticated) ... ok
test_sweet_creation (api.tests.SweetModelTests.test_sweet_creation) ... ok
test_search_by_category (api.tests.SweetSearchTests.test_search_by_category) ... ok
test_search_by_name (api.tests.SweetSearchTests.test_search_by_name) ... ok
test_search_by_price_range (api.tests.SweetSearchTests.test_search_by_price_range) ... ok
test_user_login_invalid_credentials (api.tests.UserAuthTests.test_user_login_invalid_credentials) ... ok
test_user_login_success (api.tests.UserAuthTests.test_user_login_success) ... ok
test_user_registration_password_mismatch (api.tests.UserAuthTests.test_user_registration_password_mismatch) ... ok
test_user_registration_short_password (api.tests.UserAuthTests.test_user_registration_short_password) ... ok
test_user_registration_success (api.tests.UserAuthTests.test_user_registration_success) ... ok

----------------------------------------------------------------------
Ran 24 tests in 12.858s

OK


  #  Conclusion:-

The Sweet Shop Management System demonstrates a complete full-stack application built using modern web technologies and industry best practices. By combining Django REST Framework for a secure and scalable backend with a Bootstrap-powered single-page UI, this project provides a smooth and responsive user experience for both regular users and administrators.

Throughout the development process, I followed the principles of Test-Driven Development (TDD), ensuring that each feature was validated through meaningful test cases before implementation. This approach improved the reliability, maintainability, and clarity of the codebase.

The project also reflects a responsible and transparent use of AI tools. While AI offered guidance, support, and productivity improvements, all design decisions, integration logic, and final implementations were reviewed, tested, and refined by me.

Overall, this project not only fulfills the requirements of the kata but also strengthened my skills in backend API development, authentication, frontend integration, testing, and clean coding practices. It stands as a complete demonstration of my ability to design, build, test, and document a production-ready full-stack web application.
