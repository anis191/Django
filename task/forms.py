from django import forms
from task.models import *

# Create a new task using form(Form)
'''class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : 2,
        'cols' : 15
    }))
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assign_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=[])

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees',[])
        super().__init__(*args, **kwargs)
        self.fields["assign_to"].choices=[(emp.id, emp.name) for emp in employees]
'''
# For widget using form Mixin:
class StyleFormMixin:
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
    # Call the mixin class function:
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style()
        









# It's just my a practice form
class TestForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class" : "name",
        "placeholder" : "Enter Your Name"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class" : "user-email",
        "placeholder" : "Enter Your Email"
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "rows" : 5,
        "cols" : 5
    }))
    country = forms.CharField(widget=forms.Select(choices=[('1', 'Option 1'), ('2', 'Option 2')]))
    date = forms.DateField(widget=forms.DateInput(attrs={
        "type" : "date"
    }))
    date = forms.DateField(widget=forms.SelectDateWidget)
    
