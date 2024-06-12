from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExamResult
import fitz  # PyMuPDF
import openai
import os
from openai import OpenAI
from datetime import datetime

import re

# Initialize OpenAI API key
#openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key='sk-proj-4t9jDO68yI6C1EWJvZ5hT3BlbkFJhxV1SGq1c1SlgYxvIerX')


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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil que extrai informações de relatórios de exames médicos."},
                {"role": "user", "content": (
                    "Extraia as seguintes informações do texto."
                    "1. Nome do Paciente\n"
                    "2. Data de Nascimento\n"
                    "3. Data de Entrada\n"
                    "4. Material\n"
                    "5. Nome do Exame\n"
                    "6. Método\n"
                    "7. Resultado\n"
                    "8. Valor de Referência\n"
                    "9. Nota\n\n"
                    f"Texto:\n{text}\n\n"
                    "Informações Extraídas:"
                )}
            ],
            temperature=0.5,
        )

        response_message = response.choices[0].message.content
        print(response_message)
        return response_message.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def parse_extracted_info(extracted_info):
    # Split the extracted information into separate sets for each exam
    exam_sets = extracted_info.split('\n\n')
    
    # Initialize a list to store parsed information for each exam
    parsed_info_list = []
    
    # Parse each exam set
    for exam_set in exam_sets:
        info = {}
        for line in exam_set.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                info[key.strip()] = value.strip()
        parsed_info_list.append(info)
        print(parsed_info_list)
    
    return parsed_info_list
@csrf_exempt
def loader_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            try:
                text = extract_text_from_pdf(file)
                extracted_info = extract_info_with_openai(text)
                print('extracted info:', extracted_info)
                if extracted_info:
                    # Split the extracted information into separate sets for each exam
                    exam_sets = extracted_info.split('\n\n')

                    print(exam_sets)

                    for exam_set in exam_sets:
                        info = {}
                        for line in exam_set.split('\n'):
                            if ': ' in line:
                                key, value = line.split(': ', 1)
                                info[key.strip()] = value.strip()

                        print(info)

                        # Create ExamResult object and save to database
                        exam_result = ExamResult.objects.create(
                            name=info.get('1. Nome do Paciente', ''),
                            birth_date=datetime.strptime(info.get('2. Data de Nascimento', ''), '%d/%m/%Y').date(),
                            data_entrada=datetime.strptime(info.get('3. Data de Entrada', '').split('|')[0].strip(), '%d/%m/%Y').date(),
                            material=info.get('4. Material', ''),
                            exam_type=info.get('5. Nome do Exame', ''),
                            results=info.get('7. Resultado', ''),
                            method=info.get('6. Método', ''),
                            reference_value=info.get('8. Valor de Referência', ''),
                            note=info.get('9. Nota', '')
                        )
                        exam_result.save()
                    
                    return JsonResponse({'status': 'success', 'message': 'Exam results saved successfully'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Failed to extract information'})
            except Exception as e:
                print(f"Error processing PDF file: {e}")
                return JsonResponse({'status': 'error', 'message': 'Failed to process PDF file'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'})
    return render(request, 'loader_page.html')