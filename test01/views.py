from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages

# imports for OpenCV
import cv2
import pickle
import cvzone
import numpy as np

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')  

def areas(request):
    return render(request, 'areas.html')

def area_details(request):
    return render(request, 'area-details.html')



# account
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('register')
        else:
            user =  User.objects.create_user(first_name=name, email=email, username=username, password=password)
            user.save()
            print("User Created")
            return redirect('index')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('login')  
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')


# first try code
def home(request):
    return render(request, 'index1.html')

def live(request):
    cap = cv2.VideoCapture('park/static/images/carPark.mp4')
    width, height = 103, 43
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)


    def empty(a):
        pass


    cv2.namedWindow("Vals")
    cv2.resizeWindow("Vals", 640, 240)
    cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
    cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
    cv2.createTrackbar("Val3", "Vals", 5, 50, empty)


    def checkSpaces():
        spaces = 0
        for pos in posList:
            x, y = pos
            w, h = width, height

            imgCrop = imgThres[y:y + h, x:x + w]
            count = cv2.countNonZero(imgCrop)

            if count < 900:
                color = (0, 200, 0)
                thic = 5
                spaces += 1

            else:
                color = (0, 0, 200)
                thic = 2

            cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

            cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                        color, 2)

        cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,
                        colorR=(0, 200, 0))
        spaces = spaces



    while True:

        # Get image frame
        success, img = cap.read()
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # img = cv2.imread('img.png')
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        # ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)

        val1 = cv2.getTrackbarPos("Val1", "Vals")
        val2 = cv2.getTrackbarPos("Val2", "Vals")
        val3 = cv2.getTrackbarPos("Val3", "Vals")
        if val1 % 2 == 0: val1 += 1
        if val3 % 2 == 0: val3 += 1
        imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, val1, val2)
        imgThres = cv2.medianBlur(imgThres, val3)
        kernel = np.ones((3, 3), np.uint8)
        imgThres = cv2.dilate(imgThres, kernel, iterations=1)

        checkSpaces()
        # Display Output

        cv2.imshow("Image", img)
        # cv2.imshow("ImageGray", imgThres)
        # cv2.imshow("ImageBlur", imgBlur)
        key = cv2.waitKey(1)
        if key == ord('r'):
            pass


def response(request):
    aname = request.POST.get('name')
    aphone = request.POST.get('phone')
    alocation = request.POST.get('location')
    # print(aname, alocation)
    look = {'name':aname, 'phone': aphone, 'location':alocation}
    print(look)
    return render(request, 'response.html', look)