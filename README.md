# FluentUI Gallery

A comprehensive component showcase built with **PySide6** and **QFluentWidgets**, featuring 100+ custom components with Fluent Design, rich animations, and full dark/light mode support.

---

## Features

- **100+ UI components** across 17 categories
- **Fluent Design** with smooth animations (150–300ms)
- **Full dark/light mode** support via `ThemeManager`
- **Custom QPainter-based** components for pixel-perfect rendering
- **QPropertyAnimation-driven** interactions with easing curves
- **WCAG AA contrast compliance** (4.5:1 minimum ratio)
- **Zero external dependencies** beyond PySide6 and QFluentWidgets

---

## Installation & Run

```bash
pip install PySide6 PySide6-Fluent-Widgets
python main.py
```

---

## Component Catalog

### Custom

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| GradientCard | `app.components.gradient_card` | `GradientCard(title="", description="", color1="#0078D4", color2="#0067C0", direction="horizontal")` | `refresh_theme()` | — | Hover glow |
| StatusIndicator | `app.components.status_indicator` | `StatusIndicator(status="online", size=12)` | `set_status(status)`, `set_breathing(enabled)` | — | Breathing |
| AvatarRing | `app.components.avatar_ring` | `AvatarRing(avatar_path=None, size=64, ring_color1="#0078D4", ring_color2="#60CDFF", ring_width=3)` | `set_avatar(path)`, `set_ring_colors(c1, c2)`, `set_status(show, color)` | — | Gradient ring |
| ProgressRing | `app.components.progress_ring` | `ProgressRing(size=80, stroke_width=6, color1="#0078D4", color2="#60CDFF")` | `set_value(value)`, `set_indeterminate(enabled)` | — | Arc sweep |
| GlowButton | `app.components.glow_button` | `GlowButton(text="", accent_color="#0078D4")` | `refresh_theme()` | Inherited from `QPushButton` | Hover glow |
| TypingText | `app.components.typing_text` | `TypingText(full_text="", typing_speed=60, loop=False)` | `start_typing()`, `stop_typing()`, `set_text(text)` | — | Character-by-character |
| ShimmerWidget | `app.components.shimmer_widget` | `ShimmerWidget(width=200, height=20, shape="rectangle")` | `refresh_theme()` | — | Shimmer sweep |
| AnimatedToggle | `app.components.animated_toggle` | `AnimatedToggle(on_color="#0078D4", off_color=None)` | `set_checked(checked, animate=True)`, `is_checked()` | — | Elastic spring |
| NotificationBadge | `app.components.notification_badge` | `NotificationBadge(count=0, color="#FF4444")` | `set_count(count)`, `set_color(color)` | — | Pulse scale |
| WaveProgress | `app.components.wave_progress` | `WaveProgress()` | `set_value(value)`, `get_value()` | — | Dual sine wave |
| FlipCard | `app.components.flip_card` | `FlipCard()` | `set_front(widget)`, `set_back(widget)`, `flip()` | — | 3D flip |
| AnimatedCounter | `app.components.animated_counter` | `AnimatedCounter(prefix="", suffix="", font_size=36)` | `set_value(value)`, `set_prefix(p)`, `set_suffix(s)` | — | Number roll |
| AccordionCard | `app.components.accordion_card` | `AccordionCard(title="")` | `set_content(widget)`, `set_expanded(expanded, animate=True)`, `toggle()`, `is_expanded()` | — | Height expand |
| SegmentedWidget | `app.components.segmented_widget` | `SegmentedWidget(segments=None)` | `set_current_index(index)`, `set_segments(segments)` | `currentChanged(int)` | Sliding indicator |
| Toast | `app.components.toast` | `Toast(message="", toast_type="info")` | `show_toast()`, `dismiss()`, `Toast.show(message, type, parent)` | `dismissed` | Slide-in / fade-out |
| ExpandGroup | `app.components.expand_group` | `ExpandGroup(title="")` | `set_content(widget)`, `set_expanded(expanded, animate=True)`, `toggle()` | — | Arrow rotation + expand |
| RippleButton | `app.components.ripple_button` | `RippleButton(text="", accent_color="#0078D4")` | `refresh_theme()` | Inherited from `QPushButton` | Material ripple + press scale |

