from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# import pandas as pd
import csv

class ActionCheckBookAvailability(Action):
    def name(self) -> Text:
        return "action_check_book_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lấy tên sách từ tracker
        book_name = tracker.get_slot("book_name")

        # Giả lập kiểm tra sách
        available_books = ["Harry Potter", "Sherlock Holmes", "Lập trình Python"]
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
        # Lấy thông tin từ các entities
        book_name = next(tracker.get_latest_entity_values("book_name"), None)
        author = next(tracker.get_latest_entity_values("author"), None)
        category = next(tracker.get_latest_entity_values("category"), None)

        # Giả lập dữ liệu thư viện với thông tin số lượng và vị trí
        library_books = [
            {"name": "Harry Potter", "author": "J.K. Rowling", "category": "Fantasy", "quantity": 3, "location": "kệ 2 dãy 5"},
            {"name": "Sherlock Holmes", "author": "Arthur Conan Doyle", "category": "Mystery", "quantity": 5, "location": "kệ 1 dãy 3"},
            {"name": "Lập trình Python", "author": "Hoàng Phan", "category": "Computer Science", "quantity": 2, "location": "kệ 3 dãy 1"}
        ]

        # Tìm kiếm sách
        results = []
        for book in library_books:
            if (book_name and book_name.lower() in book["name"].lower()) or \
                (author and author.lower() in book["author"].lower()) or \
                (category and category.lower() in book["category"].lower()):
                # Thêm thông tin số lượng và vị trí vào kết quả
                results.append(f"{book['name']} by {book['author']} ({book['category']}) - Số lượng: {book['quantity']} - Vị trí: {book['location']}")

        # Phản hồi kết quả
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


class ActionFindBook(Action):
    def name(self) -> Text:
        return "action_find_book"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        # Lấy từ khóa từ câu hỏi của người dùng
        book_title = tracker.get_slot("book_title")

        if not book_title:
            dispatcher.utter_message(text="Vui lòng nhập tên sách bạn muốn tìm!")
            return []

        # Đường dẫn đến file CSV
        file_path = "data/books.csv"

        # Đọc file CSV và tìm sách
        book_found = None
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if book_title.lower() in row['Title'].lower():
                        book_found = row
                        break
        except FileNotFoundError:
            dispatcher.utter_message(text="Không tìm thấy file dữ liệu sách.")
            return []

        # Phản hồi kết quả
        if book_found:
            message = (f"Sách '{book_found['Title']}' của tác giả {book_found['Author']} "
                       f"đang ở {book_found['Location']}. "
                       f"Số lượng còn lại: {book_found['Quantity']}.")
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"Không tìm thấy sách có tên '{book_title}'.")

        return []



