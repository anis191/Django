from django import forms
from task.models import *

# For widget using form Mixin:
class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style()
    
    common_class = "border-2 rounded-lg border-gray-300 px-3" 
    def apply_style(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : f"{self.common_class} w-full focus:bg-red-50",
                    'placeholder' : f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : f"{self.common_class} w-full focus:bg-red-50",
                    'placeholder' : f"Enter {field.label.lower()}",
                    'rows' : 4
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : self.common_class
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : self.common_class
                })
            else:
                field.widget.attrs.update({
                    'class' : self.common_class
                })

# Create a new task using this form(ModelForm):
class TaskModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assign_to']
        widgets = {
            'due_date' : forms.SelectDateWidget,
            'assign_to' : forms.CheckboxSelectMultiple
        }

class TaskDetailModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes']
