from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django.forms import ModelForm

from .models import Note


class Note_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "blueForms"
        self.helper.form_method = "POST"
        self.helper.form_action = ""
        # self.helper.add_input(Submit('submit', 'Save'))
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                "",
                FloatingField("title"),
                FloatingField("content", style="height: 100px"),
            ),
            Submit("submit", "Save", css_class="btn btn-light btn-outline-secondary"),
        )

    class Meta:
        model = Note
        fields = "__all__"
        exclude = ["user"]
