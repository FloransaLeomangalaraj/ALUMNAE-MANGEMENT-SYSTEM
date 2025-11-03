import os
import random
from datetime import date, datetime
import re
from urllib import request
import pymysql
import ar_master
import smtplib, ssl
from flask import Flask, render_template, flash, request, session, current_app, send_from_directory
from werkzeug.utils import redirect, secure_filename

port = 587
smtp_server = "smtp.gmail.com"
sender_email = "serverkey2018@gmail.com"
password ="Extazee2021"


app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
user='root'
password=''
host='127.0.0.1'
mm = ar_master.master_flask_code()

from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

@app.route("/")
def homepage():
    data = mm.select_direct_query("select * from alumni_details")
    return render_template('index.html',items=data)


@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        usern = mm.select_direct_query(
            "select * from admin_details where username='" + str(un) + "' and password='" + str(pa) + "'")
        if usern:
            session['admin'] = usern
            return render_template('admin_home.html', error=error)
        else:
            return render_template('admin.html', error=error)
    return render_template('admin.html')


@app.route("/admin_home")
def admin_home():
    return render_template('admin_home.html')


@app.route("/admin_add_staff", methods=['GET', 'POST'])
def admin_add_staff():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        qualification = request.form['qualification']
        address = request.form['address']
        gender = request.form['gender']
        experience = request.form['experience']
        department = request.form['department']
        password = request.form['password']

        maxin = mm.find_max_id("staff_details")  # Get next available ID
        qry = f"INSERT INTO staff_details VALUES ('{maxin}', '{name}', '{contact}', '{email}', '{qualification}', '{address}', '{gender}', '{experience}', '{department}', '{password}', '0', '0')"

        result = mm.insert_query(qry)  # Execute query

        if result:
            flash("✅ Staff Added Successfully!", "success")  # Flash success message
        else:
            flash("❌ Error! Could not register staff.", "danger")  # Flash error message

        return redirect(url_for('admin_add_staff'))  # Redirect to prevent resubmission

    return render_template('admin_add_staff.html')


@app.route("/admin_add_student", methods=['GET', 'POST'])
def admin_add_student():
    if request.method == 'POST':
       name = request.form['name']
       contact = request.form['contact']
       email = request.form['email']
       address = request.form['address']
       gender = request.form['gender']
       department = request.form['department']
       password = request.form['password']
       maxin = mm.find_max_id("student_details")
       qry = ("insert into student_details values('" + str(maxin) + "','" + str(name) + "','" + str(
        contact) + "','" + str(email) + "','" + str(address) + "','" + str(
        gender) + "','" + str(department) + "','" + str(password) + "','0','0')")
       result = mm.insert_query(qry)  # Execute query

       if result:
           flash("✅ Student Added Successfully!", "success")  # Flash success message
       else:
           flash("❌ Error! Could not register staff.", "danger")  # Flash error message

       return redirect(url_for('admin_add_student'))  # Redirect to prevent resubmission

    return render_template('admin_add_student.html')


@app.route("/admin_add_alumni", methods=['GET', 'POST'])
def admin_add_alumni():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        permanent_contact = request.form['permanent_contact']
        email = request.form['email']
        address = request.form['address']
        gender = request.form['gender']
        department = request.form['department']
        year_of_batch = request.form['year_of_batch']
        password = request.form['password']
        company_name = 'Not Defined'
        final_percentage = 'Not Defined'
        designation = 'Not Defined'
        profile_photo = 'not_defined.png'

        maxin = mm.find_max_id("alumni_details")
        qry = ("insert into alumni_details values('" + str(maxin) + "','" + str(name) + "','" + str(
            contact) + "','" + str(permanent_contact) + "','" + str(email) + "','" + str(address) + "','" + str(
            gender) + "','" + str(department) + "','" + str(year_of_batch) + "','" + str(password) + "','" + str(company_name) + "','" + str(final_percentage) + "','" + str(designation) + "','" + str(profile_photo) + "','0','0')")

        result = mm.insert_query(qry)

        if result:
            flash("✅Alumni Added Successfully!", "success")  # Flash success message
        else:
            flash("❌ Error! Could not register alumni.", "danger")  # Fix message

        print("Flash message added")  # ✅ DEBUG: Check if flash is triggered
        return redirect(url_for('admin_add_alumni'))  # Redirect to refresh page

    return render_template('admin_add_alumni.html')


