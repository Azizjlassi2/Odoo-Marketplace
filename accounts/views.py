from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def str_to_dict(data:str,args:list):
    """
    Elle aide à convertir une chaine de caractères en un dictionnaire 
    Data :  la chaine de caractères à convertir 
    Args:   les clés de dictionnaire à retourner 

    """
   
    result= {}
    for key in args:
        copy_data = data
        index = data.find(key)
        if index == -1 :
            print(f'you have a problem while indexing the key { key } !')
            break
        
        copy_data = data[index + len(key) : ]
        value = copy_data[copy_data.find(':')+1:copy_data.find(',')]
        result[str(key)]= value.replace('"','')
  

    return result

# Create your views here.
def login_user(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('mysite:index')
        else:
            messages.success(request,('There was a Error in Login ! \n There is no such account'))
            return redirect('accounts:login')
    elif request.method =='GET':
        return render(request,'authentication/login.html')

def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            print(username)
            user = authenticate(username=username,password1=password1)
            login(request,user)
            messages.success(request,('Registration Succes !'))
            return redirect('mysite:index')
    else:
        form = UserCreationForm()

    return render(request,'authentication/signup.html',{'form':form})

def logout_user(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,('Logging out !'))
        return redirect('mysite:index')

