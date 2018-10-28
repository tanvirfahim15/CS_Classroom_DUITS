#!/usr/bin/env python
# encoding: utf-8


from flask import Flask, request, session, g, redirect, url_for, render_template, Blueprint
from werkzeug.utils import secure_filename
import sqlite3
import os
import xlrd
from bson import ObjectId
from flask import Flask, render_template, request, redirect, session
from Database.database import db

# from AdapterPattern import testquery, doquery
# from AdapterPattern.AdapteeSql import AdapteeSql
# from AdapterPattern.SqlAdapter import SqlAdapter
from classes.management_class.BasicStudent import BasicStudent
from classes.management_class.ObserverPattern.AdminObserver import AdminObserver
from classes.management_class.ObserverPattern.EnrollmentData import EnrollmentData
from classes.management_class.addStudent import MyServer




#reload(sys)
#sys.setdefaultencoding('utf-8')
from classes.management_class.ageToppings import ageToppings
from classes.management_class.genderTopping import genderToppings
from classes.management_class import nameToppings
from classes.management_class.passwordToppings import passwordToppings
from classes.management_class import phonenumberToppings
from classes.management_class.studentidtoppings import studentidtoppings

app = Flask(__name__)
# app = Blueprint('StuManager', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'score')
ALLOWED_EXTENSIONS = set(['xls', 'XLS'], )
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'School.db'),
    DEBUG=False,
    SECRET_KEY='NiCaiBuDao',
))


#	---------------Database connection start---------------
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'sqlite_db'):  # 未连接数据库
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#	--------------数据库连接end------------------------

#	--------------用户管理部分start----------------------
@app.route('/')
@app.route('/index')
def index():
    return render_template('educational_management/index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    cursor = get_db()
    if request.method == "POST":
        sql = "select * from user where username = ?"
        result_set = cursor.execute(sql, (request.form['username'],))
        result = result_set.fetchone()
        if not result:
            error = "Username does not exist"
        elif result[1] != request.form['password']:
            error = "wrong password"
        elif result[2] != request.form['role']:
            error = "Role error"
        else:
            error = None
            session['role'] = request.form['role']
            session['username'] = request.form['username']
            session['lasttime'] = result[3]
            session['period'] = cursor.execute("SELECT period FROM period").fetchone()[0]
            cursor.execute("UPDATE user SET lasttime = datetime('now','localtime') WHERE username=?",
                           (request.form['username'],))
            cursor.commit()
            msg = "Successful login, welcome" + result[0] + "Last login time is：" + result[3]
            return redirect(url_for(session['role'] + '_frame'))
    return render_template('educational_management/login.html', error=error)


@app.route('/logoutall')
def logoutall():
    return render_template('educational_management/logoutall.html')


@app.route('/logout')
def logout(info=None):
    error = None
    session.pop('role', None)
    session.pop('username', None)
    session.pop('lasttime', None)
    return redirect(url_for('login'))


@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']
        if newpassword != confirmpassword:
            return fail_msg("Confirm password does not match, please re-enter", return_url=url_for('change_password'))
        username = session['username']
        cursor = get_db()
        confirmpass = cursor.execute("SELECT * FROM user WHERE username = ? AND password = ? ",
                                     (username, oldpassword)).fetchone()
        if confirmpass:
            cursor.execute("UPDATE user SET password = ? WHERE username = ?", (newpassword, username))
            cursor.commit()
            return success_msg(content="The password has been modified successfully. Please log in again.", return_url="/logoutall")
        else:
            return fail_msg(content="The old password is incorrect, please re-enter", return_url="/change_password")

    return render_template('educational_management/change_password.html')


#   ---------------用户部分end---------------------

#   ---------------管理员页面start-----------------
@app.route('/admin_main')
def admin_main():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    count_s = cursor.execute("SELECT count(*) FROM student").fetchone()[0]
    count_t = cursor.execute("SELECT count(*) FROM teacher").fetchone()[0]
    count_c = cursor.execute("SELECT count(*) FROM course").fetchone()[0]
    period = cursor.execute("SELECT period FROM period").fetchone()[0]
    data = dict()
    data['username'] = session['username']
    data['lasttime'] = session['lasttime']
    data['count_c'] = count_c
    data['count_s'] = count_s
    data['count_t'] = count_t
    data['period'] = period
    return render_template('educational_management/admin_main.html', data=data)


@app.route('/admin_frame')
def admin_frame():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/admin_frame.html')


@app.route('/admin_cou')
def admin_cou():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/admin_cou.html')


@app.route('/admin_cou_add', methods=['POST', 'GET'])
def admin_cou_add():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        cursor = get_db()
        cno = request.form['cno']
        cname = request.form['cname']
        ccredit = request.form['ccredit']
        result_set = cursor.execute("SELECT * FROM course WHERE cno =?", (cno,))
        if result_set.fetchone():
            return fail_msg(content="The course already exists", return_url='/admin_cou_add')
        else:
            sql = "insert into course(cno,cname,ccredit) values(?,?,?)"
            cursor.execute(sql, (cno, cname, ccredit))
            cursor.commit()
            return success_msg(content="Successfully added courses", return_url=url_for('admin_cou_add'))
    return render_template('educational_management/admin_cou_add.html')


@app.route('/admin_cou_import', methods=['POST', 'GET'])
def admin_cou_import():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        import_xls = request.files['import_xls']
        if import_xls and allowed_file(import_xls.filename):
            import_xls_name = secure_filename(import_xls.filename)
            import_xls.save(os.path.join(app.config['UPLOAD_FOLDER'], import_xls_name))
        stu_table = xlrd.open_workbook('static/score/' + import_xls_name).sheets()[0]
        count_row = stu_table.nrows
        cursor = get_db()
        for i in range(count_row):
            cno = stu_table.row_values(i)[0]
            cname = stu_table.row_values(i)[1]
            ccredit = int(stu_table.row_values(i)[2])
            result_set = cursor.execute("SELECT * FROM course WHERE cno =?", (cno,))
            if not result_set.fetchone():
                sql = "insert into course(cno,cname,ccredit) values(?,?,?)"
                cursor.execute(sql, (cno, cname, ccredit))
                cursor.commit()
        cursor.commit()
        return success_msg(content="Successfully imported course", return_url=url_for('admin_cou_add'))
    return render_template('educational_management/admin_cou_add.html')


@app.route('/admin_cou_del', methods=['POST', 'GET'])
@app.route('/admin_cou_del/<cno>', methods=['POST', 'GET'])
def admin_cou_del(cno=None):
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method != 'POST' and not cno:
        return render_template('educational_management/admin_cou_del.html')
    cursor = get_db()
    if not cno:
        cno = request.form['cno']
    result_set = cursor.execute("SELECT * FROM course WHERE cno =?", (cno,))
    if not result_set.fetchone():
        return fail_msg(content="The course does not exist", return_url='/admin_cou_del')
    cou = cursor.execute("SELECT * FROM tc WHERE cno =?", (cno,)).fetchone()
    if cou:
        return fail_msg("Some teachers have opened this course and cannot delete it.", '/admin_cou_del')
    cursor.execute("DELETE FROM course WHERE cno=?", (cno,))
    cursor.commit()
    return success_msg(content="successfully deleted", return_url=url_for('admin_cou_del'))


@app.route('/admin_cou_sel')
def admin_cou_sel():
    if not session.get('role') or (session['role'] != 'admin' and session['role'] != 'teacher'):
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)

    cursor = get_db()

    query = "select * from course "
    print(query)
    course_result_set = cursor.execute(query)

    data = []
    for cou in course_result_set:
        info = []
        info.append(cou[0])
        info.append(cou[1])
        info.append(cou[2])
        print(info)
        data.append(info)

    return render_template('educational_management/admin_cou_sel.html', course_data=data)


