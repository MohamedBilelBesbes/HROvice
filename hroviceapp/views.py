from django.db.models.fields import DateField
from django.forms.widgets import DateInput
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Intern, Attestation
import datetime
from fpdf import FPDF
import os
from pathlib import Path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes

at = 'Internship Attestation'
class PDF(FPDF):
  def header(self):
    self.image('media//ovicelogo.png', 10, 8, 25)
    self.set_font('courier', '', 8)
    self.set_text_color(169, 169, 169)
    #self.cell(0, 5, str(dateofsign)[:10], align='R')
    self.cell(0, 5, 'oVice.Inc', align='R')
    self.set_font('helvetica', '', 20)
    self.cell(0, 5, ' ', ln=True)
    self.cell(0, 5, ' ', ln=True)
    self.cell(0, 5, ' ', ln=True)
    self.set_text_color(158, 18, 18)
    title_w = self.get_string_width(at)
    doc_w = self.w
    self.set_x((doc_w - title_w) / 2)
    
    self.cell(0, 10, at, border=False, ln=True)
    self.ln(20)
  def footer(self):
    self.set_y(-32)
    self.set_draw_color(103, 103, 252)
    self.line(10, 243, 210, 243)
    self.set_draw_color(243, 34, 34)
    self.line(20, 244, 200, 244)
    self.set_text_color(14, 14, 243)
    with open('media//englishfooter.txt', 'rb') as ft:
      engtxt = ft.read().decode()
    with open('media//japanesefooter.txt', 'rb') as ft:
      japtxt = ft.read().decode()
    self.add_font('fireflysung', '', 'media//fireflysung.ttf', uni=True)
    self.set_font('fireflysung', '', 10)
    self.multi_cell(0, 5, japtxt, ln = True, align='C')
    self.set_font('courier', '', 11)
    self.multi_cell(0, 5, engtxt, ln = True, align='C')
    self.set_text_color(169, 169, 169)
    self.set_font('helvetica', 'I', 10)
    self.cell(0, 20, f'Page {self.page_no()}/{{nb}}', align='C')
  def chapter_body(self, filename, signer, name, school, cin, title, dateinit, dateend, dateofsign):
    with open(filename, 'rb') as fh:
      txt = fh.read().decode('latin-1')
    self.set_font('times', '', 12)
    self.multi_cell(0, 7, txt.format(signer, name, school, cin, title, str(dateinit)[:10], str(dateend)[:10]))
    self.ln()
    issued = 'This certificate is issued to the interested party to serve and make what is right.'
    self.set_font('times', 'B', 13)
    self.cell(0, 7, issued)
    self.set_font('times', 'I', 12)
    self.ln()
    self.cell(0, 15, ' ', ln=True)
    self.cell(0, 5, '--------------------', ln=True)
    self.cell(0, 5, ' ', ln=True)
    self.set_font('times', 'I', 15)
    self.cell(0, 5, 'The direction', ln=True)
    self.ln()
    self.cell(0, 5, 'Monastir, ' + str(dateofsign)[:10])

def index(request):
    return render(request, 'hrovice/index.html')

# Create your views here.

# User Class CRUD with login


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'{username}, your account was created successfully, you just need to login')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'hrovice/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'hrovice/profile.html')


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'hrovice/edit_profile.html', args)


@login_required()
def delete_user(request, pk):
    user = User.objects.filter(username=pk)
    user.delete()
    return redirect('index')

# Intern Class CRUD


@login_required()
def create_intern(request):
    if request.method == 'POST':

        name = str(request.POST.get('name'))
        cin = int(request.POST.get('cin'))
        email = str(request.POST.get('email'))
        phonenumber = int(request.POST.get('phonenumber'))
        school = str(request.POST.get('school'))

        intern = Intern.objects.create(
            name=name,
            cin=cin,
            email=email,
            phonenumber=phonenumber,
            school=school,
            )
        return redirect('display_interns')
    return render(request, 'intern/create_intern.html')


@login_required()
def display_interns(request):
    interns = Intern.objects.all()
    args = {'interns': interns}
    return render(request, 'intern/display_interns.html', args)


@login_required()
def display_intern(request, pk):
    intern = Intern.objects.get(pk=pk)
    args = {'intern': intern}
    return render(request, 'intern/display_intern.html', args)


