from pyrebase import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBbpL1cGJHXiQsqaFc7C-F41VgcG8LN3pk",
  "authDomain": "lineweb-d1174.firebaseapp.com",
  "projectId": "lineweb-d1174",
  "storageBucket": "lineweb-d1174.appspot.com",
  "messagingSenderId": "854065790129",
  "appId": "1:854065790129:web:0f9c4747e925b9fc1db690",
  "databaseURL": "https://lineweb-d1174.firebaseio.com/"
};

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

def login(email,password):
    # print("Log in...")
    # email=input("Enter email: ")
    # password=input("Enter password: ")
    try:
        login2 = auth.sign_in_with_email_and_password(email, password)
        print(login2.keys
        9)
        print("Successfully logged in!")
        # print(auth.get_account_info(login['idToken']))
       # email = auth.get_account_info(login['idToken'])['users'][0]['email']
       # print(email)
    except:
        print("Invalid email or password")
    return


login("gg3@gmail.com","abcdef")