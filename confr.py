import flet as ft
import time
from datetime import datetime, timedelta
import os

class LmazaConferenceApp:
    def __init__(self):
        self.current_verse = ""
        self.verses = [
            "فَإِنَّ كَلِمَةَ الصَّلِيبِ عِنْدَ الْهَالِكِينَ جَهَالَةٌ، وَأَمَّا عِنْدَنَا نَحْنُ الْمُخَلَّصِينَ فَهِيَ قُوَّةُ اللهِ",
            "لأَنَّهُ مَكْتُوبٌ: «سَأُبِيدُ حِكْمَةَ الْحُكَمَاءِ، وَأَرْفُضُ فَهْمَ الْفُهَمَاءِ»",
            # أضف المزيد من الآيات هنا
        ]
        self.schedule = [
            {"date": "23-9-2024", "events": [
                {"time": "12:00 ص", "title": "التحرك من المنيا"},
                {"time": "6:00 ص - 9:00 ص", "title": "وصول الأديرة وصلاة القداس"},
                {"time": "11:30 ص - 1:00 م", "title": "محاضرة الأنبا بافلي"},
                {"time": "3:30 م", "title": "التجمع للتحرك إلى الإسكندرية"},
            ]},
            {"date": "24-9-2024", "events": [
                {"time": "10:00 ص - 1:00 م", "title": "مفاجأة سيدنا الأنبا فام"},
                {"time": "2:00 م - 3:30 م", "title": "محاضرة الأنبا رافائيل"},
                {"time": "6:00 م - 8:00 م", "title": "محاضرة الأنبا متاؤس"},
            ]},
            {"date": "25-9-2024", "events": [
                {"time": "طوال اليوم", "title": "زيارة الأديرة في وادي النطرون"},
            ]},
        ]

    def main(self, page: ft.Page):
        page.title = "مؤتمر لماذا"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.rtl = True  # تفعيل الاتجاه من اليمين إلى اليسار للغة العربية
        
        # تحميل الخط العربي
        page.fonts = {
            "Amiri": "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
        }
        page.theme = ft.Theme(font_family="Amiri")

        def change_tab(e):
            index = e.control.selected_index
            t.current = tabs[index]
            page.update()

        tab_bar = ft.Tabs(
            selected_index=0,
            on_change=change_tab,
            tabs=[
                ft.Tab(text="جدول المؤتمر"),
                ft.Tab(text="حياة بولس الرسول"),
                ft.Tab(text="الترانيم"),
            ],
        )

        schedule_view = ft.ListView(spacing=10, padding=20)
        for day in self.schedule:
            schedule_view.controls.append(ft.Text(day["date"], size=20, weight=ft.FontWeight.BOLD))
            for event in day["events"]:
                schedule_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.EVENT),
                        title=ft.Text(event["title"]),
                        subtitle=ft.Text(event["time"]),
                    )
                )

        paul_life_view = ft.Container(
            content=ft.Text("حياة بولس الرسول - قيد الإنشاء", size=20),
            alignment=ft.alignment.center
        )

        hymns_view = ft.Container(
            content=ft.Text("الترانيم - قيد الإنشاء", size=20),
            alignment=ft.alignment.center
        )

        tabs = [
            schedule_view,
            paul_life_view,
            hymns_view
        ]

        t = ft.Tabs(tabs=tabs, expand=1)

        def show_verse_dialog(e):
            page.dialog = ft.AlertDialog(
                title=ft.Text("آية اليوم"),
                content=ft.Text(self.current_verse),
            )
            page.dialog.open = True
            page.update()

        verse_button = ft.FloatingActionButton(
            icon=ft.icons.FORMAT_QUOTE,
            on_click=show_verse_dialog
        )

        page.add(tab_bar, t, verse_button)

        def update_verse():
            while True:
                current_hour = datetime.now().hour
                self.current_verse = self.verses[current_hour % len(self.verses)]
                time.sleep(3600)  # انتظر ساعة واحدة

        def check_lecture_reminders():
            lectures = [
                (datetime(2024, 9, 23, 11, 15), "محاضرة الأنبا بافلي"),
                (datetime(2024, 9, 24, 9, 45), "مفاجأة سيدنا الأنبا فام"),
                (datetime(2024, 9, 24, 13, 45), "محاضرة الأنبا رافائيل"),
                (datetime(2024, 9, 24, 17, 45), "محاضرة الأنبا متاؤس"),
            ]

            while True:
                now = datetime.now()
                for lecture_time, lecture_name in lectures:
                    if now == lecture_time:
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"تذكير: {lecture_name} ستبدأ بعد 15 دقيقة"))
                        page.snack_bar.open = True
                        page.update()
                    elif now == lecture_time + timedelta(minutes=10):
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"تذكير: {lecture_name} ستبدأ بعد 5 دقائق"))
                        page.snack_bar.open = True
                        page.update()
                time.sleep(60)  # تحقق كل دقيقة

        page.window_width = 400
        page.window_height = 800
        page.update()

        import threading
        threading.Thread(target=update_verse, daemon=True).start()
        threading.Thread(target=check_lecture_reminders, daemon=True).start()

if __name__ == "__main__":
    app = LmazaConferenceApp()
    ft.app(target=app.main)