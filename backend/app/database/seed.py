"""Seed data for the learning path database — skills, resources, assessments, and demo user."""
from ..models.models import Skill, Resource, Assessment, User, UserInterest, UserSkill, LearningGoal


def get_skills():
    return [
        # Data Science / ML
        Skill(name="Python", domain="Programming", description="General-purpose programming language"),
        Skill(name="SQL", domain="Data", description="Structured Query Language for databases"),
        Skill(name="Statistics", domain="Data Science", description="Descriptive and inferential statistics"),
        Skill(name="Probability", domain="Data Science", description="Probability theory and distributions"),
        Skill(name="NumPy", domain="Data Science", description="Numerical computing with Python"),
        Skill(name="Pandas", domain="Data Science", description="Data manipulation and analysis"),
        Skill(name="Data Visualization", domain="Data Science", description="Creating charts and graphs"),
        Skill(name="Machine Learning", domain="AI/ML", description="ML algorithms and techniques"),
        Skill(name="Deep Learning", domain="AI/ML", description="Neural networks and deep learning"),
        Skill(name="NLP", domain="AI/ML", description="Natural Language Processing"),
        Skill(name="Data Cleaning", domain="Data Science", description="Cleaning and preprocessing data"),
        # Web Development
        Skill(name="HTML", domain="Web Development", description="HyperText Markup Language"),
        Skill(name="CSS", domain="Web Development", description="Cascading Style Sheets"),
        Skill(name="JavaScript", domain="Web Development", description="Web programming language"),
        Skill(name="React", domain="Web Development", description="Frontend JavaScript library"),
        Skill(name="Node.js", domain="Web Development", description="Server-side JavaScript runtime"),
        Skill(name="REST APIs", domain="Web Development", description="RESTful API design and consumption"),
        Skill(name="TypeScript", domain="Web Development", description="Typed superset of JavaScript"),
        # General
        Skill(name="Git", domain="Tools", description="Version control system"),
        Skill(name="Docker", domain="DevOps", description="Containerization platform"),
        Skill(name="Linux", domain="Tools", description="Linux operating system"),
        Skill(name="Cloud Computing", domain="Cloud", description="AWS/GCP/Azure fundamentals"),
        Skill(name="Cybersecurity", domain="Security", description="Information security fundamentals"),
        Skill(name="Algorithms", domain="Computer Science", description="Algorithms and data structures"),
        Skill(name="Testing", domain="Software Engineering", description="Software testing and QA"),
        Skill(name="Deployment", domain="DevOps", description="Application deployment"),
        Skill(name="UI/UX Design", domain="Design", description="User interface and experience design"),
        Skill(name="Agile", domain="Project Management", description="Agile methodologies"),
        Skill(name="Java", domain="Programming", description="Object-oriented programming language"),
        Skill(name="C++", domain="Programming", description="Systems programming language"),
    ]


