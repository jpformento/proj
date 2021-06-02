from flask import *
import sqlite3

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/works.html')
def works():
    return render_template("works.html")

@app.route('/work.html')
def work():
    return render_template("work.html")


@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/contact.html')
def contact():
    return render_template("contact.html")


@app.route("/save", methods=["POST", "GET"])
def save():
    msg = "msg"
    if request.method == "POST":
        try:
            email = request.form["email"]
            subject = request.form["subject"]
            message = request.form["message"]
            with sqlite3.connect("message.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into message (email, subject,message) values (?,?,?)", (email, subject, message))
                con.commit()
                msg = "Message submitted.Thank you!"
        except:
            con.rollback()
            msg = "Apology, We can not send your message."
        finally:
            return render_template("tnx.html", msg=msg)
            con.close()


@app.route('/error.html')
def error():
    return render_template("error.html")


@app.route('/nogil.html')
def nigol():
    return render_template("nogil.html")


@app.route('/nogil', methods=['POST'])
def login():
    uname = request.form['uname']
    password = request.form['pass']
    if uname == "chris" and password == "microsoft":
        return "Welcome %s" % uname


@app.route('/test', methods=['POST'])
def test():
    if request.method == "POST":
        uname = request.form['uname']
        password = request.form['pass']

    if password == "microsoft":
        resp = make_response(render_template('/succ.html'))
        resp.set_cookie('uname', uname)
        return resp
    else:
        return redirect(url_for('error'))


@app.route("/views")
def views():
    con = sqlite3.connect("message.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from message")
    rows = cur.fetchall()
    return render_template("views.html", rows=rows)


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("message.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from message where id =?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)


@app.route('/components.html')
def components():
    return render_template("components.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
