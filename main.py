from flask import Flask, request, redirect, render_template
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/signup", methods=['POST'])
def signup():
    #get form data
    user = request.form['user']
    pwd1 = request.form['pswd']
    pwd2 = request.form['verify']
    email = request.form['email']

    #initialize error messages
    user_error = ""
    pass_error = ""
    match_error = ""
    email_error = ""
    error_query = ""
    
    regex = re.compile(r"[\w-]+@[\w-]+\.\w+")

    if (user == ""):
        # the user tried to enter an invalid username
        # so we redirect back to the front page and tell them what went wrong
        user_error = "Please enter a valid user name."
    elif(len(user) < 3) or (len(user) > 20) or (" " in user):
        user_error = "The uername must be 3-20 characters and can't contain spaces"
    
    if (pwd1 == ""):
        # the user tried to enter an invalid password,
        # so we redirect back to the front page and tell them what went wrong
        pass_error = "Please enter a valid password."
    elif(len(pwd1) < 3) or (len(pwd1) > 20) or (" " in pwd1):
        pass_error = "The password must be 3-20 characters and can't contain spaces"

    if (pwd2 == "") or (pwd1 != pwd2):
        # the two passwords didn't match,
        # so we redirect back to the front page a nd tell them what went wrong
        match_error = "The passwords did not match"

    if(email != ""):
        #if(len(email) < 3) or (len(email) > 20) or (email.count("@") != 1) or (email.count(".") != 1) or (" " in email):
        valid_email = regex.match(email)
        if(len(email) < 3) or (len(email) > 20) or (not valid_email):
            # the user tried to enter an invalid email address,
            # so we redirect back to the front page and tell them what went wrong
            email_error = "The email must be 3-20 characters, must contain a '@' and a single '.', and can't contain spaces"

    if (user_error != ""):
            error_query += "&uerror=" + user_error
    
    if (pass_error != ""):
            error_query += "&perror=" + pass_error

    if (match_error != ""):
            error_query += "&merror=" + match_error

    if (email_error != ""):
            error_query += "&eerror=" + email_error

    if (error_query != ""):
        # redirect to homepage, and include error as a query parameter in the URL.
        return redirect("/?uname=" + user + "&email=" + email + error_query)
    else:    
        # if we didn't redirect by now, then all is well
        return render_template("welcome.html", title="Welcome", user=user)

@app.route("/")
def index():
    uname = request.args.get("uname")
    email = request.args.get("email")
    uerror = request.args.get("uerror")
    perror = request.args.get("perror")
    merror = request.args.get("merror")
    eerror = request.args.get("eerror")

    if uname == None:
        uname = ""
    if email == None:
        email = ""

    return render_template("form.html", title="User Signup", user=uname, email=email, uerror=uerror, perror=perror, merror=merror, eerror=eerror)

app.run()
    
