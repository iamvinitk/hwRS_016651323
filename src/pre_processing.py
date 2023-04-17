import pandas as pd


def is_url(s):
    if s.startswith("http"):
        return True
    return False


f = open("./dataset/book_info.csv", "r")

# This assumes your spacing is arbitrary
data = [line for line in f]
headers = ["book_id", "title", "author", "year", "publisher", "image_url_s",
           "image_url_m",
           "image_url_l"]

cleaned_data = []

count = 0
x = []
# reverse the order of the list
for i in range(1, len(data)):
    try:
        values = data[i].split(",")
        values.reverse()
        book_id = str(values.pop())
        start_index = 0
        image_url_s = ""
        image_url_m = ""
        image_url_l = ""
        if is_url(values[2]) and is_url(values[1]) and is_url(values[0]):
            image_url_s = values[2]
            image_url_m = values[1]
            image_url_l = values[0].replace("\n", "")
            start_index = 3
        elif is_url(values[1]) and is_url(values[0]):
            image_url_s = values[1]
            image_url_m = values[0].replace("\n", "")
            image_url_l = ""
            start_index = 2
        elif is_url(values[0]):
            image_url_s = values[0].replace("\n", "")
            image_url_m = ""
            image_url_l = ""
            start_index = 1
        # find the index from the start which is a number in the string format
        end_index = 0
        for j in range(len(values)):
            if values[j].isdigit():
                end_index = j
                break
        publisher = str(values[start_index:end_index])
        year_of_publication = int(values[end_index])
        book_author = values[end_index + 1]
        book_title = str(values[end_index + 2:])
        # remove all characters except letters and numbers
        book_title = ''.join(e for e in book_title if e.isalnum() or e == ' ')
        book_author = ''.join(e for e in book_author if e.isalnum() or e == ' ')
        publisher = ''.join(e for e in publisher if e.isalnum() or e == ' ')
        if book_id == 290831:
            print(values)
            print(book_id, book_title, book_author, year_of_publication, publisher, image_url_s, image_url_m,
                  image_url_l)
        cleaned_data.append(
            [book_id, book_title, book_author, year_of_publication, publisher, image_url_s, image_url_m, image_url_l])
    except Exception as e:
        print("Error", e)
        count += 1
        x.append(i)
        pass

# save as a new csv file
df = pd.DataFrame(cleaned_data, columns=headers)
df.to_csv('dataset/cleaned_books.csv', index=False, header=True)
print("Number of errors: ", count)