@login_required()
def edit_intern(request, idintern):
    if request.method == 'POST':
        intern = Intern.objects.filter(pk=idintern)
        name = str(request.POST.get('name'))
        cin = int(request.POST.get('cin'))
        email = str(request.POST.get('email'))
        phonenumber = int(request.POST.get('phonenumber'))
        school = str(request.POST.get('school'))
        intern.update(
            name=name,
            cin=cin,
            email=email,
            phonenumber=phonenumber,
            school=school,
            )
        return redirect('index')
    else:
        intern = Intern.objects.get(pk=idintern)

        args = {'intern': intern}

    return render(request, 'intern/edit_intern.html', args)


@login_required()
def delete_intern(request, pk):
    intern = Intern.objects.filter(pk=pk)
    intern.delete()
    return redirect('index')

# Attestation CRUD


@login_required()
def create_attestation(request, owner):
    if request.method == 'POST':
        intern = Intern.objects.filter(pk=owner).first()
        dateinit = datetime.datetime.strptime(
            request.POST.get('dateinit'), '%Y-%m-%d')
        dateend = datetime.datetime.strptime(
            request.POST.get('dateend'), '%Y-%m-%d')
        title = str(request.POST.get('title'))
        signer = str(request.POST.get('signer'))
        dateofsign = datetime.datetime.strptime(
            request.POST.get('dateofsign'), '%Y-%m-%d')

        attestation = Attestation.objects.create(
            intern=intern,
            dateinit=dateinit,
            dateend=dateend,
            title=title,
            signer=signer,
            dateofsign=dateofsign,
            )
        return redirect('display_intern', pk=intern.pk)
    intern = Intern.objects.filter(pk=owner).first()
    args = {'intern': intern}
    return render(request, 'attestation/create_attestation.html', args)


@login_required()
def display_user_attestations(request, owner):
    intern = Intern.objects.filter(pk=owner).first()
    attestations = Attestation.objects.filter(intern=owner)
    args = {'attestations': attestations, 'intern': intern}
    return render(request, 'attestation/display_user_attestations.html', args)


@login_required()
def display_attestation(request, pk):
    attestation = Attestation.objects.filter(pk=pk).first()
    args = {'attestation': attestation}
    return render(request, 'attestation/display_attestation.html', args)


@login_required()
def edit_attestation(request, idattestation):
    if request.method == 'POST':
        attestation = Attestation.objects.filter(pk=idattestation)
        dateinit = datetime.datetime.strptime(
            request.POST.get('dateinit'), '%Y-%m-%d')
        dateend = datetime.datetime.strptime(
            request.POST.get('dateend'), '%Y-%m-%d')
        title = str(request.POST.get('title'))
        signer = str(request.POST.get('signer'))
        dateofsign = datetime.datetime.strptime(
            request.POST.get('dateofsign'), '%Y-%m-%d')
        attestation.update(
            dateinit=dateinit,
            dateend=dateend,
            title=title,
            signer=signer,
            dateofsign=dateofsign,
            )
        return redirect('display_attestation', pk=attestation.first().pk)
    else:
        attestation = Attestation.objects.filter(pk=idattestation).first()
        dateinit = str(attestation.dateinit)
        dateend = str(attestation.dateend)
        dateofsign = str(attestation.dateofsign)
        args = {'attestation': attestation, 'dateinit': dateinit,
            'dateend': dateend, 'dateofsign': dateofsign}

    return render(request, 'attestation/edit_attestation.html', args)


@login_required()
def delete_attestation(request, pk):
    attestation = Attestation.objects.filter(pk=pk).first()
    intern = attestation.intern
    attestation.delete()
    return redirect('display_user_attestations', owner=intern.pk)


@login_required()
def make_attestation(request, pk):
    attestation = Attestation.objects.filter(pk=pk).first()
    intern = attestation.intern
    dateinit = attestation.dateinit
    dateend = attestation.dateend
    dateofsign = attestation.dateofsign
    title = attestation.title
    signer = attestation.signer
    name = intern.name
    school = intern.school
    cin = intern.cin
    at = 'Internship Attestation'
    pdf = PDF('P','mm','Letter')
    pdf.add_page()
    pdf.alias_nb_pages()
    pdf.chapter_body('media//content.txt', signer, name, school, cin, title, dateinit, dateend, dateofsign)
    media_root = os.path.join(Path(__file__).resolve().parent.parent, 'media')
    filepath = 'media' + '//attestation_'+str(attestation.pk)+'_intern_'+str(intern.pk)+'.pdf'
    thefile = filepath
    filename = os.path.basename(thefile)
    print('--------')
    print(filename)
    print('--------')
    pdf.output(filename)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),
      content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s" % filename
    return response
