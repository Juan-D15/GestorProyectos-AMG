from django.shortcuts import render

def tailwind_test(request):
    return render(request, "tailwind_test.html")

def daisyui_test(request):
    return render(request, "daisyui_test.html")
