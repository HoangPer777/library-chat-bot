from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd


class ActionCheckBooksBorrowed(Action):
    def name(self):
        return "action_check_books_borrowed"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.get_slot("user_id")

        if not user_id:
            dispatcher.utter_message("Vui lòng đăng nhập để kiểm tra thông tin mượn sách.")
            return []

        df = pd.read_csv("borrowed.csv")
        borrowed_books = df[df["user_id"] == user_id]

        borrowed_books_count = len(borrowed_books)

        if borrowed_books_count > 0:
            book_list = ""
            for index, row in borrowed_books.iterrows():
                book_list += f"- {row['book_title']}\n"

            dispatcher.utter_message(f"Bạn đã mượn {borrowed_books_count} cuốn sách:\n{book_list}")
        else:
            dispatcher.utter_message("Bạn chưa mượn cuốn sách nào.")

        return []


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



# class ActionSearchBook(Action):
#     def name(self) -> Text:
#         return "action_search_book"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Đọc dữ liệu từ file CSV
#         books_df = pd.read_csv("data/List_books.csv")
#
#         # Lấy thông tin từ các entities
#         book_name = next(tracker.get_latest_entity_values("book_name"), None)
#         author = next(tracker.get_latest_entity_values("author"), None)
#         category = next(tracker.get_latest_entity_values("category"), None)
#
#         # Tìm kiếm sách trong dataframe
#         results = books_df[
#             (books_df["name"].str.contains(book_name, na=False, case=False) if book_name else True) &
#             (books_df["author"].str.contains(author, na=False, case=False) if author else True) &
#             (books_df["category"].str.contains(category, na=False, case=False) if category else True)
#         ]
#
#         # Phản hồi kết quả
#         if not results.empty:
#             result_message = "\n".join(
#                 f"{row['name']} by {row['author']} ({row['category']})"
#                 for _, row in results.iterrows()
#             )
#             dispatcher.utter_message(text=f"Dưới đây là sách phù hợp:\n{result_message}")
#         else:
#             dispatcher.utter_message(text="Xin lỗi, không tìm thấy sách phù hợp với yêu cầu của bạn.")
#
#         return []
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

        # Giả lập dữ liệu thư viện
        library_books = [
            {"name": "Harry Potter", "author": "J.K. Rowling", "category": "Fantasy"},
            {"name": "Sherlock Holmes", "author": "Arthur Conan Doyle", "category": "Mystery"},
            {"name": "Lập trình Python", "author": "Hoàng Phạm", "category": "Computer Science"}
        ]

        # Tìm kiếm sách
        results = []
        for book in library_books:
            if (book_name and book_name.lower() in book["name"].lower()) or \
               (author and author.lower() in book["author"].lower()) or \
               (category and category.lower() in book["category"].lower()):
                results.append(f"{book['name']} by {book['author']} ({book['category']})")

        # Phản hồi kết quả
        if results:
            result_message = "\n".join(results)
            dispatcher.utter_message(text=f"Dưới đây là sách phù hợp:\n{result_message}")
        else:
            dispatcher.utter_message(text="Xin lỗi, không tìm thấy sách phù hợp với yêu cầu của bạn.")

        return []


