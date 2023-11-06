from flask import Flask, render_template, request, redirect, url_for, abort
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_migrate import Migrate
#from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


app = Flask(__name__)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
# app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
# jwt = JWTManager(app)

# Flask-Login setup
#login_manager = LoginManager(app)
#login_manager.login_view = 'login'


# migrate = Migrate(app, db)

#Dummy user class for demonstration purposes
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username



#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neweBerichsheft.db'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# class Report(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)  
#     department = db.Column(db.String(100), nullable=False)
#     fromDate = db.Column(db.Date, nullable=False)
#     toDate = db.Column(db.Date, nullable=True)
#     monday_tasks = db.Column(db.String(255), nullable=True)
#     monday_hours = db.Column(db.Integer, nullable=True)
#     tuesday_tasks = db.Column(db.String(255), nullable=True)
#     tuesday_hours = db.Column(db.Integer, nullable=True)
#     wednesday_tasks = db.Column(db.String(255), nullable=True)
#     wednesday_hours = db.Column(db.Integer, nullable=True)
#     thursday_tasks = db.Column(db.String(255), nullable=True)
#     thursday_hours = db.Column(db.Integer, nullable=True)
#     friday_task = db.Column(db.String(255), nullable=True)
#     friday_hours = db.Column(db.Integer, nullable=True)
#
#     def __init__(self, title, department, fromDate, toDate,
#                  monday_tasks, monday_hours,
#                  tuesday_tasks, tuesday_hours,
#                  wednesday_tasks, wednesday_hours,
#                  thursday_tasks, thursday_hours,
#                  friday_task, friday_hours):
#         self.title = title
#         self.department = department
#         self.fromDate = fromDate
#         self.toDate = toDate
#         self.monday_tasks = monday_tasks
#         self.monday_hours = monday_hours
#         self.tuesday_tasks = tuesday_tasks
#         self.tuesday_hours = tuesday_hours
#         self.wednesday_tasks = wednesday_tasks
#         self.wednesday_hours = wednesday_hours
#         self.thursday_tasks = thursday_tasks
#         self.thursday_hours = thursday_hours
#         self.friday_task = friday_task
#         self.friday_hours = friday_hours

# # Create the database tables
# with app.app_context():
#     db.create_all()

# # Function to add a new report
# def add_report(data):
#     new_report = Report(**data)
#     db.session.add(new_report)
#     db.session.commit()

# # Function to get all reports
# def get_all_reports():
#     return Report.query.all()

# # Function to get a report by ID
# def get_report_by_id(report_id):
#     return Report.query.get(report_id)

# # Function to update a report
# def update_report(report_id, data):
#     print('hello')
#     print(report_id)
#     print(data)

#     report = Report.query.get(report_id)
#     if report:
#         for key, value in data.items():
#             setattr(report, key, value)
#         db.session.commit()

# # Function to delete a report
# def delete_report(report_id):
#     report = Report.query.get(report_id)
#     if report:
#         db.session.delete(report)
#         db.session.commit()




Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)  
    department = Column(String(100), nullable=False)
    fromDate = Column(Date, nullable=False)
    toDate = Column(Date, nullable=True)
    monday_tasks = Column(String(255), nullable=True)
    monday_hours = Column(Integer, nullable=True)
    tuesday_tasks = Column(String(255), nullable=True)
    tuesday_hours = Column(Integer, nullable=True)
    wednesday_tasks = Column(String(255), nullable=True)
    wednesday_hours = Column(Integer, nullable=True)
    thursday_tasks = Column(String(255), nullable=True)
    thursday_hours = Column(Integer, nullable=True)
    friday_task = Column(String(255), nullable=True)
    friday_hours = Column(Integer, nullable=True)

