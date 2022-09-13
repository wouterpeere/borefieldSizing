# Graphical Using Interface (GUI)

```{commandline}
python -m PyInstaller --noconfirm --onefile --windowed --splash "./GHEtool/gui/icons/Icon.ico" --name "GHEtool1" --icon "./GHEtool/gui/icons/Icon.ico" "./GHEtool/gui/start_gui.py"
```

```{commandline}
python -m PyInstaller --noconfirm --onefile --console --splash "./GHEtool/gui/icons/Icon.ico" --name "GHEtool1" --icon "./GHEtool/gui/icons/Icon.ico" "./GHEtool/gui/start_gui.py"
```



### Page

add 'example_icon.svg' icon to 'icons.qrc' file which has to be located in the icons folder:

```xml
<file>icons/example_icon.svg</file>
```

Afterwards the 'icons_rc.py' has to be recompiled using the following command line:

```{commandline}
pyside6-rcc ./GHEtool/gui/icons.qrc -o ./GHEtool/gui/icons_rc.py
```



```python
from GHEtool.gui.gui_classes import Page
page_example = Page(
    default_parent=default_parent, 
    icon=":/icons/icons/example_icon.svg",
    name='Example category',
    button_name='Name of the Button',
)
```

### Category

```python
from GHEtool.gui.gui_classes import Category
category_example = Category(
    default_parent=default_parent, 
    label='Example category', 
    page=page_example,
)
```


### Float box

```python
from GHEtool.gui.gui_classes import FloatBox
option_float = FloatBox(
    default_parent=default_parent, 
    label='Float label text', 
    default_value=0.5, 
    minimal_value=0, 
    maximal_value=1,
    step=0.1,
    decimal_number=2,
    category=category_example,
)
```

### Integer box

```python
from GHEtool.gui.gui_classes import IntBox
option_int = IntBox(
    default_parent=default_parent, 
    label='Int label text', 
    default_value=2, 
    minimal_value=0, 
    maximal_value=12,
    step=2,
    category=category_example,
)
```

### Button box

```python
from GHEtool.gui.gui_classes import ButtonBox
option_buttons = ButtonBox(
    default_parent=default_parent, 
    label='Button box label text', 
    default_index=0,
    entries=['option 1', 'option 2'],
    category=category_example,
)
```

### Button box

```python
from GHEtool.gui.gui_classes import ListBox
option_list = ListBox(
    default_parent=default_parent, 
    label='List box label text', 
    default_index=0,
    entries=['option 1', 'option 2'],
    category=category_example,
)
```