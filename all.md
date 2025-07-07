>>> load csv data to django model  
Here's a step-by-step guide on how to load CSV data into a Django model:

**Step 1: Create your Django model**

Create a new model in your Django app by running the following command:
```
python manage.py makemigrations
python manage.py migrate
```
Then, create a new file called `models.py` in your app directory and add 
your model definition. For example:
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
```
**Step 2: Create a CSV file**

Create a new CSV file (e.g., `books.csv`) and add the data you want to 
load into your model. The CSV file should have the same column names as 
your model fields.

For example:
```csv
"title","author","publication_date"
"The Great Gatsby", "F. Scott Fitzgerald", 1925-04-10
"To Kill a Mockingbird", "Harper Lee", 1960-07-11
"Pride and Prejudice", "Jane Austen", 1813-01-28
```
**Step 3: Load the CSV data into your model**

You can use Django's built-in `loaddata` management command to load the 
CSV data into your model. First, create a new directory called `fixtures` 
in your app directory, and add your CSV file to it:
```bash
mkdir myapp/fixtures
mv books.csv myapp/fixtures/
```
Then, run the following command to load the data:
```
python manage.py loaddata fixtures/books.csv
```
This will create new instances of your model based on the data in the CSV 
file.

**Step 4: Verify the data is loaded correctly**

You can verify that the data has been loaded correctly by running:
```
python manage.py shell
```
Then, in the Python interpreter, you can query your model to see the 
loaded data:
```python
from myapp.models import Book

books = Book.objects.all()
for book in books:
    print(book.title, book.author, book.publication_date)
```
This should output the data from your CSV file.

That's it! You have successfully loaded CSV data into a Django model.
