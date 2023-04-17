import pandas as pd
from surprise import Reader, Dataset
from surprise import SVD

train = pd.read_csv("./dataset/train.csv")
test = pd.read_csv("./dataset/test.csv")
books = pd.read_csv("./dataset/cleaned_books.csv")
users = pd.read_csv("./dataset/user_info.csv")

users.rename(columns={'User_Id': 'user_id', 'Location': 'location', 'Age': 'age'}, inplace=True)
train = train.rename(columns={'User_Id': 'user_id', 'Rating': 'rating', 'Book_Id': 'book_id'})
test = test.rename(columns={'User_Id': 'user_id', 'Book_Id': 'book_id'})

train['rating'] = train['rating'].apply(lambda x: 10 if x > 10 else x)

validation = pd.read_csv("./test_data.csv")

hyper_params = {
    'n_epochs': [100, 1000],
    'n_factors': [10],
    'lr_all': [0.001, 0.005, 0.01, 0.05],
    'reg_all': [0.08, 0.09]
}

reader = Reader(rating_scale=(1, 10))

data = Dataset.load_from_df(train[['user_id', 'book_id', 'rating']], reader)


def process(_n_epochs, _n_factors, _lr_all, _reg_all):
    algo = SVD(n_epochs=_n_epochs, n_factors=_n_factors, lr_all=_lr_all, reg_all=_reg_all)
    algo.fit(data.build_full_trainset())
    validation['svd'] = validation.apply(lambda row: algo.predict(row['user_id'], row['book_id']).est,
                                         axis=1)
    # rmse
    rmse = ((validation['svd'] - validation['actual_rating']) ** 2).mean() ** .5
    print(f"n_epochs: {_n_epochs}, n_factors: {_n_factors}, lr_all: {_lr_all}, reg_all: {_reg_all}, rmse: {rmse}")


# if __name__ == '__main__':
#     manager = Manager()
#
#     with ProcessPoolExecutor() as executor:
#         for n_epochs in hyper_params['n_epochs']:
#             for n_factors in hyper_params['n_factors']:
#                 for lr_all in hyper_params['lr_all']:
#                     for reg_all in hyper_params['reg_all']:
#                         executor.submit(process, n_epochs, n_factors, lr_all, reg_all)


# process(100, 10, 0.001, 0.05)

books = books[['book_id', 'title', 'author', 'year', 'publisher']]
books['publisher'] = books['publisher'].fillna('Unknown')
books['author'] = books['author'].fillna('Unknown')

books['title'] = books['title'].str.replace('[^a-zA-Z0-9\s]', '')
books['title'] = books['title'].str.lower()
books['title'] = books['title'].str.replace('\s+', ' ')
books['title'] = books['title'].str.strip()

books['author'] = books['author'].str.replace('[^a-zA-Z0-9\s]', '')
books['author'] = books['author'].str.lower()
books['author'] = books['author'].str.replace('\s+', ' ')
books['author'] = books['author'].str.strip()

books['publisher'] = books['publisher'].str.replace('[^a-zA-Z0-9\s]', '')
books['publisher'] = books['publisher'].str.lower()
books['publisher'] = books['publisher'].str.replace('\s+', ' ')
books['publisher'] = books['publisher'].str.strip()

print(train.shape)
train_df = train.merge(books, on="book_id", how="left")
print(train_df.shape)
train_df = pd.merge(train_df, users, on='user_id', how='left')
print(train_df.shape)


print(validation.shape)
validation_df = validation.merge(books, on="book_id", how="left")
print(validation_df.shape)
validation_df = pd.merge(validation_df, users, on='user_id', how='left')
print(validation_df.shape)