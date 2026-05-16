from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, BodyLabel, FluentIcon as FIF, isDarkTheme)
from app.theme_aware_page import ThemeAwarePage
from app.components.bar_chart import BarChart
from app.components.line_chart import LineChart
from app.components.pie_chart import PieChart
from app.components.area_chart import AreaChart
from app.components.radar_chart import RadarChart
from app.components.gauge_chart import GaugeChart
from app.components.scatter_chart import ScatterChart
from app.components.heatmap_chart import HeatmapChart
from app.components.treemap_chart import TreemapChart
from app.components.sparkline_chart import SparklineChart
from app.components.chart_legend import ChartLegend
from app.components.chart_tooltip import ChartTooltip
from app.components.chart_axis import ChartAxis
from app.components.data_label import DataLabel
from app.components.color_scale import ColorScale
from app.components.mini_stat import MiniStat
from app.components.range_slider import RangeSlider
from app.components.time_range_picker import TimeRangePicker
from app.components.chart_filter import ChartFilter
from app.components.data_granularity import DataGranularity
from app.components.chart_export_menu import ChartExportMenu
from app.components.chart_zoom_control import ChartZoomControl


class ChartsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chartsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Charts", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Rich data visualization components with smooth animations and theme support.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_bar_chart(main_layout)
        self._build_line_chart(main_layout)
        self._build_pie_chart(main_layout)
        self._build_area_chart(main_layout)
        self._build_radar_chart(main_layout)
        self._build_gauge_chart(main_layout)
        self._build_scatter_chart(main_layout)
        self._build_heatmap_chart(main_layout)
        self._build_treemap_chart(main_layout)
        self._build_sparkline_chart(main_layout)
        self._build_chart_accessories(main_layout)
        self._build_chart_controls(main_layout)

        main_layout.addStretch()

    def _build_bar_chart(self, parent):
        group = QGroupBox("Bar Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Animated bar chart with customizable data, labels, and colors. Supports smooth entry animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        chart = BarChart(data=[65, 45, 80, 55, 70], labels=["Mon", "Tue", "Wed", "Thu", "Fri"])
        chart.setFixedHeight(200)
        layout.addWidget(chart)

        parent.addWidget(group)

    def _build_line_chart(self, parent):
        group = QGroupBox("Line Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Multi-series line chart with smooth drawing animation. Supports multiple data series overlay.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        chart = LineChart(
            series=[
                {"data": [20, 45, 30, 60, 50, 70], "color": "#0078D4", "name": "Series A"},
                {"data": [10, 35, 55, 40, 65, 45], "color": "#6CCB5F", "name": "Series B"},
            ],
            labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        )
        chart.setFixedHeight(200)
        layout.addWidget(chart)

        parent.addWidget(group)

    def _build_pie_chart(self, parent):
        group = QGroupBox("Pie Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Pie and donut charts with sweep animation. Toggle donut mode for ring-style visualization.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        pie = PieChart(
            data=[35, 25, 20, 20],
            labels=["Product A", "Product B", "Product C", "Product D"],
            colors=["#0078D4", "#6CCB5F", "#FFB900", "#FF6B6B"],
        )
        pie.setFixedSize(220, 220)

        donut = PieChart(
            data=[35, 25, 20, 20],
            labels=["Product A", "Product B", "Product C", "Product D"],
            colors=["#0078D4", "#6CCB5F", "#FFB900", "#FF6B6B"],
            donut=True,
        )
        donut.setFixedSize(220, 220)

        row.addWidget(pie)
        row.addWidget(donut)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_area_chart(self, parent):
        group = QGroupBox("Area Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Area chart with gradient fill and smooth animation. Ideal for showing volume trends over time.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        chart = AreaChart(
            series=[
                {"data": [30, 50, 40, 70, 55, 80], "color": "#0078D4", "name": "Revenue"},
            ],
            labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        )
        chart.setFixedHeight(200)
        layout.addWidget(chart)

        parent.addWidget(group)

    def _build_radar_chart(self, parent):
        group = QGroupBox("Radar Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Radar chart for multi-dimensional comparison with animated scaling from center.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        chart = RadarChart(
            categories=["Speed", "Reliability", "Comfort", "Safety", "Efficiency", "Design"],
            series=[
                {"data": [85, 70, 90, 75, 80, 65], "color": "#0078D4", "name": "Model A"},
            ],
        )
        chart.setFixedSize(260, 260)
        layout.addWidget(chart, alignment=Qt.AlignmentFlag.AlignLeft)

        parent.addWidget(group)

    def _build_gauge_chart(self, parent):
        group = QGroupBox("Gauge Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Gauge chart with arc animation and customizable value range. Perfect for KPI displays.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        gauge = GaugeChart(value=72, label="Performance")
        gauge.setFixedSize(200, 140)
        layout.addWidget(gauge, alignment=Qt.AlignmentFlag.AlignLeft)

        parent.addWidget(group)

    def _build_scatter_chart(self, parent):
        group = QGroupBox("Scatter Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Scatter chart with pop-in animation for data points. Useful for correlation analysis.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        chart = ScatterChart(
            data=[
                (15, 30), (25, 55), (40, 45), (55, 70), (70, 60),
                (35, 25), (50, 50), (65, 80), (20, 40), (80, 65),
            ],
        )
        chart.setFixedHeight(200)
        layout.addWidget(chart)

        parent.addWidget(group)

    def _build_heatmap_chart(self, parent):
        group = QGroupBox("Heatmap Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Heatmap chart with color interpolation for matrix data visualization.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        chart = HeatmapChart(
            data=[
                [10, 30, 50, 70, 90],
                [20, 40, 60, 80, 100],
                [15, 35, 55, 75, 95],
                [25, 45, 65, 85, 50],
                [5, 25, 45, 65, 85],
            ],
            x_labels=["A", "B", "C", "D", "E"],
            y_labels=["Row 1", "Row 2", "Row 3", "Row 4", "Row 5"],
        )
        chart.setFixedHeight(200)
        layout.addWidget(chart)

        parent.addWidget(group)

    def _build_treemap_chart(self, parent):
        group = QGroupBox("Treemap Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Treemap chart with expand animation for hierarchical data proportions.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        chart = TreemapChart(
            data=[
                {"name": "Desktop", "value": 45, "color": "#0078D4"},
                {"name": "Mobile", "value": 30, "color": "#6CCB5F"},
                {"name": "Tablet", "value": 15, "color": "#FFB900"},
                {"name": "Other", "value": 10, "color": "#FF6B6B"},
            ],
        )
        chart.setFixedHeight(200)
        layout.addWidget(chart)

        parent.addWidget(group)

    def _build_sparkline_chart(self, parent):
        group = QGroupBox("Sparkline Chart")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Compact sparkline chart for inline trend visualization with drawing animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        spark1 = SparklineChart(data=[20, 35, 28, 50, 42, 65, 55, 70, 60, 80], color="#0078D4")
        spark2 = SparklineChart(data=[80, 65, 70, 55, 60, 45, 50, 35, 40, 25], color="#FF6B6B")
        spark3 = SparklineChart(data=[30, 40, 35, 50, 45, 55, 60, 58, 65, 70], color="#6CCB5F")

        row.addWidget(spark1)
        row.addWidget(spark2)
        row.addWidget(spark3)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_chart_accessories(self, parent):
        group = QGroupBox("Chart Accessories")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Supporting components for charts: legends, tooltips, axes, labels, color scales, and mini stats.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        legend = ChartLegend(items=[
            {"name": "Revenue", "color": "#0078D4"},
            {"name": "Costs", "color": "#FF6B6B"},
            {"name": "Profit", "color": "#6CCB5F"},
        ])

        tooltip = ChartTooltip(title="Q1 Sales", values=[{"name": "Product A", "value": "$12K", "color": "#0078D4"}, {"name": "Product B", "value": "$8K", "color": "#6CCB5F"}])

        axis = ChartAxis(orientation="horizontal", labels=["Jan", "Feb", "Mar", "Apr"])

        data_label = DataLabel(text="1,234", color="#0078D4")

        color_scale = ColorScale(color_low="#E8F5E9", color_high="#1B5E20", min_val=0, max_val=100)

        mini_stat = MiniStat(value="2.4K", label="Users", trend="+12%", icon=FIF.PEOPLE, accent_color="#0078D4")

        row.addWidget(legend)
        row.addWidget(tooltip)
        row.addWidget(axis)
        row.addWidget(data_label)
        row.addWidget(color_scale)
        row.addWidget(mini_stat)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_chart_controls(self, parent):
        group = QGroupBox("Chart Controls")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Interactive controls for chart manipulation: range selection, time filtering, zoom, and export.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        range_slider = RangeSlider(min_val=0, max_val=100, low=20, high=80)
        time_picker = TimeRangePicker()
        chart_filter = ChartFilter(filters=["Revenue", "Costs", "Profit"])
        granularity = DataGranularity()
        export_menu = ChartExportMenu()
        zoom_control = ChartZoomControl(zoom_level=100)

        row.addWidget(range_slider)
        row.addWidget(time_picker)
        row.addWidget(chart_filter)
        row.addWidget(granularity)
        row.addWidget(export_menu)
        row.addWidget(zoom_control)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)
