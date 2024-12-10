from datetime import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pandas as pd
import csv


class ActionCheckBooksBorrowed(Action):
    def name(self):
        return "action_check_books_borrowed"

    def run(self, dispatcher, tracker):
        user_id = tracker.get_slot("user_id")

        if not user_id:
            dispatcher.utter_message("Vui lòng đăng nhập để kiểm tra thông tin mượn sách.")
            return []

        df = pd.read_csv("Borrowed.csv")
        borrowed_books = df[df["user_id"] == user_id]

        borrowed_books_count = len(borrowed_books)

        if borrowed_books_count > 0:
            book_list = ""
            for index, row in borrowed_books.iterrows():
                book_list += f"- {row['title']}\n"

            dispatcher.utter_message(f"Bạn đã mượn {borrowed_books_count} cuốn sách:\n{book_list}")
        else:
            dispatcher.utter_message("Bạn chưa mượn cuốn sách nào.")

        return []

class ActionGetDetailHistory(Action):
    def name(self) -> Text:
        return "action_get_detail_history"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.get_slot("user_id")

        if not user_id:
            dispatcher.utter_message("Vui lòng đăng nhập để kiểm tra thông tin mượn sách.")
            return []

        try:

            df = pd.read_csv("Borrowed.csv")
            books_df = pd.read_csv("Books.csv")
            user_df = pd.read_csv("Users.csv")
            user_name = user_df.loc[user_df['user_id'] == user_id, 'user_name'].values[0]
        except Exception as e:
            dispatcher.utter_message("Không thể tải dữ liệu. Vui lòng kiểm tra các file CSV.")
            return []


        borrowed_books = df[df["user_id"] == int(user_id)]

        if borrowed_books.empty:
            dispatcher.utter_message(f"Không có thông tin mượn sách cho người dùng ID: {user_id}.")
            return []

        # Generate the list of borrowed books
        book_list = ""
        for index, row in borrowed_books.iterrows():
            book_id = row['id_book']
            book_details = books_df[books_df['book_id'] == book_id]
            if not book_details.empty:
                title = book_details.iloc[0]['title']
                start_date = row['start_date']
                end_date = row['end_date']
                returned = row['returned']
                book_list += f"- {title} (Ngày mượn: {start_date}, Hạn trả: {end_date}, Ngày trả: {returned})\n"

        # Send the response
        if book_list:
            dispatcher.utter_message(f"Thông tin sách bạn đã mượn:\n{book_list}")
        else:
            dispatcher.utter_message("Không tìm thấy thông tin sách bạn đã mượn.")

        return []


class ActionCalculateFee(Action):
    def name(self) -> str:
        return "action_calculate_fee"

    def run(self, dispatcher, tracker, domain):
        # Lấy user_id từ slot
        user_id = tracker.get_slot("user_id")

        # Kiểm tra nếu không có user_id
        if not user_id:
            dispatcher.utter_message("Vui lòng đăng nhập để kiểm tra thông tin.")
            return []

        # Đọc dữ liệu từ các tệp CSV
        users_df = pd.read_csv("users.csv")
        books_df = pd.read_csv("books.csv")
        borrowed_df = pd.read_csv("borrowed.csv")

        # Lấy thông tin người dùng
        user_data = users_df[users_df['user_id'] == user_id]
        if user_data.empty:
            dispatcher.utter_message(f"Bạn chưa đăng nhập để có thể hỏi ")
            return []

        user_name = user_data['user_name'].values[0]

        # Lấy thông tin sách đã mượn của người dùng
        borrowed_books = borrowed_df[borrowed_df['user_id'] == user_id]
        total_fee = 0
        current_date = datetime.now().date()

        # Lặp qua từng sách mượn
        for _, row in borrowed_books.iterrows():
            book_id = row['book_id']
            start_date = datetime.strptime(row['start_date'], "%Y-%m-%d").date()
            end_date = datetime.strptime(row['end_date'], "%Y-%m-%d").date()
            returned_date = row['returned'] if pd.notna(row['returned']) else None

            # Lấy thông tin sách
            book_data = books_df[books_df['book_id'] == book_id]
            if book_data.empty:
                continue  # Nếu không tìm thấy sách, bỏ qua
            price_per_day = book_data['price_per_day'].values[0]

            # Tính số ngày trễ nếu có
            late_fee = 0
            if returned_date:
                returned_date = datetime.strptime(returned_date, "%Y-%m-%d").date()
                if returned_date > end_date:
                    late_days = (returned_date - end_date).days
                    late_fee = late_days * 10000  # Phí trễ, giả sử 10,000 VNĐ/ngày trễ

            # Tính phí mượn sách
            if returned_date:
                days_borrowed = (returned_date - start_date).days
            else:
                days_borrowed = (current_date - start_date).days

            book_fee = days_borrowed * price_per_day
            total_fee += book_fee + late_fee

        # Thông báo tổng số tiền phải trả
        if total_fee > 0:
            dispatcher.utter_message(f"{user_name}, bạn phải trả tổng cộng {total_fee} VNĐ cho các cuốn sách đã mượn.")
        else:
            dispatcher.utter_message(f"{user_name}, bạn không có sách nào mượn hoặc chưa có khoản phí nào.")

        return []

class ActionGetBookDescription(Action):
    def name(self) -> str:
        return "action_get_book_description"

    def run(self, dispatcher, tracker, domain):
        # Lấy thông tin từ slot (người dùng có thể hỏi theo tên sách hoặc ID sách)
        book_query = tracker.get_slot("book_query")  # Cái này sẽ chứa thông tin như tên sách hoặc ID sách

        # Kiểm tra nếu không có tên sách
        if not book_query:
            dispatcher.utter_message("Vui lòng cung cấp tên sách hoặc ID sách để tra cứu thông tin.")
            return []

        # Đọc dữ liệu từ tệp sách
        books_df = pd.read_csv("books.csv")

        # Kiểm tra nếu book_query là ID sách (số)
        if book_query.isdigit():
            book_id = int(book_query)
            book_data = books_df[books_df['book_id'] == book_id]
        else:
            # Nếu book_query là tên sách, tìm kiếm sách theo tên
            book_data = books_df[books_df['title'].str.contains(book_query, case=False, na=False)]

        # Nếu không tìm thấy sách
        if book_data.empty:
            dispatcher.utter_message(f"Không tìm thấy thông tin về cuốn sách '{book_query}'.")
            return []

        # Nếu tìm thấy sách, trả về mô tả sách
        book_title = book_data['title'].values[0]
        book_description = book_data['describe'].values[0]

        dispatcher.utter_message(f"Mô tả về cuốn sách '{book_title}': {book_description}")

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



