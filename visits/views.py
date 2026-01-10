from django.shortcuts import render, get_object_or_404, redirect
from .models import VisitRecord, Photo
from customers.models import Customer

def unresolved_cases(request): 
    customers = Customer.objects.all() # ← 本当は未済だけに絞る 
    return render(request, 'visits/unresolved_cases.html', { 
        'customers': customers })

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
        # ▼ VisitRecord を保存
        record = VisitRecord.objects.create(
            customer=customer,
            user=request.user,
            visit_date=request.POST.get('visit_date'),
            status=request.POST.get('status'),
            inspection_due_date=request.POST.get('inspection_due_date'),
            value_status=request.POST.get('value_status'),
            current_model=request.POST.get('current_model'),
            current_serial_number=request.POST.get('current_serial_number'),
            reason=request.POST.get('reason'),
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