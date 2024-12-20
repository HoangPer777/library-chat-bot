from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# import pandas as pd
import csv
library_users = [
    {"name": "Admin", "email": "admin@example.com", "password": "adminpass"}
]
library_books = [
    {"name": "Harry Potter", "author": "J.K. Rowling", "category": "Fantasy", "quantity": 3, "location": "kệ 2 dãy 5"},
    {"name": "Sherlock Holmes", "author": "Arthur Conan Doyle", "category": "Mystery", "quantity": 5,
     "location": "kệ 1 dãy 3"},
    {"name": "Lập trình Python", "author": "Hoàng Phan", "category": "Computer Science", "quantity": 2,
     "location": "kệ 3 dãy 1"},
    {"name": "The Lord of the Rings", "author": "J.R.R. Tolkien", "category": "Fantasy", "quantity": 6,
     "location": "kệ 2 dãy 6"},
    {"name": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance", "quantity": 3,
     "location": "kệ 7 dãy 2"},
    {"name": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Historical Fiction", "quantity": 4,
     "location": "kệ 3 dãy 4"},
    {"name": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "category": "History",
     "quantity": 2, "location": "kệ 9 dãy 1"},
    {"name": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "category": "Psychology", "quantity": 5,
     "location": "kệ 6 dãy 3"},
    {"name": "Atomic Habits", "author": "James Clear", "category": "Self-Help", "quantity": 7,
     "location": "kệ 1 dãy 5"},
    {"name": "The Silent Patient", "author": "Alex Michaelides", "category": "Thriller", "quantity": 3,
     "location": "kệ 8 dãy 2"},
    {"name": "The Da Vinci Code", "author": "Dan Brown", "category": "Mystery", "quantity": 4,
     "location": "kệ 4 dãy 3"},
    {"name": "Steve Jobs", "author": "Walter Isaacson", "category": "Biography", "quantity": 2,
     "location": "kệ 5 dãy 1"},
    {"name": "Mastering the Art of French Cooking", "author": "Julia Child", "category": "Cookbook", "quantity": 1,
     "location": "kệ 10 dãy 4"},
    {"name": "Tôi thấy hoa vàng trên cỏ xanh", "author": "Nguyễn Nhật Ánh", "category": "Fiction",
     "quantity": 5, "location": "kệ 3 dãy 2"},
    {"name": "Đất rừng phương Nam", "author": "Đoàn Giỏi", "category": "Adventure", "quantity": 3,
     "location": "kệ 6 dãy 1"},
    {"name": "Gone Girl", "author": "Gillian Flynn", "category": "Thriller", "quantity": 4,
     "location": "kệ 7 dãy 3"},
    {"name": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "category": "Science Fiction",
     "quantity": 6, "location": "kệ 9 dãy 4"},
    {"name": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic", "quantity": 2,
     "location": "kệ 2 dãy 1"},
    {"name": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "category": "Finance", "quantity": 7,
     "location": "kệ 10 dãy 2"},
    {"name": "The Alchemist", "author": "Paulo Coelho", "category": "Philosophical Fiction", "quantity": 5,
     "location": "kệ 5 dãy 4"},
    {"name": "Kafka on the Shore", "author": "Haruki Murakami", "category": "Magical Realism", "quantity": 3,
     "location": "kệ 8 dãy 1"}
]
class ActionRegisterUser(Action):
    def name(self) -> Text:
        return "action_register_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        password = tracker.get_slot("password")

        if name and email and password:
            # Lưu thông tin vào cơ sở dữ liệu hoặc logic khác
            message = f"Đăng ký thành công! Chào mừng {name}."
        else:
            message = "Thông tin không đầy đủ. Vui lòng thử lại."

        dispatcher.utter_message(text=message)
        return []

class ActionLoginUser(Action):
    def name(self) -> Text:
        return "action_login_user"

    def run(self, dispatcher, tracker, domain):
        email = tracker.get_slot("email")
        password = tracker.get_slot("password")

        # Kiểm tra thông tin đăng nhập
        user = next((user for user in library_users if user["email"] == email and user["password"] == password), None)

        if user:
            dispatcher.utter_message(response="utter_login_success")
            return [SlotSet("is_authenticated", True)]
        else:
            dispatcher.utter_message(response="utter_login_failure")
            return [SlotSet("is_authenticated", False)]

