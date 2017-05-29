from transitKhi import app

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField
from transitKhi.displayRoute import main
import smtplib
 
class busSearch(Form):
    frm = TextField('From:', validators=[validators.required("Please Enter Start Point")])
    to = TextField('To:', validators=[validators.required("Please Enter End Point")])

class Options(Form):
     text= TextAreaField('text')

class Contact(Form):
    name = TextField("Name", [validators.Required("Please Enter Your Name")])
    email = TextField("Email",[validators.Required("Please enter your email address"), validators.email("Please enter your email address")])
    subject = TextField("Subject", [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message", [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")    

def options(info):
    formx = Options()
    formx.text.data = info
    return formx

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/', methods=['POST', 'GET'])
def student():
    form = busSearch(request.form)
## if form.validate():
##            # Save the comment here.
##            flash('Hello you want to go from ' + frm  + 'to' + to)
    return render_template('busSearch.html', form=form)


@app.route("/busoptions", methods=['POST', 'GET'])
def busoptions():
    form = busSearch()
    #print (form.errors)
    if request.method == 'POST':
        #name=request.form['name']
        #print (name)
        frm=request.form['frm']
        to=request.form['to']
        print(frm, to)
        info=main(frm, to)
        print(info)
        form=options(info)
        
##        if form.validate():
##            # Save the comment here.
##            flash('Hello you want to go from ' + frm  + 'to' + to)
##        else:
##            flash('All the form fields are required. ')
 
    return render_template('busoptions.html', form=form)

@app.route("/allroutes")
def route():
    return render_template('allroutes.html')

@app.route("/contactus", methods=['POST', 'GET'])
def contact():
    form=Contact(request.form)
    TO= ["af00370@st.habib.edu.pk"]
    FROM= "fatimaanusha420@gmail.com"
    SUBJECT="TransitKhi Contactus"
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        text="name: "+ name + "\n"+ request.form['message']
        message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (email, TO[0], subject, text)
        print(message)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("fatimaanusha420@gmail.com", "Alhumdulill@h")
        server.sendmail(email, TO, message)
        server.quit()
    return render_template('contactus.html', form=form)

@app.route("/thankyou")
def thank():
    return render_template('thankyou.html')



@app.route("/addbus")
def add():
    return render_template('addbus.html')

@app.route("/reviews")
def review():
    return render_template('reviews.html')

@app.route("/mymap")
def show():
    return render_template('mymap.html')
 
if __name__ == "__main__":
    app.run()


