
from typing import Any, Text, Dict, List
from datetime import datetime, timedelta
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

library_users = [
    {"id": 1, "name": "Hung Le", "username": "hung123", "password": "haha123"},
    {"id": 2, "name": "Nguyen Thanh", "username": "nguyen456", "password": "password456"},
    {"id": 3, "name": "Tran Minh", "username": "tran789", "password": "secure789"},
    {"id": 4, "name": "Pham Anh", "username": "pham101", "password": "mysecret101"},
    {"id": 5, "name": "Le Hoang", "username": "lehoang112", "password": "mypassword112"}
]
library_books = [
    {"name": "Harry Potter", "author": "J.K. Rowling", "category": "Fantasy", "quantity": 3, "location": "kệ 2 dãy 5", "rating": 4.8, "borrow_count": 15},
    {"name": "Sherlock Holmes", "author": "Arthur Conan Doyle", "category": "Mystery", "quantity": 5, "location": "kệ 1 dãy 3", "rating": 4.7, "borrow_count": 20},
    {"name": "Lập trình Python", "author": "Hoàng Phan", "category": "Computer Science", "quantity": 2, "location": "kệ 3 dãy 1", "rating": 4.5, "borrow_count": 10},
    {"name": "The Lord of the Rings", "author": "J.R.R. Tolkien", "category": "Fantasy", "quantity": 6, "location": "kệ 2 dãy 6", "rating": 4.9, "borrow_count": 25},
    {"name": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance", "quantity": 3, "location": "kệ 7 dãy 2", "rating": 4.6, "borrow_count": 18},
    {"name": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Historical Fiction", "quantity": 4, "location": "kệ 3 dãy 4", "rating": 4.8, "borrow_count": 22},
    {"name": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "category": "History", "quantity": 2, "location": "kệ 9 dãy 1", "rating": 4.7, "borrow_count": 14},
    {"name": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "category": "Psychology", "quantity": 5, "location": "kệ 6 dãy 3", "rating": 4.6, "borrow_count": 16},
    {"name": "Atomic Habits", "author": "James Clear", "category": "Self-Help", "quantity": 7, "location": "kệ 1 dãy 5", "rating": 4.9, "borrow_count": 30},
    {"name": "The Silent Patient", "author": "Alex Michaelides", "category": "Thriller", "quantity": 3, "location": "kệ 8 dãy 2", "rating": 4.5, "borrow_count": 13},
    {"name": "The Da Vinci Code", "author": "Dan Brown", "category": "Mystery", "quantity": 4, "location": "kệ 4 dãy 3", "rating": 4.6, "borrow_count": 19},
    {"name": "Steve Jobs", "author": "Walter Isaacson", "category": "Biography", "quantity": 2, "location": "kệ 5 dãy 1", "rating": 4.7, "borrow_count": 12},
    {"name": "Mastering the Art of French Cooking", "author": "Julia Child", "category": "Cookbook", "quantity": 1, "location": "kệ 10 dãy 4", "rating": 4.3, "borrow_count": 8},
    {"name": "Tôi thấy hoa vàng trên cỏ xanh", "author": "Nguyễn Nhật Ánh", "category": "Fiction", "quantity": 5, "location": "kệ 3 dãy 2", "rating": 4.8, "borrow_count": 17},
    {"name": "Đất rừng phương Nam", "author": "Đoàn Giỏi", "category": "Adventure", "quantity": 3, "location": "kệ 6 dãy 1", "rating": 4.7, "borrow_count": 11},
    {"name": "Gone Girl", "author": "Gillian Flynn", "category": "Thriller", "quantity": 4, "location": "kệ 7 dãy 3", "rating": 4.6, "borrow_count": 20},
    {"name": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "category": "Science Fiction", "quantity": 6, "location": "kệ 9 dãy 4", "rating": 4.7, "borrow_count": 23},
    {"name": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic", "quantity": 2, "location": "kệ 2 dãy 1", "rating": 4.4, "borrow_count": 9},
    {"name": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "category": "Finance", "quantity": 7, "location": "kệ 10 dãy 2", "rating": 4.6, "borrow_count": 18},
    {"name": "The Alchemist", "author": "Paulo Coelho", "category": "Philosophical Fiction", "quantity": 5, "location": "kệ 5 dãy 4", "rating": 4.9, "borrow_count": 27},
    {"name": "Kafka on the Shore", "author": "Haruki Murakami", "category": "Magical Realism", "quantity": 3, "location": "kệ 8 dãy 1", "rating": 4.7, "borrow_count": 15}
]

library_borrowed = [
    {"id": 1, "id_user": 1, "namebook": "Kafka on the Shore", "date_start": "2024-12-10", "status": 0},
    {"id": 2, "id_user": 2, "namebook": "Harry Potter", "date_start": "2024-12-05", "status": -1},
    {"id": 3, "id_user": 3, "namebook": "To Kill a Mockingbird", "date_start": "2024-12-12", "status": 1},
    {"id": 4, "id_user": 4, "namebook": "The Great Gatsby", "date_start": "2024-12-15", "status": 0},
    {"id": 5, "id_user": 5, "namebook": "Rich Dad Poor Dad", "date_start": "2024-12-08", "status": -1},
    {"id": 6, "id_user": 1, "namebook": "The Alchemist", "date_start": "2024-12-20", "status": 0},
    {"id": 7, "id_user": 2, "namebook": "Sapiens: A Brief History of Humankind", "date_start": "2024-12-09", "status": 1},
    {"id": 8, "id_user": 3, "namebook": "Atomic Habits", "date_start": "2024-12-18", "status": -1},
    {"id": 9, "id_user": 4, "namebook": "Pride and Prejudice", "date_start": "2024-12-11", "status": 0},
    {"id": 10, "id_user": 5, "namebook": "The Silent Patient", "date_start": "2024-12-16", "status": 1},
    {"id": 11, "id_user": 1, "namebook": "The Hitchhiker's Guide to the Galaxy", "date_start": "2024-12-05", "status": 0},
    {"id": 12, "id_user": 2, "namebook": "The Lord of the Rings", "date_start": "2024-12-03", "status": -1},
    {"id": 13, "id_user": 3, "namebook": "Sherlock Holmes", "date_start": "2024-12-07", "status": 0},
    {"id": 14, "id_user": 4, "namebook": "Mastering the Art of French Cooking", "date_start": "2024-12-14", "status": 1},
    {"id": 15, "id_user": 5, "namebook": "Gone Girl", "date_start": "2024-12-17", "status": 0},
    {"id": 16, "id_user": 1, "namebook": "Thinking, Fast and Slow", "date_start": "2024-12-02", "status": -1},
    {"id": 17, "id_user": 2, "namebook": "The Da Vinci Code", "date_start": "2024-12-04", "status": 0},
    {"id": 18, "id_user": 3, "namebook": "Lập trình Python", "date_start": "2024-12-13", "status": 1},
    {"id": 19, "id_user": 4, "namebook": "The Great Gatsby", "date_start": "2024-12-06", "status": 1},
    {"id": 20, "id_user": 5, "namebook": "Steve Jobs", "date_start": "2024-12-01", "status": 0}
]

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


class ActionCheckBooksBorrowed(Action):
    def name(self) -> str:
        return "action_check_books_borrowed"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        username = tracker.get_slot('username')

        # Tìm user_id từ username
        user = next((user for user in library_users if user['username'] == username), None)

        if not user:
            dispatcher.utter_message(text="Bạn chưa đăng nhập hoặc username không đúng.")
            return []

        user_id = user['id']

        # Lọc sách mượn của người dùng theo id_user
        user_books = [book for book in library_borrowed if book['id_user'] == user_id]

        if not user_books:
            dispatcher.utter_message(text="Bạn chưa mượn sách nào.")
            return []

        # Kiểm tra và tính phí phạt
        today = datetime.now()
        penalty_details = []

        for book in user_books:
            date_start = datetime.strptime(book["date_start"], "%d-%m-%Y")
            days_borrowed = (today - date_start).days

            if book["status"] == 0:  # Nếu sách chưa trả
                if days_borrowed > 14:
                    # Phạt 2000 VNĐ mỗi ngày nếu quá hạn sau 14 ngày
                    penalty = (days_borrowed - 14) * 2000
                    penalty_details.append(f"{book['namebook']} - Quá hạn {days_borrowed} ngày, phạt {penalty} VNĐ")
                else:
                    # Phạt 50.000 VNĐ nếu sách chưa trả
                    penalty_details.append(f"{book['namebook']} - Chưa trả, phạt 50.000 VNĐ")
            elif book["status"] == 1:
                # Nếu sách đã trả
                penalty_details.append(f"{book['namebook']} - Đã trả")

        # Hiển thị kết quả
        if penalty_details:
            message = "\n".join(penalty_details)
        else:
            message = "Bạn chưa mượn sách nào."

        dispatcher.utter_message(text=message)
        return []