def get_resources():
    return [
        # ── Python ──────────────────────────────────────────
        Resource(
            title="Python Fundamentals",
            description="Learn Python from scratch — variables, data types, control flow, functions, and basic OOP.",
            domain="Programming", skill="Python", difficulty="beginner",
            estimated_hours=15, type="course",
            prerequisites=[], url="https://docs.python.org/3/tutorial/",
            rating=4.8, tags=["python", "beginner", "fundamentals"]
        ),
        Resource(
            title="Intermediate Python",
            description="Decorators, generators, context managers, error handling, and modules.",
            domain="Programming", skill="Python", difficulty="intermediate",
            estimated_hours=12, type="course",
            prerequisites=["Python Fundamentals"], url="https://realpython.com/",
            rating=4.7, tags=["python", "intermediate"]
        ),
        Resource(
            title="Python for Data Science",
            description="Using Python specifically for data science tasks — file I/O, string processing, regular expressions.",
            domain="Data Science", skill="Python", difficulty="intermediate",
            estimated_hours=10, type="course",
            prerequisites=["Python Fundamentals"], url="https://www.kaggle.com/learn/python",
            rating=4.6, tags=["python", "data science"]
        ),
        Resource(
            title="Python Coding Challenges",
            description="50 practice problems to solidify your Python skills.",
            domain="Programming", skill="Python", difficulty="beginner",
            estimated_hours=8, type="project",
            prerequisites=["Python Fundamentals"], url="https://www.hackerrank.com/domains/python",
            rating=4.5, tags=["python", "practice", "project"]
        ),

        # ── SQL ─────────────────────────────────────────────
        Resource(
            title="SQL Fundamentals",
            description="SELECT, WHERE, JOIN, GROUP BY, subqueries, and database design basics.",
            domain="Data", skill="SQL", difficulty="beginner",
            estimated_hours=10, type="course",
            prerequisites=[], url="https://www.w3schools.com/sql/",
            rating=4.6, tags=["sql", "database", "beginner"]
        ),
        Resource(
            title="Advanced SQL Queries",
            description="Window functions, CTEs, optimization, and complex joins.",
            domain="Data", skill="SQL", difficulty="intermediate",
            estimated_hours=8, type="course",
            prerequisites=["SQL Fundamentals"], url="https://mode.com/sql-tutorial/",
            rating=4.5, tags=["sql", "advanced"]
        ),
        Resource(
            title="SQL Practice Problems",
            description="Real-world SQL query challenges on sample datasets.",
            domain="Data", skill="SQL", difficulty="beginner",
            estimated_hours=6, type="project",
            prerequisites=["SQL Fundamentals"], url="https://sqlzoo.net/",
            rating=4.4, tags=["sql", "practice"]
        ),

        # ── Statistics & Probability ────────────────────────
        Resource(
            title="Statistics for Data Science",
            description="Descriptive statistics, distributions, central tendency, variance, and correlation.",
            domain="Data Science", skill="Statistics", difficulty="beginner",
            estimated_hours=12, type="course",
            prerequisites=[], url="https://www.khanacademy.org/math/statistics-probability",
            rating=4.7, tags=["statistics", "data science"]
        ),
        Resource(
            title="Probability Fundamentals",
            description="Probability rules, Bayes' theorem, distributions, and expected values.",
            domain="Data Science", skill="Probability", difficulty="beginner",
            estimated_hours=10, type="course",
            prerequisites=["Statistics for Data Science"],
            url="https://www.khanacademy.org/math/statistics-probability",
            rating=4.6, tags=["probability", "math"]
        ),
        Resource(
            title="Hypothesis Testing & Inference",
            description="p-values, confidence intervals, t-tests, chi-squared tests, and A/B testing.",
            domain="Data Science", skill="Statistics", difficulty="intermediate",
            estimated_hours=8, type="course",
            prerequisites=["Statistics for Data Science", "Probability Fundamentals"],
            url="https://www.coursera.org/learn/inferential-statistics-intro",
            rating=4.5, tags=["statistics", "hypothesis testing"]
        ),

        # ── NumPy / Pandas / Data Cleaning ──────────────────
        Resource(
            title="NumPy Essentials",
            description="Arrays, broadcasting, linear algebra, and random number generation with NumPy.",
            domain="Data Science", skill="NumPy", difficulty="beginner",
            estimated_hours=6, type="course",
            prerequisites=["Python Fundamentals"],
            url="https://numpy.org/doc/stable/user/quickstart.html",
            rating=4.6, tags=["numpy", "python", "data science"]
        ),
        Resource(
            title="Pandas for Data Analysis",
            description="DataFrames, Series, indexing, groupby, merge, pivot tables, and time series.",
            domain="Data Science", skill="Pandas", difficulty="beginner",
            estimated_hours=10, type="course",
            prerequisites=["Python Fundamentals", "NumPy Essentials"],
            url="https://pandas.pydata.org/docs/getting_started/",
            rating=4.7, tags=["pandas", "data analysis"]
        ),
        Resource(
            title="Data Cleaning with Python",
            description="Handle missing values, outliers, duplicates, and data type conversions.",
            domain="Data Science", skill="Data Cleaning", difficulty="intermediate",
            estimated_hours=8, type="tutorial",
            prerequisites=["Pandas for Data Analysis"],
            url="https://www.kaggle.com/learn/data-cleaning",
            rating=4.5, tags=["data cleaning", "pandas"]
        ),
        Resource(
            title="Data Cleaning Mini-Project",
            description="Clean a messy real-world dataset end-to-end and prepare it for analysis.",
            domain="Data Science", skill="Data Cleaning", difficulty="intermediate",
            estimated_hours=5, type="project",
            prerequisites=["Data Cleaning with Python"],
            url="", rating=4.4, tags=["project", "data cleaning"]
        ),

        # ── Visualization ───────────────────────────────────
        Resource(
            title="Data Visualization with Matplotlib & Seaborn",
            description="Create bar charts, histograms, scatter plots, heatmaps, and more.",
            domain="Data Science", skill="Data Visualization", difficulty="beginner",
            estimated_hours=8, type="course",
            prerequisites=["Pandas for Data Analysis"],
            url="https://matplotlib.org/stable/tutorials/",
            rating=4.5, tags=["visualization", "matplotlib", "seaborn"]
        ),
        Resource(
            title="Exploratory Data Analysis Project",
            description="Perform a full EDA on a dataset — visualize distributions, correlations, and trends.",
            domain="Data Science", skill="Data Visualization", difficulty="intermediate",
            estimated_hours=10, type="project",
            prerequisites=["Data Visualization with Matplotlib & Seaborn", "Pandas for Data Analysis"],
            url="", rating=4.6, tags=["eda", "project"]
        ),

        # ── Machine Learning ────────────────────────────────
        Resource(
            title="Machine Learning Fundamentals",
            description="Supervised vs unsupervised learning, bias-variance tradeoff, model evaluation.",
            domain="AI/ML", skill="Machine Learning", difficulty="intermediate",
            estimated_hours=15, type="course",
            prerequisites=["Python Fundamentals", "NumPy Essentials", "Statistics for Data Science"],
            url="https://www.coursera.org/learn/machine-learning",
            rating=4.9, tags=["ml", "fundamentals"]
        ),
        Resource(
            title="Linear & Logistic Regression",
            description="Understand and implement regression models from scratch and with scikit-learn.",
            domain="AI/ML", skill="Machine Learning", difficulty="intermediate",
            estimated_hours=8, type="tutorial",
            prerequisites=["Machine Learning Fundamentals"],
            url="https://scikit-learn.org/stable/supervised_learning.html",
            rating=4.7, tags=["regression", "ml"]
        ),
        Resource(
            title="Classification Algorithms",
            description="Decision trees, random forests, SVM, KNN, and Naive Bayes.",
            domain="AI/ML", skill="Machine Learning", difficulty="intermediate",
            estimated_hours=10, type="course",
            prerequisites=["Machine Learning Fundamentals"],
            url="https://scikit-learn.org/stable/supervised_learning.html",
            rating=4.6, tags=["classification", "ml"]
        ),
        Resource(
            title="Model Evaluation & Tuning",
            description="Cross-validation, grid search, precision-recall, ROC curves, and feature selection.",
            domain="AI/ML", skill="Machine Learning", difficulty="intermediate",
            estimated_hours=6, type="tutorial",
            prerequisites=["Linear & Logistic Regression", "Classification Algorithms"],
            url="",
            rating=4.5, tags=["model evaluation", "tuning"]
        ),
        Resource(
            title="Customer Churn Prediction Project",
            description="Build an end-to-end ML model to predict customer churn using real-world data.",
            domain="AI/ML", skill="Machine Learning", difficulty="intermediate",
            estimated_hours=12, type="project",
            prerequisites=["Classification Algorithms", "Model Evaluation & Tuning", "Pandas for Data Analysis"],
            url="", rating=4.8, tags=["project", "churn", "ml"]
        ),
        Resource(
            title="Sales Forecasting Project",
            description="Use time series analysis and regression to forecast sales from historical data.",
            domain="AI/ML", skill="Machine Learning", difficulty="intermediate",
            estimated_hours=10, type="project",
            prerequisites=["Linear & Logistic Regression", "Pandas for Data Analysis"],
            url="", rating=4.5, tags=["project", "forecasting"]
        ),
        Resource(
            title="Sentiment Analysis Project",
            description="Build a sentiment analysis pipeline using NLP techniques and ML classification.",
            domain="AI/ML", skill="NLP", difficulty="intermediate",
            estimated_hours=12, type="project",
            prerequisites=["Classification Algorithms", "Python Fundamentals"],
            url="", rating=4.6, tags=["project", "nlp", "sentiment"]
        ),

        # ── Deep Learning ───────────────────────────────────
        Resource(
            title="Introduction to Deep Learning",
            description="Neural network basics, backpropagation, activation functions, and TensorFlow/PyTorch intro.",
            domain="AI/ML", skill="Deep Learning", difficulty="advanced",
            estimated_hours=20, type="course",
            prerequisites=["Machine Learning Fundamentals", "NumPy Essentials"],
            url="https://www.deeplearning.ai/",
            rating=4.8, tags=["deep learning", "neural networks"]
        ),

        # ── Web Development ─────────────────────────────────
        Resource(
            title="HTML & CSS Fundamentals",
            description="Semantic HTML, CSS box model, flexbox, grid, and responsive design.",
            domain="Web Development", skill="HTML", difficulty="beginner",
            estimated_hours=10, type="course",
            prerequisites=[], url="https://developer.mozilla.org/en-US/docs/Learn/HTML",
            rating=4.7, tags=["html", "css", "web"]
        ),
        Resource(
            title="CSS Layouts & Responsive Design",
            description="Advanced CSS — animations, transitions, media queries, and modern layouts.",
            domain="Web Development", skill="CSS", difficulty="intermediate",
            estimated_hours=8, type="course",
            prerequisites=["HTML & CSS Fundamentals"],
            url="https://css-tricks.com/", rating=4.5, tags=["css", "responsive"]
        ),
        Resource(
            title="JavaScript Fundamentals",
            description="Variables, functions, DOM manipulation, events, promises, and async/await.",
            domain="Web Development", skill="JavaScript", difficulty="beginner",
            estimated_hours=15, type="course",
            prerequisites=["HTML & CSS Fundamentals"],
            url="https://javascript.info/", rating=4.8, tags=["javascript", "web"]
        ),
        Resource(
            title="Advanced JavaScript",
            description="Closures, prototypes, modules, error handling, and ES6+ features.",
            domain="Web Development", skill="JavaScript", difficulty="intermediate",
            estimated_hours=10, type="course",
            prerequisites=["JavaScript Fundamentals"],
            url="https://javascript.info/", rating=4.6, tags=["javascript", "advanced"]
        ),
        Resource(
            title="React Fundamentals",
            description="Components, props, state, hooks, routing, and building single-page applications.",
            domain="Web Development", skill="React", difficulty="intermediate",
            estimated_hours=15, type="course",
            prerequisites=["JavaScript Fundamentals"],
            url="https://react.dev/learn", rating=4.8, tags=["react", "frontend"]
        ),
        Resource(
            title="Building REST APIs with Node.js",
            description="Express.js, middleware, routing, authentication, and database integration.",
            domain="Web Development", skill="Node.js", difficulty="intermediate",
            estimated_hours=12, type="course",
            prerequisites=["JavaScript Fundamentals"],
            url="https://expressjs.com/", rating=4.6, tags=["node", "api", "backend"]
        ),
        Resource(
            title="REST API Design & Consumption",
            description="HTTP methods, status codes, JSON, API design best practices, and testing with Postman.",
            domain="Web Development", skill="REST APIs", difficulty="beginner",
            estimated_hours=6, type="tutorial",
            prerequisites=["JavaScript Fundamentals"],
            url="", rating=4.5, tags=["api", "rest"]
        ),
        Resource(
            title="Portfolio Website Project",
            description="Build a responsive personal portfolio website using HTML, CSS, and JavaScript.",
            domain="Web Development", skill="HTML", difficulty="beginner",
            estimated_hours=8, type="project",
            prerequisites=["HTML & CSS Fundamentals", "JavaScript Fundamentals"],
            url="", rating=4.6, tags=["project", "portfolio"]
        ),
        Resource(
            title="Task Manager App Project",
            description="Build a full-stack task manager with React frontend and Node.js backend.",
            domain="Web Development", skill="React", difficulty="intermediate",
            estimated_hours=15, type="project",
            prerequisites=["React Fundamentals", "Building REST APIs with Node.js"],
            url="", rating=4.7, tags=["project", "fullstack"]
        ),
        Resource(
            title="E-commerce Website Project",
            description="Build a complete e-commerce platform with product listings, cart, and checkout.",
            domain="Web Development", skill="React", difficulty="advanced",
            estimated_hours=25, type="project",
            prerequisites=["React Fundamentals", "Building REST APIs with Node.js", "REST API Design & Consumption"],
            url="", rating=4.8, tags=["project", "ecommerce"]
        ),
        Resource(
            title="Real-time Chat Application Project",
            description="Build a chat app using WebSockets, React, and Node.js.",
            domain="Web Development", skill="Node.js", difficulty="advanced",
            estimated_hours=15, type="project",
            prerequisites=["React Fundamentals", "Building REST APIs with Node.js"],
            url="", rating=4.6, tags=["project", "websocket", "chat"]
        ),

        # ── Git ─────────────────────────────────────────────
        Resource(
            title="Git & GitHub Essentials",
            description="Version control fundamentals — init, commit, branch, merge, pull requests, and collaboration.",
            domain="Tools", skill="Git", difficulty="beginner",
            estimated_hours=5, type="course",
            prerequisites=[], url="https://git-scm.com/book/en/v2",
            rating=4.7, tags=["git", "github", "version control"]
        ),

        # ── Algorithms ──────────────────────────────────────
        Resource(
            title="Data Structures & Algorithms",
            description="Arrays, linked lists, trees, graphs, sorting, searching, and Big-O notation.",
            domain="Computer Science", skill="Algorithms", difficulty="intermediate",
            estimated_hours=20, type="course",
            prerequisites=["Python Fundamentals"],
            url="https://www.geeksforgeeks.org/data-structures/",
            rating=4.7, tags=["algorithms", "data structures", "cs"]
        ),

        # ── Testing ─────────────────────────────────────────
        Resource(
            title="Software Testing Fundamentals",
            description="Unit testing, integration testing, TDD, and pytest/Jest basics.",
            domain="Software Engineering", skill="Testing", difficulty="beginner",
            estimated_hours=8, type="course",
            prerequisites=["Python Fundamentals"],
            url="", rating=4.4, tags=["testing", "qa"]
        ),

        # ── Deployment ──────────────────────────────────────
        Resource(
            title="Web App Deployment",
            description="Deploy web applications to Heroku, Vercel, and AWS — CI/CD basics.",
            domain="DevOps", skill="Deployment", difficulty="intermediate",
            estimated_hours=6, type="tutorial",
            prerequisites=["Git & GitHub Essentials"],
            url="", rating=4.3, tags=["deployment", "devops"]
        ),

        # ── TypeScript ──────────────────────────────────────
        Resource(
            title="TypeScript Essentials",
            description="Types, interfaces, generics, enums, and integrating TypeScript with React.",
            domain="Web Development", skill="TypeScript", difficulty="intermediate",
            estimated_hours=10, type="course",
            prerequisites=["JavaScript Fundamentals"],
            url="https://www.typescriptlang.org/docs/", rating=4.6,
            tags=["typescript", "web"]
        ),

        # ── Cloud ───────────────────────────────────────────
        Resource(
            title="Cloud Computing Fundamentals",
            description="AWS/GCP/Azure overview, compute, storage, networking, and cloud architecture.",
            domain="Cloud", skill="Cloud Computing", difficulty="beginner",
            estimated_hours=12, type="course",
            prerequisites=["Linux"],
            url="", rating=4.5, tags=["cloud", "aws"]
        ),

        # ── Docker ──────────────────────────────────────────
        Resource(
            title="Docker for Developers",
            description="Containers, images, Dockerfiles, volumes, and docker-compose.",
            domain="DevOps", skill="Docker", difficulty="intermediate",
            estimated_hours=8, type="course",
            prerequisites=["Linux", "Git & GitHub Essentials"],
            url="https://docs.docker.com/get-started/",
            rating=4.6, tags=["docker", "containers"]
        ),

        # ── Linux ───────────────────────────────────────────
        Resource(
            title="Linux Command Line Basics",
            description="File system navigation, permissions, shell scripting, and common utilities.",
            domain="Tools", skill="Linux", difficulty="beginner",
            estimated_hours=8, type="course",
            prerequisites=[], url="",
            rating=4.5, tags=["linux", "terminal"]
        ),

        # ── Cybersecurity ───────────────────────────────────
        Resource(
            title="Cybersecurity Fundamentals",
            description="CIA triad, encryption, authentication, network security, and common attack vectors.",
            domain="Security", skill="Cybersecurity", difficulty="beginner",
            estimated_hours=12, type="course",
            prerequisites=["Linux Command Line Basics"],
            url="", rating=4.5, tags=["security", "cybersecurity"]
        ),

        # ── UI/UX ───────────────────────────────────────────
        Resource(
            title="UI/UX Design Principles",
            description="Design thinking, wireframing, prototyping, color theory, and usability testing.",
            domain="Design", skill="UI/UX Design", difficulty="beginner",
            estimated_hours=10, type="course",
            prerequisites=[], url="",
            rating=4.6, tags=["design", "ux", "ui"]
        ),

        # ── NLP ─────────────────────────────────────────────
        Resource(
            title="Natural Language Processing Fundamentals",
            description="Text preprocessing, tokenization, TF-IDF, word embeddings, and text classification.",
            domain="AI/ML", skill="NLP", difficulty="intermediate",
            estimated_hours=15, type="course",
            prerequisites=["Machine Learning Fundamentals", "Python Fundamentals"],
            url="", rating=4.6, tags=["nlp", "ml", "text"]
        ),

        # ── Additional courses for variety ──────────────────
        Resource(
            title="Python Quick Reference Guide",
            description="A concise video walkthrough of Python syntax and best practices.",
            domain="Programming", skill="Python", difficulty="beginner",
            estimated_hours=3, type="video",
            prerequisites=[], url="https://www.youtube.com/",
            rating=4.4, tags=["python", "video", "quick"]
        ),
        Resource(
            title="SQL Quick Reference",
            description="A short article covering essential SQL commands with examples.",
            domain="Data", skill="SQL", difficulty="beginner",
            estimated_hours=2, type="article",
            prerequisites=[], url="https://www.w3schools.com/sql/",
            rating=4.3, tags=["sql", "article"]
        ),
        Resource(
            title="Machine Learning with Scikit-Learn",
            description="Hands-on ML using scikit-learn — pipelines, transformers, and model persistence.",
            domain="AI/ML", skill="Machine Learning", difficulty="intermediate",
            estimated_hours=10, type="tutorial",
            prerequisites=["Machine Learning Fundamentals", "Pandas for Data Analysis"],
            url="https://scikit-learn.org/stable/",
            rating=4.7, tags=["sklearn", "ml", "hands-on"]
        ),
    ]


