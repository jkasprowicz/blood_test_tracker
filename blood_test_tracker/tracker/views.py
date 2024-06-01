from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExamResult
import fitz  # PyMuPDF
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


def tracker_view(request):
    return render(request, 'enter_page.html')

def extract_text_from_pdf(file):
    text = ""
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def extract_info_with_openai(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Extraia essas informações do texto, levando em consideração que é um texto extraído de um laudo de exame:\n\n"
               f"1. Nome Paciente\n"
               f"2. Data de Nascimento\n"
               f"3. Material\n"
               f"4. Nome do Exame\n\n"
               f"5. Material\n\n"
               f"6. Resultado\n\n"
               f"7. Valor de Referência\n\n"
               f"8. Nota\n\n"
               f"Text:\n{text}\n\n"
               f"Extracted Information:\n",
        max_tokens=200,
        temperature=0.5
    )
    return response.choices[0].text.strip()

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
