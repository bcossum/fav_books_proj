from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
  def validator(self, postData):
    errors = {}
    for email_check in User.objects.all():
      if email_check.email == postData['email']:
        errors["email"] = "Email already exists in database"
    
    if not NAME_REGEX.match(postData['first_name']):
      errors['first_name'] = "First name must contain only letters"

    if not NAME_REGEX.match(postData['last_name']):
      errors['last_name'] = "Last name must contain only letters"

    if len(postData['first_name']) < 2:
      errors['first_name'] = "First name must be at least two characters long"

    if len(postData['last_name']) < 2:
      errors['last_name'] = "Last name must be at least two characters long"
    
    if not EMAIL_REGEX.match(postData['email']):      
      errors['email'] = ("Invalid email address!")

    if len(postData['password']) < 8:
      errors['password'] = "Password must be at least eight characters"

    if postData['confirm'] != postData['password']:
      errors['confirm'] = "Password does not match"

    return errors

  def authenticate(self, email, password):
    users = self.filter(email=email)
    if not users:
        return False

    user = users[0]
    return bcrypt.checkpw(password.encode(), user.password.encode())

  def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )

class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

class BookManager(models.Manager):
  def book_validator(self, postData):
    errors = {}
    if len(postData['title']) < 1:
      errors['title'] = "Title must be more than one character"
    if len(postData['desc']) < 5:
      errors['desc'] = "Description must be more than five characters" 
    return errors

class Book(models.Model):
  title = models.CharField(max_length=255)
  desc = models.TextField()
  uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
  liked_by = models.ManyToManyField(User, related_name="liked_books")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = BookManager()