@app.route('/admin_cou_selrs', methods=['POST', 'GET'])
def admin_cou_selrs():
    if not session.get('role') or (session['role'] != 'admin' and session['role'] != 'teacher'):
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        cno = '%' + request.form['cno'] + '%'
        cname = '%' + request.form['cname'] + '%'
        ccredit = '%' + request.form['ccredit'] + '%'
        sql = "select * from course where cno like ? and cname like ? and ccredit like ?"
        cursor = get_db()
        result_set = cursor.execute(sql, (cno, cname, ccredit))
        cous = result_set.fetchall()
        data = []
        for cou in cous:
            info = dict()
            info['cno'] = cou[0]
            info['cname'] = cou[1]
            info['ccredit'] = cou[2]
            data.append(info)
        return render_template('educational_management/xadmin_cou_selrs.html', data=data)
    return render_template('educational_management/admin_cou_sel.html')


@app.route('/admin_cou_set')
@app.route('/admin_cou_set/<period>')
def admin_cou_set(period=None):
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if period == 'begin':
        cursor = get_db()
        sql = "update period set period='Elective course'"
        cursor.execute(sql)
        sql = "update period set date=datetime('now','localtime')"
        cursor.commit()
        session['period'] = "Elective course"
        return success_msg(content=u"Start the course setting successfully", return_url='/admin_cou_set')
    elif period == 'end':
        cursor = get_db()
        sql = "update period set period='Learn'"
        cursor.execute(sql)
        sql = "update period set date=datetime('now','localtime')"
        cursor.commit()
        session['period'] = "Learn"
        return success_msg(content=u'End the course setting successfully', return_url='/admin_cou_set')
    else:
        return render_template('educational_management/xadmin_cou_set.html')


@app.route('/admin_cou_upd', methods=['POST', 'GET'])
@app.route('/admin_cou_upd/<cno>', methods=['POST', 'GET'])
def admin_cou_upd(cno=None):

    print("In course update")
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method != 'POST' and not cno:

        enroll_stu = []
        for data in db.xenrolled_student.find():
                stu={}
                stu['sno']=data['sno']
                stu['cno']=data['cno']
                enroll_stu.append(stu)

        enroll_tea = []
        for data in db.xenrolled_techer.find():
            tea = {}
            tea['tno'] = data['tno']
            tea['cno'] = data['cno']
            enroll_tea.append(tea)

        # enroll_stu = db.xenrolled_student.find("sno"  , "cno")
        # enroll_stu= db.xenrolled_student.({"sno": str(sno)})
        # enroll_tech = db.xenrolled_techer.find("tno"  , "cno")
        #
        # s = list(enroll_stu)
        # stu_list={}
        # stu_list['cno']=s[0]
        # stu_list['sno']=s[1]
        # t= list(enroll_tech)
        # tea_list ={}
        # tea_list['cno'] = t[0]
        # tea_list['sno'] = t[1]


        print(enroll_tea)
        print(enroll_stu)
        return render_template('educational_management/xadmin_cou_upd.html', stu_list=enroll_stu, tea_list=enroll_tea)

    if not cno:
        cno = request.form['cno']
    cursor = get_db()
    result_set = cursor.execute("SELECT * FROM course WHERE cno=?", (cno,))
    data = result_set.fetchone()
    if data:
        return render_template('educational_management/xadmin_cou_updrs.html', data=data)
    else:
        return fail_msg(content="The course does not exist", return_url="/admin_cou_upd")


@app.route('/admin_cou_updrs', methods=['POST', 'GET'])
def admin_cou_updrs():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        cursor = get_db()
        cno = request.form['cno']
        cname = request.form['cname']
        ccredit = request.form['ccredit']
        cursor.execute("UPDATE course SET cname=?,ccredit=? WHERE cno = ?", (cname, ccredit, cno))
        cursor.commit()
        return success_msg(content="Course information updated successfully", return_url='/admin_cou_upd')
    return render_template('educational_management/xadmin_cou_upd.html')


@app.route('/admin_navi')
def admin_navi():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/admin_navi.html')


@app.route('/admin_stu')
def admin_stu():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/admin_stu.html')


# class MyServer:
#     def __init__(self):
#         self.globalData = "hello"
#
#
#     def function(self):
#         print("Here1")
#         return render_template("admin_stu_add.html")
#
#     def admin_stu_add(self):
#         print("Here2")
#         if not session.get('role') or session['role'] != 'admin':
#             error = "You are not logged in or you are not an administrator"
#             return render_template("login.html", error=error)
#         if request.method == 'POST':
#             cursor = get_db()
#             sno = request.form['sno']
#             sname = request.form['sname']
#             ssex = request.form['ssex']
#             sage = request.form['sage']
#             sdept = request.form['sdept']
#             sphone = request.form['sphone']
#             spassword = request.form['spassword']
#             result_set = cursor.execute("SELECT * FROM student WHERE sno =?", (sno,))
#             if result_set.fetchone():
#                 return fail_msg(content="The student already exists", return_url='/admin_stu_add')
#             else:
#                 sql = "insert into student(sno,sname,ssex,sage,sdept,sphone) values(?,?,?,?,?,?)"
#                 cursor.execute(sql, (sno, sname, ssex, sage, sdept, sphone))
#                 cursor.execute("INSERT INTO user(username,password,role,lasttime) VALUES(?,?,?,?)",
#                                (sno, spassword, 'student', u'You are logging in to the system for the first time.'))
#                 cursor.commit()
#                 return success_msg(content="Successfully added the student", return_url=url_for('admin_stu_add'))
#         return render_template('admin_stu_add.html')


# 增加学生
my_server = MyServer()
my_person= BasicStudent()

@app.route('/admin_stu_add', methods=['POST', 'GET'])  #, methods=['POST', 'GET']
def admin_stu_add():
    global my_person
    return my_server.admin_stu_add(my_person)




@app.route('/receivedata', methods=['POST'])
def receive_data():
    global my_person
    print("in receiving")

    if(request.form.get('sno')!=None):
        my_person= studentidtoppings(request.form.get('sno'),my_person)
        # print(request.form.get('sno'))

    if (request.form.get('sname') != None):
        my_person = nameToppings(request.form.get('sname'), my_person)
        # print(request.form.get('sname'))

    if (request.form.get('ssex') != None):
        my_person = genderToppings(request.form.get('ssex'), my_person)

    if (request.form.get('sage') != None):
        my_person = ageToppings(request.form.get('sage'), my_person)

    if (request.form.get('sphone') != None):
        my_person = phonenumberToppings(request.form.get('sphone'), my_person)

    if (request.form.get('spassword') != None):
        my_person = passwordToppings(request.form.get('spassword'), my_person)


    print(my_person.getDescription())

    # print(request.form.get('ssex'))
    # print(request.form.get('sage'))
    # print(request.form.get('sphone'))
    # print(request.form.get('spassword'))



    return "shohan"

#
# @app.route('/admin_stu_add', methods=['POST', 'GET'])
# def admin_stu_add():
#     if not session.get('role') or session['role'] != 'admin':
#         error = "You are not logged in or you are not an administrator"
#         return render_template("login.html", error=error)
#     if request.method == 'POST':
#         cursor = get_db()
#         sno = request.form['sno']
#         sname = request.form['sname']
#         ssex = request.form['ssex']
#         sage = request.form['sage']
#         sdept = request.form['sdept']
#         sphone = request.form['sphone']
#         spassword = request.form['spassword']
#         result_set = cursor.execute("SELECT * FROM student WHERE sno =?", (sno,))
#         if result_set.fetchone():
#             return fail_msg(content="The student already exists", return_url='/admin_stu_add')
#         else:
#             sql = "insert into student(sno,sname,ssex,sage,sdept,sphone) values(?,?,?,?,?,?)"
#             cursor.execute(sql, (sno, sname, ssex, sage, sdept, sphone))
#             cursor.execute("INSERT INTO user(username,password,role,lasttime) VALUES(?,?,?,?)",
#                            (sno, spassword, 'student', u'You are logging in to the system for the first time.'))
#             cursor.commit()
#             return success_msg(content="Successfully added the student", return_url=url_for('admin_stu_add'))
#     return render_template('admin_stu_add.html')