### Charts

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| LineChart | `app.components.line_chart` | `LineChart(series=None, labels=None)` | `refresh_theme()` | — | Draw progress |
| BarChart | `app.components.bar_chart` | `BarChart(data=None, labels=None, colors=None)` | `set_data(data, labels)`, `refresh_theme()` | — | Grow from baseline |
| PieChart | `app.components.pie_chart` | `PieChart(data=None, labels=None, colors=None, donut=False)` | `refresh_theme()` | — | Sweep reveal |
| AreaChart | `app.components.area_chart` | `AreaChart(series=None, labels=None)` | `refresh_theme()` | — | Fill fade-in |
| ScatterChart | `app.components.scatter_chart` | `ScatterChart(data=None)` | `refresh_theme()` | — | Pop from center |
| GaugeChart | `app.components.gauge_chart` | `GaugeChart(value=0, min_val=0, max_val=100, label="")` | `set_value(value)` | — | Needle rotation |
| RadarChart | `app.components.radar_chart` | `RadarChart(categories=None, series=None)` | `refresh_theme()` | — | Scale from center |
| SparklineChart | `app.components.sparkline_chart` | `SparklineChart(data=None, color="#0078D4")` | `refresh_theme()` | — | Draw progress |
| HeatmapChart | `app.components.heatmap_chart` | `HeatmapChart(data=None, x_labels=None, y_labels=None, color_low="#E8F5E9", color_high="#1B5E20")` | `refresh_theme()` | — | Row-by-row fade |
| TreemapChart | `app.components.treemap_chart` | `TreemapChart(data=None)` | `refresh_theme()` | — | Expand from center |

### Chart Utilities

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| ChartAxis | `app.components.chart_axis` | `ChartAxis()` | `refresh_theme()` | — | — |
| ChartExportMenu | `app.components.chart_export_menu` | `ChartExportMenu()` | `refresh_theme()` | — | — |
| ChartFilter | `app.components.chart_filter` | `ChartFilter()` | `refresh_theme()` | — | — |
| ChartLegend | `app.components.chart_legend` | `ChartLegend()` | `refresh_theme()` | — | — |
| ChartTooltip | `app.components.chart_tooltip` | `ChartTooltip()` | `refresh_theme()` | — | — |
| ChartZoomControl | `app.components.chart_zoom_control` | `ChartZoomControl()` | `refresh_theme()` | — | — |

### Diagrams

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| FlowchartNode | `app.components.flowchart_node` | `FlowchartNode(title="", subtitle="", node_type="process")` | `animate_in()`, `refresh_theme()` | — | Draw border |
| FlowchartConnector | `app.components.flowchart_connector` | `FlowchartConnector(direction="down", label="")` | `animate_in()`, `refresh_theme()` | — | Arrow draw |
| MindMapNode | `app.components.mind_map_node` | `MindMapNode(title="", level=0)` | `set_expanded(expanded)`, `is_expanded()` | `expandChanged(bool)` | Expand progress |
| MindMapBranch | `app.components.mind_map_branch` | `MindMapBranch(direction="right")` | `animate_in()`, `refresh_theme()` | — | Curve draw |
| OrgChartNode | `app.components.org_chart_node` | `OrgChartNode(name="", role="")` | `animate_in()`, `refresh_theme()` | — | Fade + highlight |

### Social

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| LikeButton | `app.components.like_button` | `LikeButton(count=0, liked=False)` | `set_liked(liked, animate=True)`, `set_count(count)` | `likedChanged(bool, int)` | Bounce scale |
| FollowButton | `app.components.follow_button` | `FollowButton(following=False)` | `set_following(following)`, `is_following()` | `followChanged(bool)` | Progress morph |
| CommentBubble | `app.components.comment_bubble` | `CommentBubble(text="", author="", timestamp="", is_own=False)` | `set_text(text)`, `set_author(author)`, `set_timestamp(ts)` | — | Slide + fade |
| ReactionPicker | `app.components.reaction_picker` | `ReactionPicker()` | `refresh_theme()` | `reactionSelected(str)` | Pop from center |
| ShareMenu | `app.components.share_menu` | `ShareMenu()` | `toggle_menu()` | `shareRequested(str)` | Slide expand |

