import os
from celery import shared_task
import google.generativeai as genai


@shared_task
def summarize_page_task(page_id):
    from .models import Page
    try:
        page = Page.objects.get(id=page_id)
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Зроби коротке резюме (2-3 речення) цієї вікі-сторінки українською мовою:\n\nНазва: {page.title}\n\nЗміст: {page.content}"
        response = model.generate_content(prompt)
        page.summary = response.text
        page.save()
    except Exception as e:
        print(f"Помилка ШІ: {e}")
