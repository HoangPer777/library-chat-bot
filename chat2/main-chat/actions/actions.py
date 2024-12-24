
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

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
library_users = [{"id":1,"name":"Hung Le", "username":"hung123", "password":"haha123"}]

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

class ActionHandleUser(Action):
    def name(self) -> str:
        return "action_handle_user"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        username = tracker.get_slot("username")
        password = tracker.get_slot("password")

        # Kiểm tra nếu `name` là None (người dùng muốn đăng nhập)
        if name is None:
            if username is None or password is None:
                dispatcher.utter_message(text="Vui lòng cung cấp đầy đủ tên đăng nhập và mật khẩu.")
                return []

            # Thực hiện đăng nhập
            for user in library_users:
                if user["username"] == username and user["password"] == password:
                    dispatcher.utter_message(text=f"Đăng nhập thành công! Chào mừng, {user['name']}.")
                    return [SlotSet("name", user["name"])]

            dispatcher.utter_message(text="Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng thử lại.")
            return [SlotSet("name", None)]

        # Nếu `name` có giá trị (người dùng muốn đăng ký)
        if username is None or password is None:
            dispatcher.utter_message(text="Đăng ký thất bại. Vui lòng cung cấp đầy đủ thông tin.")
            return []

        # Tạo ID tự động cho người dùng mới
        user_id = len(library_users) + 1

        # Lưu thông tin người dùng vào danh sách
        library_users.append({
            "id": user_id,
            "name": name,
            "username": username,
            "password": password
        })

        dispatcher.utter_message(
            text=f"Đăng ký thành công! Chúc mừng {name}, bạn đã đăng ký với tên người dùng: {username}.")
        return []