# Replace 'sqlite:///neweBerichsheft.db' with your actual database connection string
engine = create_engine('sqlite:///neweBerichsheft.db', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_report(data):
    new_report = Report(**data)
    session.add(new_report)
    session.commit()

def get_all_reports():
    return session.query(Report).all()

def get_report_by_id(report_id):
    return session.query(Report).get(report_id)

def update_report(report_id, data):
    report = session.query(Report).get(report_id)
    if report:
        for key, value in data.items():
            setattr(report, key, value)
        session.commit()

def delete_report(report_id):
    report = session.query(Report).get(report_id)
    if report:
        session.delete(report)
        session.commit()


@app.route("/")
def home():
    return redirect("/reports")

# Flask route to display all reports
@app.route('/reports')
def reports():
    all_reports = get_all_reports()
    return render_template('reports.html', reports=all_reports
                          # , username=current_user.username
                           )



# Flask route to add a new report
@app.route('/add_report', methods=['GET', 'POST'])
def add_new_report():
    if request.method == 'POST':
        data = {
            'department': request.form.get('department'),
            'title': request.form.get('title'),
            'fromDate': datetime.strptime(request.form.get('fromDate'), '%Y-%m-%d').date() if request.form.get('toDate') else None,
            'toDate': datetime.strptime(request.form.get('toDate'), '%Y-%m-%d').date() if request.form.get('toDate') else None,
            'monday_tasks': request.form.get('monday_tasks'),
            'monday_hours': int(request.form.get('monday_hours')),
            'tuesday_tasks': request.form.get('tuesday_tasks'),
            'tuesday_hours': int(request.form.get('tuesday_hours')),
            'wednesday_tasks': request.form.get('wednesday_tasks'),
            'wednesday_hours': int(request.form.get('wednesday_hours')),
            'thursday_tasks': request.form.get('thursday_tasks'),
            'thursday_hours': int(request.form.get('thursday_hours')),
            'friday_task': request.form.get('friday_task'),
            'friday_hours': int(request.form.get('friday_hours')),
        }
        add_report(data)

        return redirect(url_for('reports'))
 
    return render_template('edit_report.html')


@app.route('/view_report/<int:report_id>')
def view_report(report_id):
    report = get_report_by_id(report_id)  # Replace with your function to get the report from the database

    if report is None:
        abort(404)  # Report not found, return a 404 error

    return render_template('read_report.html', report=report)

@app.route('/update_report/<int:report_id>', methods=['GET', 'POST'])
def update_existing_report(report_id):
    # Get the existing report from the database
    existing_report = get_report_by_id(report_id)

    if existing_report is None:
        # Handle the case where the report is not found
        return render_template('404.html'), 404

    if request.method == 'POST':
        # Handle the form submission for editing the report
        updated_data = {
            'department': request.form.get('department'),
            'title': request.form.get('title'),
            'fromDate': datetime.strptime(request.form.get('fromDate'), '%Y-%m-%d').date() if request.form.get('toDate') else None,
            'toDate': datetime.strptime(request.form.get('toDate'), '%Y-%m-%d').date() if request.form.get('toDate') else None,
            'monday_tasks': request.form.get('monday_tasks'),
            'monday_hours': int(request.form.get('monday_hours')),
            'tuesday_tasks': request.form.get('tuesday_tasks'),
            'tuesday_hours': int(request.form.get('tuesday_hours')),
            'wednesday_tasks': request.form.get('wednesday_tasks'),
            'wednesday_hours': int(request.form.get('wednesday_hours')),
            'thursday_tasks': request.form.get('thursday_tasks'),
            'thursday_hours': int(request.form.get('thursday_hours')),
            'friday_task': request.form.get('friday_task'),
            'friday_hours': int(request.form.get('friday_hours')),
            # Include other fields as needed
        }

        # Update the existing report with the new data
        update_report(report_id, updated_data)  # Implement this function

        # Redirect to the view page for the updated report
        return redirect(url_for('view_report', report_id=report_id))

    # Render the edit page with the existing report data
    return render_template ('edit_report.html', report=existing_report)

# Flask route to delete a report
@app.route('/delete_report/<int:report_id>')
def delete_existing_report(report_id):
    delete_report(report_id)
    return redirect(url_for('reports'))




# # Flask route to add a new report
# @app.route('/add_report', methods=['POST'])
# def add_new_report():
#     if request.method == 'POST':
#         data = {
#             'department': request.form.get('department'),
#             'fromDate': datetime.strptime(request.form.get('fromDate'), '%Y-%m-%d').date(),
#             'toDate': datetime.strptime(request.form.get('toDate'), '%Y-%m-%d').date() if request.form.get('toDate') else None,
#             'monday_tasks': request.form.get('monday_tasks'),
#             'monday_hours': int(request.form.get('monday_hours')),
#             'tuesday_tasks': request.form.get('tuesday_tasks'),
#             'tuesday_hours': int(request.form.get('tuesday_hours')),
#             'wednesday_tasks': request.form.get('wednesday_tasks'),
#             'wednesday_hours': int(request.form.get('wednesday_hours')),
#             'thursday_tasks': request.form.get('thursday_tasks'),
#             'thursday_hours': int(request.form.get('thursday_hours')),
#             'friday_task': request.form.get('friday_task'),
#             'friday_hours': int(request.form.get('friday_hours')),
#         }
#         add_report(data)

#     return redirect(url_for('reports'))



# # Flask route to update a report
# @app.route('/update_report/<int:report_id>', methods=['POST'])
# def update_existing_report(report_id):
#     if request.method == 'POST':
#         data = {
#             'department': request.form.get('department'),
#             'title': request.form.get('title'),
#             'fromDate': datetime.strptime(request.form.get('fromDate'), '%Y-%m-%d').date(),
#             'toDate': datetime.strptime(request.form.get('toDate'), '%Y-%m-%d').date() if request.form.get('toDate') else None,
#             'monday_tasks': request.form.get('monday_tasks'),
#             'monday_hours': int(request.form.get('monday_hours')),
#             'tuesday_tasks': request.form.get('tuesday_tasks'),
#             'tuesday_hours': int(request.form.get('tuesday_hours')),
#             'wednesday_tasks': request.form.get('wednesday_tasks'),
#             'wednesday_hours': int(request.form.get('wednesday_hours')),
#             'thursday_tasks': request.form.get('thursday_tasks'),
#             'thursday_hours': int(request.form.get('thursday_hours')),
#             'friday_task': request.form.get('friday_task'),
#             'friday_hours': int(request.form.get('friday_hours')),
#         }
#         update_report(report_id, data)

#    return redirect(url_for('reports'))
# @app.route('/update_report/<int:report_id>', methods=['POST'])
# def update_existing_report(report_id):
#     # Assuming you have a function to fetch the existing report from the database
#     existing_report = get_report_by_id(report_id)

#     if existing_report is None:
#         # Handle the case where the report is not found
#         return render_template('404.html'), 404

#     # Get the updated data from the form
#     updated_data = {
#              'department': request.form.get('department'),
#              'title': request.form.get('title'),
#              'fromDate': datetime.strptime(request.form.get('fromDate'), '%Y-%m-%d').date(),
#              'toDate': datetime.strptime(request.form.get('toDate'), '%Y-%m-%d').date() if request.form.get('toDate') else None,
#              'monday_tasks': request.form.get('monday_tasks'),
#              'monday_hours': int(request.form.get('monday_hours')),
#              'tuesday_tasks': request.form.get('tuesday_tasks'),
#              'tuesday_hours': int(request.form.get('tuesday_hours')),
#              'wednesday_tasks': request.form.get('wednesday_tasks'),
#              'wednesday_hours': int(request.form.get('wednesday_hours')),
#              'thursday_tasks': request.form.get('thursday_tasks'),
#              'thursday_hours': int(request.form.get('thursday_hours')),
#              'friday_task': request.form.get('friday_task'),
#              'friday_hours': int(request.form.get('friday_hours')),
#     }

#     # Update the existing report with the new data
#     update_report(existing_report, updated_data)  # Implement this function

#     # Redirect to the view page for the updated report
#     return render_template('edit_report', report_id=report_id)



# from flask import Flask, request, jsonify, redirect, url_for, render_template

# import json
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# # from sqlalchemy import create_engine, Column, String, Integer, JSON, Date
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker

# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
# db = SQLAlchemy(app)




# class Report(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     tasks = db.Column(db.Text)
#     fromDate = db.Column(db.DateTime)
#     toDate = db.Column(db.DateTime)
#     department = db.Column(db.String(20))

#     def __init__(self, title, tasks, fromDate, toDate, department):
#         self.title = title
#         self.tasks = tasks
#         self.fromDate = fromDate
#         self.toDate = toDate
#         self.department = department

# # Create the database tables
# db.create_all()

# # Function to add a new report
# def add_report(title, tasks, fromDate, toDate, department):
#     new_report = Report(title=title, tasks=tasks, fromDate=fromDate, toDate=toDate, department=department)
#     db.session.add(new_report)
#     db.session.commit()

# # Function to get all reports
# def get_all_reports():
#     return Report.query.all()

# # Function to get a report by ID
# def get_report_by_id(report_id):
#     return Report.query.get(report_id)

# # Function to update a report
# def update_report(report_id, title, tasks, fromDate, toDate, department):
#     report = Report.query.get(report_id)
#     if report:
#         report.title = title
#         report.tasks = tasks
#         report.fromDate = fromDate
#         report.toDate = toDate
#         report.department = department
#         db.session.commit()

# # Function to delete a report
# def delete_report(report_id):
#     report = Report.query.get(report_id)
#     if report:
#         db.session.delete(report)
#         db.session.commit()

# # Flask route to display all reports
# @app.route('/reports')
# def reports():
#     all_reports = get_all_reports()
#     return render_template('reports.html', reports=all_reports)

# # Flask route to add a new report
# @app.route('/add_report', methods=['POST'])
# def add_new_report():
#     if request.method == 'POST':
#         title = request.form.get('title')
#         tasks = request.form.get('tasks')
#         fromDate = datetime.strptime(request.form.get('fromDate'), '%Y-%m-%d')
#         toDate = datetime.strptime(request.form.get('toDate'), '%Y-%m-%d') if request.form.get('toDate') else None
#         department = request.form.get('department')

#         add_report(title, tasks, fromDate, toDate, department)

#     return redirect(url_for('reports'))

# # Flask route to update a report
# @app.route('/update_report/<int:report_id>', methods=['POST'])
# def update_existing_report(report_id):
#     if request.method == 'POST':
#         title = request.form.get('title')
#         tasks = request.form.get('tasks')
#         fromDate = datetime.strptime(request.form.get('fromDate'), '%Y-%m-%d')
#         toDate = datetime.strptime(request.form.get('toDate'), '%Y-%m-%d') if request.form.get('toDate') else None
#         department = request.form.get('department')

#         update_report(report_id, title, tasks, fromDate, toDate, department)

#     return redirect(url_for('reports'))

# # Flask route to delete a report
# @app.route('/delete_report/<int:report_id>')
# def delete_existing_report(report_id):
#     delete_report(report_id)
#     return redirect(url_for('reports'))










@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Replace this with your actual login logic
        username = request.form['username']
        password = request.form['password']

        # Validate the username and password (you should replace this with your own validation logic)
        if username == 'user1@bla.bla' and password == 'password':
            user = User(1, username)
            login_user(user)
            return redirect(url_for('reports'))
        else:

            return ''' <a href=/></a> <br>Invalid login credentials'''

    return render_template('login.html')
# # app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
# # jwt = JWTManager(app)

# # # Dummy user data for demonstration purposes
# # users = {
# #     'schkja@sk.ja': {'password': 'admin'},
# #     'user2': {'password': 'password2'}
# # }

# # # Middleware to check for a valid token
# # @app.before_request
# # def check_jwt_token():
# #     # Specify the routes that don't require authentication
# #     if request.endpoint and request.endpoint not in ['login', 'protected']:
# #         # Check for a valid token in the request headers
# #         token = request.headers.get('Authorization', '').split('Bearer ')[-1]
# #         try:
# #             # Verify the token
# #             get_jwt_identity()
# #         except:
# #             # Redirect to the login page if the token is invalid or not present
# #             return redirect(url_for('login'))

# # # Endpoint for user login
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form.get('username')
# #         password = request.form.get('password')

# #         if username in users and users[username]['password'] == password:
# #             # Identity can be any data that is json serializable
# #             access_token = create_access_token(identity=username)
# #             return jsonify(access_token=access_token), 200
# #         else:
# #             return render_template('login.html', error='Invalid credentials')

# #     return render_template('login.html', error=None)

# # # Protected endpoint that requires a valid token
# # @app.route('/protected', methods=['GET'])
# # @jwt_required()
# # def protected():
# #     # Access the identity of the current user with get_jwt_identity
# #     current_user = get_jwt_identity()
# #     return jsonify(logged_in_as=current_user), 200


# # # # Endpoint for user login
# # # @app.route('/login', methods=['POST'])
# # # def login():
# # #     data = request.json
# # #     username = data.get('username')
# # #     password = data.get('password')

# # #     if username in users and users[username]['password'] == password:
# # #         # Identity can be any data that is json serializable
# # #         access_token = create_access_token(identity=username)
# # #         return jsonify(access_token=access_token), 200
# # #     else:
# # #         return jsonify(message='Invalid credentials'), 401

# # # # Protected endpoint that requires a valid token
# # # @app.route('/protected', methods=['GET'])
# # # @jwt_required()
# # # def protected():
# # #     # Access the identity of the current user with get_jwt_identity
# # #     current_user = get_jwt_identity()
# # #     return jsonify(logged_in_as=current_user), 200




# @app.route('/')
# def start():
#     return redirect(url_for('login'))


# @app.route('/forgot_password')
# def forgot_password():
#     return render_template('forgot_password.html')

# @app.route('/reports', methods=['GET', 'POST'])
# def reports():
#     # Session = sessionmaker(bind=engine)
#     # session = Session()

#     # # Get all weekly reports
#     # reports = []
#     # all_reports = get_all_weekly_reports(session)
#     # for report in all_reports:
#     #     reports.append(report.__dict__)
#     # print(reports)
#     reports = Report.query.all()

#     return render_template('reports.html', username=current_user.username, allreports=reports)

# @app.route('/newberichtsheft', methods=['GET', 'POST'])
# def newberichtsheft():
#     if request.method == 'POST':
#         # Extract data from the form

#         department = request.form.get('department')
#         fromDate = request.form.get('fromDate')
#         toDate = request.form.get('toDate')

#         monday_tasks = request.form.get('monday_tasks')
#         monday_hours = request.form.get('monday_hours')

#         tuesday_tasks = request.form.get('tuesday_tasks')
#         tuesday_hours = request.form.get('tuesday_hours')

#         wednesday_tasks = request.form.get('wednesday_tasks')
#         wednesday_hours = request.form.get('wednesday_hours')

#         thursday_tasks = request.form.get('thursday_tasks')
#         thursday_hours = request.form.get('thursday_hours')

#         friday_task = request.form.get('friday_task')
#         friday_hours = request.form.get('friday_hours')

#                 # Example usage
#         data = {
#             "title": "test",
#             "department": department,
#             "fromDate": datetime.strptime(fromDate, "%Y-%m-%d"),
#             "toDate": datetime.strptime(toDate, "%Y-%m-%d"),
#             "tasks": {
#                 "Monday": {"tasks": monday_tasks, "hours": monday_hours},
#                 "Tuesday": {"tasks": tuesday_tasks, "hours": tuesday_hours},
#                 "Wednesday": {"tasks": wednesday_tasks, "hours": wednesday_hours},
#                 "Thursday": {"tasks": thursday_tasks, "hours": thursday_hours},
#                 "Friday": {"tasks": friday_task, "hours": friday_hours}
#             }
#         }
#         print(data)
#         new_report = Report(title= "test", department: department,
#             fromDate: datetime.strptime(fromDate, "%Y-%m-%d"),
#             toDate: datetime.strptime(toDate, "%Y-%m-%d"),
#             tasks: {
#                 "Monday": {"tasks": monday_tasks, "hours": monday_hours},
#                 "Tuesday": {"tasks": tuesday_tasks, "hours": tuesday_hours},
#                 "Wednesday": {"tasks": wednesday_tasks, "hours": wednesday_hours},
#                 "Thursday": {"tasks": thursday_tasks, "hours": thursday_hours},
#                 "Friday": {"tasks": friday_task, "hours": friday_hours})
#         db.session.add(new_report)
#         db.session.commit()
#         return redirect(url_for('reports'))
#         # # Creating a new weekly report
#         # Session = sessionmaker(bind=engine)
#         # session = Session()
#         # add_weekly_report(session, data)
#     return render_template('newberichtsheft.html')

@app.route('/userpage')
def userpage():
    return render_template('userpage.html'
                          # , username=current_user.username
                           )

# @app.route('/tab2')
# def tab2():
#     return render_template('tab2.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return 'Logged out successfully'

# if __name__ == '__main__':
#     app.run(debug=True) 




if __name__ == '__main__':
    app.run(debug=True, port=5040)