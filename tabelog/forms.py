from django import forms
from .models import Store, Category, Reservation, Review

import datetime

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "adress", "opening_hours", "close_hours", "budget", "tel", "image", "category"]
        labels = {
            'name': '店舗名',
            'adress': '住所',
            'opening_hours': '開店時間',
            'close_hours': '閉店時間',
            'budget': '予算',
            'tel': '電話番号',
            'image': '画像',
            'category': 'カテゴリー',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        labels = {
            'name': 'カテゴリ名',
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["date", "time", "people"]
        labels = {
            'date': '予約日',
            'time': '予約時間',
            'people': '予約人数',
        }

    def __init__(self, *args, **kwargs):
        self.store = kwargs.pop('store', None)
        print(f'Store: {self.store}')  # デバッグ用
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data['date']
        dt = datetime.date.today()
        if dt > date:
            raise forms.ValidationError('過去の日付は入力することはできません。')
        return date

    def clean_time(self):
        time = self.cleaned_data['time']
        if self.store:
            open_time = self.store.opening_hours
            close_time = self.store.close_hours
            if not (open_time <= time <= close_time):
                raise forms.ValidationError('営業時間外です。')
        return time


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["star", "content"]
        labels = {
            'star': '評価',
            'content': 'レビュー',
        }