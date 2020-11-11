from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages

def index(request):
  context = {
    'all_users': User.objects.all()
  }
  if request.method == 'POST':
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/')
    else:
      new_user = User.objects.register(request.POST)
      request.session['userid'] = new_user.id
      messages.success(request, "Thank you for registering")
      return redirect('/success')
  return render(request, 'index.html', context)

def login(request):
  if request.method == 'GET':
    return redirect('/')
  if not User.objects.authenticate(request.POST['email'], request.POST['password']):
    messages.error(request, 'Invalid Email/Password')
    return redirect('/')
  logged_user = User.objects.get(email=request.POST['email'])
  request.session['userid'] = logged_user.id
  return redirect('/books')

def logout(request):
  request.session.clear()
  return redirect('/')

def success(request):
    if 'userid' not in request.session:
      return redirect('/')
    else:
      context = {
        'user': User.objects.get(id=request.session['userid']),
        'all_books': Book.objects.all()
      }
      return render(request, 'books.html', context)

def add_book(request):
  errors = Book.objects.book_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/books')
  else:
    user = User.objects.get(id=request.session['userid'])
    book = Book.objects.create(
      title = request.POST['title'],
      desc = request.POST['desc'],
      uploaded_by = User.objects.get(id=request.session['userid']),
    )
    user.liked_books.add(book)
    
    return redirect(f'/books/{book.id}')

def show_book(request, book_id):
  context = {
    'book': Book.objects.get(id=book_id),
    'user': User.objects.get(id=request.session['userid']),
  }
  return render(request, 'book_view.html', context)

def update(request, book_id):
  book_update = Book.objects.get(id=book_id)
  book_update.title = request.POST['title']
  book_update.desc = request.POST['desc']
  book_update.save()
  return redirect(f'/books/{book_id}')

def unlike(request, book_id):
  user = User.objects.get(id=request.session['userid'])
  book = Book.objects.get(id=book_id)
  user.liked_books.remove(book)
  return redirect(f'/books/{book_id}')

def like(request, book_id):
  user = User.objects.get(id=request.session['userid'])
  book = Book.objects.get(id=book_id)
  user.liked_books.add(book)
  return redirect(f'/books/{book_id}')

def delete(request, book_id):
  delete_book = Book.objects.get(id=book_id)
  delete_book.delete()
  return redirect('/books')