@app.route("/admin_add_event", methods=['GET', 'POST'])
def admin_add_event():
    if request.method == 'POST':
       event_name = request.form['event_name']
       event_data = request.form['event_data']
       event_description = request.form['event_description']
       time = request.form['time']


       maxin = mm.find_max_id("event_details")
       qry = ("insert into event_details values('" + str(maxin) + "','" + str(event_name) + "','" + str(
        event_data) + "','" + str(event_description) + "','" + str(time) + "','0','0')")

       result = mm.insert_query(qry)  # Execute query

       if result:
           flash("✅ Event Added Successful!", "success")  # Flash success message
       else:
           flash("❌ Error! Could not register staff.", "danger")  # Flash error message

       return redirect(url_for('admin_add_event'))  # Redirect to prevent resubmission

    return render_template('admin_add_event.html')



@app.route("/admin_add_fund_request", methods=['GET', 'POST'])
def admin_add_fund_request():
    if request.method == 'POST':
       fund_for = request.form['fund_for']
       fund_amount = request.form['fund_amount']


       maxin = mm.find_max_id("fund_request_details")
       qry = ("insert into fund_request_details values('" + str(maxin) + "','" + str(fund_for) + "','" + str(fund_amount) + "','0','0')")
       result = mm.insert_query(qry)  # Execute query

       if result:
           flash("✅ Fund Request Sent!", "success")  # Flash success message
       else:
           flash("❌ Error! Could not register alumni.", "danger")  # Flash error message

       print("Flash message added")  # ✅ DEBUG: Check if flash is triggered
       return redirect(url_for('admin_add_fund_request'))  # Redirect to refresh page

    return render_template('admin_add_fund_request.html')



@app.route("/admin_add_gallery", methods=['GET', 'POST'])
def admin_add_gallery():
    if request.method == 'POST':
       function_name = request.form['function_name']

       f = request.files['file']
       f.save(os.path.join("static/uploads/", secure_filename(f.filename)))

       f2 = request.files['file2']
       f2.save(os.path.join("static/uploads/", secure_filename(f2.filename)))

       f3 = request.files['file3']
       f3.save(os.path.join("static/uploads/", secure_filename(f3.filename)))

       f4 = request.files['file4']
       f4.save(os.path.join("static/uploads/", secure_filename(f4.filename)))

       f5 = request.files['file5']
       f5.save(os.path.join("static/uploads/", secure_filename(f5.filename)))


       maxin = mm.find_max_id("gallery_details")
       qry = ("insert into gallery_details values('" + str(maxin)
              + "','" + str(function_name)
              + "','" + str(secure_filename(f.filename))
              + "','" + str(secure_filename(f2.filename))
              + "','" + str(secure_filename(f3.filename))
              + "','" + str(secure_filename(f4.filename))
              + "','" + str(secure_filename(f5.filename))
              + "','0','0')")
       result = mm.insert_query(qry)  # Execute query

       if result:
           flash("✅Gallery Added Successfully!", "success")  # Flash success message
       else:
           flash("❌ Error! Could not register alumni.", "danger")  # Flash error message

       print("Flash message added")  # ✅ DEBUG: Check if flash is triggered
       return redirect(url_for('admin_add_gallery'))  # Redirect to refresh page

    return render_template('admin_add_gallery.html')

@app.route("/admin_view_event")
def admin_view_event():
    data = mm.select_direct_query("select * from event_details")
    return render_template('admin_view_event.html',items=data)


@app.route("/admin_view_fund")
def admin_view_fund():
    data = mm.select_direct_query("select * from fund_request_details")
    return render_template('admin_view_fund.html',items=data)



@app.route("/admin_view_gallery")
def admin_view_gallery():
    data = mm.select_direct_query("select * from gallery_details")
    return render_template('admin_view_gallery.html',items=data)



@app.route("/admin_view_staff")
def admin_view_staff():
    data = mm.select_direct_query("select * from staff_details")
    return render_template('admin_view_staff.html',items=data)



@app.route("/admin_view_student")
def admin_view_student():
    data = mm.select_direct_query("select * from student_details")
    return render_template('admin_view_student.html',items=data)




