from django.shortcuts import render
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
# Create your views here.
from django.shortcuts import render, HttpResponse,redirect

# Create your views here.


def home(request):
    return render(request, 'home/home.html')

# def blog(request):
#     return render(request, 'blog/bloghome.html')    


def about(request):
    messages.success(request, "this is about ")

    return render(request, 'home/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name) < 2 or len(email) < 2 or len(phone) < 10 or len(content) < 4:
            messages.error(request, 'fill the form correctly')
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(request, 'message has set successfully')
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    #allPosts = Post.objects.all()
    else:
        allPostsTitle = Post.objects.filter(title__icontains = query)
        allPostsContent = Post.objects.filter(content__icontains = query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,"please enter a valid query")    
    params = {'allPosts': allPosts, 'query': query}
    return render(request,'home/search.html', params)
 
def handleSignup(request):
    if request.method == 'POST':
        #get the post parameters
        username = request.POST.get('username','')
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('email','')
        pass1 = request.POST.get('pass1','')
        pass2 = request.POST.get('pass2','')

        #check for error inputs
        if len(username)>10:
            messages.error(request,"Username mustbe under 10 characters")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,"password do not match")
            return redirect('home')  
        if not username.isalnum():
            messages.error(request,"username only contain letters and numbers")
            return redirect('home') 

        # create the user
        myuser = User.objects.create(username=username,email=email,password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
    
        myuser.save()
        messages.success(request,"account Created")
        return redirect('home')
    
    else:
        return HttpResponse('404 - Not Allowed')    