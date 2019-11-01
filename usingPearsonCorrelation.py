from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# datasets books,student,rating
books = pd.read_csv('booksForExcel.csv', error_bad_lines=False, encoding="latin-1")
# columns of books dataset
books.columns = ['ISBN', 'bookTitle',
                 'bookAuthor', 'yearOfPublication', 'publisher']
print(books)
users = pd.read_csv('student.csv', error_bad_lines=False, encoding="latin-1")
# columns of student dataset
users.columns = ['userID', 'Name', 'Age', 'Interest']
print(users)
ratings = pd.read_csv('ratings.csv',
                      error_bad_lines=False, encoding="latin-1")
# columns of rating dataset
ratings.columns = ['userID', 'ISBN', 'bookRating']
print(ratings)

# shape of rating dataset,gives the dimension of dataset i.e the number of rows and columns
print(ratings.shape)
# list of rating columns
print(list(ratings.columns))

print(books.shape)
# list of books columns
print(list(books.columns))

print(users.shape)
# list of student columns
print(list(users.columns))


# rating distributution using histogram
plt.rc("font", size=15)
ratings.bookRating.value_counts(sort=False).plot(kind='bar')
plt.title('Rating Distribution\n')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.savefig('system1.png', bbox_inches='tight')
plt.show()

# student age distributution using histogram
users.Age.hist(bins=[18, 20, 22, 24, 26, 28, 30, 32, 40])
plt.title('Age Distribution\n')
plt.xlabel('Age')
plt.ylabel('Count')
plt.savefig('system2.png', bbox_inches='tight')
plt.show()


# recommendation based on rating count
rating_count = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
print(rating_count)
# sorting of the counts of rating to get the highest rated books
rating_count.sort_values('bookRating', ascending=False).head()
xy = rating_count.sort_values('bookRating', ascending=False).head(5)
print(xy)


# books details of first 5 book which received highest rating by students
most_rated_books = pd.DataFrame(['978-8120349391', '978-0198070887', '978-9351341741',
                                 '978-0198083542', '978-9351343257'], index=np.arange(5), columns=['ISBN'])
most_rated_books_summary = pd.merge(most_rated_books, books, on='ISBN')
most_rated_books_summary


# recommendations based on correlations
# here Pearson correlation coefficient used to measure the linear correlation between
# two variable --- the ratings for two books
# fetch the average rating and the count of rating each book received
average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
print(average_rating)
average_rating['ratingCount'] = pd.DataFrame(
    ratings.groupby('ISBN')['bookRating'].count())
average_rating.sort_values('ratingCount', ascending=False).head(10)
# here the main disadvantage is that, the book which got highest number of rating
# has the rating average is low
# observation-- in this dataset the book that received the most rating counts was not highly
# rated at all. So if we are going to use recommendation based on
# rating counts,we would definitely make mistake or wrong recommendation.


# to ensure statistical significance,

# student who rate books and their count >=3
counts1 = ratings['userID'].value_counts()
print(counts1)
ratings = ratings[ratings['userID'].isin(counts1[counts1 >= 1].index)]
print(ratings)
counts = ratings['bookRating'].value_counts()
print(counts)
# rating of book > 2
ratings = ratings[ratings['bookRating'].isin(counts[counts >= 1].index)]
print(ratings)


# ---------------------------------------------------------------
# using pearson correlation

# rating matrix
# convert the rating table into 2D matrix.
# generate sparse matrix because not all students rated book
# by using pivot table we will be able to create combination of userId and isbn
# this will give us that whether the student is rated a book either NAN is given
#
ratings_pivot = ratings.pivot(index='userID', columns='ISBN').bookRating
userID = ratings_pivot.index
print(userID)
ISBN = ratings_pivot.columns
print(ISBN)
print(ratings_pivot.shape)
ratings_pivot.head()

# pearson algorithm to find correlation between the isbn with other

someBookIsbn_ratings = ratings_pivot['978-0070634244']
similar_to_someBookIsbn_ratings = ratings_pivot.corrwith(someBookIsbn_ratings)
corr_someBookIsbn = pd.DataFrame(
    similar_to_someBookIsbn_ratings, columns=['pearsonR'])
corr_someBookIsbn.dropna(inplace=True)
corr_summary = corr_someBookIsbn.join(average_rating['ratingCount'])
corr_summary[corr_summary['ratingCount'] >= 2].sort_values(
    'pearsonR', ascending=False).head(10)
#  book details
books_corr_to_someBookIsbn = pd.DataFrame(['978-0070634244', '978-9351341741'],
                                          index=np.arange(2), columns=['ISBN'])
corr_books = pd.merge(books_corr_to_someBookIsbn, books, on='ISBN')
corr_books
