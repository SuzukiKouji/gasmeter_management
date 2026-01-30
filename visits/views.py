from django.shortcuts import render, get_object_or_404, redirect
from .models import VisitRecord, Photo
from customers.models import Customer
from django.db.models import OuterRef, Subquery
import csv

def unresolved_cases(request):

    # ▼ CSVアップロード処理（DictReader 方式 + 重複スキップ）
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        # ▼ Excel の CSV（UTF-8 with BOM）を正しく読み込む
        decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            name = row.get("name", "").strip()
            address1 = row.get("address1", "").strip()

            # ▼ 必須チェック（name または address1 が空ならスキップ）
            if not name or not address1:
                continue

            # ▼ 重複チェック（name + address1 が一致したらスキップ）
            exists = Customer.objects.filter(
                name=name,
                address1=address1
            ).exists()

            if exists:
                continue  # ← 既存なら何もせずスキップ

            # ▼ 新規のみ作成
            Customer.objects.create(
                name=name,
                address1=address1,
                address2=row.get("address2", "").strip(),
                address3=row.get("address3", "").strip(),
                tel=row.get("tel", "").strip(),
                meter_location=row.get("meter_location", "").strip(),
                usage_code=row.get("usage_code", "").strip(),
                excess_category=row.get("excess_category", "").strip()
            )

        return redirect("unresolved_cases")

    # ▼ 通常の一覧表示
    customers = Customer.objects.all()  # ← 本当は未済だけに絞る

    # ▼ ステータスの日本語ラベル
    STATUS_LABELS = {
        'done': '完了',
        'pending': '未完了',
    }

    # ▼ 各顧客に最新ステータスを付与
    for customer in customers:
        latest_record = customer.visit_records.order_by('-visit_date').first()

        if latest_record:
            customer.latest_status = STATUS_LABELS.get(latest_record.status, '未記録')
        
        else:
            customer.latest_status = '未記録'

    return render(request, 'visits/unresolved_cases.html', {
        'customers': customers
    })


# ▼ 追加：顧客削除ビュー
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect("unresolved_cases")


def customer_detail(request, customer_id):  # ← customer_id を受け取る
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'visits/customer_detail.html', {
        'customer': customer
    })


def visit_record(request, customer_id):  # ← customer_id を受け取る
    customer = get_object_or_404(Customer, id=customer_id)

    # ▼ 中段に表示する過去訪問記録
    records = VisitRecord.objects.filter(customer=customer).order_by('-visit_date')

    if request.method == 'POST':
        print("POST内容:", request.POST)
        # ▼ VisitRecord を保存（モデルに存在するフィールドだけ）
        record = VisitRecord.objects.create(
            customer=customer,
            user=request.user,
            visit_date=request.POST.get('visit_date'),
            status=request.POST.get('status'),
            memo=request.POST.get('memo'),
        )

        # ▼ 写真を保存
        if 'photo' in request.FILES:
            Photo.objects.create(
                visit_record=record,
                file_path=request.FILES['photo']
            )

        # 保存後も同じ画面に戻る（中段に追加されて見える）
        return redirect('visit_record', customer_id=customer.id)

    return render(request, 'visits/visit_record.html', {
        'customer': customer,
        'records': records,
    })


# ▼ 地図表示用
def customer_map(request):
    latest_visit = VisitRecord.objects.filter(
        customer=OuterRef('pk')
    ).order_by('-visit_date')

    customers = Customer.objects.annotate(
        latest_status=Subquery(latest_visit.values('status')[:1])
    ).exclude(
        latitude__isnull=True,
        longitude__isnull=True
    )

    return render(request, 'visits/customer_map.html', {
        'customers': customers
    })