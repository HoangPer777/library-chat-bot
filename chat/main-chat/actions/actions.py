from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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