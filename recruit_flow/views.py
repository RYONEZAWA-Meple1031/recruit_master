from django.shortcuts import render, get_object_or_404, redirect
from .models import Applicant, RecruitmentCost
from .forms import ApplicantForm
from django.db.models import Q, Sum  # Sumをインポート

# グラフ表示用
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUIを使わないバックエンドに変更

from django.shortcuts import render
from django.http import HttpResponse
import io
import urllib, base64

def applicant_list(request):

    # 検索クエリの取得
    name_query = request.GET.get('name', '')
    application_date_query = request.GET.get('application_date', '')
    application_route_query = request.GET.get('application_route', '')
    selection_phase_query = request.GET.get('selection_phase', '')
    selection_status_query = request.GET.get('selection_status', '')
    job_position_query = request.GET.get('job_position', '')
    region_query = request.GET.get('region', '')

    # 応募者リストの取得
    applicants = Applicant.objects.all()

    # 検索条件によるフィルタリング
    if name_query:
        applicants = applicants.filter(name__icontains=name_query)

    if application_date_query:
        applicants = applicants.filter(application_date=application_date_query)

    if application_route_query:
        applicants = applicants.filter(application_route__icontains=application_route_query)

    if selection_phase_query:
        applicants = applicants.filter(selection_phase=selection_phase_query)

    if selection_status_query:
        applicants = applicants.filter(selection_status=selection_status_query)

    if job_position_query:
        applicants = applicants.filter(job_position__icontains=job_position_query)

    if region_query:
        applicants = applicants.filter(region__icontains=region_query)


    # 総応募数の計算
    total_applicants = applicants.count()

    # 有効応募の計算
    # 選考フェーズが「書類選考, 1次面接, 2次面接, 内定」であり、
    # 選考ステータスが 0 (未処理) または 2 (選考NG) 以外
    valid_applicants = applicants.filter(
        selection_phase__in=[1, 2, 3, 4],  # 書類選考, 1次面接, 2次面接, 内定
        selection_status__in=[1, 3, 4, 5, 6, 7, 8]  # 未処理・選考NG以外
    ).count()

    # 有効応募率の計算 (総応募数が0の場合は0にする)
    if total_applicants > 0:
        valid_applicant_rate = (valid_applicants / total_applicants) * 100
    else:
        valid_applicant_rate = 0

    # 1次面接実施率
    first_interview_count = applicants.filter(first_interview_date__isnull=False).count()
    first_interview_rate = (first_interview_count / total_applicants * 100) if total_applicants > 0 else 0

    # 2次面接実施率
    second_interview_count = applicants.filter(second_interview_date__isnull=False).count()
    second_interview_rate = (second_interview_count / total_applicants * 100) if total_applicants > 0 else 0

    # 内定打診（通知）率
    offer_count = applicants.filter(offer_date__isnull=False).count()
    offer_rate = (offer_count / total_applicants * 100) if total_applicants > 0 else 0

    # 内定承諾率
    offer_acceptance_count = applicants.filter(offer_acceptance_date__isnull=False).count()
    offer_acceptance_rate = (offer_acceptance_count / total_applicants * 100) if total_applicants > 0 else 0

    # 採用費の合計を取得
    total_cost = RecruitmentCost.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # 採用一人単価を計算
    cost_per_hire = total_cost / offer_acceptance_count if offer_acceptance_count > 0 else 0

    # list.htmlへ渡す
    return render(request, 'recruit_flow/applicant_list.html', {
        'applicants': applicants,
        'total_applicants': total_applicants,
        'valid_applicants': valid_applicants,
        'valid_applicant_rate': valid_applicant_rate,
        'first_interview_rate': first_interview_rate,
        'second_interview_rate': second_interview_rate,
        'offer_rate': offer_rate,
        'offer_acceptance_rate': offer_acceptance_rate,
        'total_cost': total_cost,
        'cost_per_hire': cost_per_hire,
        'request': request,  # 検索フォームで利用するため
    })

def applicant_detail(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    return render(request, 'recruit_flow/applicant_detail.html', {'applicant': applicant})

def applicant_create(request):
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('applicant_list')
    else:
        form = ApplicantForm()
    return render(request, 'recruit_flow/applicant_form.html', {'form': form})

def applicant_edit(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant_list')
    else:
        form = ApplicantForm(instance=applicant)
    return render(request, 'recruit_flow/applicant_form.html', {'form': form})

def applicant_delete(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    applicant.delete()
    return redirect('applicant_list')

# グラフ表示
def applicant_graph(request):
    # グラフの作成
    plt.figure(figsize=(10, 6))
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
    plt.title("Sample Graph")

    # 画像を保存するためのバッファを作成
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    # テンプレートに画像を渡して表示
    return render(request, 'recruit_flow/graph.html', {'data': uri})