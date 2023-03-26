import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'dashboard/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, 'Please enter a valid username and password.')
            return render(request, 'dashboard/login.html')
        # sanitize input
        username = username.strip()
        password = password.strip()
        # check if user exists and password is correct
        with open('Admin.txt', 'r') as f:
            json_string = f.read()
            users = json.loads(json_string)
            if username in users and users[username]['password'] == password:
                role = users[username]['role']
                request.session['role'] = role
                response = render(request, 'dashboard/index.html', {'username': username})
                response.set_cookie("username",username)
                response.set_cookie("user",username)
                return response
            else:
                messages.error(request, 'Invalid credentials...!')
                return render(request, 'dashboard/login.html')
    else:
        return render(request, 'dashboard/login.html')


def forget(request):
    return render(request, 'dashboard/forget.html')

import json
from django.shortcuts import render

def change_password(request):
    if request.method == 'POST':
        with open("Admin.txt", "r") as f:
            users = json.load(f)
        username = request.POST.get('username1')
        new_password = request.POST.get('npass')
        confirm_password = request.POST.get('cpass')
        entered_sc = request.POST.get('security_code')
        print(f"username={username}, new_password={new_password}, confirm_password={confirm_password}, entered_sc={entered_sc}")
        if not username or not new_password or not confirm_password or not entered_sc:
            error_message = "Please fill out all the fields."
            return render(request, "dashboard/forget.html", {'error_message': error_message})
        username = username.strip()
        new_password = new_password.strip()
        confirm_password = confirm_password.strip()
        entered_sc = entered_sc.strip()
        if username not in users:
            error_message = "The username does not exist."
            return render(request, "dashboard/forget.html", {'error_message': error_message})
        elif new_password != confirm_password:
            error_message = "The new password and confirm password do not match."
            return render(request, "dashboard/forget.html", {'error_message': error_message})
        elif users[username]["sc"] != entered_sc:
            error_message = "The security code is incorrect."
            return render(request, "dashboard/forget.html", {'error_message': error_message})
        users[username]["password"] = new_password
        with open("Admin.txt", "w") as f:
            json.dump(users, f)

        success_message = "Password successfully updated."
        return render(request, "dashboard/forget.html", {'success_message': success_message})
    else:
        return render(request, "dashboard/forget.html")