### Media

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| AudioPlayer | `app.components.audio_player` | `AudioPlayer(title="", duration=180)` | `refresh_theme()` | — | Fade progress |
| MediaPlayerBar | `app.components.media_player_bar` | `MediaPlayerBar()` | `refresh_theme()` | — | Press scale |
| ImageGallery | `app.components.image_gallery` | `ImageGallery(images=None, columns=3)` | `refresh_theme()` | — | Fade + hover overlay |
| VideoThumbnail | `app.components.video_thumbnail` | `VideoThumbnail(title="", duration="3:45", color="#333333")` | `refresh_theme()` | — | Hover scale |
| LightboxOverlay | `app.components.lightbox_overlay` | `LightboxOverlay()` | `show_content(widget)`, `close_lightbox()` | — | Scale + fade |
| CarouselWidget | `app.components.carousel_widget` | `CarouselWidget(items=None)` | `refresh_theme()` | — | Slide transition |

### Form+

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| FloatingLabelInput | `app.components.floating_label_input` | `FloatingLabelInput(label="", placeholder="")` | `text()`, `set_text(text)` | `textChanged(str)` | Float label |
| CreditCardInput | `app.components.credit_card_input` | `CreditCardInput()` | `card_number()`, `set_card_number(num)` | `cardChanged(str)` | Segment focus |
| OtpInput | `app.components.otp_input` | `OtpInput(length=6)` | `code()`, `set_code(code)`, `clear()` | `codeEntered(str)` | Focus shift |
| DateRangePicker | `app.components.date_range_picker` | `DateRangePicker()` | `start_date()`, `end_date()`, `set_range(start, end)` | `rangeChanged` | Calendar slide |
| TimeRangePicker | `app.components.time_range_picker` | `TimeRangePicker()` | `start_time()`, `end_time()` | `rangeChanged` | Dial spin |
| ColorTagInput | `app.components.color_tag_input` | `ColorTagInput(placeholder="")` | `tags()`, `add_tag(tag)`, `clear_tags()` | `tagsChanged(list)` | Tag pop-in |
| StepperInput | `app.components.stepper_input` | `StepperInput(value=0, min_val=0, max_val=100, step=1)` | `value()`, `set_value(val)`, `step_up()`, `step_down()` | `valueChanged(int)` | Number roll |

### Status

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| ConnectionStatus | `app.components.connection_status` | `ConnectionStatus(connected=True)` | `set_connected(connected)`, `is_connected()` | `connectionChanged(bool)` | Dot pulse |
| SignalStrength | `app.components.signal_strength` | `SignalStrength(level=4)` | `set_level(level)`, `get_level()` | `levelChanged(int)` | Bar grow |
| BatteryIndicator | `app.components.battery_indicator` | `BatteryIndicator(level=80, charging=False)` | `set_level(level)`, `set_charging(charging)` | `levelChanged(int)` | Fill animate |
| StatusPill | `app.components.status_pill` | `StatusPill(text="", color="#0078D4")` | `set_text(text)`, `set_color(color)` | — | Fade |
| CountdownTimer | `app.components.countdown_timer` | `CountdownTimer(seconds=60)` | `start()`, `pause()`, `reset()`, `set_seconds(s)` | `finished`, `tick(int)` | Arc sweep |
| InfiniteLoader | `app.components.infinite_loader` | `InfiniteLoader(size=40, color="#0078D4")` | `start()`, `stop()` | — | Continuous spin |
| PullRefresh | `app.components.pull_refresh` | `PullRefresh()` | `set_refreshing(refreshing)`, `is_refreshing()` | `refreshTriggered` | Pull arc |

### Advanced

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| MorphingShape | `app.components.morphing_shape` | `MorphingShape(color="#0078D4")` | `morph_to(shape_name)` — shapes: `"circle"`, `"square"`, `"triangle"`, `"star"` | — | Point interpolation |
| ParticleBackground | `app.components.particle_background` | `ParticleBackground(particle_count=50, color="#0078D4")` | `set_color(color)` | — | Continuous drift + lines |
| ParallaxScroll | `app.components.parallax_scroll` | `ParallaxScroll()` | `refresh_theme()` | — | Multi-layer parallax |
| CommandPalette | `app.components.command_palette` | `CommandPalette(commands=None)` | `show_palette()`, `hide_palette()` | `commandSelected(str)` | Fade + scale |
| ContextMenu | `app.components.context_menu` | `ContextMenu(items=None)` | `popup(pos)` | `itemSelected(str)` | Scale from 0.95 |
| AnimatedBorder | `app.components.animated_border` | `AnimatedBorder(title="")` | `set_title(title)` | — | Rotating conical gradient |
| NeonBorder | `app.components.neon_border` | `NeonBorder(color="#0078D4")` | `set_color(color)` | — | Pulsing glow |
| GradientText | `app.components.gradient_text` | `GradientText(text="", color1="#0078D4", color2="#005A9E")` | `set_text(text)`, `set_colors(c1, c2)` | — | Flowing gradient |

