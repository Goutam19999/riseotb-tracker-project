from django.db import models


class ModerationStream(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Moderation Stream Name"
    )
    logo = models.ImageField(upload_to="stream_logos/", null=True, blank=True)

    def __str__(self):
        return self.name


class PostModeration(models.Model):
    moderation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Moderation Date"
    )
    agent_name = models.CharField(max_length=255, verbose_name="Agent Name (Full Name)")
    curalate_image_id = models.CharField(max_length=100, unique=True, verbose_name="1. Curalate Image ID")
    curalate_post_id = models.CharField(max_length=100, unique=True, verbose_name="2. Curalate Post ID")

    moderation_stream = models.ForeignKey(
        ModerationStream, on_delete=models.CASCADE, verbose_name="Moderation Stream"
    )

    AGENT_ACTION_CHOICES = [
        ("approved", "Approved"),
        (
            "approved-Instagram Admin Rights Required",
            "Approved-Instagram Admin Rights Required",
        ),
        ("rejected", "Rejected"),
    ]
    agent_action = models.CharField(
        max_length=50, choices=AGENT_ACTION_CHOICES, verbose_name="3. Agent Action"
    )

    selected_labels = models.JSONField(
        verbose_name="Selected Labels for the Post", default=list
    )
    start_time = models.TimeField(verbose_name="Start Time", null=True, blank=True)
    end_time = models.TimeField(verbose_name="End Time", null=True, blank=True)
 
    def __str__(self):
        return f"{self.agent_name} moderated post {self.curalate_post_id} on {self.moderation_date.strftime('%Y-%m-%d')}"


APPROVE_LABEL_CHOICES = [
    "apparel",
    "womens-apparel",
    "mens-apparel",
    "kids-apparel",
    "home",
    "beauty",
    "food",
    "electronics",
    "health-wellness",
    "toys",
    "baby",
    "pets",
    "patio-garden",
    "sporting-goods",
    "arts-crafts",
    "party",
    "hardware",
    "office",
    "halloween",
    "holiday",
    "new-years-reset",
    "valentines-day",
    "easter",
    "mothers-day",
    "fathers-day",
    "back-to-college",
    "back-to-school",
    "winter",
    "spring",
    "summer",
    "fall",
    "Media",
]

REJECT_LABEL_CHOICES = [
    "Text on Image",
    "Shelf Item/In Store",
    "In-Package",
    "Collage Image",
    "Not lifestyle",
    "Image Quality",
    "Duplicate Image",
    "Image Not Available/Post Archive",
    "Competitor or Reseller",
    "Competing Link",
    "Offensive Content",
    "Restricted Influencer",
    "Minor Account",
    "Restricted Hashtags",
    "Reposted Content",
    "Edited Post",
    "Product not found in Content",
    "Past Seasonal Item Post",
    "Not a US Citizen or Influencer",
    "Reels Duration Exceeded 60 Sec",
    "Landscape Mode Reel",
    "Product Tagging Timeout (15 min)",
    "Reels Duration Less Than 10 Sec",
    "Food Items only",
    "Already Rejected",
]
