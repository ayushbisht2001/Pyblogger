from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import   login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
# Create your views here.
from django.views.generic  import *
from .models import BlogPost
from .forms import *
from django.http import JsonResponse,HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from json import dumps
from UserProfile.models import Profile
from PIL import  Image
from pathlib import Path
import os

BASE = Path(__file__).resolve().parent.parent
CDN = os.path.join('static_cdn_test')
MEDIA =  os.path.join(CDN,'media')


# get  ---> 1 object
# filter ----> list of objects

# def blog_post_detail_page(request,slug):
#     # try:
#     #     obj = BlogPost.objects.get(id=post_id)
#     # except BlogPost.DoesNotExist:
#     #     raise Http404
#     # except ValueError:
#     #     raise  Http404
#
#     # queryset = BlogPost.objects.filter(slug=slug)
#     # if queryset.count() == 0:
#     #     raise  Http404
#     #
#     # obj = queryset.first()
#     obj = get_object_or_404(BlogPost,slug=slug)    # id  :  should be an integer value
#
#     template_name = "blog_post_detail.html"
#     context = {"object" : obj}
#     return render(request,template_name,context)

# CRUD : create , retrieve , update, delete
# ..... GET --> Retrieve / List
#.......POST --> Create / update / Delete



# ..................................................................................................................

def blog_post_list_view(request):
    # list out objects
    #  also search
    qs = BlogPost.objects.all().published() # list of python objects
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)  # here filter is used  :  getting objects belongs to currently authenticated user
        qs = (qs | my_qs).distinct()
    # qs = BlogPost.objects.filter(title__icontains = 'hello')        # Searching .... .. . On the basis of title
    template_name = 'blog/list.html'
    context = {'object_list': qs}
    return render(request,template_name,context)


@ login_required(login_url='/login/')
def blog_post_create_view(request):
    # create objects / create blogs
    # use of form
    # request.user will return something if "   @ staff_member_required or above one is present "
    form = BlogPostModelForm(request.POST or None , request.FILES or None)      # request.FILES is used to upload the file from the device, s.t images in our case
    if form.is_valid():
        # print(form.cleaned_data)
        obj = form.save(commit = False)             # commit = False means it is not saving the data .
        obj.user = request.user                     # assigning blog only to that user, who actually create it
        profile = get_object_or_404(Profile, username=str(request.user))
        obj.title = form.cleaned_data.get("title")
        obj.profile = profile
        obj.slug = obj.title + str(obj.pk)              
        slug = obj.title + str(obj.pk)              
        obj.save()                                # here by default commit is True        
        obj = get_object_or_404(BlogPost, slug=slug)     
        if str(obj.image) != "":
            img_loc = str(obj.image)  
            blog_img = Image.open(MEDIA+"\image\\"+img_loc[5:])
            blog_img = blog_img.resize((500, 200), Image.ANTIALIAS)            
            blog_img.save(MEDIA + "/image/" + img_loc[5:])
   
        """
         cd = {"x" : 3, "y": 6}

         then  **cd gives (x=3,y = 6) arguments
         => create(**form.cleaned_data) === create(title=title, slug = slug,content = content)

        """
        # obj = BlogPost.objects.create(**form.cleaned_data)   : this is undertaken by BlogPostModelForm
        form = BlogPostModelForm()      # To reinitialise the form

        """
        obj = BlogPost.objects.create(title = title,slug=slug,content =content)
             # or  ................
        obj = BlogPost()
        obj.title = title
        obj.save()
            """

    template_name = 'blog/form.html'
    context = {'form': form}
    return render(request, template_name, context)


def blog_post_detail_view(request,slug):
    # 1 object --> detail view
    obj = get_object_or_404(BlogPost, slug=slug)    # id  :  should be an integer value
    #comment = Comment.objects.create(post = obj , name = str(request.user), body = content)
    profile = get_object_or_404(Profile, username=str(obj.user))
    cf = CommentForm()
    rf= ReplyForm()
    template_name = "blog/detail.html"
    context       =  {"object": obj,"comment_form":cf , "reply_form":rf, "profile": profile}
    return render(request, template_name, context)


def blog_post_comment(request,slug):
    if request.is_ajax and request.method == "POST":
        # get the form data
        cf = CommentForm(request.POST or None)
        # save the data and after fetch the object in instance
        if cf.is_valid():
            instance = cf.save(commit=False)
            if request.user.is_authenticated:
                instance.name = str(request.user)
            else:
                instance.name = "Annonymous"
            instance.post = get_object_or_404(BlogPost,slug=slug)
            instance.c_user = request.user

            # instance.comment_date = request.POST["comment_data"]
            # serialize in new friend object in json
            instance.save()
            num_of_comments = instance.post.number_of_comments
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance, "id" : instance.id , "comments" : num_of_comments}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    # some error occured
    return JsonResponse({"error": ""}, status=400)