### Data

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| StatCard | `app.components.stat_card` | `StatCard(title="", value="", icon=FluentIcon.APPLICATION, trend="", accent_color="#0078D4")` | `refresh_theme()` | — | Hover offset |
| MiniStat | `app.components.mini_stat` | `MiniStat(label="", value="", color="#0078D4")` | `set_value(val)`, `set_label(label)` | — | Number roll |
| DataLabel | `app.components.data_label` | `DataLabel(text="", label_type="info")` | `set_text(text)`, `set_type(label_type)` | — | Fade |
| DataGranularity | `app.components.data_granularity` | `DataGranularity(options=None)` | `current()`, `set_current(option)` | `granularityChanged(str)` | Indicator slide |
| ColorScale | `app.components.color_scale` | `ColorScale(min_val=0, max_val=100, color_low="#E8F5E9", color_high="#1B5E20")` | `set_value(val)`, `get_value()` | `valueChanged(float)` | Fill sweep |

### Layout

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| GlassCard | `app.components.glass_card` | `GlassCard(title="")` | `set_title(title)` | — | Blur progress |
| SpotlightCard | `app.components.spotlight_card` | `SpotlightCard(title="", description="")` | `refresh_theme()` | — | Spotlight follow |
| StickyHeader | `app.components.sticky_header` | `StickyHeader(title="")` | `set_title(title)`, `refresh_theme()` | — | Fade on scroll |
| WaveDivider | `app.components.wave_divider` | `WaveDivider(color="#0078D4", height=40)` | `set_color(color)` | — | Wave oscillation |
| GradientPicker | `app.components.gradient_picker` | `GradientPicker(color1="#0078D4", color2="#005A9E")` | `gradient()`, `set_gradient(c1, c2, direction)` | `gradientChanged(str)` | Stop slide |

### Navigation

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| DragSortableList | `app.components.drag_sortable_list` | `DragSortableList(items=None)` | `items()`, `set_items(items)`, `add_item(text)` | `orderChanged(list)` | Drag lift + swap |
| KanbanCard | `app.components.kanban_card` | `KanbanCard(title="", description="", tag_color="#0078D4")` | `set_title(title)`, `set_description(desc)` | — | Hover lift |
| SwimLane | `app.components.swim_lane` | `SwimLane(title="", cards=None)` | `add_card(card)`, `remove_card(index)` | `cardMoved(int, int)` | Slide reorder |
| VirtualScrollList | `app.components.virtual_scroll_list` | `VirtualScrollList(item_count=0, item_height=40)` | `set_item_count(count)`, `scroll_to(index)` | `visibleRangeChanged(int, int)` | Smooth scroll |
| StepIndicator | `app.components.step_indicator` | `StepIndicator(steps=None, current=0)` | `set_current(index)`, `current()`, `set_steps(steps)` | `stepChanged(int)` | Progress fill |

### Feedback

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| ColorPaletteCard | `app.components.color_palette_card` | `ColorPaletteCard(title="Color Palette", colors=None)` | `refresh_theme()` | `colorCopied(str)` | Click copy |
| ColorPicker | `app.components.color_picker` | `ColorPicker(color="#0078D4")` | `refresh_theme()` | `colorChanged(str)` | Drag select |
| BookmarkButton | `app.components.bookmark_button` | `BookmarkButton(bookmarked=False)` | `set_bookmarked(bookmarked)`, `is_bookmarked()` | `bookmarkChanged(bool)` | Fill sweep |
| RatingStars | `app.components.rating_stars` | `RatingStars(count=5, value=0, size=24)` | `set_value(val)`, `value()` | `ratingChanged(int)` | Star fill |
| RatingEmoji | `app.components.rating_emoji` | `RatingEmoji(value=0)` | `set_value(val)`, `value()` | `ratingChanged(int)` | Emoji morph |

