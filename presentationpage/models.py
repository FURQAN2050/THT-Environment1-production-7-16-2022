from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField, StreamBlock
from wagtail.core.blocks import StructBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel

# Create your models here.


# Presentation Page
class PresentationPage(Page):

    max_count = 1

    password_required_template = "templates/presentationpage/presentation_page.html"

    visionTitle = StreamField([
        ('text', blocks.CharBlock(default="Vision")),
    ], blank=True)

    visionText = StreamField([
        ('text', blocks.TextBlock(default="Vision")),
    ], blank=True)

    missionTitle = StreamField([
        ('text', blocks.CharBlock(default="Mission")),
    ], blank=True)

    missionText = StreamField([
        ('text', blocks.TextBlock(default="Mission")),
    ], blank=True)

    notesTitle = StreamField([
        ('text', blocks.CharBlock(default="Notes")),
    ], blank=True)

    notesText = StreamField([
        ('text', blocks.TextBlock(default="Notes")),
    ], blank=True)

    contactusTitle = StreamField([
        ('text', blocks.CharBlock(default="Contact Us")),
    ], blank=True)

    contactusText = StreamField([
        ('text', blocks.TextBlock(default="Contact Us")),
    ], blank=True)

    videoURL = StreamField([
        
        ('video', StructBlock([
            ('videoURL', blocks.CharBlock()),
            ('videoTitle', blocks.CharBlock()),
        ]))
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            StreamFieldPanel('visionTitle'),
            StreamFieldPanel('visionText'),
        ],
        heading="Vision",
        classname="collapsible"
        ),

        MultiFieldPanel([
            StreamFieldPanel('missionTitle'),
            StreamFieldPanel('missionText'),
        ],
        heading="Mission",
        classname="collapsible"
        ),

        MultiFieldPanel([
            StreamFieldPanel('notesTitle'),
            StreamFieldPanel('notesText'),
        ],
        heading="Notes",
        classname="collapsible"
        ),

        MultiFieldPanel([
            StreamFieldPanel('contactusTitle'),
            StreamFieldPanel('contactusText'),
        ],
        heading="Contact Us",
        classname="collapsible"
        ),

        StreamFieldPanel('videoURL'),

    ]

class IntroPage(Page):

    max_count = 1

    password_required_template = "templates/presentationpage/intro_page.html"


    visionTitle = StreamField([
        ('text', blocks.CharBlock(default="Vision")),
    ], blank=True)

    visionText = StreamField([
        ('text', blocks.RichTextBlock(features=['h2', 'bold', 'italic', 'link', 'ul', 'hr'], default="Vision")),
    ], blank=True)

    explainTitle = StreamField([
        ('text', blocks.CharBlock(default="Explain")),
    ], blank=True)

    explainText = StreamField([
        ('text', blocks.RichTextBlock(features=['h2', 'bold', 'italic', 'link', 'ul', 'hr'], default="Explain")),
    ], blank=True)

    sellingTitle = StreamField([
        ('text', blocks.CharBlock(default="Why this is for you")),
    ], blank=True)

    sellingText = StreamField([
        ('text', blocks.RichTextBlock(features=['h2', 'bold', 'italic', 'link', 'ul', 'hr'], default="Why this is for you")),
    ], blank=True)

    notesTitle = StreamField([
        ('text', blocks.CharBlock(default="Learn more")),
    ], blank=True)

    notesText = StreamField([
        ('text', blocks.RichTextBlock(features=['h2', 'bold', 'italic', 'link', 'ul', 'hr'], default="Learn more")),
    ], blank=True)

    contactusTitle = StreamField([
        ('text', blocks.CharBlock(default="Contact Us")),
    ], blank=True)

    contactusText = StreamField([
        ('text', blocks.TextBlock(default="Contact Us")),
    ], blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            StreamFieldPanel('visionTitle'),
            StreamFieldPanel('visionText'),
        ], 
        heading="Vision",
        classname="collapsible"
        ),

        MultiFieldPanel([
            StreamFieldPanel('explainTitle'),
            StreamFieldPanel('explainText'),
        ],
        heading="Explain Text",
        classname="collapsible"
        ),

        MultiFieldPanel([
            StreamFieldPanel('sellingTitle'),
            StreamFieldPanel('sellingText'),
        ],
        heading="Sell",
        classname="collapsible"
        ),

        MultiFieldPanel([
            StreamFieldPanel('notesTitle'),
            StreamFieldPanel('notesText'),
        ],
        heading="Notes Text",
        classname="collapsible"
        ),

        MultiFieldPanel([
            StreamFieldPanel('contactusTitle'),
            StreamFieldPanel('contactusText'),
        ],
        heading="Contact Us",
        classname="collapsible"
        ),
    ]


