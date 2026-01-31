"""
Formularios de la aplicación webAMG.
"""
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """
    Formulario de login personalizado.
    Hereda de Django's AuthenticationForm para usar la validación integrada.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar widgets y labels si es necesario
        self.fields['username'].widget.attrs.update({
            'class': 'input-custom w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#8a4534]/20 transition-all',
            'placeholder': 'Ingrese su usuario',
            'autofocus': True,
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'input-custom w-full pl-12 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#8a4534]/20 transition-all',
            'placeholder': 'Ingrese su contraseña',
        })