@app.route('/admin_stu_import', methods=['POST', 'GET'])
def admin_stu_import():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        import_xls = request.files['import_xls']
        if import_xls and allowed_file(import_xls.filename):
            import_xls_name = secure_filename(import_xls.filename)
            import_xls.save(os.path.join(app.config['UPLOAD_FOLDER'], import_xls_name))
        stu_table = xlrd.open_workbook('static/score/' + import_xls_name).sheets()[0]
        count_row = stu_table.nrows
        cursor = get_db()
        for i in range(count_row):
            sno = stu_table.row_values(i)[0]
            sname = stu_table.row_values(i)[1]
            ssex = stu_table.row_values(i)[2]
            sage = int(stu_table.row_values(i)[3])
            sdept = stu_table.row_values(i)[4]
            sphone = int(stu_table.row_values(i)[5])
            spassword = stu_table.row_values(i)[6]
            result_set = cursor.execute("SELECT * FROM student WHERE sno =?", (sno,))
            if not result_set.fetchone():
                sql = "insert into student(sno,sname,ssex,sage,sdept,sphone) values(?,?,?,?,?,?)"
                cursor.execute(sql, (sno, sname, ssex, sage, sdept, sphone))
                cursor.execute("INSERT INTO user(username,password,role,lasttime) VALUES(?,?,?,?)",
                               (sno, spassword, 'student', u'You are logging in to the system for the first time.'))
        cursor.commit()
        return success_msg(content="Successfully imported students", return_url=url_for('admin_stu_add'))
    return render_template('educational_management/admin_stu_add.html')


# 删除学生
@app.route('/admin_stu_del/<sno>', methods=['POST', 'GET'])
@app.route('/admin_stu_del', methods=['POST', 'GET'])
def admin_stu_del(sno=None):
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method != 'POST' and not sno:
        return render_template('educational_management/admin_stu_del.html')
    cursor = get_db()
    if not sno:
        sno = request.form['sno']
    result_set = cursor.execute("SELECT * FROM student WHERE sno =?", (sno,))
    if not result_set.fetchone():
        return fail_msg(content="The student does not exist", return_url='/admin_stu_del')
    cursor.execute("DELETE FROM user WHERE username=?", (sno,))
    cursor.execute("DELETE FROM student WHERE sno=?", (sno,))
    cursor.execute("DELETE FROM sc WHERE sno=?", (sno,))
    cursor.commit()
    return success_msg(content="successfully deleted", return_url=url_for('admin_stu_del'))


@app.route('/admin_stu_sel')
def admin_stu_sel():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)

    cursor = get_db()

    query = "select * from student "
    print(query)
    student_result_set = cursor.execute(query)

    data = []
    for cou in student_result_set:
        info = []
        info.append(cou[0])
        info.append(cou[1])
        info.append(cou[4])
        info.append(cou[5])
        print(info)
        data.append(info)

    # print(student_result_set)
    # return render_template('student_enter_course.html', student_data=data)

    return render_template('educational_management/admin_stu_sel.html', student_data=data)


@app.route('/admin_stu_selrs', methods=['POST', 'GET'])
def admin_stu_selrs():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        sno = '%' + request.form['sno'] + '%'
        sname = '%' + request.form['sname'] + '%'
        sdept = '%' + request.form['sdept'] + '%'
        sql = "select * from student where sno like ? and sname like ? and sdept like ?"
        cursor = get_db()
        result_set = cursor.execute(sql, (sno, sname, sdept))
        stus = result_set.fetchall()
        data = []
        for stu in stus:
            info = dict()
            password = cursor.execute("SELECT password FROM user WHERE username= ?", (stu[0],)).fetchone()[0]
            sum_credit = cursor.execute("SELECT sum(ccredit) FROM sc ,course\
                                         WHERE sc.cno = course.cno AND grade >60 AND sno =?", (stu[0],)).fetchone()
            avg_grade = cursor.execute("SELECT avg(grade) FROM sc,course\
                                         WHERE sc.cno=course.cno AND sno=?", (stu[0],)).fetchone()
            info['sno'] = stu[0]
            info['sname'] = stu[1]
            info['ssex'] = stu[2]
            info['sage'] = stu[3]
            info['sphone'] = stu[4]
            info['sdept'] = stu[5]
            info['spassword'] = password;
            if not avg_grade or not avg_grade[0]:
                info['avg_grade'] = 0
            else:
                info['avg_grade'] = avg_grade[0]
            rank = cursor.execute("SELECT count(*)+1 AS count\
                                  FROM (SELECT sno ,avg(grade) AS stu_avg\
                                  FROM sc,course WHERE sc.cno=course.cno GROUP BY sno)\
                                  WHERE stu_avg>?", (info['avg_grade'],)).fetchone()
            if rank:
                info['rank'] = rank[0]
            else:
                info['rank'] = 1
            if sum_credit and sum_credit[0]:
                info['sum_credit'] = sum_credit[0]
            else:
                info['sum_credit'] = 0
            data.append(info)
        return render_template('educational_management/xadmin_stu_selrs.html', data=data)
    return redirect(url_for('admin_stu_sel'))


# 更新学生信息
@app.route('/admin_stu_upd', methods=['GET', 'POST'])
@app.route('/admin_stu_upd/<sno>', methods=['GET', 'POST'])
def admin_stu_upd(sno=None):
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method != 'POST' and not sno:
        return render_template('educational_management/xadmin_stu_upd.html')
    if not sno:
        sno = request.form['sno']
    cursor = get_db()
    result_set = cursor.execute("SELECT * FROM student WHERE sno=?", (sno,))
    data = result_set.fetchone()
    if data:
        password = cursor.execute("SELECT password FROM user WHERE username = ?", (sno,)).fetchone()[0]
        return render_template('educational_management/xadmin_stu_updrs.html', data=data, spassword=password)
    else:
        return fail_msg(content="The student does not exist", return_url="/admin_stu_upd")


@app.route('/admin_stu_updrs', methods=['GET', 'POST'])
def admin_stu_updrs():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
        return success_msg(content="Student information updated successfully", return_url='/admin_stu_upd')
    if request.method == 'POST':
        cursor = get_db()
        sno = request.form['sno']
        sname = request.form['sname']
        ssex = request.form['ssex']
        sage = request.form['sage']
        sdept = request.form['sdept']
        sphone = request.form['sphone']
        spassword = request.form['spassword']
        cursor.execute("UPDATE student SET sname=?,sage=?,ssex=?,sdept=?,sphone=? WHERE sno=?",
                       (sname, sage, ssex, sdept, sphone, sno))
        cursor.execute("UPDATE user SET password=? WHERE username = ?", (spassword, sno))
        cursor.commit()
        return success_msg(content="Student information updated successfully", return_url='/admin_stu_upd')
    return render_template('educational_management/xadmin_stu_upd.html')


@app.route('/admin_tea')
def admin_tea():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/admin_tea.html')


@app.route('/admin_tea_add', methods=['POST', 'GET'])
def admin_tea_add():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        tno = request.form['tno']
        tname = request.form['tname']
        tphone = request.form['tphone']
        tpassword = request.form['tpassword']
        cursor = get_db()
        result_set = cursor.execute("SELECT * FROM teacher WHERE tno=?", (tno,))
        if result_set.fetchone():
            return fail_msg(content='Teacher ID already exists', return_url='/admin_tea_add')
        cursor.execute("INSERT INTO teacher(tno,tname,tphone) VALUES(?,?,?)", (tno, tname, tphone))
        cursor.execute("INSERT INTO user(username,password,role,lasttime) VALUES(?,?,?,?)",
                       (tno, tpassword, 'teacher', u'You are logging in to the system for the first time.'))
        cursor.commit()
        return success_msg(content='Successful teacher entry', return_url='/admin_tea_add')
    return render_template('educational_management/admin_tea_add.html')


