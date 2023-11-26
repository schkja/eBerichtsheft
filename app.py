from flask import Flask, render_template, request, redirect, url_for, abort, make_response
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from flask_weasyprint import HTML, render_pdf
from datetime import datetime

app = Flask(__name__)




Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    surname = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255))

    firm = Column(String(255))
    studyclass = Column(String(255))
    role = relationship('Role', back_populates='users')
    report_books = relationship('ReportBook', back_populates='user')

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(255))
    users = relationship('User', back_populates='role')

class ReportBook(Base):
    __tablename__ = 'report_books'
    reportBook_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    start = Column(Date)
    end = Column(Date)
    user = relationship('User', back_populates='report_books') 
    reports = relationship('Report', back_populates='report_book') 

class Report(Base):
    __tablename__ = 'reports'
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    status_id = Column(Integer, ForeignKey('statuses.status_id'))
    reportBook_id = Column(Integer, ForeignKey('report_books.reportBook_id'))
    calenderweek = Column(Date)
    mon = Column(Text)
    tue = Column(Text)
    wed = Column(Text)
    thu = Column(Text)
    fri = Column(Text)
    report_book = relationship('ReportBook', back_populates='reports')
    status = relationship('Status', back_populates='reports')

class Status(Base):
    __tablename__ = 'statuses'
    status_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    reports = relationship('Report', back_populates='status')

engine = create_engine('sqlite:///eBerichtsheft.db', echo=True)
Base.metadata.create_all(engine)



Session = sessionmaker(bind=engine)
session = Session()

# Populate the Status table when the app is first created
with app.app_context():
        # Check if the statuses are already populated
    if session.query(Status).count()  == 0:
        # Define the initial statuses
        initial_statuses = [
            {'name': 'New'},
            {'name': 'In Progress'},
            {'name': 'Declined'},
            {'name': 'Accepted'},
        ]
    
        # Add statuses to the database
        for status_data in initial_statuses:
            new_status = Status(**status_data)
            session.add(new_status)
        session.commit()
    if session.query(Role).count()  == 0:
        # Define the initial roles
        initial_roles = [
            {'role': 'Azubi'},
            {'role': 'Ausbilder'},
            {'role': 'Lehrer'},
            {'role': 'IHK'},
        ]

        # Add roles to the database
        for role_data in initial_roles:
            new_role = Role(**role_data)
            session.add(new_role)

        session.commit()


#@app.route('/')
#def index():
#    return redirect(url_for('users'))

@app.route("/")
def home():
    return redirect("/readme")

