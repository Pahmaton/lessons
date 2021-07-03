with open("simple movie reviews.txt", "r") as file:
    documents = file.read().splitlines()

print(documents)