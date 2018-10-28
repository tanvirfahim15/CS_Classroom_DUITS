from flask import request, session, url_for, render_template




class MyServer:
    def __init__(self):
        self.globalData = "hello"


    def function(self):
        print("Here1")
        return render_template("educational_management/admin_stu_add.html")

    def admin_stu_add(self,my_person):
        print("Here2")
        if not session.get('role') or session['role'] != 'admin':
            error = "You are not logged in or you are not an administrator"
            return render_template("educational_management/login.html", error=error)
        if request.method == 'POST':
            cursor = get_db()
            # sno = request.form['sno']
            # sname = request.form['sname']
            # ssex = request.form['ssex']
            # sage = request.form['sage']
            # sdept = request.form['sdept']
            # sphone = request.form['sphone']
            # spassword = request.form['spassword']

            print("In adding student")
            info=my_person.getDescription()

            sno = info['Id']
            sname = info['Name']
            ssex = info['Gender']
            sage = info['Age']
            sdept = request.form['sdept']
            sphone = info['Phone']
            spassword = info['Password']



            result_set = cursor.execute("SELECT * FROM student WHERE sno =?", (sno,))
            if result_set.fetchone():
                return fail_msg(content="The student already exists", return_url='/admin_stu_add')
            else:
                sql = "insert into student(sno,sname,ssex,sage,sdept,sphone) values(?,?,?,?,?,?)"
                cursor.execute(sql, (sno, sname, ssex, sage, sdept, sphone))
                cursor.execute("INSERT INTO user(username,password,role,lasttime) VALUES(?,?,?,?)",
                               (sno, spassword, 'student', u'You    are logging in to the system for the first time.'))
                cursor.commit()
                return success_msg(content="Successfully added the student", return_url=url_for('admin_stu_add'))
        return render_template('educational_management/admin_stu_add.html')


from StuManager import get_db, fail_msg,success_msg