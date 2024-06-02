from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExamResult
import fitz  # PyMuPDF
from openai import OpenAI
import os
import openai


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



def tracker_view(request):
    return render(request, 'enter_page.html')

def extract_text_from_pdf(file):
    text = ""
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

budget = 5  # dollars
cost_per_1000_tokens = 0.002  # GPT-3.5-Turbo

def extract_info_with_openai(text):
    global budget
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts information from medical exam reports."},
                {"role": "user", "content": (
                    "Extract the following information from the text. Consider that it is text extracted from a medical exam report:\n\n"
                    "1. Patient Name\n"
                    "2. Date of Birth\n"
                    "3. Material\n"
                    "4. Exam Name\n"
                    "5. Method\n"
                    "6. Result\n"
                    "7. Reference Value\n"
                    "8. Note\n\n"
                    f"Text:\n{text}\n\n"
                    "Extracted Information:"
                )}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        usage = response['usage']
        total_tokens = usage['total_tokens']
        cost = (total_tokens / 1000) * cost_per_1000_tokens
        budget -= cost

        if budget < 0:
            raise Exception("Exceeded budget")

        print(f"Prompt tokens: {usage['prompt_tokens']}, Completion tokens: {usage['completion_tokens']}, Total tokens: {usage['total_tokens']}, Remaining budget: ${budget:.2f}")
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_extracted_info(extracted_info):
    info = {}
    for line in extracted_info.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            info[key.strip()] = value.strip()
    return info

@csrf_exempt
def loader_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        text = extract_text_from_pdf(file)
        extracted_info = extract_info_with_openai(text)
        parsed_info = parse_extracted_info(extracted_info)
        exam_result = ExamResult(**parsed_info)
        exam_result.save()
        return JsonResponse({'status': 'success', 'data': parsed_info})

    return render(request, 'loader_page.html')