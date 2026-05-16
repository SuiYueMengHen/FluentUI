from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox, QHeaderView)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             TableWidget, TreeWidget, CardWidget,
                             HeaderCardWidget, GroupHeaderCardWidget,
                             AvatarWidget, HyperlinkLabel, FluentIcon as FIF,
                             PushButton, StrongBodyLabel, setTheme, Theme)

from app.theme_aware_page import ThemeAwarePage


class DataWidgetsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dataWidgetsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Data Widgets", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Components for displaying, organizing, and interacting with data.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_table(main_layout)
        self._build_tree(main_layout)
        self._build_cards(main_layout)
        self._build_avatars(main_layout)

        main_layout.addStretch()

    def _build_table(self, parent):
        group = QGroupBox("Table Widget")
        self._track_group(group)
        layout = QVBoxLayout(group)

        table = TableWidget()
        table.setColumnCount(4)
        table.setRowCount(5)
        table.setHorizontalHeaderLabels(["Name", "Role", "Department", "Status"])

        data = [
            ["Alice Chen", "Engineer", "Platform", "Active"],
            ["Bob Wang", "Designer", "UX Team", "Active"],
            ["Carol Li", "Manager", "Product", "On Leave"],
            ["David Zhang", "Engineer", "Backend", "Active"],
            ["Eve Liu", "Analyst", "Data", "Remote"],
        ]

        for row, row_data in enumerate(data):
            for col, text in enumerate(row_data):
                from PySide6.QtWidgets import QTableWidgetItem
                item = QTableWidgetItem(text)
                table.setItem(row, col, item)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setFixedHeight(220)
        table.setBorderVisible(True)
        table.setBorderRadius(8)

        layout.addWidget(table)
        parent.addWidget(group)

    def _build_tree(self, parent):
        group = QGroupBox("Tree Widget")
        self._track_group(group)
        layout = QVBoxLayout(group)

        tree = TreeWidget()
        tree.setHeaderLabels(["Name", "Type"])
        tree.setBorderVisible(True)
        tree.setBorderRadius(8)

        from PySide6.QtWidgets import QTreeWidgetItem

        root1 = QTreeWidgetItem(["src", "Folder"])
        root1.addChild(QTreeWidgetItem(["main.py", "Python"]))
        root1.addChild(QTreeWidgetItem(["app", "Folder"]))
        child = QTreeWidgetItem(["components", "Folder"])
        child.addChild(QTreeWidgetItem(["gradient_card.py", "Python"]))
        child.addChild(QTreeWidgetItem(["stat_card.py", "Python"]))
        root1.addChild(child)

        root2 = QTreeWidgetItem(["resources", "Folder"])
        root2.addChild(QTreeWidgetItem(["icons", "Folder"]))
        root2.addChild(QTreeWidgetItem(["qss", "Folder"]))

        tree.addTopLevelItem(root1)
        tree.addTopLevelItem(root2)
        tree.expandAll()
        tree.setFixedHeight(200)

        layout.addWidget(tree)
        parent.addWidget(group)

    def _build_cards(self, parent):
        group = QGroupBox("Card Widgets")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        card1 = CardWidget()
        card1_layout = QVBoxLayout(card1)
        card1_layout.setContentsMargins(20, 16, 20, 16)
        card1_layout.addWidget(StrongBodyLabel("Card Widget"))
        card1_layout.addWidget(BodyLabel("A basic card container with hover effect and rounded corners."))
        layout.addWidget(card1)

        header_card = HeaderCardWidget()
        header_card.setTitle("Header Card Widget")
        label = BodyLabel("A card with a header bar, suitable for grouped content sections.")
        label.setParent(header_card)
        header_card.layout().addWidget(label)
        layout.addWidget(header_card)

        parent.addWidget(group)

    def _build_avatars(self, parent):
        group = QGroupBox("Avatar & Links")
        self._track_group(group)
        layout = QHBoxLayout(group)
        layout.setSpacing(24)

        avatar = AvatarWidget()
        avatar.setFixedSize(64, 64)
        layout.addWidget(avatar)

        link1 = HyperlinkLabel("https://qfluentwidgets.com")
        link1.setUrl("https://qfluentwidgets.com")
        layout.addWidget(link1)

        link2 = HyperlinkLabel("https://doc.qt.io")
        link2.setUrl("https://doc.qt.io")
        layout.addWidget(link2)

        layout.addStretch()
        parent.addWidget(group)
