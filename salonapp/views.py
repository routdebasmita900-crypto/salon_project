from django.shortcuts import render, redirect,get_object_or_404
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from . models import Customer,Service,Appointment
from django.db.models import Sum
from datetime import date
from django.core.paginator import Paginator

def home(request):
    form = AppointmentForm()
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'home.html', {'form': form})


@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()

    # Search filter
    query = request.GET.get('q')
    if query:
        appointments = appointments.filter(customer__name__icontains=query)

    # Status filter
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)

    # Date filter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
     appointments = appointments.filter(
            date__range=[start_date, end_date]
        )
    paginator = Paginator(appointments, 5)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    context = {
        'appointments': appointments
    }

    return render(request,'appointment_list.html',context)
   
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('appointments')
def update_status(request, id, status):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = status
    appointment.save()
    return redirect('appointments')
from .models import Customer, Service, Appointment

@login_required

def dashboard(request):
    if not request.user.is_superuser:
        return redirect('/login/')
   
    total_customers = Customer.objects.count()
    total_services = Service.objects.count()
    total_appointments = Appointment.objects.count()
    total_revenue = Appointment.objects.filter(
           status="Completed").aggregate(total=Sum('price'))['total'] or 0
    completed = Appointment.objects.filter(status='Completed').count()
    pending = Appointment.objects.filter(status='Pending').count()
    cancelled=Appointment.objects.filter(status='Cancelled').count()
    today_appointments=Appointment.objects.filter(date=date.today()).count()

    context = {
        'total_customers': total_customers,
        'total_services': total_services,
        'total_appointments': total_appointments,
        'completed': completed,
        'pending': pending,
        'cancelled':cancelled,
        'total_revenue':total_revenue,
        'today_appointments':today_appointments,
    }

    return render(request, 'dashboard.html', context)
def mark_completed(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = 'Completed'
    appointment.save()
    return redirect('appointment_list')
def mark_cancelled(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = 'Cancelled'
    appointment.save()
    return redirect('appointment_list')

def complete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = "Completed"
    appointment.save()
    return redirect('appointments')   # name check kar lena

def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = "Cancelled"
    appointment.save()
    return redirect('appointments')