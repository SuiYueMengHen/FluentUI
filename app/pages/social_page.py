from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, BodyLabel, isDarkTheme)
from app.theme_aware_page import ThemeAwarePage
from app.components.like_button import LikeButton
from app.components.rating_stars import RatingStars
from app.components.rating_emoji import RatingEmoji
from app.components.reaction_picker import ReactionPicker
from app.components.follow_button import FollowButton
from app.components.share_menu import ShareMenu
from app.components.comment_bubble import CommentBubble
from app.components.user_card import UserCard
from app.components.tag_chip import TagChip
from app.components.bookmark_button import BookmarkButton


class SocialPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("socialPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Social", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Interactive social components for likes, ratings, sharing, and user engagement.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_like_button(main_layout)
        self._build_rating_stars(main_layout)
        self._build_rating_emoji(main_layout)
        self._build_reaction_picker(main_layout)
        self._build_follow_button(main_layout)
        self._build_share_menu(main_layout)
        self._build_comment_bubble(main_layout)
        self._build_user_card(main_layout)
        self._build_tag_chips(main_layout)
        self._build_bookmark_button(main_layout)

        main_layout.addStretch()

    def _build_like_button(self, parent):
        group = QGroupBox("Like Button")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Animated like button with bounce effect, count display, and toggle state.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        like1 = LikeButton(count=42, liked=False)
        like2 = LikeButton(count=128, liked=True)
        like3 = LikeButton(count=0, liked=False)

        row.addWidget(like1)
        row.addWidget(like2)
        row.addWidget(like3)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_rating_stars(self, parent):
        group = QGroupBox("Rating Stars")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Star rating component with hover preview, click selection, and fill animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        stars = RatingStars(rating=3, max_stars=5)
        layout.addWidget(stars)
        parent.addWidget(group)

    def _build_rating_emoji(self, parent):
        group = QGroupBox("Rating Emoji")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Emoji-based rating with scale animation on selection for expressive feedback.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        emoji = RatingEmoji(rating=0)
        layout.addWidget(emoji)
        parent.addWidget(group)

    def _build_reaction_picker(self, parent):
        group = QGroupBox("Reaction Picker")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Multi-reaction picker with like, love, laugh, wow, sad, and angry options.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        picker = ReactionPicker()
        layout.addWidget(picker)
        parent.addWidget(group)

    def _build_follow_button(self, parent):
        group = QGroupBox("Follow Button")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Follow/unfollow toggle with smooth transition animation between states.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        follow1 = FollowButton(following=False)
        follow2 = FollowButton(following=True)

        row.addWidget(follow1)
        row.addWidget(follow2)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_share_menu(self, parent):
        group = QGroupBox("Share Menu")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Share menu with multiple platform options and hover highlight effects.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        menu = ShareMenu()
        layout.addWidget(menu)
        parent.addWidget(group)

    def _build_comment_bubble(self, parent):
        group = QGroupBox("Comment Bubble")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Chat-style comment bubbles with own/other differentiation and slide-in animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        own = CommentBubble(
            text="This is a great feature!",
            author="You",
            timestamp="2 min ago",
            is_own=True,
        )
        other = CommentBubble(
            text="Thanks for the feedback, we appreciate it!",
            author="Alice",
            timestamp="1 min ago",
            is_own=False,
        )

        layout.addWidget(own)
        layout.addWidget(other)
        parent.addWidget(group)

    def _build_user_card(self, parent):
        group = QGroupBox("User Card")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("User profile card with name, bio, and social stats with hover lift effect.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        card = UserCard(
            name="Jane Cooper",
            bio="Product Designer at Acme Corp",
            posts=142,
            followers=2340,
            following=186,
        )
        layout.addWidget(card)
        parent.addWidget(group)

    def _build_tag_chips(self, parent):
        group = QGroupBox("Tag Chips")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Removable tag chips with selection state and color customization.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(12)

        chip1 = TagChip(text="Python", color="#0078D4", removable=True, selected=True)
        chip2 = TagChip(text="PySide6", color="#6CCB5F", removable=True, selected=False)
        chip3 = TagChip(text="FluentUI", color="#FFB900", removable=True, selected=False)

        row.addWidget(chip1)
        row.addWidget(chip2)
        row.addWidget(chip3)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_bookmark_button(self, parent):
        group = QGroupBox("Bookmark Button")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Bookmark toggle with flip animation for saving and unsaving content.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        bm1 = BookmarkButton(bookmarked=False)
        bm2 = BookmarkButton(bookmarked=True)

        row.addWidget(bm1)
        row.addWidget(bm2)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)
