from django import forms
from .models import Store, Category

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
