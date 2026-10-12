import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


Window.clearcolor = (0.06, 0.08, 0.13, 1)


class AqarAS(App):

    def build(self):
        self.title = "عقار AS"

        self.db_path = (
            self.user_data_dir + "/aqar_as.db"
        )

        self.init_database()

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        title = Label(
            text="[b]عقار AS[/b]",
            markup=True,
            font_size="30sp",
            size_hint_y=None,
            height=dp(55),
            color=(0.2, 0.85, 0.65, 1)
        )
        root.add_widget(title)

        subtitle = Label(
            text="نظام إدارة العملاء والتسويق العقاري",
            font_size="15sp",
            size_hint_y=None,
            height=dp(35)
        )
        root.add_widget(subtitle)

        self.name_input = self.make_input(
            "اسم العميل"
        )
        root.add_widget(self.name_input)

        self.phone_input = self.make_input(
            "رقم الهاتف"
        )
        root.add_widget(self.phone_input)

        self.area_input = self.make_input(
            "المنطقة أو المحافظة"
        )
        root.add_widget(self.area_input)

        self.budget_input = self.make_input(
            "الميزانية"
        )
        root.add_widget(self.budget_input)

        self.notes_input = self.make_input(
            "ملاحظات العميل"
        )
        root.add_widget(self.notes_input)

        save_button = Button(
            text="حفظ العميل",
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=(0.05, 0.55, 0.40, 1)
        )
        save_button.bind(
            on_press=self.save_customer
        )
        root.add_widget(save_button)

        list_button = Button(
            text="عرض العملاء المحفوظين",
            size_hint_y=None,
            height=dp(45)
        )
        list_button.bind(
            on_press=self.show_customers
        )
        root.add_widget(list_button)

        self.status = Label(
            text="مرحبًا بك في عقار AS",
            size_hint_y=None,
            height=dp(35)
        )
        root.add_widget(self.status)

        return root

    def make_input(self, hint):
        return TextInput(
            hint_text=hint,
            multiline=False,
            size_hint_y=None,
            height=dp(46),
            padding=[dp(10), dp(12)],
            font_size="16sp"
        )

    def init_database(self):
        with sqlite3.connect(
            self.db_path
        ) as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    area TEXT,
                    budget TEXT,
                    notes TEXT,
                    created_at TEXT
                )
            """)

    def save_customer(self, instance):
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()
        area = self.area_input.text.strip()
        budget = self.budget_input.text.strip()
        notes = self.notes_input.text.strip()

        if not name:
            self.status.text = (
                "من فضلك اكتب اسم العميل"
            )
            return

        with sqlite3.connect(
            self.db_path
        ) as connection:

            connection.execute("""
                INSERT INTO customers
                (name, phone, area, budget, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                phone,
                area,
                budget,
                notes,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
            ))

        self.name_input.text = ""
        self.phone_input.text = ""
        self.area_input.text = ""
        self.budget_input.text = ""
        self.notes_input.text = ""

        self.status.text = (
            "تم حفظ بيانات العميل بنجاح"
        )

    def show_customers(self, instance):
        with sqlite3.connect(
            self.db_path
        ) as connection:

            customers = connection.execute("""
                SELECT id, name, phone, area, budget
                FROM customers
                ORDER BY id DESC
            """).fetchall()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(10)
        )

        scroll = ScrollView()

        customer_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )
        customer_list.bind(
            minimum_height=customer_list.setter(
                "height"
            )
        )

        if not customers:
            customer_list.add_widget(
                Label(
                    text="لا يوجد عملاء محفوظون",
                    size_hint_y=None,
                    height=dp(50)
                )
            )

        for customer in customers:
            customer_id, name, phone, area, budget = customer

            text = (
                f"رقم العميل: {customer_id}\n"
                f"الاسم: {name}\n"
                f"الهاتف: {phone or '-'}\n"
                f"المنطقة: {area or '-'}\n"
                f"الميزانية: {budget or '-'}"
            )

            customer_list.add_widget(
                Label(
                    text=text,
                    size_hint_y=None,
                    height=dp(115),
                    halign="right",
                    valign="middle",
                    text_size=(None, None)
                )
            )

        scroll.add_widget(customer_list)
        content.add_widget(scroll)

        close_button = Button(
            text="إغلاق",
            size_hint_y=None,
            height=dp(45)
        )

        popup = Popup(
            title="العملاء المسجلون",
            content=content,
            size_hint=(0.95, 0.85)
        )

        close_button.bind(
            on_press=popup.dismiss
        )
        content.add_widget(close_button)

        popup.open()


if __name__ == "__main__":
    AqarAS().run()
