from django import forms


class BootstrapFormMixin:
    """Le pone a cada campo las clases de Bootstrap, para que el formulario se vea bien."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, forms.CheckboxInput):
                clase = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                clase = "form-select"
            else:
                clase = "form-control"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {clase}".strip()

    def full_clean(self):
        super().full_clean()
        # los campos con error se marcan en rojo
        for nombre in (self._errors or {}):
            if nombre in self.fields:
                widget = self.fields[nombre].widget
                widget.attrs["class"] = f"{widget.attrs.get('class', '')} is-invalid".strip()