@app.route('/readme')
def readme():
    return render_template('readme.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Replace this with your actual login logic
        username = request.form['username']
        password = request.form['password']

        # Validate the username and password (you should replace this with your own validation logic)
        if username == 'user1@bla.bla' and password == 'password':
            # = User(1, username)
            #login_user(user)
            return redirect(url_for('users'))
        else:

            return render_template('login.html', error='False credentials, please try again')

    return render_template('login.html')

@app.route('/users')
def users():
    all_users = session.query(User).all()
    return render_template('users.html', users=all_users)

@app.route('/user_report_books/<int:user_id>')
def user_report_books(user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)

    report_books = session.query(ReportBook).filter_by(user_id=user_id).all()
    return render_template('user_report_books.html', user=user, report_books=report_books)



@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    roles = session.query(Role).all()
    if request.method == 'POST':
        data = {
            'role_id': request.form.get('role_id'),
            'surname': request.form.get('surname'),
            'lastname': request.form.get('lastname'),
            'email': request.form.get('email'),
            'firm': request.form.get('firm'),
            'studyclass': request.form.get('studyclass'),
        }
        new_user = User(**data)
        session.add(new_user)
        session.commit()
        return redirect(url_for('users'))

    return render_template('add_user.html', roles=roles)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    roles = session.query(Role).all()

    if request.method == 'POST':
        updated_data = {
            'role_id': request.form.get('role_id'),
            'surname': request.form.get('surname'),
            'lastname': request.form.get('lastname'),
            'email': request.form.get('email'),
            'firm': request.form.get('firm'),
            'studyclass': request.form.get('studyclass'),
        }
        for key, value in updated_data.items():
            setattr(user, key, value)
        session.commit()
        print(updated_data)
        return redirect(url_for('users'))

    return render_template('edit_user.html', user=user, roles=roles)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()

    return redirect(url_for('users'))














@app.route('/add_report_book/<int:user_id>', methods=['GET', 'POST'])
def add_report_book(user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)

    if request.method == 'POST':
        data = {
            'user_id': user_id,
            'start': datetime.strptime(request.form.get('start'), '%Y-%m-%d').date(),
            'end': datetime.strptime(request.form.get('end'), '%Y-%m-%d').date(),
        }
        new_report_book = ReportBook(**data)
        session.add(new_report_book)
        session.commit()
        return redirect(url_for('user_report_books', user_id=user_id))

    return render_template('add_report_book.html', user=user)

@app.route('/edit_report_book/<int:user_id>/<int:reportBook_id>', methods=['GET', 'POST'])
def edit_report_book(user_id, reportBook_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)

    report_book = session.query(ReportBook).get(reportBook_id)
    if not report_book:
        abort(404)

    if request.method == 'POST':
        updated_data = {
            'start': datetime.strptime(request.form.get('start'), '%Y-%m-%d').date(),
            'end': datetime.strptime(request.form.get('end'), '%Y-%m-%d').date(),
        }
        for key, value in updated_data.items():
            setattr(report_book, key, value)
        session.commit()
        return redirect(url_for('user_report_books', user_id=user_id))

    return render_template('edit_report_book.html', user=user, report_book=report_book)

@app.route('/delete_report_book/<int:user_id>/<int:reportBook_id>')
def delete_report_book(user_id, reportBook_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)

    report_book = session.query(ReportBook).get(reportBook_id)
    if report_book:
        session.delete(report_book)
        session.commit()

    return redirect(url_for('user_report_books', user_id=user_id))





# @app.route('/reports')
# def reports():
#     all_reports = session.query(Report).all()
#     return render_template('reports.html', reports=all_reports)


@app.route('/add_report/<int:user_id>/<int:reportBook_id>', methods=['GET', 'POST'])
def add_report(user_id, reportBook_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)

    report_book = session.query(ReportBook).get(reportBook_id)
    if not report_book:
        abort(404)
    # Get the available statuses
    statuses = session.query(Status).all()

    if request.method == 'POST':
        data = {
            'status_id': int(request.form.get('status_id')),
            'calenderweek': datetime.strptime(request.form.get('calenderweek'), '%Y-%m-%d').date() if request.form.get('calenderweek') else None,
            'mon': request.form.get('mon'),
            'tue': request.form.get('tue'),
            'wed': request.form.get('wed'),
            'thu': request.form.get('thu'),
            'fri': request.form.get('fri'),
        }
        new_report = Report(**data)
        report_book.reports.append(new_report)
        session.commit()
        return redirect(url_for('user_report_books', user_id=user_id))

    return render_template('edit_report.html', user=user, report_book=report_book, statuses=statuses)

@app.route('/edit_report/<int:report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    report = session.query(Report).join(Status).filter(Report.report_id == report_id).first()

    # Get the available statuses
    statuses = session.query(Status).all()
    #report = session.query(Report).get(report_id)
    if not report:
        abort(404)

    user_id = request.args.get('user_id')
    #print('hello'+user_id)
    #user_id = request.args["user_id"] #kinda the same
    user = session.query(User).get(user_id)
    print(user)
    if not user:
        abort(404)

    if request.method == 'POST':
        updated_data = {
            'status_id': int(request.form.get('status_id')),
            'calenderweek': datetime.strptime(request.form.get('calenderweek'), '%Y-%m-%d').date(),
            'mon': request.form.get('mon'),
            'tue': request.form.get('tue'),
            'wed': request.form.get('wed'),
            'thu': request.form.get('thu'),
            'fri': request.form.get('fri'),
        }
        print('hello')
        print(updated_data['status_id'])
        for key, value in updated_data.items():
            setattr(report, key, value)
        session.commit()
        #return redirect(url_for('user_report_books', user_id=report.report_book.user_id))
        return render_template('edit_report.html', report=report, onlyread=True, user=user, statuses=statuses)


    return render_template('edit_report.html', report=report, user=user, statuses=statuses)


# this function is still in development
@app.route('/view_report/<int:report_id>/pdf')
def view_report_pdf(report_id):
    # Fetch the report and other necessary data
    report = session.query(Report).get(report_id)
    if not report:
        abort(404)
    user_id = request.args.get('user_id')
    #user_id = request.args["user_id"] #kinda the same
    # Get the available statuses
    statuses = session.query(Status).all()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    # Render the PDF template
    # The template can be anything
    html = render_template('edit_report.html', report=report,  onlyread=True, user=user, statuses=statuses)

    # Generate the PDF
    pdf = HTML(string=html).write_pdf()

    # Create a response with the PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=view_report_{report_id}.pdf'

    return response

@app.route('/view_report/<int:report_id>', methods=['GET', 'POST'])
def view_report(report_id):
    report = session.query(Report).get(report_id)
    if not report:
        abort(404)
    user_id = request.args.get('user_id')
    #user_id = request.args["user_id"] #kinda the same
    # Get the available statuses
    statuses = session.query(Status).all()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    
    
    if request.method == 'POST':
        # updated_data = {
        #     'status_id': int(request.form.get('status_id')),
        #     'calenderweek': datetime.strptime(request.form.get('calenderweek'), '%Y-%m-%d').date(),
        #     'mon': request.form.get('mon'),
        #     'tue': request.form.get('tue'),
        #     'wed': request.form.get('wed'),
        #     'thu': request.form.get('thu'),
        #     'fri': request.form.get('fri'),
        # }
        # for key, value in updated_data.items():
        #     setattr(report, key, value)
        # session.commit()
        return redirect(url_for('user_report_books', user_id=user_id))

    return render_template('edit_report.html', report=report, onlyread=True, user=user, statuses=statuses)

@app.route('/delete_report/<int:report_id>')
def delete_report(report_id):
    report = session.query(Report).get(report_id)
    
    if report:
        report_book_user_id = report.report_book.user_id  # Access the attribute before committing
        session.delete(report)
        session.commit()

        return redirect(url_for('user_report_books', user_id=report_book_user_id))

    # Handle the case where the report is not found
    return "Report not found", 404

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=5041)