@app.route('/admin_tea_import', methods=['POST', 'GET'])
def admin_tea_import():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        import_xls = request.files['import_xls']
        if import_xls and allowed_file(import_xls.filename):
            import_xls_name = secure_filename(import_xls.filename)
            import_xls.save(os.path.join(app.config['UPLOAD_FOLDER'], import_xls_name))
        stu_table = xlrd.open_workbook('static/score/' + import_xls_name).sheets()[0]
        count_row = stu_table.nrows
        cursor = get_db()
        for i in range(count_row):
            tno = stu_table.row_values(i)[0]
            tname = stu_table.row_values(i)[1]
            tphone = int(stu_table.row_values(i)[2])
            tpassword = stu_table.row_values(i)[3]
            result_set = cursor.execute("SELECT * FROM teacher WHERE tno =?", (tno,))
            if not result_set.fetchone():
                sql = "insert into teacher(tno,tname,tphone) values(?,?,?)"
                cursor.execute(sql, (tno, tname, tphone))
                cursor.execute("INSERT INTO user(username,password,role,lasttime) VALUES(?,?,?,?)",
                               (tno, tpassword, 'teacher', u'You are logging in to the system for the first time.'))
        cursor.commit()
        return success_msg(content="Successfully imported teachers", return_url=url_for('admin_tea_add'))
    return render_template('educational_management/admin_tea_add.html')


# 删除教师
@app.route('/admin_tea_del/<tno>', methods=['POST', 'GET'])
@app.route('/admin_tea_del', methods=['POST', 'GET'])
def admin_tea_del(tno=None):
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method != 'POST' and not tno:
        return render_template('educational_management/admin_tea_del.html')
    cursor = get_db()
    if not tno:
        tno = request.form['tno']
    result_set = cursor.execute("SELECT * FROM teacher WHERE tno=?", (tno,))
    if not result_set.fetchone():
        return fail_msg(content='Teacher ID does not exist', return_url='/admin_tea_del')
    cou = cursor.execute("SELECT * FROM tc WHERE tno=?", (tno,)).fetchone()
    if cou:
        return fail_msg("This teacher started the course and cannot be deleted.", '/admin_tea_del')
    cursor.execute("DELETE FROM user WHERE username=?", (tno,))
    cursor.execute("DELETE FROM teacher WHERE tno=?", (tno,))
    cursor.commit()
    return success_msg(content="successfully deleted", return_url=url_for('admin_tea_del'))


@app.route('/admin_tea_sel')
def admin_tea_sel():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)

    cursor = get_db()

    query = "select * from teacher "
    print(query)
    teacher_result_set = cursor.execute(query)

    data = []
    for cou in teacher_result_set:
        info = []
        info.append(cou[0])
        info.append(cou[1])
        info.append(cou[2])
        print(info)
        data.append(info)



    return render_template('educational_management/admin_tea_sel.html', teacher_data=data)


@app.route('/admin_tea_selrs', methods=['POST', 'GET'])
def admin_tea_selrs():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        tno = '%' + request.form['tno'] + '%'
        tname = '%' + request.form['tname'] + '%'
        sql = "select * from teacher where tno like ? and tname like ?"
        cursor = get_db()
        result_set = cursor.execute(sql, (tno, tname))
        teas = result_set.fetchall()
        data = []
        for tea in teas:
            info = dict()
            tpassword = cursor.execute("SELECT password FROM user WHERE username= ?", (tea[0],)).fetchone()[0]
            info['tno'] = tea[0]
            info['tname'] = tea[1]
            info['tphone'] = tea[2]
            info['tpassword'] = tpassword
            data.append(info)
        return render_template('educational_management/xadmin_tea_selrs.html', data=data)
    return render_template('educational_management/xadmin_tea_selrs.html')


@app.route('/admin_tea_upd', methods=['POST', 'GET'])
@app.route('/admin_tea_upd/<tno>', methods=['POST', 'GET'])
def admin_tea_upd(tno=None):
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method != 'POST' and not tno:
        return render_template('educational_management/xadmin_tea_upd.html')
    cursor = get_db()
    if not tno:
        tno = request.form['tno']
    result_set = cursor.execute("SELECT * FROM teacher WHERE tno=?", (tno,))
    data = result_set.fetchone()
    if data:
        password = cursor.execute("SELECT password FROM user WHERE username = ?", (tno,)).fetchone()[0]
        return render_template('educational_management/xadmin_tea_updrs.html', data=data, tpassword=password)
    else:
        return fail_msg(content="The teacher does not exist", return_url="/admin_tea_upd")
    return render_template('educational_management/xadmin_tea_upd.html')


@app.route('/admin_tea_updrs', methods=['POST', 'GET'])
def admin_tea_updrs():
    if not session.get('role') or session['role'] != 'admin':
        error = "You are not logged in or you are not an administrator"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        cursor = get_db()
        tno = request.form['tno']
        tname = request.form['tname']
        tphone = request.form['tphone']
        tpassword = request.form['tpassword']
        cursor.execute("UPDATE teacher SET tname=?,tphone=? WHERE tno=?", (tname, tphone, tno))
        cursor.execute("UPDATE user SET password=? WHERE username = ?", (tpassword, tno))
        cursor.commit()
        return success_msg(content="Teacher information updated successfully", return_url='/admin_tea_upd')
    return render_template('educational_management/xadmin_tea_upd.html')


#   --------------------管理员end---------------

#   --------------------student start---------------

@app.route('/student_cho')    #gives the animation
def student_cho():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/student_cho.html')


@app.route('/student_cho_del/<cno>', methods=['POST', 'GET'])  #deletes a course
def student_cho_del(cno):
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    if cursor.execute("SELECT period FROM period ").fetchone()[0] != "Elective course":
        return fail_msg("It is not a class time now.，Cannot delete course")
    cursor.execute("DELETE FROM sc WHERE sno=? AND cno=?", (session['username'], cno))
    print(session['username'])
    cursor.commit()
    return success_msg("successfully deleted", "/student_cho_sub")


# Edited by me
# not done yet
# adaptee= AdapteeSql()
# adapter= SqlAdapter(adaptee)
@app.route('/student_enter_course/<cno>', methods=['POST', 'GET'])
def student_enter_course(cno):

    # adapter.queryStudent()
    # doquery(adapter)

    cursor = get_db()

    query= "select * from student where sno in (SELECT sno from sc where cno=\'COM0018')"
    # query="SELECT sno from sc where cno=\'COM0018'"
    print(query)
    student_result_set= cursor.execute(query)

    data = []
    for cou in student_result_set:
        info =[]
        info.append(cou[0])
        info.append(cou[1])
        print(info)
        data.append(info)

    # print(student_result_set)
    return render_template('educational_management/student_enter_course.html', student_data=data)


@app.route('/student_cho_sel', methods=['POST', 'GET'])  #Query course information
def student_cho_sel():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    # if request.method == 'POST':
    #     cno = '%' + request.form['cno'] + '%'
    #     cname = '%' + request.form['cname'] + '%'
    #     ccredit = '%' + request.form['ccredit'] + '%'
    #     ctime = '%' + request.form['ctime1'] + request.form['ctime2'] + '%'
    #     clocation = '%' + request.form['clocation'] + '%'
    #     tname = '%' + request.form['tname'] + '%'
    #     cursor = get_db()
    #     result_set = cursor.execute("SELECT course.cno,cname,ccredit,clocation,cmaxcount,teacher.tno,tname,ctime FROM teacher,tc,course WHERE\
    #                                 tc.cno=course.cno AND tc.tno=teacher.tno AND tc.tno LIKE ? AND cname LIKE ? AND ccredit LIKE ? AND ctime LIKE ?\
    #                                 AND clocation LIKE ? AND tname LIKE ?",
    #                                 (cno, cname, ccredit, ctime, clocation, tname)).fetchall()
    #     data = []
    #     for cou in result_set:
    #         info = dict()
    #         info['cno'] = cou[0]
    #         info['cname'] = cou[1]
    #         info['ccredit'] = cou[2]
    #         info['clocation'] = cou[3]
    #         info['cmaxcount'] = cou[4]
    #         info['tno'] = cou[5]
    #         info['tname'] = cou[6]
    #         info['ctime'] = cou[7]
    #         res = cursor.execute("SELECT count(*) FROM sc WHERE cno=?", (cou[0],)).fetchone()
    #         info['cselected'] = res[0]
    #         data.append(info)
    #     return render_template('student_cho_selrs.html', data=data)

    cursor = get_db()

    query = "select * from course "
    print(query)
    course_result_set = cursor.execute(query)

    data = []
    for cou in course_result_set:
        info = []
        info.append(cou[0])
        info.append(cou[1])
        info.append(cou[2])
        print(info)
        data.append(info)

    # return render_template('admin_cou_sel.html', course_data=data)

    return render_template('educational_management/student_cho_sel.html', course_data=data)


