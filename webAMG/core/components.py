"""
Componentes de ReactPy para el sistema WebAMG.
"""
from reactpy import component, html, hooks


@component
def simple():
    """Componente muy simple sin hooks para debug"""
    return "HELLO FROM REACTPY"


@component
def hello_world(recipient: str):
    """Componente simple de saludo"""
    return html.div(
        html.h1(f"Hello {recipient}!"),
        html.p("This is from hello_world component")
    )


@component
def counter():
    """Componente contador interactivo"""
    count, set_count = hooks.use_state(0)

    return html.div(
        html.h3(f"Contador: {count}"),
        html.p("Este es un componente de prueba con estado"),
        html.button(
            {"on_click": lambda event: set_count(count + 1)},
            "Incrementar",
        ),
    )


@component
def test_component():
    """Componente de prueba para verificar que ReactPy funciona"""
    return html.div(
        html.p("¡ReactPy está funcionando correctamente!")
    )


# =====================================================
# COMPONENTES DEL DASHBOARD
# =====================================================

@component
def dashboard_stat_card(title: str, value: str, icon: str, color: str, trend: str = None):
    """
    Componente de tarjeta de estadística para el dashboard.
    
    Args:
        title: Título de la estadística
        value: Valor a mostrar
        icon: SVG del icono
        color: Color corporativo (primary, secondary, accent)
        trend: Texto de tendencia (opcional)
    """
    color_map = {
        'primary': '#8a4534',
        'secondary': '#07680b',
        'accent': '#334e76',
    }
    bg_color = color_map.get(color, '#07680b')
    
    return html.div(
        {
            "class_name": "bg-white rounded-xl p-6 shadow-sm border border-gray-100 card-hover"
        },
        html.div(
            {"class_name": "flex items-center justify-between"},
            html.div(
                html.p({"class_name": "text-sm font-medium text-gray-500"}, title),
                html.p({"class_name": "text-2xl font-bold text-gray-900 mt-1"}, value),
            ),
            html.div(
                {
                    "class_name": "w-12 h-12 rounded-lg flex items-center justify-center",
                    "style": {"background_color": f"{bg_color}20"}
                },
                html.div({"dangerously_set_inner_html": icon}),
            ),
        ),
        html.p(
            {
                "class_name": "text-xs mt-3 flex items-center",
                "style": {"color": bg_color}
            },
            trend if trend else ""
        )
    )


@component
def project_row(project_name: str, location: str, status: str, progress: int, date: str):
    """
    Componente de fila de proyecto para la tabla.
    
    Args:
        project_name: Nombre del proyecto
        location: Ubicación del proyecto
        status: Estado del proyecto
        progress: Porcentaje de progreso
        date: Fecha del proyecto
    """
    status_colors = {
        'En Progreso': 'bg-amber-100 text-amber-700',
        'Planificado': 'bg-yellow-100 text-yellow-700',
        'Completado': 'bg-blue-100 text-blue-700',
        'Pausado': 'bg-orange-100 text-orange-700',
        'Cancelado': 'bg-red-100 text-red-700',
    }
    
    status_class = status_colors.get(status, 'bg-gray-100 text-gray-700')
    
    return html.tr(
        {"class_name": "border-b border-gray-50 hover:bg-gray-50"},
        html.td(
            {"class_name": "py-4 px-4"},
            html.p({"class_name": "font-medium text-gray-900"}, project_name),
            html.p({"class_name": "text-sm text-gray-500"}, location),
        ),
        html.td(
            {"class_name": "py-4 px-4"},
            html.span(
                {
                    "class_name": f"status-badge {status_class}",
                },
                status
            )
        ),
        html.td(
            {"class_name": "py-4 px-4"},
            html.div(
                {"class_name": "w-full bg-gray-200 rounded-full h-2"},
                html.div(
                    {
                        "class_name": "h-2 rounded-full",
                        "style": {
                            "width": f"{progress}%",
                            "background_color": "#8a4534"
                        }
                    }
                )
            ),
            html.p({"class_name": "text-xs text-gray-500 mt-1"}, f"{progress}%"),
        ),
        html.td(
            {"class_name": "py-4 px-4 text-sm text-gray-500"},
            date
        )
    )