def get_assessments():
    return [
        Assessment(
            title="Python Basics Quiz",
            skill="Python", difficulty="beginner",
            questions=[
                {
                    "question": "What is the output of print(type(3.14))?",
                    "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'double'>"],
                    "correct": 1,
                    "explanation": "3.14 is a floating-point number, so its type is 'float'."
                },
                {
                    "question": "Which keyword is used to define a function in Python?",
                    "options": ["function", "func", "def", "define"],
                    "correct": 2,
                    "explanation": "Python uses 'def' to define functions."
                },
                {
                    "question": "What does len([1, 2, 3]) return?",
                    "options": ["2", "3", "4", "Error"],
                    "correct": 1,
                    "explanation": "len() returns the number of elements in a list. [1,2,3] has 3 elements."
                },
                {
                    "question": "Which data structure uses key-value pairs?",
                    "options": ["List", "Tuple", "Dictionary", "Set"],
                    "correct": 2,
                    "explanation": "Dictionaries store data as key-value pairs."
                },
                {
                    "question": "What is the correct way to create a list in Python?",
                    "options": ["list = (1,2,3)", "list = [1,2,3]", "list = {1,2,3}", "list = <1,2,3>"],
                    "correct": 1,
                    "explanation": "Lists are created using square brackets []."
                },
                {
                    "question": "What does 'break' do in a loop?",
                    "options": ["Skips the current iteration", "Exits the loop", "Pauses the loop", "Restarts the loop"],
                    "correct": 1,
                    "explanation": "'break' exits the loop immediately."
                },
                {
                    "question": "Which operator is used for exponentiation?",
                    "options": ["^", "**", "//", "%%"],
                    "correct": 1,
                    "explanation": "Python uses ** for exponentiation (e.g., 2**3 = 8)."
                },
                {
                    "question": "What will 'hello'[1] return?",
                    "options": ["h", "e", "l", "o"],
                    "correct": 1,
                    "explanation": "String indexing starts at 0, so index 1 is 'e'."
                },
                {
                    "question": "Which of these is a mutable data type?",
                    "options": ["String", "Tuple", "List", "Integer"],
                    "correct": 2,
                    "explanation": "Lists are mutable — you can change their elements after creation."
                },
                {
                    "question": "How do you add an element to a list?",
                    "options": ["list.add(x)", "list.append(x)", "list.push(x)", "list.insert(x)"],
                    "correct": 1,
                    "explanation": "The append() method adds an element to the end of a list."
                }
            ]
        ),
        Assessment(
            title="SQL Fundamentals Quiz",
            skill="SQL", difficulty="beginner",
            questions=[
                {
                    "question": "Which SQL command is used to retrieve data?",
                    "options": ["GET", "FETCH", "SELECT", "RETRIEVE"],
                    "correct": 2,
                    "explanation": "SELECT is used to query data from a database."
                },
                {
                    "question": "Which clause filters rows in a query?",
                    "options": ["HAVING", "WHERE", "FILTER", "CONDITION"],
                    "correct": 1,
                    "explanation": "WHERE filters rows based on conditions."
                },
                {
                    "question": "Which JOIN returns all rows from both tables?",
                    "options": ["INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN"],
                    "correct": 2,
                    "explanation": "FULL OUTER JOIN returns all rows from both tables, with NULLs where there's no match."
                },
                {
                    "question": "What does GROUP BY do?",
                    "options": ["Sorts results", "Groups rows with same values", "Limits results", "Joins tables"],
                    "correct": 1,
                    "explanation": "GROUP BY groups rows that have the same values in specified columns."
                },
                {
                    "question": "Which function counts the number of rows?",
                    "options": ["SUM()", "COUNT()", "TOTAL()", "NUM()"],
                    "correct": 1,
                    "explanation": "COUNT() returns the number of rows that match a condition."
                }
            ]
        ),
        Assessment(
            title="Statistics Quiz",
            skill="Statistics", difficulty="beginner",
            questions=[
                {
                    "question": "What is the mean of [2, 4, 6, 8, 10]?",
                    "options": ["5", "6", "7", "8"],
                    "correct": 1,
                    "explanation": "Mean = (2+4+6+8+10)/5 = 30/5 = 6."
                },
                {
                    "question": "What is the median of [3, 1, 4, 1, 5]?",
                    "options": ["1", "3", "4", "2.8"],
                    "correct": 1,
                    "explanation": "Sorted: [1,1,3,4,5]. Middle value is 3."
                },
                {
                    "question": "What does standard deviation measure?",
                    "options": ["Central tendency", "Spread of data", "Correlation", "Causation"],
                    "correct": 1,
                    "explanation": "Standard deviation measures how spread out data points are from the mean."
                },
                {
                    "question": "A correlation of -0.9 indicates?",
                    "options": ["No relationship", "Strong positive", "Strong negative", "Weak negative"],
                    "correct": 2,
                    "explanation": "-0.9 is close to -1, indicating a strong negative linear relationship."
                },
                {
                    "question": "What type of chart best shows distribution?",
                    "options": ["Pie chart", "Line chart", "Histogram", "Scatter plot"],
                    "correct": 2,
                    "explanation": "Histograms display the distribution of a single variable."
                }
            ]
        ),
        Assessment(
            title="Machine Learning Basics Quiz",
            skill="Machine Learning", difficulty="intermediate",
            questions=[
                {
                    "question": "Which is a supervised learning algorithm?",
                    "options": ["K-Means", "PCA", "Linear Regression", "DBSCAN"],
                    "correct": 2,
                    "explanation": "Linear Regression is supervised — it learns from labeled input-output pairs."
                },
                {
                    "question": "What is overfitting?",
                    "options": [
                        "Model performs well on test data",
                        "Model performs well on training data but poorly on test data",
                        "Model is too simple",
                        "Model has high bias"
                    ],
                    "correct": 1,
                    "explanation": "Overfitting means the model memorizes training data and fails to generalize."
                },
                {
                    "question": "What metric is used for classification accuracy?",
                    "options": ["RMSE", "R²", "F1 Score", "MAE"],
                    "correct": 2,
                    "explanation": "F1 Score balances precision and recall for classification tasks."
                },
                {
                    "question": "What does cross-validation help prevent?",
                    "options": ["Underfitting", "Overfitting", "Data leakage", "Feature scaling"],
                    "correct": 1,
                    "explanation": "Cross-validation helps detect and prevent overfitting by testing on different data splits."
                },
                {
                    "question": "Which algorithm is best for a binary classification problem?",
                    "options": ["Linear Regression", "Logistic Regression", "K-Means", "PCA"],
                    "correct": 1,
                    "explanation": "Logistic Regression is designed for binary classification problems."
                }
            ]
        ),
        Assessment(
            title="HTML & CSS Quiz",
            skill="HTML", difficulty="beginner",
            questions=[
                {
                    "question": "What does HTML stand for?",
                    "options": [
                        "Hyper Text Markup Language",
                        "High Tech Modern Language",
                        "Hyper Transfer Markup Language",
                        "Home Tool Markup Language"
                    ],
                    "correct": 0,
                    "explanation": "HTML stands for HyperText Markup Language."
                },
                {
                    "question": "Which CSS property changes text color?",
                    "options": ["text-color", "font-color", "color", "text-style"],
                    "correct": 2,
                    "explanation": "The 'color' property sets the text color in CSS."
                },
                {
                    "question": "Which HTML tag creates a hyperlink?",
                    "options": ["<link>", "<a>", "<href>", "<url>"],
                    "correct": 1,
                    "explanation": "The <a> (anchor) tag creates hyperlinks."
                },
                {
                    "question": "What does CSS 'flexbox' help with?",
                    "options": ["Animation", "Layout", "Typography", "Color"],
                    "correct": 1,
                    "explanation": "Flexbox is a CSS layout model for arranging elements in a container."
                },
                {
                    "question": "Which property makes a website responsive?",
                    "options": ["float", "media queries", "position", "z-index"],
                    "correct": 1,
                    "explanation": "Media queries apply different styles based on screen size."
                }
            ]
        ),
        Assessment(
            title="JavaScript Fundamentals Quiz",
            skill="JavaScript", difficulty="beginner",
            questions=[
                {
                    "question": "Which keyword declares a constant in JavaScript?",
                    "options": ["var", "let", "const", "define"],
                    "correct": 2,
                    "explanation": "'const' declares a variable that cannot be reassigned."
                },
                {
                    "question": "What is the output of typeof null?",
                    "options": ["'null'", "'undefined'", "'object'", "'boolean'"],
                    "correct": 2,
                    "explanation": "This is a known JavaScript quirk — typeof null returns 'object'."
                },
                {
                    "question": "What does '===' check?",
                    "options": ["Value only", "Type only", "Value and type", "Reference"],
                    "correct": 2,
                    "explanation": "'===' is the strict equality operator that checks both value and type."
                },
                {
                    "question": "Which method adds an element to the end of an array?",
                    "options": ["push()", "pop()", "shift()", "unshift()"],
                    "correct": 0,
                    "explanation": "push() adds one or more elements to the end of an array."
                },
                {
                    "question": "What is a Promise in JavaScript?",
                    "options": [
                        "A data type",
                        "An object representing eventual completion of an async operation",
                        "A loop structure",
                        "A CSS feature"
                    ],
                    "correct": 1,
                    "explanation": "A Promise represents the eventual result of an asynchronous operation."
                }
            ]
        ),
        Assessment(
            title="React Basics Quiz",
            skill="React", difficulty="intermediate",
            questions=[
                {
                    "question": "What is JSX?",
                    "options": [
                        "A database query language",
                        "A syntax extension for JavaScript",
                        "A CSS framework",
                        "A testing library"
                    ],
                    "correct": 1,
                    "explanation": "JSX lets you write HTML-like syntax in JavaScript files."
                },
                {
                    "question": "What hook manages state in functional components?",
                    "options": ["useEffect", "useState", "useRef", "useContext"],
                    "correct": 1,
                    "explanation": "useState is the primary hook for managing local state."
                },
                {
                    "question": "What is the virtual DOM?",
                    "options": [
                        "A copy of the server",
                        "A lightweight copy of the real DOM",
                        "A CSS preprocessor",
                        "A database layer"
                    ],
                    "correct": 1,
                    "explanation": "React uses a virtual DOM to efficiently update only the changed parts of the real DOM."
                },
                {
                    "question": "How do you pass data from parent to child component?",
                    "options": ["State", "Props", "Context", "Refs"],
                    "correct": 1,
                    "explanation": "Props (properties) pass data from parent to child components."
                },
                {
                    "question": "When does useEffect run by default?",
                    "options": [
                        "Only on mount",
                        "After every render",
                        "Only on unmount",
                        "Only when state changes"
                    ],
                    "correct": 1,
                    "explanation": "Without a dependency array, useEffect runs after every render."
                }
            ]
        ),
        Assessment(
            title="NumPy Quiz",
            skill="NumPy", difficulty="beginner",
            questions=[
                {
                    "question": "How do you create a NumPy array?",
                    "options": ["np.array([1,2,3])", "np.list([1,2,3])", "np.create([1,2,3])", "np.new([1,2,3])"],
                    "correct": 0,
                    "explanation": "np.array() creates a NumPy array from a Python list."
                },
                {
                    "question": "What does np.zeros((3,3)) create?",
                    "options": ["3x3 matrix of ones", "3x3 matrix of zeros", "1D array of 3 zeros", "Error"],
                    "correct": 1,
                    "explanation": "np.zeros((3,3)) creates a 3x3 matrix filled with zeros."
                },
                {
                    "question": "What is broadcasting in NumPy?",
                    "options": [
                        "Sending data to GPU",
                        "Operating on arrays of different shapes",
                        "Printing arrays",
                        "Saving arrays to disk"
                    ],
                    "correct": 1,
                    "explanation": "Broadcasting allows NumPy to operate on arrays of different shapes element-wise."
                },
                {
                    "question": "How do you get the shape of array a?",
                    "options": ["a.shape", "a.size()", "a.dimensions", "len(a)"],
                    "correct": 0,
                    "explanation": "The .shape attribute returns the dimensions of a NumPy array."
                },
                {
                    "question": "What does np.dot(a, b) compute?",
                    "options": ["Element-wise product", "Dot product / matrix multiplication", "Cross product", "Division"],
                    "correct": 1,
                    "explanation": "np.dot() computes the dot product of two arrays or matrix multiplication."
                }
            ]
        ),
        Assessment(
            title="Pandas Quiz",
            skill="Pandas", difficulty="beginner",
            questions=[
                {
                    "question": "What is a DataFrame?",
                    "options": [
                        "A 1D labeled array",
                        "A 2D labeled data structure",
                        "A database connection",
                        "A chart type"
                    ],
                    "correct": 1,
                    "explanation": "A DataFrame is a 2D labeled data structure with rows and columns."
                },
                {
                    "question": "How do you read a CSV file in Pandas?",
                    "options": ["pd.read_csv()", "pd.load_csv()", "pd.open_csv()", "pd.import_csv()"],
                    "correct": 0,
                    "explanation": "pd.read_csv() reads a CSV file into a DataFrame."
                },
                {
                    "question": "How do you handle missing values?",
                    "options": ["df.dropna()", "df.remove_null()", "df.clean()", "df.fix()"],
                    "correct": 0,
                    "explanation": "df.dropna() removes rows with missing values. df.fillna() replaces them."
                },
                {
                    "question": "What does df.groupby('col').mean() do?",
                    "options": [
                        "Sorts by column",
                        "Groups by column and calculates mean for each group",
                        "Filters by column",
                        "Renames the column"
                    ],
                    "correct": 1,
                    "explanation": "groupby groups rows by unique values, then mean() calculates the average per group."
                },
                {
                    "question": "How do you select a column in a DataFrame?",
                    "options": ["df.get('col')", "df['col']", "df.col()", "df.select('col')"],
                    "correct": 1,
                    "explanation": "df['col'] selects a column by name, returning a Series."
                }
            ]
        ),
        Assessment(
            title="Git Basics Quiz",
            skill="Git", difficulty="beginner",
            questions=[
                {
                    "question": "What command initializes a Git repository?",
                    "options": ["git start", "git init", "git create", "git new"],
                    "correct": 1,
                    "explanation": "git init initializes a new Git repository."
                },
                {
                    "question": "What does 'git commit' do?",
                    "options": [
                        "Uploads code to GitHub",
                        "Records changes to the repository",
                        "Deletes a branch",
                        "Merges branches"
                    ],
                    "correct": 1,
                    "explanation": "git commit records a snapshot of staged changes to the repository."
                },
                {
                    "question": "How do you create a new branch?",
                    "options": ["git branch new-branch", "git create new-branch", "git new new-branch", "git make new-branch"],
                    "correct": 0,
                    "explanation": "git branch <name> creates a new branch."
                },
                {
                    "question": "What does 'git pull' do?",
                    "options": [
                        "Pushes changes to remote",
                        "Fetches and merges changes from remote",
                        "Creates a new repository",
                        "Deletes a branch"
                    ],
                    "correct": 1,
                    "explanation": "git pull fetches changes from a remote repository and merges them."
                },
                {
                    "question": "What file tells Git which files to ignore?",
                    "options": [".gitconfig", ".gitignore", ".gitexclude", ".gitskip"],
                    "correct": 1,
                    "explanation": ".gitignore lists file patterns that Git should not track."
                }
            ]
        ),
    ]


