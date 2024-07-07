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
client = openai.OpenAI(api_key='')

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
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil que extrai todas as informações de relatórios de exames médicos, cada analito deve ter seu resultado!"},
                {"role": "user", "content": (
                    "Extraia as seguintes informações do texto.\n"
                    "1. Nome do Paciente\n"
                    "2. Data de Nascimento\n"
                    "3. Data de Entrada\n"
                    "4. Material\n"
                    "5. Nome do Exame\n"
                    "6. Método\n"
                    "7. Resultado\n"
                    "8. Valor de Referência, ou Valores de Referência ou Intervalo de Referência\n"
                    "9. Nota\n\n"
                    f"Texto:\n{text}\n\n"
                    "Informações Extraídas:"
                )}
            ],
            temperature=0.5,
        )
        response_message = response.choices[0].message.content
        return response_message.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def parse_extracted_info(extracted_info):
    exam_sets = extracted_info.split('\n\n')
    parsed_info_list = []

    for exam_set in exam_sets:
        info = {}
        current_key = None
        for line in exam_set.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                if key.strip().startswith('8. Valor de Referência'):
                    current_key = key.strip()
                    info[current_key] = value.strip()
                else:
                    info[key.strip()] = value.strip()
                    current_key = key.strip()
            else:
                if current_key:
                    info[current_key] += f"\n{line.strip()}"
        parsed_info_list.append(info)

    return parsed_info_list

@csrf_exempt
def loader_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            try:
                text = extract_text_from_pdf(file)
                print(f"Extracted text: {text}")

                extracted_info = extract_info_with_openai(text)
                print(f"Extracted info from OpenAI: {extracted_info}")

                if extracted_info:
                    parsed_info_list = parse_extracted_info(extracted_info)
                    print(f"Parsed info list: {parsed_info_list}")

                    for info in parsed_info_list:
                        # Create ExamResult object for each exam
                        reference_value = info.get('8. Valor de Referência', '')
                        for key in list(info.keys()):
                            if key.startswith('- '):
                                reference_value += f"\n{key} {info.pop(key)}"

                        exam_result = ExamResult(
                            name=info.get('1. Nome do Paciente', ''),
                            birth_date=datetime.strptime(info.get('2. Data de Nascimento', ''), '%d/%m/%Y').date(),
                            data_entrada=datetime.strptime(info.get('3. Data de Entrada', '').split('|')[0].strip(), '%d/%m/%Y').date(),
                            material=info.get('4. Material', ''),
                            exam_type=info.get('5. Nome do Exame', ''),
                            results=info.get('7. Resultado', ''),
                            method=info.get('6. Método', ''),
                            reference_value=reference_value.strip(),
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

