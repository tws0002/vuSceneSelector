import os
splitterIMG = os.path.dirname(__file__) + "/graphics/UiElements/"

# SETTINGS
from core import Settings
SETTINGS = Settings.SETTINGS
COLOR_HOVER				= SETTINGS["COLOR_HOVER"]
COLOR_ERROR_EMPTYLIST	= SETTINGS["COLOR_ERROR_EMPTYLIST"]

COLOR_BACKGROUND		= SETTINGS["COLOR_BACKGROUND"]
COLOR_SELECTION			= SETTINGS["COLOR_SELECTION"]
COLOR_TEXT				= SETTINGS["COLOR_TEXT"]
COLOR_TEXT_GREY 		= SETTINGS["COLOR_TEXT_GREY"]
COLOR_BORDER			= SETTINGS["COLOR_BORDER"]
COLOR_LIST				= SETTINGS["COLOR_LIST"]


fontGrey = """
QWidget
{
	color: %(COLOR_HOVER)s;

}
"""

styleTextGrey = """
QWidget
{
	color: %(COLOR_TEXT_GREY)s;
}
""" % {"COLOR_TEXT_GREY" : COLOR_TEXT_GREY}







template = """
QWidget
{
	color: %(COLOR_TEXT)s;
	background-color: %(COLOR_BACKGROUND)s;
}

QLabel1
{
	border: 1px solid green;
}


QMenu
{
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;
}


QMenu::item:selected
{
	background-color: %(COLOR_HOVER)s;
}


QTabWidget::pane {
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;
}


QTabBar::tab {
	padding: 3px;
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;
	padding: 2px;

	border-bottom-style: 0px;
}

QTabBar::tab:selected{
	color: black;
	background: %(COLOR_HOVER)s;
}

QTabBar::tab:hover {
	background: %(COLOR_HOVER)s;
}

QPushButton
{
	background: %(COLOR_LIST)s;
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
	margin-top: 5px;
	padding-top: 5px;
}

QGroupBox::title {
	subcontrol-origin: margin;
	subcontrol-position: top left;
	margin-top: -1px;
	left: 10px;
}

QTextEdit
{
	background: #4d483d;
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;
}
"""


#############################
#
#	QScrollBars
#
#

template += """

QScrollBar:vertical{	width: 10px;	}
QScrollBar:horizontal{	height: 10px;	}

QScrollBar::handle:vertical
{
	background: %(COLOR_BACKGROUND)s;
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;

	border-right-width: 0px;
	margin-top: -1px;
	margin-bottom: -1px;
}

QScrollBar::handle:horizontal
{
	background: %(COLOR_BACKGROUND)s;
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;

	border-bottom-width: 0px;
	margin-left: -1px;
	margin-right: -1px;
}


QScrollBar::add-page, QScrollBar::sub-page
{
	background: %(COLOR_LIST)s;
}


QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{}
QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal{}
"""


#                            #
#                            #
##############################
#                            #
#      Lists and Tables      #
#                            #
##############################
#                            #
#                            #

template += """
QListWidget, QTableWidget
{
	background: %(COLOR_LIST)s;
	border: 1px solid %(COLOR_BORDER)s;
}


QListWidget:item:selected:active, QTableWidget:item:selected:active,
QListWidget:item:selected:!disabled, QTableWidget:item:selected:!disabled
{
	background: %(COLOR_SELECTION)s;
}



QListWidget:item:hover, QTableWidget:item:hover
{
	color: white;
	background: %(COLOR_HOVER)s;
}

QHeaderView::section
{
	color: %(COLOR_TEXT)s;
	background: %(COLOR_BACKGROUND)s;
	border: 0px solid black;
}


TableAssetsIcon
{
	background-color: %(COLOR_LIST)s;
}
"""


# Set Template
STYLE = template % {
	"COLOR_BACKGROUND": COLOR_BACKGROUND,
	"COLOR_TEXT": COLOR_TEXT,
	"COLOR_HOVER": COLOR_HOVER,
	"COLOR_SELECTION": COLOR_SELECTION,
	"COLOR_BORDER": COLOR_BORDER,
	"COLOR_LIST": COLOR_LIST
	}






#                            #
#                            #
##############################
#                            #
#      Splitter Handle       #
#                            #
##############################
#                            #
#                            #

styleHandleNormal = """
QSplitter::handle:horizontal
{
	width:  6px;
	image: url(""" + splitterIMG  + "splitter_Normal_h.png" + """)
}

QSplitter::handle:vertical
{
	height:  6px;
	image: url(""" + splitterIMG  + "splitter_Normal_v.png" + """)
}
"""

styleHandleHover = """
QSplitter::handle:horizontal
{
	width:  6px;
	image: url(""" + splitterIMG  + "splitter_Hover_h.png" + """);
}

QSplitter::handle:vertical
{
	height:  6px;
	image: url(""" + splitterIMG  + "splitter_Hover_v.png" + """)
}
"""






