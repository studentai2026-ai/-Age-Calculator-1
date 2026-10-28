# -Age-Calculator-1
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from datetime import datetime
import threading
import time

# ألوان مريحة للعين (Dark Theme)
Window.clearcolor = get_color_from_hex('#1E1E2E')

class AgeCalculatorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.title_label = Label(
            text='🎂 حاسبة العمر التفاعلية',
            font_size='26sp',
            color=get_color_from_hex('#CBA6F7'),
            size_hint_y=0.15
        )
        layout.add_widget(self.title_label)
        
        self.input = TextInput(
            hint_text='أدخل سنة ميلادك (مثال: 1995)',
            multiline=False,
            font_size='20sp',
            size_hint_y=0.12,
            background_color=get_color_from_hex('#313244'),
            foreground_color=get_color_from_hex('#CDD6F4'),
            padding=[15, 15]
        )
        layout.add_widget(self.input)
        
        self.btn = Button(
            text='احسب عمري ✨',
            font_size='22sp',
            size_hint_y=0.12,
            background_color=get_color_from_hex('#89B4FA'),
            background_normal=''
        )
        self.btn.bind(on_press=self.animate_button, on_release=self.start_calculation)
        layout.add_widget(self.btn)
        
        self.progress = ProgressBar(max=100, value=0, size_hint_y=0.08)
        layout.add_widget(self.progress)
        
        self.result_label = Label(
            text='أدخل سنتك ثم اضغط الزر...',
            font_size='18sp',
            color=get_color_from_hex('#A6ADC8'),
            size_hint_y=0.53,
            halign='center',
            valign='middle'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        layout.add_widget(self.result_label)
        
        return layout

    def animate_button(self, instance):
        anim = Animation(background_color=get_color_from_hex('#45475A'), duration=0.1)
        anim.start(self.btn)

    def start_calculation(self, instance):
        anim = Animation(background_color=get_color_from_hex('#89B4FA'), duration=0.1)
        anim.start(self.btn)
        
        year_str = self.input.text.strip()
        
        if not year_str.isdigit():
            self.show_error("⚠️ الرجاء إدخال سنة صحيحة (أرقام فقط)")
            return
            
        year = int(year_str)
        current_year = datetime.now().year
        
        if year > current_year or year < 1900:
            self.show_error("⚠️ الرجاء إدخال سنة ميلاد واقعية")
            return
            
        self.result_label.text = "⏳ جاري الحساب..."
        self.result_label.color = get_color_from_hex('#F9E2AF')
        self.progress.value = 0
        
        threading.Thread(target=self.calculate_logic, args=(year, current_year), daemon=True).start()

    def calculate_logic(self, year, current_year):
        for i in range(1, 101):
            time.sleep(0.01)
            self.progress.value = i
            
        age_years = current_year - year
        age_days = age_years * 365
        age_hours = age_days * 24
        
        year_100 = year + 100
        progress_percent = min((age_years / 100) * 100, 100)
        
        if age_years < 13:
            msg = "🌟 أنت في مرحلة الطفولة، استمتع بكل لحظة!"
        elif age_years < 20:
            msg = "🚀 مرحلة الشباب والحماس، ابنِ مستقبلك!"
        elif age_years < 40:
            msg = "💪 في عز عطائك، استمر في التطور!"
        elif age_years < 60:
            msg = "🌳 مرحلة الحكمة، خبرتك كنز!"
        else:
            msg = "👑 أنت مصدر إلهام للجميع، استمتع بالحياة!"

        self.progress.value = progress_percent
        self.result_label.text = (
            f"عمرك: {age_years} سنة\n"
            f"(حوالي {age_days:,} يوماً - {age_hours:,} ساعة)\n\n"
            f"🎯 لقد عشت {progress_percent:.1f}% من رحلتك إلى الـ 100!\n"
            f"🎉 ستبلغ 100 عام في سنة: {year_100}\n\n"
            f"{msg}"
        )
        self.result_label.color = get_color_from_hex('#A6E3A1')

    def show_error(self, message):
        self.progress.value = 0
        self.result_label.text = message
        self.result_label.color = get_color_from_hex('#F38BA8')

if __name__ == '__main__':
    AgeCalculatorApp().run()