@app.route("/admin_view_alumni")
def admin_view_alumni():
    data = mm.select_direct_query("select * from alumni_details")
    return render_template('admin_view_alumni.html',items=data)


@app.route("/admin_view_feedback")
def admin_view_feedback():
    data = mm.select_direct_query("select * from feedback_details")
    return render_template('admin_view_feedback.html',items=data)

############################################################################



@app.route("/alumni", methods=['GET', 'POST'])
def alumni():
    msg = ''
    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        usern = mm.select_direct_query(
            "select * from alumni_details where email='" + str(un) + "' and password='" + str(pa) + "'")
        if usern:
            session['alumni'] = un

            return render_template('alumni_home.html', msg=msg,items=usern)
        else:
            msg = 'Failed'
            return render_template('alumni.html', msg=msg)
    return render_template('alumni.html')



@app.route("/alumni_home")
def alumni_home():
    alumni=session['alumni']
    usern = mm.select_direct_query("select * from alumni_details where email='" + str(alumni) + "'")
    return render_template('alumni_home.html',items=usern)


@app.route("/alumni_home1", methods=['GET', 'POST'])
def alumni_home1():
    if request.method == 'POST':
        email1 = session['alumni']
        name = request.form['name']
        contact = request.form['contact']
        permanent_contact = request.form['permanent_contact']
        email = request.form['email']
        address = request.form['address']
        gender = request.form['gender']
        department = request.form['department']
        year_of_batch = request.form['year_of_batch']
        password = request.form['password']

        company_name = request.form['company_name']
        final_percentage = request.form['final_percentage']
        designation = request.form['designation']

        f1 = request.files['file']
        f1.save(os.path.join("static/uploads/", secure_filename(f1.filename)))

        session['alumni']=email
        qry = ("update alumni_details set name='" + str(name) + "',contact='" + str(
        contact) + "',permanent_contact='" + str(permanent_contact) + "',email='" + str(email) + "',address='" + str(address) + "',gender='" + str(
        gender) + "',department='" + str(department) + "',year_of_batch='" + str(year_of_batch) + "',password='" + str(password) + "',company_name='" + str(company_name) + "',final_percentage='" + str(final_percentage) + "',designation='" + str(designation) + "',profile_photo='" + str(secure_filename(f1.filename)) + "' where email='"+str(email1)+"'")
        result = mm.insert_query(qry)
        return alumni_home()
    return render_template('alumni_home.html')



@app.route("/alumni_view_event")
def alumni_view_event():
    data = mm.select_direct_query("select * from event_details")
    return render_template('alumni_view_event.html',items=data)


@app.route("/alumni_view_gallery")
def alumni_view_gallery():
    data = mm.select_direct_query("select * from gallery_details")
    return render_template('alumni_view_gallery.html',items=data)



@app.route("/alumni_view_fund_request")
def alumni_view_fund_request():
    data = mm.select_direct_query("select * from fund_request_details")
    return render_template('alumni_view_fund_request.html',items=data)


@app.route("/alumni_add_placement", methods=['GET', 'POST'])
def alumni_add_placement():
    if request.method == 'POST':
       company_name = request.form['company_name']
       required_skills = request.form['required_skills']
       interview_date = request.form['interview_date']
       interview_timing = request.form['interview_timing']

       alumni=session['alumni']
       maxin = mm.find_max_id("placement_details")
       qry = ("insert into placement_details values('" + str(maxin) + "','" + str(alumni) + "','" + str(company_name) + "','" + str(required_skills) + "','" + str(interview_date) + "','" + str(interview_timing) + "','0','0')")
       result = mm.insert_query(qry)  # Execute query

       if result:
           flash("✅Added Successfully!", "success")  # Flash success message
       else:
           flash("❌ Error! Could not register alumni.", "danger")  # Flash error message

       print("Flash message added")  # ✅ DEBUG: Check if flash is triggered
       return redirect(url_for('alumni_add_placement'))  # Redirect to refresh page

    return render_template('alumni_add_placement.html')


