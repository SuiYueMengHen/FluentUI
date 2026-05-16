from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, BodyLabel, isDarkTheme)
from app.theme_aware_page import ThemeAwarePage
from app.components.flowchart_node import FlowchartNode
from app.components.flowchart_connector import FlowchartConnector
from app.components.mind_map_node import MindMapNode
from app.components.mind_map_branch import MindMapBranch
from app.components.org_chart_node import OrgChartNode
from app.components.timeline_item import TimelineItem
from app.components.kanban_card import KanbanCard
from app.components.swim_lane import SwimLane


class DiagramsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("diagramsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Diagrams", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Flowcharts, mind maps, org charts, timelines, and kanban boards.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_flowchart(main_layout)
        self._build_mind_map(main_layout)
        self._build_org_chart(main_layout)
        self._build_timeline(main_layout)
        self._build_kanban(main_layout)
        self._build_swim_lane(main_layout)

        main_layout.addStretch()

    def _build_flowchart(self, parent):
        group = QGroupBox("Flowchart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Flowchart nodes with four types (start, process, decision, end) and directional connectors.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(12)

        start = FlowchartNode(title="Start", node_type="start")
        process = FlowchartNode(title="Process", subtitle="Do work", node_type="process")
        decision = FlowchartNode(title="Decision?", node_type="decision")
        end = FlowchartNode(title="End", node_type="end")

        row.addWidget(start)
        connector1 = FlowchartConnector(direction="right")
        row.addWidget(connector1)
        row.addWidget(process)
        connector2 = FlowchartConnector(direction="right")
        row.addWidget(connector2)
        row.addWidget(decision)
        connector3 = FlowchartConnector(direction="right")
        row.addWidget(connector3)
        row.addWidget(end)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_mind_map(self, parent):
        group = QGroupBox("Mind Map")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Mind map nodes with hierarchical levels and branch connectors for visual thinking.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(8)

        center_node = MindMapNode(title="Central Idea", level=0)
        row.addWidget(center_node)

        branch1 = MindMapBranch(direction="right")
        row.addWidget(branch1)

        col1 = QVBoxLayout()
        col1.setSpacing(8)
        node1 = MindMapNode(title="Branch A", level=1)
        node2 = MindMapNode(title="Branch B", level=1)
        col1.addWidget(node1)
        col1.addWidget(node2)
        row.addLayout(col1)

        branch2 = MindMapBranch(direction="right")
        row.addWidget(branch2)

        col2 = QVBoxLayout()
        col2.setSpacing(8)
        node3 = MindMapNode(title="Branch C", level=2)
        node4 = MindMapNode(title="Branch D", level=2)
        col2.addWidget(node3)
        col2.addWidget(node4)
        row.addLayout(col2)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_org_chart(self, parent):
        group = QGroupBox("Org Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Organizational chart nodes showing hierarchy with name and role information.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        ceo = OrgChartNode(name="Alice Chen", role="CEO")
        cto = OrgChartNode(name="Bob Lee", role="CTO")
        cfo = OrgChartNode(name="Carol Wu", role="CFO")

        row.addWidget(ceo)
        row.addWidget(cto)
        row.addWidget(cfo)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_timeline(self, parent):
        group = QGroupBox("Timeline")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Vertical timeline items with title, description, timestamp, and color-coded markers.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        item1 = TimelineItem(
            title="Project Kickoff",
            description="Initial planning and team alignment meeting.",
            timestamp="Jan 15, 2025",
            color="#0078D4",
        )
        item2 = TimelineItem(
            title="Development Phase",
            description="Core feature implementation and testing.",
            timestamp="Mar 01, 2025",
            color="#6CCB5F",
        )
        item3 = TimelineItem(
            title="Release",
            description="Product launch and deployment.",
            timestamp="Jun 20, 2025",
            color="#FFB900",
        )

        layout.addWidget(item1)
        layout.addWidget(item2)
        layout.addWidget(item3)
        parent.addWidget(group)

    def _build_kanban(self, parent):
        group = QGroupBox("Kanban")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Kanban cards with priority indicators, tags, and hover effects for task management.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        card1 = KanbanCard(
            title="Fix Login Bug",
            description="Users cannot login on mobile devices.",
            priority="high",
            tags=["bug", "mobile"],
        )
        card2 = KanbanCard(
            title="Add Dark Mode",
            description="Implement theme switching support.",
            priority="medium",
            tags=["feature", "ui"],
        )
        card3 = KanbanCard(
            title="Update Docs",
            description="Refresh API documentation for v2.",
            priority="low",
            tags=["docs"],
        )

        row.addWidget(card1)
        row.addWidget(card2)
        row.addWidget(card3)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_swim_lane(self, parent):
        group = QGroupBox("Swim Lane")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Swim lane diagram for process flow across departments or teams.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        lane = SwimLane(title="Engineering", color="#0078D4")
        layout.addWidget(lane)

        parent.addWidget(group)
