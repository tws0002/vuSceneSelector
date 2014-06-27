HEADER_IMG = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/SceneSelector/Header_SceneSelector_v005_vu.png"

# GLOBAL
COLOR_SELECTION = "#1a803c"
COLOR_HOVER = "#4d805e"
COLOR_ERROR_EMPTYLIST = "#cc4747"


template = """
QWidget
{
    color: %(COLOR_TEXT)s;
    background-color: %(COLOR_BACKGROUND)s;
}

QPushButton
{
	background: %(COLOR_BACKGROUND)s;
	padding: 3px;
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;
}

QPushButton::hover
{
	background: %(COLOR_HOVER)s;
}

QGroupBox
{
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;
}

QListWidget
{
	background: %(COLOR_LIST)s;
	border-color: %(COLOR_BORDER)s;
	border-width: 1px;
	border-style: solid;
}

QListWidget:item:selected:active
{
	background: %(COLOR_SELECTION)s;
}

QListWidget:item:hover
{
	color: white;
	background: %(COLOR_HOVER)s;
}

QListWidget:item:selected:!disabled {
	background: %(COLOR_SELECTION)s;
}"""



def light():
	global COLOR_BACKGROUND;	COLOR_BACKGROUND = "#f0f0f0"
	global COLOR_TEXT;			COLOR_TEXT = "black"
	global COLOR_BORDER;		COLOR_BORDER = "#828790"
	global COLOR_LIST;			COLOR_LIST = "#FFF"
	global STYLE;				STYLE = template % {
			"COLOR_BACKGROUND": COLOR_BACKGROUND,
			"COLOR_TEXT": COLOR_TEXT,
			"COLOR_HOVER": COLOR_HOVER,
			"COLOR_SELECTION": COLOR_SELECTION,
			"COLOR_BORDER": COLOR_BORDER,
			"COLOR_LIST": COLOR_LIST
			}


def dark():
	global COLOR_SELECTION; 	COLOR_SELECTION = "#4d805e"
	global COLOR_HOVER; 		COLOR_HOVER = "#4d805e"

	global COLOR_BACKGROUND; 	COLOR_BACKGROUND = "#444444"
	global COLOR_TEXT;			COLOR_TEXT = "#c8c8c8"
	global COLOR_BORDER;		COLOR_BORDER = "#272727"
	global COLOR_LIST;			COLOR_LIST = "#333333"

	global STYLE; STYLE = template % {
			"COLOR_BACKGROUND": COLOR_BACKGROUND,
			"COLOR_TEXT": COLOR_TEXT,
			"COLOR_HOVER": COLOR_HOVER,
			"COLOR_SELECTION": COLOR_SELECTION,
			"COLOR_BORDER": COLOR_BORDER,
			"COLOR_LIST": COLOR_LIST
			}