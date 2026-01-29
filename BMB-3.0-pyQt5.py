import sys
import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QLineEdit, QPushButton, QToolBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# PATHS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_FILE = os.path.join(SCRIPT_DIR, "home-page.html")
# Dacă nu găsește fișierul, pune Google ca să nu dea eroare la pornire
HOME_URL = QUrl.fromLocalFile(HOME_FILE) if os.path.exists(HOME_FILE) else QUrl("https://www.google.com")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMB 3.0")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.setup_toolbar()
        self.add_new_tab(HOME_URL, "Home")

    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        back_btn = QPushButton("<")
        back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
        self.toolbar.addWidget(back_btn)

        forward_btn = QPushButton(">")
        forward_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())
        self.toolbar.addWidget(forward_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        self.toolbar.addWidget(self.url_bar)

        new_tab_btn = QPushButton("+")
        new_tab_btn.clicked.connect(lambda: self.add_new_tab(HOME_URL, "New Tab"))
        self.toolbar.addWidget(new_tab_btn)

    def add_new_tab(self, url, title):
        browser = QWebEngineView()
        index = self.tabs.addTab(browser, title)
        self.tabs.setCurrentIndex(index)
        browser.setUrl(url)

        # Update titlu și iconiță când se încarcă pagina
        browser.titleChanged.connect(lambda t: self.tabs.setTabText(self.tabs.indexOf(browser), t))
        browser.iconChanged.connect(lambda icon: self.tabs.setTabIcon(self.tabs.indexOf(browser), icon))
        browser.urlChanged.connect(lambda u: self.update_url(u, browser))

    def navigate(self):
        text = self.url_bar.text().strip()
        if not text: return
        if "://" not in text:
            text = "http://" + text if "." in text else "https://www.google.com/search?q=" + text
        self.tabs.currentWidget().setUrl(QUrl(text))

    def update_url(self, qurl, browser):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(qurl.toString())

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            self.tabs.removeTab(index)
            widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())