@app.route('/student_cho_sel_cno/<cno>', methods=['POST', 'GET'])
def student_cho_sel_cno(cno=None):
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    if not cno:
        return fail_msg("The course does not exist！")
    cursor = get_db()
    cou = cursor.execute("SELECT course.cno,cname,ccredit,clocation,cmaxcount,teacher.tno,tname,ctime FROM teacher,tc,course WHERE\
                                    tc.cno=course.cno AND tc.tno=teacher.tno AND tc.cno=?", (cno,)).fetchone()
    data = []
    info = dict()
    info['cno'] = cou[0]
    info['cname'] = cou[1]
    info['ccredit'] = cou[2]
    info['clocation'] = cou[3]
    info['cmaxcount'] = cou[4]
    info['tno'] = cou[5]
    info['tname'] = cou[6]
    info['ctime'] = cou[7]
    res = cursor.execute("SELECT count(*) FROM sc WHERE cno=?", (cou[0],)).fetchone()
    info['cselected'] = res[0]
    data.append(info)
    return render_template('educational_management/student_cho_selrs.html', data=data)


@app.route('/student_cou_cloud')
def student_cou_cloud():
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    cous = cursor.execute(
        "SELECT sc.cno,cname,count(*) AS count FROM sc,course WHERE sc.cno = course.cno GROUP BY sc.cno ORDER BY sc.cno DESC LIMIT 0,10").fetchall()
    tags = "<tags>"
    for cou in cous:
        link = "<a href='/student_cho_sel_cno/" + cou[0] + "' style='22' color='0xff0000' hicolor='0x00cc00'>" + cou[
            0] + "</a>"
        tags = tags + link
    tags = tags + "</tags>"
    print("zheli")
    print(tags)
    return render_template('educational_management/tags_cloud.html', title='Popular course', tags=tags)


# 学生标签云
@app.route('/student_stu_sel_sno/<sno>', methods=['POST', 'GET'])
def student_sel_sno(sno=None):
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    stu = cursor.execute("SELECT * FROM student WHERE sno=?", (sno,)).fetchone()
    data = []
    info = dict()
    sum_credit = cursor.execute("SELECT sum(ccredit) FROM sc ,course\
                                 WHERE sc.cno = course.cno AND grade >60 AND sno =?", (stu[0],)).fetchone()
    avg_grade = cursor.execute("SELECT avg(grade) FROM sc,course\
                                 WHERE sc.cno=course.cno AND sno=?", (stu[0],)).fetchone()
    info['sno'] = stu[0]
    info['sname'] = stu[1]
    info['ssex'] = stu[2]
    info['sage'] = stu[3]
    info['sphone'] = stu[4]
    info['sdept'] = stu[5]
    if not avg_grade or not avg_grade[0]:
        info['avg_grade'] = 0
    else:
        info['avg_grade'] = avg_grade[0]
    rank = cursor.execute("SELECT count(*)+1 AS count\
                          FROM (SELECT sno ,avg(grade) AS stu_avg\
                          FROM sc,course WHERE sc.cno=course.cno GROUP BY sno)\
                          WHERE stu_avg>?", (info['avg_grade'],)).fetchone()
    if rank:
        info['rank'] = rank[0]
    else:
        info['rank'] = 1
    if sum_credit and sum_credit[0]:
        info['sum_credit'] = sum_credit[0]
    else:
        info['sum_credit'] = 0
    data.append(info)
    return render_template('educational_management/xstudent_sel_other_rs.html', data=data)


@app.route('/student_stu_cloud')
def student_stu_cloud():
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    stus = cursor.execute(
        "SELECT sc.sno,sname,avg(grade) AS avg FROM sc,student WHERE sc.sno= student.sno GROUP BY sc.sno ORDER BY avg DESC LIMIT 0,10").fetchall()
    tags = "<tags>"
    for stu in stus:
        link = "<a href='/student_stu_sel_sno/" + stu[0] + "' style='22' color='0xff0000' hicolor='0x00cc00'>" + stu[
            0] + "</a>"
        tags = tags + link
    tags = tags + "</tags>"
    return render_template('educational_management/tags_cloud.html', title='Student ranking', tags=tags)


@app.route('/student_cho_selrs')
def student_cho_selrs():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/student_cho_sel.html')


#this one
@app.route('/student_cho_sub', methods=['POST', 'GET'])
def student_cho_sub():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    if request.method == 'POST':
        # if cursor.execute("SELECT period FROM period").fetchone()[0] != "Elective course":
        #     return fail_msg("It is not a class time now.，Can't choose course", '/student_cho_sub')
        cno = request.form['cno']
        exist = cursor.execute("SELECT * FROM tc WHERE cno=?", (cno,)).fetchone()
        if not exist or not exist[0]:
            return fail_msg(content="The course does not exist!", return_url="/student_cho_sub")
        # ctime = cursor.execute("SELECT ctime FROM tc WHERE cno=?", (cno,)).fetchone()[0]
        # time_conflict = cursor.execute("SELECT * FROM sc,tc WHERE sc.cno=tc.cno AND sno=? AND ctime=?",
        #                                (session['username'], ctime)).fetchone()
        # if time_conflict:
        #     return fail_msg("Your class time conflicts with this class, please adjust and choose", '/student_cho_sub')
        # cmaxcount = cursor.execute("SELECT cmaxcount FROM tc WHERE cno=?", (cno,)).fetchone()[0]
        # cselected = cursor.execute("SELECT count(*) FROM sc WHERE cno=?", (cno,)).fetchone()[0]
        # if cmaxcount <= cselected:
        #     return fail_msg("The course is full, please choose another course", return_url="/student_cho_sub")


        # ObserverPattern
        studentdata = {}
        enrollData = EnrollmentData()
        studentdata['sno'] = session['username']
        studentdata['cno'] = cno

        adminObserver = AdminObserver()
        enrollData.registerObserver(adminObserver)
        enrollData.putStudentRequest(studentdata)
        enrollData.removeObserver(adminObserver)




        cursor.execute("INSERT INTO sc(sno,cno) VALUES(?,?)", (session['username'], cno))
        cursor.commit()
        return success_msg("Successful course selection!", return_url="/student_cho_sub")
    cous = cursor.execute(
        "SELECT sc.cno,cname,ccredit,tname,ctime,clocation FROM course,sc,tc,teacher WHERE sc.sno=? AND course.cno=sc.cno AND tc.cno=sc.cno AND tc.tno=teacher.tno",
        (session['username'],)).fetchall()



    # return render_template('educational_management/student_cho_sub.html', cous=cous, result=result)
    return render_template('educational_management/student_cho_sub.html', cous=cous)




@app.route('/student_cho_sub_cno/<cno>', methods=['POST', 'GET'])
def student_cho_sub_cno(cno):
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    if cursor.execute("SELECT period FROM period").fetchone()[0] != "Elective course":
        return fail_msg("It is not a class time now，Can't choose course", '/student_cho_sub')
    exist = cursor.execute("SELECT * FROM tc WHERE cno=?", (cno,)).fetchone()
    if not exist or not exist[0]:
        return fail_msg(content="The course does not exist!", return_url="/student_cho_sub")
    ctime = cursor.execute("SELECT ctime FROM tc WHERE cno=?", (cno,)).fetchone()[0]
    time_conflict = cursor.execute("SELECT * FROM sc,tc WHERE sc.cno=tc.cno AND sno=? AND ctime=?",
                                   (session['username'], ctime)).fetchone()
    if time_conflict:
        return fail_msg("Your class time conflicts with this class, please adjust and choose", '/student_cho_sub')
    cmaxcount = cursor.execute("SELECT cmaxcount FROM tc WHERE cno=?", (cno,)).fetchone()[0]
    cselected = cursor.execute("SELECT count(*) FROM sc WHERE cno=?", (cno,)).fetchone()[0]
    if cmaxcount <= cselected:
        return fail_msg("The course is full, please choose another course", return_url="/student_cho_sub")
    cursor.execute("INSERT INTO sc(sno,cno) VALUES(?,?)", (session['username'], cno))
    cursor.commit()
    return success_msg("Successful course selection!", return_url="/student_cho_sub")


