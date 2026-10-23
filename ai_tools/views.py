from django.shortcuts import render
from .utils import summarize_text
# from .utils import translate_text
from accounts.models import BlogPost
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import language_tool_python
tool = language_tool_python.LanguageTool("en-US")
import logging
from argostranslate import translate
logger = logging.getLogger(__name__)
from django.conf import settings
from gtts import gTTS
from gtts.tts import gTTSError
import os
import uuid

@require_POST
def check_writing(request):
    text = request.POST.get("text", "")

    matches = tool.check(text)

    corrections = []

    for match in matches:
        corrections.append({
            "message": match.message,
            "offset": match.offset,
            "length": match.error_length,
            "suggestions": match.replacements[:5],
        })

    return JsonResponse({
        "corrections": corrections
    })

def dashboard(request):
    return render(request, 'ai_tools/dashboard.html')

def summarizer(request):

    summary = ""
    blog_text = ""
    length = 3

    original_words = 0
    summary_words = 0
    compression = 0

    if request.method == "POST":

        blog_text = request.POST.get("blog_text", "")
        length = int(request.POST.get("length", 3))

        if blog_text:

            summary = summarize_text(
                blog_text,
                length
            )

            original_words = len(
                blog_text.split()
            )

            summary_words = len(
                summary.split()
            )

            compression = round(
                (
                    (original_words - summary_words)
                    / original_words
                ) * 100,
                1
            )

    return render(
        request,
        "ai_tools/summarizer.html",
        {
            "summary": summary,
            "blog_text": blog_text,
            "length": length,
            "original_words": original_words,
            "summary_words": summary_words,
            "compression": compression,
        }
    )

def translator(request):
    text = ""
    translated_text = ""
    source_language = "en"
    language = "hi"
    message = ""

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        source_language = request.POST.get("source_language", "en")
        language = request.POST.get("language", "hi")

        if not text:
            message = "Please enter some text to translate."

        elif len(text) > 5000:
            message = "Please enter no more than 5000 characters."

        elif source_language not in ("en", "hi") or language not in ("en", "hi"):
            message = "Please select a supported language."

        elif source_language == language:
            message = "Please select different source and target languages."

        else:
            try:
                translated_text = translate.translate(
                    text,
                    source_language,
                    language,
                )

                if not translated_text:
                    message = "No translation was returned."

            except Exception:
                logger.exception("Offline translation failed.")
                message = "Translation failed. Please try again."

    return render(
        request,
        "ai_tools/translator.html",
        {
            "text": text,
            "translated_text": translated_text,
            "source_language": source_language,
            "language": language,
            "message": message,
        },
    )

def text_to_speech(request):
    audio_file = None
    text = ""
    language = " en "
    error_message = ""

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        language = request.POST.get("language", "en")

        # Allow only supported language choices from your form
        allowed_languages = ["en", "hi", "mr"]

        if language not in allowed_languages:
            language = "en"
            error_message = "Please select a valid language."

        elif not text:
            error_message = "Please enter some text."

        else:
            try:
                # Create media folder if it doesn't exist
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

                # Generate a unique filename for each audio file
                filename = f"speech_{uuid.uuid4().hex}.mp3"

                filepath = os.path.join(
                    settings.MEDIA_ROOT,
                    filename
                )

                # Convert text directly into speech
                tts = gTTS(
                    text=text,
                    lang=language
                )

                tts.save(filepath)

                audio_file = settings.MEDIA_URL + filename

            except (gTTSError, OSError):
                error_message = (
                    "Unable to generate speech right now. "
                    "Please check your internet connection "
                    "and try again."
                )

    return render(
        request,
        "ai_tools/text_to_speech.html",
        {
            "audio_file": audio_file,
            "text": text,
            "language": language,
            "error_message": error_message,
        }
    )

MOOD_KEYWORDS = {

    "happy": [
        "success",
        "achievement",
        "fun",
        "joy",
        "travel"
    ],

    "motivated": [
        "career",
        "growth",
        "productivity",
        "discipline",
        "success"
    ],

    "curious": [
        "ai",
        "technology",
        "science",
        "python",
        "django"
    ],

    "relaxed": [
        "travel",
        "stories",
        "books",
        "nature"
    ],

    "bored": [
        "fun",
        "interesting",
        "tips",
        "technology"
    ],

    "stressed": [
        "mindfulness",
        "health",
        "meditation",
        "motivation"
    ]
}
def mood_selector(request):

    selected_mood = None
    recommended_blogs = []

    if request.method == "POST":

        selected_mood = request.POST.get("mood")

        keywords = MOOD_KEYWORDS.get(
            selected_mood,
            []
        )

        query = Q()

        for keyword in keywords:

            query |= Q(
                title__icontains=keyword
            )

            query |= Q(
                content__icontains=keyword
            )

        recommended_blogs = BlogPost.objects.filter(
            query
        ).distinct()

    return render(
        request,
        "ai_tools/mood_selector.html",
        {
            "selected_mood": selected_mood,
            "recommended_blogs": recommended_blogs,
        }
    )
