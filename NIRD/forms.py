from django import forms
from .models import ChatMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tapez votre message...',
            })
        }
