from django.shortcuts import render,get_object_or_404, redirect
from .models import datab , datab2
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.db.models import Q
import pytesseract
from django.contrib import messages
import cv2
from pytesseract import Output
from django.conf import settings
from pathlib import Path
import os


#pytesseract.pytesseract.tesseract_cmd = r"C:\Users\RAD 177\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def highlight_text_in_image(image_path, keywords, output_path):
    color = (0, 0, 255)  
    padding =3  
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Could not load image from path'{image_path}'. Please check the file path.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    d = pytesseract.image_to_data(thresh, output_type=Output.DICT)
    
    n_boxes = len(d['text'])
    highlighted = False
    
    keyword_list = keywords.lower().split()

    for i in range(n_boxes):
        word_in_image = d['text'][i].strip().lower()
    
        if any(keyword in word_in_image for keyword in keyword_list):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            x -= padding
            y -= padding
            w += 2*padding
            h += 2*padding

            img = cv2.rectangle(img, (x, y), (x + w, y + h),color,2)
            highlighted = True

    cv2.imwrite(output_path, img)

    return output_path

STOP_WORDS = set([
    "i","me","my","myself", "we", "our", "ours", "ourselves", "you", "your", 
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", 
    "these", "those", "am","is", "are", "was", "were", "be", "been", "being", 
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
    "the", "and", "but","if", "or","because", "as", "until", "while", "of", 
    "at", "by", "for", "with", "about", "against", "between", "into", "through", 
    "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", 
    "once", "here", "there", "when", "where", "why", "how", "all", "any", 
    "both", "each", "few", "more", "most", "other", "some", "such", "no", 
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", 
    "t", "can", "will", "just","don","should","now"
])
ALPHABETS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def remove_stop_words(text):
    words=text.split()
    filtered_words =[word for word in words if word.lower() not in STOP_WORDS and word.isalnum()]
    return ' '.join(filtered_words)


def login_fun(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        password = request.POST.get('psw')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('imageUpload') 
        else:
            messages.error(request,"Invalid Username or Password")
    return render(request,"login.html")

@login_required(login_url = 'login')

def imageUpload(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        image=request.FILES.get('image')
        jn = request.POST.get('jn')
        vn = request.POST.get('vn')
        sn = request.POST.get('sn')
        my = request.POST.get('my')

        if title and image:
            try:
                doc=datab.objects.create(title=title,image=image,jn=jn,vn=vn,sn=sn,my=my)

                image=Image.open(doc.image)

                content=pytesseract.image_to_string(image)

                filtered_text=remove_stop_words(content)

                doc.content=filtered_text
                doc.save()

                messages.success(request,'Uploaded successfully')

            except Exception as e:
                messages.error(request,f'Not Uploaded: {e}')

        else:
            messages.error(request,'Title and image are required')

    count_file = os.path.join(settings.MEDIA_ROOT, 'data', 'count_viewers.txt')

    if not os.path.exists(count_file):
            with open(count_file,'w') as file:
                file.write('0')

    with open(count_file,'r') as file:
        count = int(file.read())
  
    return render(request,'upload.html',{'count':count})


def search_view(request):
    query = request.GET.get('q','')
    show = request.GET.get('pdfs','')
    keyword = query
    years = None
    matches = []

    if query and query not in STOP_WORDS and query.lower() not in ALPHABETS:
        matches = datab.objects.filter(content__icontains=query)
    else:
        matches = []

    if show:
        all_records = datab2.objects.order_by('-year')
        seen_years = set()
        years = []
        for record in all_records:
            if record.year not in seen_years:
                years.append(record)
                seen_years.add(record.year)

    count_file = os.path.join(settings.MEDIA_ROOT,'data','count_viewers.txt')
    os.makedirs(os.path.dirname(count_file),exist_ok = True)

    try:
        with open(count_file,'r') as file:
            count = int(file.read())
    except FileNotFoundError:
        count = 0
    except ValueError:
        count = 0

    count += 1 

    with open(count_file, 'w') as file:
        file.write(str(count)) 

    return render(request, 'search.html',{'results': matches,'query':query, 'years':years})


def image_detail(request, id):
    image = get_object_or_404(datab, id=id)
    keyword = request.GET.get('keyword', '')

    highlight_path = Path(settings.MEDIA_ROOT)/f"highlighted_images/highlight_img_.jpg"
    
    output_path = highlight_text_in_image(image.image.path,keyword,str(highlight_path))
    
    relative_path = highlight_path.relative_to(settings.MEDIA_ROOT)
    highlighted_image_url = f"{settings.MEDIA_URL}{relative_path}"

    return render(request, 'image_detail.html',{'highlighted_image_url': highlighted_image_url, 'image' : image})


def year_fun(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        pdf = request.FILES.get('pdf')
        if year and pdf:
            try:
                doc2 = datab2.objects.create(year=year,pdf=pdf)
                doc2.save()
                messages.success(request,"Uploaded successfully")    
            except Exception as e:
                messages.error(request,f"Not uploaded{e}")
            
        else:
            messages.error(request,"File not found")

    return render(request,'upload_year.html')