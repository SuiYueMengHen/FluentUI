from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, BodyLabel, isDarkTheme)
from app.theme_aware_page import ThemeAwarePage
from app.components.image_gallery import ImageGallery
from app.components.audio_player import AudioPlayer
from app.components.video_thumbnail import VideoThumbnail
from app.components.carousel_widget import CarouselWidget
from app.components.media_player_bar import MediaPlayerBar
from app.components.color_picker import ColorPicker
from app.components.gradient_picker import GradientPicker


class MediaPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("mediaPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Media", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Media display and interaction components for images, audio, video, and color selection.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_image_gallery(main_layout)
        self._build_audio_player(main_layout)
        self._build_video_thumbnail(main_layout)
        self._build_carousel(main_layout)
        self._build_media_player_bar(main_layout)
        self._build_color_picker(main_layout)
        self._build_gradient_picker(main_layout)

        main_layout.addStretch()

    def _build_image_gallery(self, parent):
        group = QGroupBox("Image Gallery")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Grid-based image gallery with hover zoom effect and fade-in animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        gallery = ImageGallery(columns=4)
        gallery.setFixedHeight(200)
        layout.addWidget(gallery)

        parent.addWidget(group)

    def _build_audio_player(self, parent):
        group = QGroupBox("Audio Player")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Audio player with playback controls, progress bar, and volume visualization.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        player = AudioPlayer(title="Ambient Soundscape", duration=180)
        layout.addWidget(player)

        parent.addWidget(group)

    def _build_video_thumbnail(self, parent):
        group = QGroupBox("Video Thumbnail")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Video thumbnail cards with hover scale effect, play overlay, and duration badge.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        thumb1 = VideoThumbnail(title="Tutorial", duration="12:30", color="#2D5F8A")
        thumb2 = VideoThumbnail(title="Demo Reel", duration="3:45", color="#5F2D8A")
        thumb3 = VideoThumbnail(title="Keynote", duration="45:00", color="#8A5F2D")

        row.addWidget(thumb1)
        row.addWidget(thumb2)
        row.addWidget(thumb3)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_carousel(self, parent):
        group = QGroupBox("Carousel")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Sliding carousel with arrow navigation and smooth slide transitions.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        carousel = CarouselWidget(items=["Slide 1", "Slide 2", "Slide 3"])
        carousel.setFixedHeight(200)
        layout.addWidget(carousel)

        parent.addWidget(group)

    def _build_media_player_bar(self, parent):
        group = QGroupBox("Media Player Bar")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Full-featured media player bar with play/pause, progress, volume, and time display.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        bar = MediaPlayerBar()
        layout.addWidget(bar)

        parent.addWidget(group)

    def _build_color_picker(self, parent):
        group = QGroupBox("Color Picker")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("HSV color picker with saturation-brightness panel and hue slider.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        picker = ColorPicker(color="#0078D4")
        layout.addWidget(picker)

        parent.addWidget(group)

    def _build_gradient_picker(self, parent):
        group = QGroupBox("Gradient Picker")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Two-stop gradient picker with preview bar and draggable color stops.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        picker = GradientPicker(color1="#0078D4", color2="#005A9E")
        layout.addWidget(picker)

        parent.addWidget(group)
