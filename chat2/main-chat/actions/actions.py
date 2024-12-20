# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk import Tracker  # Thêm import Tracker
import re

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


class ActionSearchBook(Action):
    def name(self) -> str:
        return "action_search_book"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain) -> list:
        book_name = tracker.get_slot("book_name")

        # Tìm kiếm sách trong danh sách
        book_found = next((book for book in library_books if book_name.lower() in book['name'].lower()), None)

        if book_found:
            # Trả lời với thông tin vị trí sách và cập nhật slot
            dispatcher.utter_message(text=f"Cuốn sách {book_found['name']} có tại {book_found['location']}.")
            return [SlotSet("book_name", book_found['name']), SlotSet("book_location", book_found['location'])]
        else:
            # Nếu không tìm thấy sách
            dispatcher.utter_message(text="Xin lỗi, chúng tôi không tìm thấy cuốn sách đó trong thư viện.")
            return [SlotSet("book_name", None), SlotSet("book_location", None)]