### Basic

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| CircularProgress | `app.components.circular_progress` | `CircularProgress(value=0, size=100, stroke_width=8, color="#0078D4")` | `set_value(value)` | — | Arc sweep |
| TagChip | `app.components.tag_chip` | `TagChip(text="", color="#0078D4", removable=True)` | `set_text(text)`, `set_color(color)` | `removeClicked` | Pop-in |
| MultiSelect | `app.components.multi_select` | `MultiSelect(options=None, selected=None)` | `selected()`, `set_selected(items)`, `add_option(text)` | `selectionChanged(list)` | Checkbox toggle |
| RangeSlider | `app.components.range_slider` | `RangeSlider(min_val=0, max_val=100, low=20, high=80)` | `low()`, `high()`, `set_range(low, high)` | `rangeChanged(int, int)` | Handle slide |
| UserCard | `app.components.user_card` | `UserCard(name="", role="", avatar_path=None)` | `set_name(name)`, `set_role(role)`, `set_avatar(path)` | — | Hover highlight |

### Timeline

| Component | Import | Constructor | Key Methods | Signals | Key Animation |
|-----------|--------|-------------|-------------|---------|---------------|
| LinearTimeline | `app.components.linear_timeline` | `LinearTimeline(items=None)` | `add_item(item)`, `set_current(index)` | `currentChanged(int)` | Connector draw |
| TimelineItem | `app.components.timeline_item` | `TimelineItem(title="", description="", timestamp="", color="#0078D4")` | `set_title(title)`, `set_description(desc)` | — | Dot pulse |
| FileDropZone | `app.components.file_drop_zone` | `FileDropZone(label="Drop files here", accept_multiple=False)` | `set_accept_multiple(enabled)`, `file_paths()` | `filesDropped(list)` | Border dash |

---

## Usage Examples

### GradientCard

```python
from app.components.gradient_card import GradientCard

card = GradientCard(
    title="Ocean Blue",
    description="Horizontal gradient with hover effect",
    color1="#0078D4",
    color2="#005A9E",
    direction="horizontal"
)
layout.addWidget(card)
```

### StatusIndicator

```python
from app.components.status_indicator import StatusIndicator

indicator = StatusIndicator(status=StatusIndicator.ONLINE, size=14)
indicator.set_breathing(True)
layout.addWidget(indicator)
```

### LineChart

```python
from app.components.line_chart import LineChart

chart = LineChart(
    series=[
        {"name": "Revenue", "data": [12, 19, 3, 5, 2, 3], "color": "#0078D4"},
        {"name": "Profit", "data": [8, 12, 6, 9, 4, 7], "color": "#6CCB5F"},
    ],
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
)
layout.addWidget(chart)
```

### Toast

```python
from app.components.toast import Toast

Toast.show("Operation completed successfully!", "success", self)
Toast.show("Something went wrong.", "error", self)
```

### AnimatedToggle

```python
from app.components.animated_toggle import AnimatedToggle

toggle = AnimatedToggle(on_color="#0078D4")
toggle.set_checked(True)
layout.addWidget(toggle)
```

### GaugeChart

```python
from app.components.gauge_chart import GaugeChart

gauge = GaugeChart(value=72, min_val=0, max_val=100, label="CPU Usage")
gauge.set_value(85)
layout.addWidget(gauge)
```

### LikeButton

```python
from app.components.like_button import LikeButton

like = LikeButton(count=42, liked=False)
like.likedChanged.connect(lambda liked, count: print(f"Liked: {liked}, Count: {count}"))
layout.addWidget(like)
```

### ColorPicker

```python
from app.components.color_picker import ColorPicker

picker = ColorPicker(color="#FF6B6B")
picker.colorChanged.connect(lambda color: print(f"Selected: {color}"))
layout.addWidget(picker)
```

### CommandPalette

```python
from app.components.command_palette import CommandPalette

palette = CommandPalette(commands=[
    {"name": "Open File", "action": "open", "icon": FIF.OPEN, "shortcut": "Ctrl+O"},
    {"name": "Save", "action": "save", "icon": FIF.SAVE, "shortcut": "Ctrl+S"},
])
palette.commandSelected.connect(lambda action: print(f"Action: {action}"))
palette.show_palette()
```

### FlowchartNode

```python
from app.components.flowchart_node import FlowchartNode
from app.components.flowchart_connector import FlowchartConnector

start = FlowchartNode("Start", node_type="start")
process = FlowchartNode("Process Data", subtitle="Step 1", node_type="process")
connector = FlowchartConnector(direction="down")
```

---

## Architecture