@app.route('/student_frame')
def student_frame():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/student_frame.html')


@app.route('/student_main')
def student_main():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)



    cursor = get_db()
    info = dict()
    stu_result = cursor.execute("SELECT * FROM student WHERE sno=?", (session['username'],)).fetchone()

    data = []


    for cou in stu_result:
        data.append(cou)

    print(data)

    return render_template('educational_management/student_main.html', stu_info=data)


@app.route('/student_menu')
def student_menu():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    return render_template('student_menu.html')


@app.route('/student_navi')
def student_navi():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/student_navi.html')


@app.route('/student_sel')
def student_sel():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/xstudent_sel.html')


@app.route('/student_sel_other')
def student_sel_other():
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/xstudent_sel_other.html')


@app.route('/student_sel_other_cours/<sno>', methods=['POST', 'GET'])
def student_sel_other_cours(sno):
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    cous = cursor.execute(
        "SELECT sc.cno,cname,ccredit,ctime,clocation,grade,cstatus FROM course,sc,tc WHERE sc.sno=? AND course.cno=sc.cno AND tc.cno=sc.cno",
        (sno,)).fetchall()
    data = dict()
    for cou in cous:
        if cou[6] == "submitted":
            info = dict()
            info['rank'] = \
            cursor.execute("SELECT count(*)+1 FROM sc WHERE cno=? AND grade>?", (cou[0], cou[5])).fetchone()[0]
            data[cou[0]] = info
    return render_template('educational_management/student_sel_other_cours.html', data=data, cous=cous, sno=sno)


@app.route('/student_sel_other_rs', methods=['POST', 'GET'])
def student_sel_other_rs():
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        sno = '%' + request.form['sno'] + '%'
        sdept = '%' + request.form['sdept'] + '%'
        sname = '%' + request.form['sname'] + '%'
        cursor = get_db()
        result_set = cursor.execute("SELECT * FROM student WHERE sno LIKE ? AND sname LIKE ? AND sdept LIKE ?",
                                    (sno, sname, sdept))
        stus = result_set.fetchall()
        data = []
        for stu in stus:
            info = dict()
            sum_credit = cursor.execute("SELECT sum(ccredit) FROM sc ,course\
                                         WHERE sc.cno = course.cno AND grade >60 AND sno =?", (stu[0],)).fetchone()
            avg_grade = cursor.execute("SELECT avg(grade) FROM sc,course\
                                         WHERE sc.cno=course.cno AND sno=?", (stu[0],)).fetchone()
            info['sno'] = stu[0]
            info['sname'] = stu[1]
            info['ssex'] = stu[2]
            info['sage'] = stu[3]
            info['sphone'] = stu[4]
            info['sdept'] = stu[5]
            if not avg_grade or not avg_grade[0]:
                info['avg_grade'] = 0
            else:
                info['avg_grade'] = avg_grade[0]
            rank = cursor.execute("SELECT count(*)+1 AS count\
                                  FROM (SELECT sno ,avg(grade) AS stu_avg\
                                  FROM sc,course WHERE sc.cno=course.cno GROUP BY sno)\
                                  WHERE stu_avg>?", (info['avg_grade'],)).fetchone()
            if rank:
                info['rank'] = rank[0]
            else:
                info['rank'] = 1
            if sum_credit and sum_credit[0]:
                info['sum_credit'] = sum_credit[0]
            else:
                info['sum_credit'] = 0
            data.append(info)
        return render_template('educational_management/xstudent_sel_other_rs.html', data=data)
    return render_template('educational_management/xstudent_sel_other.html')


@app.route('/student_sel_self')
def student_sel_self():
    if not session.get('role') or session['role'] != 'student':
        error = "You are not logged in or you are not a student"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    cous = cursor.execute(
        "SELECT sc.cno,cname,ccredit,ctime,clocation,grade,cstatus FROM course,sc,tc WHERE sc.sno=? AND course.cno=sc.cno AND tc.cno=sc.cno",
        (session['username'],)).fetchall()
    data = dict()
    for cou in cous:
        if cou[6] == "submitted":
            info = dict()
            info['rank'] = \
            cursor.execute("SELECT count(*)+1 FROM sc WHERE cno=? AND grade>?", (cou[0], cou[5])).fetchone()[0]
            data[cou[0]] = info
    return render_template('educational_management/student_sel_self.html', cous=cous, data=data)


#   --------------student end----------------------

#   --------------teacher start--------------------
@app.route('/teacher_cho')
def teacher_cho():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    data = dict()
    data['tno'] = session['username']
    return render_template('educational_management/teacher_cho.html', data=data)


@app.route('/teacher_cho_del', methods=['POST', 'GET'])
def teacher_cho_del():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    period = cursor.execute("SELECT period FROM period").fetchone()[0]
    if period != 'Elective course':
        return fail_msg(content="It is not a class time now.，不能删除课程")
    tno = session['username']
    if request.method == 'POST':
        cnos = request.form.getlist('to_delete')
        for cno in cnos:
            print("here")
            print(cno)
            cursor.execute("DELETE FROM tc WHERE cno =?", (cno,))
        cursor.commit()
        return success_msg(content="successfully deleted", return_url="/teacher_cho_del")
    else:
        cous = cursor.execute("SELECT * FROM tc WHERE tno = ?", (tno,)).fetchall()
        data = []
        if cous:
            for cou in cous:
                info = dict()
                info['cno'] = cou[1]
                res = cursor.execute("SELECT cname,ccredit FROM course WHERE cno = ?", (cou[1],)).fetchone()
                info['cname'] = res[0]
                info['ccredit'] = res[1]
                result = cursor.execute("SELECT count(*) FROM sc WHERE cno = ?", (info['cno'],)).fetchone()
                if result:
                    info['cstudentcount'] = result[0]
                else:
                    info['cstudentcount'] = 0
                if info['cstudentcount'] == 0:
                    data.append(info)
        return render_template('educational_management/xteacher_cho_del.html', data=data)


@app.route('/teacher_cho_sel')
def teacher_cho_sel():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)

    cursor = get_db()

    query = "select * from course "
    print(query)
    course_result_set = cursor.execute(query)

    data = []
    for cou in course_result_set:
        info = []
        info.append(cou[0])
        info.append(cou[1])
        info.append(cou[2])
        print(info)
        data.append(info)


    return render_template('educational_management/teacher_cho_sel.html', course_data=data)


@app.route('/teacher_cho_selrs', methods=['POST', 'GET'])
def teacher_cho_selrs():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        cno = '%' + request.form['cno'] + '%'
        cname = '%' + request.form['cname'] + '%'
        ccredit = '%' + request.form['ccredit'] + '%'
        sql = "select * from course where cno like ? and cname like ? and ccredit like ?"
        cursor = get_db()
        result_set = cursor.execute(sql, (cno, cname, ccredit))
        cous = result_set.fetchall()
        data = []
        for cou in cous:
            info = dict()
            info['cno'] = cou[0]
            info['cname'] = cou[1]
            info['ccredit'] = cou[2]
            data.append(info)
        return render_template('educational_management/teacher_cho_selrs.html', data=data)
    return render_template('educational_management/teacher_cho_sel.html')


@app.route('/teacher_cho_sel_cno/<cno>', methods=['POST', 'GET'])
def teacher_cho_sel_cno(cno=None):
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    sql = "select * from course where cno=?"
    cursor = get_db()
    result_set = cursor.execute(sql, (cno,))
    cou = result_set.fetchone()
    data = []
    info = dict()
    info['cno'] = cou[0]
    info['cname'] = cou[1]
    info['ccredit'] = cou[2]
    data.append(info)
    return render_template('educational_management/teacher_cho_selrs.html', data=data)


