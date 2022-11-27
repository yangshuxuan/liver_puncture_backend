from mangepicfudan.settings import BASE_DIR
from django.http import HttpResponseBadRequest,HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from pathology.models import Patient
from pathlib import PurePath
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_BREAK_TYPE, WD_UNDERLINE
from docx.shared import RGBColor,Pt
from docx.shared import Inches
from datetime import date
from io import BytesIO
from docx.oxml.ns import qn
from  django.http import HttpResponse
import re
from docxtpl import DocxTemplate
from django.utils.encoding import escape_uri_path


@login_required(login_url='/login/')
def protected_serve_patient(request, path, document_root=None, show_indexes=False):
    # patientId = request.GET.get("patient__id")
    patientId = str(PurePath(path).parent)
    if re.compile(r"\d+").fullmatch(patientId) is None:
        return HttpResponseBadRequest("<h3>非本病例剖验医生,无权查看</h3>")
    p = get_object_or_404(Patient, pk=patientId)
    if p.doctors.filter(id = request.user.id).exists():
        return serve(request, path, document_root, show_indexes)
    else:
        return HttpResponseForbidden("<h3>非本病例剖验医生,无权查看</h3>")

@login_required(login_url='/login/')
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)






@login_required(login_url='/login/')
def generateDocument(request):
    patientId = request.GET.get("patient__id")
    if patientId is None:
        return HttpResponseBadRequest("<h3>非本病例诊断医生,无权查看诊断报告</h3>")
    p = get_object_or_404(Patient, pk=patientId)
    # if p.doctors.filter(id = request.user.id).exists():
    docx_title=f"{p.name}诊断报告.docx"
    tpl = DocxTemplate(BASE_DIR / 'template.docx')

    context = {
        'name':p.name,
        'sex':p.sex,
        'age': p.age,
        'receive': p.receiveDate,
        'sampleNumber': p.sampleNumber,
        'hospital': p.hospital,
        'roomNumber':p.roomNumber,
        'bedNumber':p.bedNumber,
        'admissionNumber':p.admissionNumber,
        'microscopy':p.microscopy,
        'advice':p.advice,
        'receiveDate':p.receiveDate.strftime('%Y.%m.%d'),
        'reportDate':p.reportDate.strftime('%Y.%m.%d'),
        'doctors':f"{' '.join([ d.last_name+d.first_name for d in list(p.doctors.all())])}"
    }
    context = dict((k,context[k] if context[k] else "") for k in context)

    tpl.render(context,autoescape=True)
    


    

    # Prepare document for download        
    # -----------------------------
    f = BytesIO()
    tpl.save(f)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename={escape_uri_path(docx_title)}'
    response['Content-Length'] = length
    return response
    # else:
    #     return HttpResponseForbidden("<h3>非本病例剖验医生,无权查看</h3>")
