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



def setStyle(style):
	# GLOBAL
	global COLOR_BACKGROUND
	global COLOR_SELECTION
	global COLOR_HOVER
	global COLOR_TEXT
	global COLOR_BORDER
	global COLOR_LIST
	global STYLE


	# Shared
	COLOR_HOVER = "#4d805e"
	COLOR_ERROR_EMPTYLIST = "#cc4747"


	# Light Style
	if style == "light":
		COLOR_BACKGROUND = "#f0f0f0"
		COLOR_SELECTION = "#1a803c"
		COLOR_TEXT = "black"
		COLOR_BORDER = "#828790"
		COLOR_LIST = "#FFF"

	# Dark Style
	if style == "dark":
		COLOR_BACKGROUND = "#444444"
		COLOR_SELECTION = "#4d805e"
		COLOR_TEXT = "#c8c8c8"
		COLOR_BORDER = "#272727"
		COLOR_LIST = "#333333"


	# Set Template
	STYLE = template % {
		"COLOR_BACKGROUND": COLOR_BACKGROUND,
		"COLOR_TEXT": COLOR_TEXT,
		"COLOR_HOVER": COLOR_HOVER,
		"COLOR_SELECTION": COLOR_SELECTION,
		"COLOR_BORDER": COLOR_BORDER,
		"COLOR_LIST": COLOR_LIST
		}