class ActionCheckBookAvailability(Action):
    def name(self) -> Text:
        return "action_check_book_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        book_name = tracker.get_slot("book_name")

        # Kiểm tra sách từ library_books toàn cục
        available_books = [book["name"] for book in library_books]
        if book_name in available_books:
            message = f"Sách '{book_name}' hiện có sẵn trong thư viện."
        else:
            message = f"Xin lỗi, sách '{book_name}' hiện không có sẵn."

        dispatcher.utter_message(text=message)
        return []

class ActionIAmABot(Action):
    def name(self) -> str:
        return "utter_iamabot"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I am a library chatbot. How can I assist you today?")
        return []

class ActionSearchBook(Action):
    def name(self) -> Text:
        return "action_search_book"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        book_name = next(tracker.get_latest_entity_values("book_name"), None)
        author = next(tracker.get_latest_entity_values("author"), None)
        category = next(tracker.get_latest_entity_values("category"), None)

        # Tìm kiếm sách trong library_books toàn cục
        results = []
        for book in library_books:
            if (book_name and book_name.lower() in book["name"].lower()) or \
                (author and author.lower() in book["author"].lower()) or \
                (category and category.lower() in book["category"].lower()):
                results.append(f"{book['name']} by {book['author']} ({book['category']}) - Số lượng: {book['quantity']} - Vị trí: {book['location']}")

        if results:
            result_message = "\n".join(results)
            dispatcher.utter_message(text=f"Dưới đây là sách phù hợp:\n{result_message}")
        else:
            dispatcher.utter_message(text="Xin lỗi, không tìm thấy sách phù hợp với yêu cầu của bạn.")

        return []

class ActionSetCategory(Action):
    def name(self):
        return "action_set_category"

    def run(self, dispatcher, tracker, domain):
        # Lấy thông tin category từ câu hỏi của người dùng
        category = tracker.latest_message.get('text', '').lower()

        # Xác định category từ câu hỏi
        if "java" in category:
            category_value = "Java"
        elif "python" in category:
            category_value = "Python"
        elif "c#" in category:
            category_value = "C#"
        else:
            category_value = None  # Không xác định được

        if not category_value:
            dispatcher.utter_message(text="Bạn có thể cho tôi biết chủ đề sách bạn muốn tìm không?")
        else:
            return [SlotSet("category", category_value)]  # Trả về SlotSet


class ActionGetRecommendedBooks(Action):
    def name(self):
        return "action_get_recommended_books"

    def run(self, dispatcher, tracker, domain):
        # Lấy giá trị category từ slot
        category = tracker.get_slot("category")

        # Danh sách sách tham khảo cho từng category
        books = {
            "Java": ["Effective Java", "Java: The Complete Reference"],
            "Python": ["Learning Python", "Python Crash Course"],
            "C#": ["C# in Depth", "The C# Programming Language"],
            "khác": ["Sách khác về lập trình"]
        }

        # Kiểm tra nếu category không có sách tham khảo
        if category not in books:
            dispatcher.utter_message(text="Xin lỗi, hiện tại tôi không có sách tham khảo cho chủ đề này.")
        else:
            recommended_books = books.get(category, [])
            dispatcher.utter_message(
                text=f"Dưới đây là một số sách tham khảo về {category}: {', '.join(recommended_books)}")

        return []


# class ActionFindBook(Action):
#     def name(self) -> Text:
#         return "action_find_book"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict) -> list:
#         # Lấy từ khóa từ câu hỏi của người dùng
#         book_title = tracker.get_slot("book_title")
#
#         if not book_title:
#             dispatcher.utter_message(text="Vui lòng nhập tên sách bạn muốn tìm!")
#             return []
#
#         # Đường dẫn đến file CSV
#         file_path = "data/books.csv"
#
#         # Đọc file CSV và tìm sách
#         book_found = None
#         try:
#             with open(file_path, newline='', encoding='utf-8') as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 for row in reader:
#                     if book_title.lower() in row['Title'].lower():
#                         book_found = row
#                         break
#         except FileNotFoundError:
#             dispatcher.utter_message(text="Không tìm thấy file dữ liệu sách.")
#             return []
#
#         # Phản hồi kết quả
#         if book_found:
#             message = (f"Sách '{book_found['Title']}' của tác giả {book_found['Author']} "
#                        f"đang ở {book_found['Location']}. "
#                        f"Số lượng còn lại: {book_found['Quantity']}.")
#             dispatcher.utter_message(text=message)
#         else:
#             dispatcher.utter_message(text=f"Không tìm thấy sách có tên '{book_title}'.")
#
#         return []