@app.route('/teacher_cho_set', methods=['POST', 'GET'])
def teacher_cho_set():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    data = dict()
    cursor = get_db()
    period = cursor.execute("SELECT period FROM period").fetchone()[0]
    data['period'] = period
    if period != 'Elective course':
        return fail_msg(content="It is not a class time now.，Can't open a course")
    if request.method == 'POST':
        cno = request.form['cno'].rsplit('-', 2)[0]
        tno = session['username']
        clocation = request.form['clocation']
        try:
            cmaxcount = int(request.form['cmaxcount'])
        except(ValueError):
            return fail_msg("Course capacity should be a number！", "/teacher_cho_set")
        ctime = request.form['ctime1'] + request.form['ctime2']
        result_set = cursor.execute("SELECT * FROM tc WHERE tno=? AND ctime=?", (tno, ctime)).fetchone()
        if result_set:
            return fail_msg('You have already opened a course in the current time, please choose another time', 'teacher_cho_set')
        result_set = cursor.execute("SELECT * FROM course WHERE cno =?", (cno,))
        if result_set.fetchone():
            result_set = cursor.execute("SELECT * FROM tc WHERE cno = ?", (cno,))
            if result_set.fetchone():
                return fail_msg(content="This course has been opened by teachers. Please choose another course.", return_url="/teacher_cho_set")
            sql = "insert into tc(tno,cno,clocation,cmaxcount,ctime) values(?,?,?,?,?)"
            cursor.execute(sql, (tno, cno, clocation, cmaxcount, ctime))
            cursor.commit()
            return success_msg(content="Successful course", return_url=url_for('teacher_cho_set'))
        else:
            return fail_msg(content="The course does not exist，Please ask the administrator to add a course before opening the course.", return_url='/teacher_cho_set')
    cous = cursor.execute("SELECT * FROM course")
    return render_template('educational_management/teacher_cho_set.html', data=data, cous=cous)


@app.route('/teacher_cho_seted/<tno>')
def teacher_cho_seted(tno):
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    cous = cursor.execute("SELECT * FROM tc WHERE tno = ?", (tno,)).fetchall()
    data = []
    if cous:
        for cou in cous:
            info = dict()
            info['cno'] = cou[1]
            # print(cou[1])
            res = cursor.execute("SELECT cname,ccredit FROM course WHERE cno = ?", (cou[1],)).fetchone()

            # query= "SELECT cname,ccredit FROM course WHERE cno = \'COM0011\'"
            # print(query)
            # res= cursor.execute(query)
            info['cname'] = res[0]
            info['ccredit'] = res[1]
            # info['clocation'] = cou[2]
            # info['ctime'] = cou[4]
            # info['cmaxcount'] = cou[3]
            # result = cursor.execute("SELECT count(*) FROM sc WHERE cno = ?", (info['cno'],)).fetchone()
            # if result:
            #     info['cstudentcount'] = result[0]
            # else:
            #     info['cstudentcount'] = 0
            data.append(info)
        print(data)
        print("I have data")
        return render_template('educational_management/teacher_cho_seted.html', data=data, tno=tno)
    else:
        print("I dont")
        return render_template('educational_management/teacher_cho_seted.html', data=None, tno=tno)


# when teach chooses new course


@app.route('/teacher_cho_course', methods=['POST', 'GET'])
def teacher_cho_course():
    if not session.get('role') or session['role'] != 'teacher':
        error = "You are not logged in or you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    if request.method == 'POST':
        # if cursor.execute("SELECT period FROM period").fetchone()[0] != "Elective course":
        #     return fail_msg("It is not a class time now.，Can't choose course", '/student_cho_sub')
        cno = request.form['cno']
        # exist = cursor.execute("SELECT * FROM tc WHERE cno=?", (cno,)).fetchone()
        # if not exist or not exist[0]:
        #     return fail_msg(content="The course does not exist!", return_url="/student_cho_sub")
        # ctime = cursor.execute("SELECT ctime FROM tc WHERE cno=?", (cno,)).fetchone()[0]
        # time_conflict = cursor.execute("SELECT * FROM sc,tc WHERE sc.cno=tc.cno AND sno=? AND ctime=?",
        #                                (session['username'], ctime)).fetchone()
        # if time_conflict:
        #     return fail_msg("Your class time conflicts with this class, please adjust and choose", '/student_cho_sub')
        # cmaxcount = cursor.execute("SELECT cmaxcount FROM tc WHERE cno=?", (cno,)).fetchone()[0]
        # cselected = cursor.execute("SELECT count(*) FROM sc WHERE cno=?", (cno,)).fetchone()[0]
        # if cmaxcount <= cselected:
        #     return fail_msg("The course is full, please choose another course", return_url="/student_cho_sub")
        tno=session['username']


        # observer Pattern
        teachdata={}
        enrollData= EnrollmentData()
        teachdata['tno']=session['username']
        teachdata['cno']=cno
        teachdata['clocation']='x'
        teachdata['cmaxcount']=10
        teachdata['ctime']='y'
        teachdata['cstatus']='z'

        adminObserver=AdminObserver()
        enrollData.registerObserver(adminObserver)
        enrollData.putTeacherRequest(teachdata)
        enrollData.removeObserver(adminObserver)


        cursor.execute("INSERT INTO tc(tno,cno,clocation,cmaxcount,ctime,cstatus) VALUES(?,?,?,?,?,?)", (session['username'], cno, 'x',10, 'y' ,'z'))
        cursor.commit()
        return success_msg("Successful course selection!", return_url="/teacher_cho_course")


    tno = session['username']
    cursor = get_db()
    cous = cursor.execute("SELECT * FROM tc WHERE tno = ?", (tno,)).fetchall()
    data = []
    if cous:
        for cou in cous:
            info = dict()
            info['cno'] = cou[1]
            # print("coursemine")
            # print(cou)
            res = cursor.execute("SELECT cname,ccredit FROM course WHERE cno = ?", (cou[1],)).fetchone()
            info['cname'] = res[0]
            info['ccredit'] = res[1]

            data.append(info)

    print(data)
    return render_template('educational_management/teacher_cho_seted.html', data=data, tno=tno)
# till here




@app.route('/teacher_frame')
def teacher_frame():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/teacher_frame.html')


@app.route('/teacher_main')
def teacher_main():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    # cursor = get_db()
    # tname = cursor.execute("SELECT tname FROM teacher WHERE tno =?", (session['username'],))
    # period = cursor.execute("SELECT period FROM period").fetchone()[0]
    # data = dict()
    # data['tno'] = session['username']
    # data['tname'] = tname.fetchone()[0]
    # data['lasttime'] = session['lasttime']
    # data['period'] = period
    # if period == 'Elective course':
    #     data['message'] = u"You can open a course or information inquiry or submit a grade."
    # else:
    #     data['message'] = u"You can make an inquiry or submit a grade."
    # return render_template('educational_management/teacher_main.html', data=data)

    cursor = get_db()
    info = dict()
    tec_result = cursor.execute("SELECT * FROM teacher WHERE tno=?", (session['username'],)).fetchone()

    data = []

    for cou in tec_result:
        data.append(cou)

    print(data)

    return render_template('educational_management/teacher_main.html', tech_info=data)


@app.route('/teacher_menu')
def teacher_menu():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged in Or you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    return render_template('teacher_menu.html')


@app.route('/teacher_navi')
def teacher_navi():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged in Or you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/teacher_navi.html')


@app.route('/teacher_cou_cloud')
def teacher_cou_cloud():
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    cous = cursor.execute(
        "SELECT sc.cno,cname,count(*) AS count FROM sc,course WHERE sc.cno = course.cno GROUP BY sc.cno ORDER BY sc.cno DESC LIMIT 0,10").fetchall()
    tags = "<tags>"
    for cou in cous:
        link = "<a href='/teacher_cho_sel_cno/" + cou[0] + "' style='22' color='0xff0000' hicolor='0x00cc00'>" + cou[
            0] + "</a>"
        tags = tags + link
    tags = tags + "</tags>"
    return render_template('educational_management/tags_cloud.html', title='热门课程', tags=tags)


