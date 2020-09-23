from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count,Q
from marketing.models import Signup
from django.urls import reverse
from .models import*
from .forms import *


def get_author(user):
	qs = Author.objects.filter(user=user)
	if qs.exists():
		return qs[0]
	return None

def get_category_count():
	queryset=Post.objects.values('categories__title').annotate(Count('categories__title'))
	return queryset

def search(request):
	querset=Post.objects.all()
	query=request.GET.get('q')
	if query:
		queryset=querset.filter(
			Q(title__icontains=query)|
			Q(overview__icontains=query)
			).distinct()
	context={'queryset':queryset}
	return render(request,'search_results.html',context)



def index(request):
	object_list=Post.objects.filter(featured=True)
	latest=Post.objects.order_by('-timestamp')[:3]
	if request.POST:
		email=request.POST['email']
		new_signup=Signup()
		new_signup.email=email
		new_signup.save()
	context={'object_list':object_list,
			'latest':latest,
	}
	return render(request,'index.html',context)

def Blog(request):
	category_count=get_category_count()
	most_recent=Post.objects.order_by('-timestamp')[:3]
	object_list=Post.objects.all()
	paginator = Paginator(object_list, 4)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)
	context={'object_list': paginated_queryset,
			'page_request_var': page_request_var,
			"most_recent":most_recent,
			'category_count':category_count
	}
	return render(request,'blog.html',context)
def PostDetail(request,pk):
	category_count=get_category_count()
	most_recent=Post.objects.order_by('-timestamp')[:3]
	post=get_object_or_404(Post,pk=pk)

	form = CommentForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			form.instance.user = request.user
			form.instance.post = post
			form.save()
			return redirect(reverse("detail", kwargs={
							'pk': post.pk
							}))
	context={'post':post,
	"most_recent":most_recent,
	'category_count':category_count,
	'form':form
	}
	return render(request,'post.html',context)


def PostCreate(request):
	title='Create'
	form=PostForm(request.POST or None, request.FILES or None)
	author=get_author(request.user)
	if request.POST:
		if form.is_valid():
			form.instance.author=author
			form.save()
			return redirect(reverse('detail',kwargs={'pk':form.instance.pk}))
	context={'form':form,'title':title}
	return render(request,'post_create.html',context)

def PostDelete(request,pk):
	post=get_object_or_404(Post,pk=pk)
	post.delete()
	return redirect(reverse('index'))

def PostUpdate(request,pk):
	title='Update'
	post=get_object_or_404(Post,pk=pk)
	form=PostForm(request.POST or None, request.FILES or None,instance=post)
	author=get_author(request.user)
	if request.POST:
		if form.is_valid():
			form.instance.author=author
			form.save()
			return redirect(reverse('detail',kwargs={'pk':form.instance.pk}))
	context={'form':form,'title':title}
	return render(request,'post_create.html',context)