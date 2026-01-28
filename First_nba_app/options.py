from dash import dcc, html


def title(text, level=3):
    """Titre centré"""
    return getattr(html, f"H{level}")(children=text, style={'textAlign': 'center'})

def markdown(text):
    """Markdown centré à gauche"""
    return dcc.Markdown(children=text, style={'textAlign': 'left'})

def dropdown(id_name, options_list, default=None, multi=False, style_align='left'):
    """Dropdown générique"""
    return dcc.Dropdown(
        id=id_name,
        options=[{'label': label, 'value': value} for label, value in options_list],
        value=default,
        multi=multi,
        style={'textAlign': style_align}
    )

def radio_items(id_name, options_list, default=None, style_align='left'):
    """RadioItems générique"""
    return dcc.RadioItems(
        id=id_name,
        options=[{'label': label, 'value': value} for label, value in options_list],
        value=default,
        style={'textAlign': style_align}
    )

def slider(id_name, min_val, max_val, step, default):
    """Slider avec marks automatiques"""
    marks = {i: str(i) for i in range(min_val, max_val + 1, step)}
    return dcc.Slider(id=id_name, min=min_val, max=max_val, step=step, value=default, marks=marks)

def range_slider(id_name, min_val, max_val, default):
    """RangeSlider avec marks automatiques"""
    marks = {i: str(i) for i in range(min_val, max_val + 1)}
    return dcc.RangeSlider(id=id_name, min=min_val, max=max_val, value=default, marks=marks, step=1, count=1)
