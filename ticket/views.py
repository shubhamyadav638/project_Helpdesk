
import datetime
from django.shortcuts import render, redirect,reverse
from django.contrib import messages
from .models import Ticket
from .form import CreateTicketForm, UpdateTicketForm
from users.models import User
from django.contrib.auth.decorators import login_required

#view ticket details
@login_required()
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username = ticket.created_by)
    ticket_per_user = t.created_by.all()

    context = {
        'ticket': ticket, 'ticket_per_user':ticket_per_user,
    }
    return render(request, 'tickets/ticket_details.html', context)


#creating a ticket
@login_required()
def create_ticket(request):
    if request.method == "POST":
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = "Pending"
            var.save()
            messages.info(request, "Your ticket has been successfully submitted. An engineer would be assigned to your ticket shortly.")
            return redirect('dashboard')
        else:
            messages.warning(request, "Something went wrong. Please check form input.")
            return redirect("create-ticket")
    else:
        form = CreateTicketForm()
        context = {"form": form}
        return render(request, "tickets/create_ticket.html", context)


#updating a ticket
@login_required()
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved:
        if request.method == "POST":
            form = UpdateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request, "Your ticket has been successfully updated.")
                return redirect('dashboard')
            else:
                messages.warning(request, "Something went wrong. Please check form input.")
                return redirect("update-ticket", pk)
        else:
            form = UpdateTicketForm(instance=ticket)
            context = {"form": form}
            return render(request, "tickets/update_ticket.html", context)
    else:
        messages.info(request, "You cannot make any changes")
        return redirect('dashboard')
    
#viewing all created tickets
@login_required()
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by = request.user).order_by('-date_created')
    context = {'tickets': tickets}
    return render(request, 'tickets/all_ticket.html',context)


"""For engineers """
@login_required()
#view ticket queue
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = {
        'tickets': tickets,
    }
    return render(request, 'tickets/ticket_queue.html', context)

#accept ticket from the queue
@login_required()
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted. Please resolve as soon as possible.')
    return redirect('workspace')

#close the ticket
@login_required()
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been resolved. Thank you brilliant Support Engineer!')
    return redirect('ticket-queue')

#tickets engineer is working on
@login_required()
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {
        'tickets': tickets,
    }
    return render(request, 'tickets/workspace.html', context)

#all closed/resolved tickets
@login_required()
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {
        'tickets': tickets,
    }
    return render(request, 'tickets/all_closed_tickets.html', context)


# all engineering tickets
@login_required()
def all_engineer_tickets(request):
 tickets = Ticket.objects.all().order_by('-date_created')
 return render(request, 'tickets/all_engineer_tickets.html', {'tickets': tickets})