def create_demo_user(db):
    """Create the demo user 'Alex' with pre-populated profile."""
    from sqlalchemy.orm import Session

    # Check if demo user exists
    existing = db.query(User).filter(User.email == "alex@demo.com").first()
    if existing:
        return existing

    user = User(
        name="Alex",
        email="alex@demo.com",
        education="Bachelor's in Computer Science",
        experience_level="beginner",
        weekly_hours=8,
        learning_preferences=["projects", "videos"],
        current_role="Student"
    )
    db.add(user)
    db.flush()

    # Interests
    for interest in ["Data Science", "Machine Learning", "Programming"]:
        db.add(UserInterest(user_id=user.id, interest=interest))

    # Skills — get skill IDs
    python_skill = db.query(Skill).filter(Skill.name == "Python").first()
    sql_skill = db.query(Skill).filter(Skill.name == "SQL").first()

    if python_skill:
        db.add(UserSkill(user_id=user.id, skill_id=python_skill.id, proficiency=25))
    if sql_skill:
        db.add(UserSkill(user_id=user.id, skill_id=sql_skill.id, proficiency=20))

    # Goal
    db.add(LearningGoal(
        user_id=user.id,
        goal_text="I want to become a Data Scientist within 6 months.",
        target_role="Data Scientist",
        is_active=True
    ))

    db.commit()
    return user