@app.route('/teacher_tea_cloud')
def teacher_tea_cloud():
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    teas = cursor.execute(
        "SELECT tc.tno,tname,count(*) AS count FROM sc,tc,teacher WHERE sc.cno=tc.cno AND tc.tno=teacher.tno GROUP BY tc.tno ORDER BY count DESC LIMIT 0,10").fetchall()
    tags = "<tags>"
    for tea in teas:
        link = "<a href='/teacher_sel_other_tno/" + tea[0] + "' style='22' color='0xff0000' hicolor='0x00cc00'>" + tea[
            0] + "</a>"
        tags = tags + link
    tags = tags + "</tags>"
    return render_template('educational_management/tags_cloud.html', title='Popular teacher', tags=tags)


@app.route('/teacher_sel_other_tno/<tno>')
def teacher_sel_other_tno(tno=None):
    if not session.get('role'):
        error = "you have not logged in"
        return render_template("educational_management/login.html", error=error)
    sql = "select * from teacher where tno=?"
    cursor = get_db()
    result_set = cursor.execute(sql, (tno,))
    tea = result_set.fetchone()
    data = []
    info = dict()
    info['tno'] = tea[0]
    info['tname'] = tea[1]
    info['tphone'] = tea[2]
    data.append(info)
    return render_template('educational_management/teacher_sel_other_rs.html', data=data)


@app.route('/teacher_sel')
def teacher_sel():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/teacher_sel.html')


@app.route('/teacher_sel_other')
def teacher_sel_other():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/teacher_sel_other.html')


@app.route('/teacher_sel_other_rs', methods=['POST', 'GET'])
def teacher_sel_other_rs():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        tno = '%' + request.form['tno'] + '%'
        tname = '%' + request.form['tname'] + '%'
        sql = "select * from teacher where tno like ? and tname like ?"
        cursor = get_db()
        result_set = cursor.execute(sql, (tno, tname))
        teas = result_set.fetchall()
        data = []
        for tea in teas:
            info = dict()
            info['tno'] = tea[0]
            info['tname'] = tea[1]
            info['tphone'] = tea[2]
            data.append(info)
        return render_template('educational_management/teacher_sel_other_rs.html', data=data)
    return render_template('educational_management/teacher_sel_other.html')


@app.route('/teacher_sel_self')
def teacher_sel_self():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    sql = "select * from teacher where tno = ?"
    cursor = get_db()
    result_set = cursor.execute(sql, (session['username'],))
    tea = result_set.fetchone()
    tdata = dict()
    tdata['tno'] = tea[0]
    tdata['tname'] = tea[1]
    tdata['tphone'] = tea[2]
    tdata['tpassword'] = cursor.execute("SELECT password FROM user WHERE username= ?", (tea[0],)).fetchone()[0]
    cdata = []
    cous = cursor.execute(
        "SELECT course.cno,course.cname,course.ccredit FROM tc,course WHERE tc.cno=course.cno AND tno=? GROUP BY course.cno,course.cname,course.ccredit",
        (tdata['tno'],)).fetchall()
    score = dict()
    for cou in cous:
        info = dict()
        res = cursor.execute("SELECT avg(grade),max(grade),min(grade),count(*) FROM sc WHERE cno = ?",
                             (cou[0],)).fetchone()
        if res:
            if res[0]:
                info["avg_grade"] = res[0]
            else:
                info["avg_grade"] = 0
            if res[1]:
                info["max_grade"] = res[1]
            else:
                info["max_grade"] = 0
            if res[2]:
                info["min_grade"] = res[2]
            else:
                info["min_grade"] = 0
            if res[3]:
                info["count"] = res[3]
            else:
                info["count"] = 0
        else:
            info["avg_grade"] = 0
            info["max_grade"] = 0
            info["min_grade"] = 0
            info["count"] = 0
        score[cou[0]] = info
    return render_template('educational_management/teacher_sel_self.html', tdata=tdata, cous=cous, score=score)


@app.route('/teacher_sel_self_coul/<cno>')
def teacher_sel_self_coul(cno):
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    ccredit = cursor.execute("SELECT ccredit FROM course WHERE cno=?", (cno,)).fetchone()[0]
    snos = cursor.execute("SELECT sno FROM sc WHERE cno=?", (cno,)).fetchall()
    data = dict()
    data['cstatus'] = cursor.execute("SELECT cstatus FROM tc WHERE cno=?", (cno,)).fetchone()[0]
    for sno in snos:
        info = dict()
        info['sname'] = cursor.execute("SELECT sname FROM student WHERE sno=?", (sno[0],)).fetchone()[0]
        info["rank"] = cursor.execute(
            "SELECT count(*)+1 AS count FROM sc AS a,sc AS b WHERE a.grade>b.grade AND a.cno=b.cno AND a.cno=? AND b.sno=?",
            (cno, sno[0])).fetchone()[0]
        info["grade"] = cursor.execute("SELECT grade FROM sc WHERE sno=? AND cno=?", (sno[0], cno)).fetchone()[0]
        if not info["grade"]:
            info["grade"] = 0
        data[sno[0]] = info
    return render_template('educational_management/teacher_sel_self_coul.html', ccredit=ccredit, cno=cno, snos=snos, data=data)


@app.route('/teacher_sub')
def teacher_sub():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    return render_template('educational_management/xteacher_sub.html')


@app.route('/teacher_sub_cl/<status>', methods=['POST', 'GET'])
def teacher_sub_cl(status):
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    cursor = get_db()
    if status == 'subed':
        result_set = cursor.execute(
            "SELECT tc.cno,cname FROM tc,course WHERE tc.cno=course.cno AND tc.cstatus=? AND tno=?",
            (u"submitted", session['username'])).fetchall()
    else:
        result_set = cursor.execute(
            "SELECT tc.cno,cname FROM tc,course WHERE tc.cno=course.cno AND (tc.cstatus IS NULL OR tc.cstatus!=?) AND tno=?",
            (u"submitted", session['username'])).fetchall()
    return render_template('educational_management/xteacher_sub_cl.html', data=result_set, cstatus=status)


@app.route('/teacher_sub_input')
def teacher_sub_input():
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    return render_template('teacher_sub_input.html')


@app.route('/teacher_sub_score/<cno>', methods=['POST', 'GET'])
def teacher_sub_score(cno):
    if not session.get('role') or session['role'] != 'teacher':
        error = "you have not logged inOr you are not a teacher"
        return render_template("educational_management/login.html", error=error)
    score_xls = request.files[cno]
    if score_xls and allowed_file(score_xls.filename):
        score_xls_name = secure_filename(score_xls.filename)
        score_xls.save(os.path.join(app.config['UPLOAD_FOLDER'], score_xls_name))
    score_table = xlrd.open_workbook('static/score/' + score_xls_name).sheets()[0]
    count_row = score_table.nrows
    cursor = get_db()
    str1 = ""
    for i in range(count_row):
        sno = score_table.row_values(i)[0]
        grade = score_table.row_values(i)[1]
        exist = cursor.execute("SELECT * FROM sc WHERE sno=?", (sno,)).fetchone()
        if exist:
            cursor.execute("UPDATE sc SET grade=? WHERE cno=? AND sno=?", (grade, cno, sno))
    cursor.execute("UPDATE tc SET cstatus=? WHERE cno=?", (u"submitted", cno))
    cursor.commit()
    return success_msg("成绩上传成功", '/teacher_sub_cl/subing')


#   --------------teacher end--------------------

#   --------------util start--------------------------
def success_msg(content, return_url=None):
    if not return_url:
        return '<img src=' + url_for('static',
                                     filename='image/t.png') + ' ><font size=6 color=red>' + content + '</font>'
    else:
        return '<meta http-equiv="refresh" content=1;url="' + return_url + '">' + '\n' + '<img src=' + url_for('static',
                                                                                                               filename='image/t.png') + ' ><font size=6 color=red>' + content + '</font>'


def fail_msg(content, return_url=None):
    if not return_url:
        return '<img src=' + url_for('static',
                                     filename='image/f.png') + '><font size=6 color=red>' + content + '</font>'
    else:
        return '<meta http-equiv="refresh" content=1;url="' + return_url + '">' + '\n' + '<img src=' + url_for('static',
                                                                                                               filename='image/f.png') + '><font size=6 color=red>' + content + '</font>'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#   --------------util end--------------------------
#	---------------run----------------------------
if __name__ == '__main__':
    app.run(port=8082)
