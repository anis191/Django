from django import forms
from task.models import *

# Create a new task using this form
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

# Create a new task using this form(ModelForm):
class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assign_to']
        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : "border-2 rounded-lg border-gray-300 px-3 w-full focus:bg-red-50",
                "placeholder" : "Write the task title",
            }),
            'description' : forms.Textarea(attrs={
                'class' : "border-2 rounded-lg border-gray-300 px-3 w-full",
                "placeholder" : "Write the description",
                'rows': 4
            }),
            'due_date' : forms.SelectDateWidget(attrs={
                'class' : "border-2 rounded-lg border-gray-300 px-3",
                "placeholder" : "Write the description",
                'rows': 4
            }),
            'assign_to' : forms.CheckboxSelectMultiple(attrs={
                'class' : "border-2 rounded-lg border-gray-300 px-3",
                "placeholder" : "Write the description",
                'rows': 4
            })
        }









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
    