@app.route("/alumni_add_feedback", methods=['GET', 'POST'])
def alumni_add_feedback():
    if request.method == 'POST':
       feedback = request.form['feedback']
       alumni = session['alumni']
       maxin = mm.find_max_id("feedback_details")
       cdate=datetime.now()
       qry = ("insert into feedback_details values('" + str(maxin) + "','" + str(alumni) + "','" + str(feedback) + "','" + str(cdate) + "','0','0')")
       result = mm.insert_query(qry)  # Execute query

       if result:
           flash("✅Feedback Successfully Given!", "success")  # Flash success message
       else:
           flash("❌ Error! Could not register alumni.", "danger")  # Flash error message

       return redirect(url_for('alumni_add_feedback'))  # Redirect to refresh page

    return render_template('alumni_add_feedback.html')




@app.route("/alumni_donate_book", methods=['GET', 'POST'])
def alumni_donate_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        author = request.form['author']
        year_of_publish = request.form['year_of_publish']
        publication = request.form['publication']
        maxin = mm.find_max_id("donate_book_details")
        cdate=datetime.now()
        qry = ("insert into donate_book_details values('" + str(maxin) + "','" + str(alumni) + "','" + str(book_name) + "','" + str(author) + "','" + str(year_of_publish) + "','" + str(publication) + "','0','0')")
        result = mm.insert_query(qry)  # Execute query

        if result:
            flash("✅Book Donation Successful!", "success")  # Flash success message
        else:
            flash("❌ Error! Could not register alumni.", "danger")  # Flash error message

        return redirect(url_for('alumni_donate_book'))  # Redirect to refresh page

    return render_template('alumni_donate_book.html')



@app.route("/alumni_share_meetings", methods=['GET', 'POST'])
def alumni_share_meetings():
    if request.method == 'POST':

        alumni = session['alumni']
        meeting_date = request.form['meeting_date']
        topic = request.form['topic']
        total_hourse = request.form['total_hourse']
        days = request.form['days']
        meet_link = request.form['meet_link']

        cdate = datetime.now()


        maxin = mm.find_max_id("meeting_details")

        qry = ("insert into meeting_details values('" + str(maxin) + "','" + str(alumni) + "','" + str(meeting_date) + "','" + str(topic) + "','" + str(total_hourse) + "','" + str(days) + "','" + str(meet_link) + "','0','0')")
        # print(qry)

        result = mm.insert_query(qry)  # Execute query

        if result:
            flash("✅Information Successfully Sent!", "success")  # Flash success message
        else:
            flash("❌ Error! Could not register alumni.", "danger")  # Flash error message

        return redirect(url_for('alumni_share_meetings'))  # Redirect to refresh page

    return render_template('alumni_share_meetings.html')

@app.route("/staff", methods=['GET', 'POST'])
def staff():
    msg = ''
    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        usern = mm.select_direct_query(
            "select * from staff_details where email='" + str(un) + "' and password='" + str(pa) + "'")
        if usern:
            session['staff'] = un

            return render_template('staff_home.html', msg=msg,items=usern)
        else:
            msg = 'Failed'
            return render_template('staff.html', msg=msg)
    return render_template('staff.html')



@app.route("/staff_home")
def staff_home():
    return render_template('staff_home.html')


@app.route("/student", methods=['GET', 'POST'])
def student():
    msg = ''
    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        usern = mm.select_direct_query(
            "select * from student_details where email='" + str(un) + "' and password='" + str(pa) + "'")
        if usern:
            session['student'] = un

            return render_template('student_home.html', msg=msg,items=usern)
        else:
            msg = 'Failed'
            return render_template('student.html', msg=msg)
    return render_template('student.html')



@app.route("/student_home")
def student_home():
    return render_template('student_home.html')



@app.route("/student_view_job")
def student_view_event():
    data = mm.select_direct_query("select * from placement_details")
    return render_template('student_view_job.html',items=data)



@app.route("/student_view_meet")
def student_view_meet():
    data = mm.select_direct_query("select * from meeting_details")
    return render_template('student_view_meet.html',items=data)



@app.route("/student_view_gallery")
def student_view_gallery():
    data = mm.select_direct_query("select * from gallery_details")
    return render_template('student_view_gallery.html',items=data)

@app.route("/student_view_books")
def student_view_books():
    data=  mm.select_direct_query("select * from donate_book_details")
    return  render_template("student_view_books.html",items=data)


############################################################################
if __name__ == '__main__':
    # app.run(debug=True, use_reloader=True)
    app.run(host='0.0.0.0', port=5501,debug=True)