```
app/
├── main_window.py          # Main FluentWindow with 15 navigation pages
├── theme_manager.py         # Theme switching (dark/light) with signal propagation
├── theme_aware_page.py      # Base page class with theme tracking
├── theme_helpers.py         # Theme utility functions
├── application.py           # QApplication setup and configuration
├── splash_screen.py         # Splash screen on startup
├── components/              # 99 custom components
│   ├── __init__.py
│   ├── gradient_card.py     # Custom card components
│   ├── line_chart.py        # Chart components
│   ├── flowchart_node.py    # Diagram components
│   ├── like_button.py       # Social components
│   ├── audio_player.py      # Media components
│   ├── floating_label_input.py # Form components
│   ├── connection_status.py # Status components
│   ├── morphing_shape.py    # Advanced components
│   └── ...                  # 90+ more components
├── pages/                   # 15 showcase pages
│   ├── hero_page.py         # Landing / overview page
│   ├── basic_widgets.py     # QFluentWidgets basic components
│   ├── input_widgets.py     # Input components
│   ├── navigation_widgets.py # Navigation components
│   ├── feedback_widgets.py  # Feedback components
│   ├── data_widgets.py      # Data display components
│   ├── layout_widgets.py    # Layout components
│   ├── custom_widgets_page.py # Custom components showcase
│   ├── charts_page.py       # Chart components
│   ├── diagrams_page.py     # Diagram components
│   ├── social_page.py       # Social components
│   ├── media_page.py        # Media components
│   ├── form_enhanced_page.py # Enhanced form components
│   ├── status_page.py       # Status components
│   └── advanced_page.py     # Advanced components
├── icons/
│   └── __init__.py
└── resources/
    └── __init__.py
```

### Theme System

The theme system is built around `ThemeManager` which emits `themeChanged(Theme)` signals. All pages inherit from `ThemeAwarePage` which provides:

- `_track_group(group)` — auto-refresh QGroupBox styles on theme change
- `_track_label(label, role)` — auto-refresh QLabel colors on theme change
- `_track_title(label)` — auto-refresh title labels
- `_track_custom_widget(widget)` — auto-refresh custom components via `refresh_theme()`
- `refresh_theme()` — full recursive theme update

### Animation Standards

| Animation Type | Duration | Easing Curve |
|---------------|----------|--------------|
| Hover effects | 150–200ms | `OutCubic` |
| Expand/collapse | 200–250ms | `OutCubic` |
| Page transitions | 300ms | `InOutCubic` |
| Elastic toggles | 300ms | `OutElastic` |
| Ripple effects | 300ms | `OutCubic` |
| Shimmer loops | 1500ms | `InOutCubic` |
| Breathing pulses | 50ms tick | Sine wave |

---

## Design Standards

### Color System

| Token | Light Mode | Dark Mode | Usage |
|-------|-----------|-----------|-------|
| `--bg-primary` | `#FFFFFF` | `#202020` | Page background |
| `--bg-card` | `rgba(255,255,255,0.7)` | `rgba(255,255,255,0.04)` | Card background |
| `--text-primary` | `#1A1A1A` | `#FFFFFF` | Primary text |
| `--text-secondary` | `#616161` | `#9E9E9E` | Secondary text |
| `--border` | `rgba(0,0,0,0.1)` | `rgba(255,255,255,0.08)` | Borders |
| `--accent` | `#0078D4` | `#60CDFF` | Accent color |

### WCAG AA Compliance

All text/background combinations maintain a minimum contrast ratio of **4.5:1**:

- Primary text on background: `#1A1A1A` / `#FFFFFF` → **17.4:1** ✅
- Secondary text on background: `#616161` / `#FFFFFF` → **5.7:1** ✅
- Dark mode primary: `#FFFFFF` / `#202020` → **15.7:1** ✅
- Dark mode secondary: `#9E9E9E` / `#202020` → **6.3:1** ✅

### Border Radius Scale

| Size | Value | Usage |
|------|-------|-------|
| `sm` | 4px | Small elements (tags, chips) |
| `md` | 8px | Buttons, inputs |
| `lg` | 12px | Cards, groups |
| `xl` | 20px | Pills, avatars |

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Tight spacing |
| `sm` | 8px | Between related items |
| `md` | 12–16px | Between groups |
| `lg` | 20–24px | Section spacing |
| `xl` | 32–40px | Page margins |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