@component
def user_avatar(name: str, size: str = "md"):
    """
    Componente de avatar de usuario con iniciales.
    
    Args:
        name: Nombre completo del usuario
        size: Tamaño del avatar (sm, md, lg)
    """
    size_classes = {
        'sm': 'w-8 h-8 text-sm',
        'md': 'w-10 h-10 text-base',
        'lg': 'w-12 h-12 text-lg',
    }
    
    size_class = size_classes.get(size, 'w-10 h-10')
    
    def get_initials(n):
        parts = n.split(' ')
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return n[:2].upper()
    
    initials = get_initials(name)
    
    return html.div(
        {
            "class_name": f"{size_class} rounded-full flex items-center justify-center text-white font-semibold",
            "style": {
                "background": "linear-gradient(135deg, #8a4534, #334e76)"
            }
        },
        initials
    )


@component
def sidebar_item(label: str, icon: str, href: str, active: bool = False):
    """
    Componente de item del sidebar.
    
    Args:
        label: Texto del item
        icon: SVG del icono
        href: URL de navegación
        active: Si está activo
    """
    active_class = "sidebar-item-active" if active else "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
    
    return html.a(
        {
            "href": href,
            "class_name": f"sidebar-item flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors {active_class}"
        },
        html.div({"dangerously_set_inner_html": icon}),
        html.span(label)
    )


@component
def notification_badge(count: int):
    """
    Componente de badge de notificaciones.
    
    Args:
        count: Número de notificaciones
    """
    return html.button(
        {
            "class_name": "p-2 text-gray-400 hover:text-gray-600 transition-colors relative"
        },
        html.div(
            {"dangerously_set_inner_html": """
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                </svg>
            """}
        ),
        html.span(
            {
                "class_name": "absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center",
                "style": {"display": "block" if count > 0 else "none"}
            },
            str(count) if count > 9 else f"+{count}"
        )
    )


@component
def loading_spinner():
    """Componente de spinner de carga."""
    return html.div(
        {
            "class_name": "flex items-center justify-center",
            "style": {"padding": "2rem"}
        },
        html.div(
            {
                "class_name": "animate-spin rounded-full h-12 w-12 border-4 border-gray-200 border-t-[#07680b]"
            }
        )
    )


@component
def empty_state(message: str, icon: str = None):
    """
    Componente de estado vacío.
    
    Args:
        message: Mensaje a mostrar
        icon: SVG del icono (opcional)
    """
    default_icon = """
        <svg class="w-16 h-16 text-gray-300 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
    """
    
    return html.div(
        {"class_name": "text-center py-12"},
        html.div(
            {"dangerously_set_inner_html": icon if icon else default_icon}
        ),
        html.p({"class_name": "text-gray-500 mt-4"}, message)
    )


@component
def confirm_dialog(title: str, message: str, on_confirm, on_cancel):
    """
    Componente de diálogo de confirmación.
    
    Args:
        title: Título del diálogo
        message: Mensaje de confirmación
        on_confirm: Función al confirmar
        on_cancel: Función al cancelar
    """
    show, set_show = hooks.use_state(True)
    
    def handle_confirm(event):
        set_show(False)
        on_confirm()
    
    def handle_cancel(event):
        set_show(False)
        on_cancel()
    
    if not show:
        return html.div()
    
    return html.div(
        {
            "class_name": "fixed inset-0 flex items-center justify-center z-50",
            "style": {"background_color": "rgba(0, 0, 0, 0.5)"}
        },
        html.div(
            {
                "class_name": "bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-xl"
            },
            html.h3({"class_name": "text-lg font-semibold text-gray-900 mb-2"}, title),
            html.p({"class_name": "text-gray-600 mb-6"}, message),
            html.div(
                {"class_name": "flex space-x-3 justify-end"},
                html.button(
                    {
                        "class_name": "px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors",
                        "on_click": handle_cancel
                    },
                    "Cancelar"
                ),
                html.button(
                    {
                        "class_name": "px-4 py-2 bg-[#07680b] hover:bg-[#0a8a0f] text-white rounded-lg transition-colors",
                        "on_click": handle_confirm
                    },
                    "Confirmar"
                )
            )
        )
    )
