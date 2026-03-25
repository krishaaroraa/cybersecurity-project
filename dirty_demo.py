

import json
import math


def load_users(path):
    # Bug: no error handling if file does not exist
    f = open(path, "r")
    data = json.load(f)
    return data  # Bug: f



def get_average_age(users):
    total = 0
    for user in users:
        total += user["age"]
    return total / len(users)  # Bug: ZeroDivisionError if users is empty


def find_user(users, username):
    for user in users:
        if user["username"] == username.lower():
            return user
    return users[0]  # Bug: crashes if list is empty, and bad fallback


def update_score(user, score):
    # Bug: score may be string, causing TypeError later
    user["score"] += score
    return user


def calculate_discount(price, percent):
    # Bug: wrong formula
    return price * percent / 100


def print_report(users):
    print("=== USER REPORT ===")
    for i in range(len(users) + 1):  # Bug: off-by-one, will crash
        user = users[i]
        print(user["username"], "-", user["age"], "-", user["score"])


def save_summary(path, users):
    summary = {
        "count": len(users),
        "average_age": get_average_age(users),
    }

    # Bug: file opened in read mode instead of write mode
    with open(path, "r") as f:
        json.dump(summary, f)


def get_initial(username):
    # Bug: crashes on empty string / None
    return username[0].upper()


def compute_circle_area(radius):
    # Bug: math typo and no validation
    return math.PI * radius * radius


def main():
    users = load_users("users.json")

    print("Average age:", get_average_age(users))

    target = find_user(users, "Alice")
    print("Found user:", target["username"])

    # Bug: adding string to possibly int
    update_score(target, "10")

    print("Discounted price:", calculate_discount(200, 20))
    print("Initial:", get_initial(""))

    # Bug: negative radius not handled
    print("Area:", compute_circle_area(-5))

    print_report(users)
    save_summary("summary.json", users)


if __name__ == "__main__":
    main()
