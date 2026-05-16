from qfluentwidgets import isDarkTheme


def group_box_style():
    if isDarkTheme():
        return """
            QGroupBox {
                font-size: 16px; font-weight: 600;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                margin-top: 16px;
                padding: 20px;
                padding-top: 36px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px;
            }
        """
    else:
        return """
            QGroupBox {
                font-size: 16px; font-weight: 600;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 12px;
                margin-top: 16px;
                padding: 20px;
                padding-top: 36px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px;
            }
        """


def secondary_text_color():
    return "#9E9E9E" if isDarkTheme() else "#616161"


def card_bg_color():
    return "#2D2D2D" if isDarkTheme() else "#FFFFFF"


def border_color():
    return "rgba(255,255,255,0.08)" if isDarkTheme() else "rgba(0,0,0,0.1)"


def surface_bg_style(object_name):
    if isDarkTheme():
        return f"""
            #{object_name} {{
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
            }}
        """
    else:
        return f"""
            #{object_name} {{
                background: rgba(0,0,0,0.03);
                border: 1px solid rgba(0,0,0,0.08);
                border-radius: 12px;
            }}
        """
