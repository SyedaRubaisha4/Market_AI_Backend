# api/controllers/Social/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from socialchimp.platform import ChooseAccount, Finished
from domain.models.Brand import Brand

# Import functions from service.py
from .service import (
    start_facebook_login,
    process_facebook_callback,
    complete_facebook_connection
)

@login_required
def connect_facebook(request):
    if request.method == "GET":
        brands = Brand.objects.filter(user=request.user)
        return render(request, "social/select_brand.html", {"brands": brands})
    
    # Save brand_id in session
    request.session["pending_brand_id"] = request.POST.get("brand_id")

    # Call service to start login
    step = start_facebook_login(request.user.pk)
    
    # Save state in session
    request.session["fb_state"] = step.state
    request.session["fb_remember"] = step.remember
    
    return redirect(step.url)

@login_required
def callback_facebook(request):
    # Call service to process callback
    step = process_facebook_callback(
        callback_data=request.GET.dict(),
        state=request.session.get("fb_state"),
        remember=request.session.get("fb_remember")
    )

    if isinstance(step, ChooseAccount):
        request.session["fb_resume_token"] = step.resume_token
        return render(request, "social/pick_page.html", {"options": step.options})

    return redirect("social-connect-success")

@login_required
def choose_facebook_page(request):
    brand_id = request.session.pop("pending_brand_id", None)
    
    # Call service to complete connection
    step = complete_facebook_connection(
        account_id=request.POST["account_id"],
        resume_token=request.session.pop("fb_resume_token"),
        state=request.session.get("fb_state"),
        remember=request.session.get("fb_remember"),
        user=request.user,
        brand_id=brand_id
    )

    return redirect("social-connect-success")

@login_required
def connect_success(request):
    return render(request, "social/success.html")