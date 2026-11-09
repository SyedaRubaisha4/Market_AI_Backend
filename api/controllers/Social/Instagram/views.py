# api/controllers/Social/Instagram/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils import timezone
from socialchimp.platform import ChooseAccount, Finished
from domain.models.Brand import Brand
from domain.models.SocialConnect import SocialConnect
from domain.models import User as DomainUser
from .service import start_instagram_login, process_instagram_callback, choose_instagram_account

@login_required
@login_required
def connect_instagram(request):
    brand_id = request.GET.get('brand_id')
    
    if not brand_id:
        brand = Brand.objects.filter(user=request.user).first()
        if brand:
            brand_id = brand.id
            
    if not brand_id:
        return HttpResponseBadRequest("<h2>No Brand found. Please create a brand first.</h2>")

    request.session["pending_brand_id"] = brand_id
    
    step = start_instagram_login(request.user.pk)
    
    request.session["ig_state"] = step.state
    request.session["ig_remember"] = step.remember
    return redirect(step.url)
@login_required
def callback_instagram(request):
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseBadRequest("<h2>Instagram Login Failed or Cancelled. Try again.</h2>")

    step = process_instagram_callback(
        callback_data=request.GET.dict(),
        state=request.session.get("ig_state"),
        remember=request.session.get("ig_remember")
    )
    if isinstance(step, ChooseAccount):
        request.session["ig_resume_token"] = step.resume_token
        csrf_token = request.COOKIES.get('csrftoken', '')
        
        html = "<h2>Select Instagram/Facebook Page:</h2>"
        html += f"<form method='POST' action='/api/social/instagram/choose/'><input type='hidden' name='csrfmiddlewaretoken' value='{csrf_token}' />"
        for option in step.options:
            html += f"<button type='submit' name='account_id' value='{option.id}' style='margin:10px; padding:5px;'>Page: {option.name}</button><br>"
        html += "</form>"
        return HttpResponse(html)
    
    elif isinstance(step, Finished):
        save_instagram_connection(request, step)
        return redirect("ig-success")

    return HttpResponseBadRequest("Unexpected step.")

@login_required
def choose_page_instagram(request):
    step = choose_instagram_account(
        account_id=request.POST["account_id"],
        resume_token=request.session.pop("ig_resume_token"),
        state=request.session.get("ig_state"),
        remember=request.session.get("ig_remember")
    )

    if isinstance(step, Finished):
        save_instagram_connection(request, step)
        return redirect("ig-success")

    return HttpResponseBadRequest("Unexpected step.")

def save_instagram_connection(request, step):
    """Database mein user aur brand attach karne ka helper function"""
    brand_id = request.session.pop("pending_brand_id", None)
    
    conn = SocialConnect.objects.filter(platform="instagram", user__isnull=True).order_by("-id").first()
    
    if conn:
        actual_user = None
        if hasattr(request.user, 'email') and request.user.email:
            actual_user = DomainUser.objects.filter(email=request.user.email).first()
        if not actual_user and hasattr(request.user, 'username'):
            actual_user = DomainUser.objects.filter(name=request.user.username).first()
        if not actual_user:
            actual_user = DomainUser.objects.first()

        if actual_user:
            conn.user = actual_user
            if brand_id:
                conn.brand_id = brand_id
            conn.connected_at = timezone.now()
            conn.save()
            print(f" Instagram Connection saved with DomainUser: {actual_user}")

@login_required
def connect_success(request):
    return HttpResponse("<h2>Instagram Connected Successfully!</h2><p>Check database.</p>")