def blog_post_comment_reply(request,slug):
    if request.is_ajax and request.method == 'POST':
        rf = ReplyForm(request.POST or None)
        if rf.is_valid():
            instance = rf.save(commit=False)
            if request.user.is_authenticated:
                instance.name = str(request.user)
            else:
                instance.name = "Annonymous"
            instance.r_user = request.user
            instance.replyto = get_object_or_404(Comment, id=request.POST.get("replyto"))
            nu_of_replies = instance.replyto.reply_set.all().count() + 1
            instance.save()
            ser_instance = serializers.serialize('json',[instance , ])
            return JsonResponse({"instance": ser_instance , "replies" : nu_of_replies, "id" : instance.pk}, status = 200)
        else:
            return JsonResponse({"error": ""}, status =400)
    return JsonResponse({"error":""}, status = 400)


def blog_get_reply(request,slug):
    # if request.is_ajax and request.method ==  'POST':
    obj = get_object_or_404(BlogPost, slug = slug)
    json_data = dict()
    id =  request.POST.get('id')
    it = 0
    cmt_obj = get_object_or_404(Comment, id = id)
    for rep in cmt_obj.reply:
        temp_json = dict()
        print(rep.replyto)
        temp_json["name"] = str(rep.name)
        temp_json["date"] = str(rep.reply_date)
        temp_json["body"] = str(rep.body)
        temp_json["id"] = int(rep.pk)
        json_data[it] = temp_json
        it += 1
    json_data = dumps(json_data)
    return JsonResponse({"data": json_data  },status = 200)

@login_required(login_url='/login/')
def delete_comments(request,slug):
    id = request.POST.get("id")
    post = get_object_or_404(BlogPost, slug=slug)
    cmt = get_object_or_404(Comment,id = id)
    cmt.delete()
    n_cmt = post.number_of_comments
    try:
        return JsonResponse({"num_of_comments" :n_cmt },status = 200)
    except ValidationError:
        return JsonResponse({"error" : " "},status = 400)

@login_required(login_url='/login/')
def delete_replies(request, slug):
    id = request.POST.get("id")
    id_reply = request.POST.get("id_reply")
    post = get_object_or_404(BlogPost, slug=slug)
    cmt = get_object_or_404(Comment, id = id)
    reply = get_object_or_404(Reply, id= id_reply)
    reply.delete()
    n_rep = cmt.number_of_reply
    try:
        return JsonResponse({"num_of_reply" : n_rep},status = 200)
    except ValidationError:
        return JsonResponse({"error" : " "}, status = 400)


@login_required(login_url='/login/')
def blog_post_likes(request,slug):
    posts = get_object_or_404(BlogPost,slug=slug)
    flag = 1
    if posts.likes.filter(id__iexact=request.user.id).exists():
        posts.likes.remove(request.user)
        flag = 0
    else:
        posts.likes.add(request.user)
        flag = 1
    like_count = posts.likes.count()
    try:
        return JsonResponse({"like": like_count, "flag": flag},status = 200)
    except ValidationError :
        return JsonResponse({"error":""},status = 400)
    # return HttpResponseRedirect(reverse('blogpost-detail',args=[str(slug)]))


@login_required(login_url='/login/')
def blog_post_dislikes(request,slug):
    posts = get_object_or_404(BlogPost,slug=slug)
    flag = 1
    if posts.dislikes.filter(id__iexact=request.user.id).exists():
        posts.dislikes.remove(request.user)
        flag = 0
    else:
        posts.dislikes.add(request.user)
        flag = 1

    dislike_count = posts.dislikes.count()
    try:
        return JsonResponse({"dislike": dislike_count, "flag" : flag},status = 200)
    except ValidationError :
        return JsonResponse({"error":""},status = 400)

    # return HttpResponseRedirect(reverse("blogpost-detail",args = [str(slug)]))


""" Generic way for implementing Detail View
"""
# class BlogPostDetailView(DetailView):
#     model = BlogPost

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         post = Comment.objects.all().order_by('-comment_date')
#         data['comment_set']  = post
#         data['comment_form'] = CommentForm(instance=self.request.user)
#         return data

#     def post(self, request, *args, **kwargs):
#         new_comment =Comment(body=request.POST.get('body'),
#                                   name=self.request.user,
#                                   post=self.get_object())
#         new_comment.save()
#         return self.get(self, request, *args, **kwargs)


def blog_post_update_view(request,slug):
    obj = get_object_or_404(BlogPost, slug=slug)    # id  :  should be an integer value
    form = BlogPostModelForm(request.POST or None ,instance=obj)
    if form.is_valid():
        form.save()
    template_name = "blog/form.html"
    context = {  'form' : form , "title" : f"Update {obj.title} "}
    return render(request, template_name, context)


def blog_post_delete_view(request , slug):
    obj = get_object_or_404(BlogPost, slug=slug)    # id  :  should be an integer value
    template_name = "blog/delete.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)
