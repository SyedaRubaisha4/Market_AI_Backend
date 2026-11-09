# api/controllers/Social/Facebook/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils import timezone
from socialchimp.platform import ChooseAccount, Finished
from domain.models.Brand import Brand
from domain.models.SocialConnect import SocialConnect
from domain.models import User as DomainUser  
from .service import start_facebook_login, process_facebook_callback, choose_facebook_page
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from domain.models import SocialConnect
@login_required
def connect_facebook(request):
    if request.method == "GET":
        brands = Brand.objects.filter(user=request.user)
        csrf_token = request.COOKIES.get('csrftoken', '')
        
        # Simple HTML for testing
        html = "<h2>Select Brand to connect Facebook:</h2><form method='POST'>"
        html += f"<input type='hidden' name='csrfmiddlewaretoken' value='{csrf_token}' />"
        
        if not brands:
            html += "<p>No brands found. Create one in Admin.</p>"
        else:
            for brand in brands:
                html += f"<button type='submit' name='brand_id' value='{brand.id}' style='margin:10px; padding:5px;'>{brand.business_name}</button><br>"
        html += "</form>"
        return HttpResponse(html)
    
    request.session["pending_brand_id"] = request.POST.get("brand_id")
    step = start_facebook_login(request.user.pk)
    
    request.session["fb_state"] = step.state
    request.session["fb_remember"] = step.remember
    return redirect(step.url)

@login_required
def callback_facebook(request):
    # Check if user cancelled or an error occurred
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseBadRequest("<h2>Facebook Login Failed or Cancelled. Try again.</h2>")

    step = process_facebook_callback(
        callback_data=request.GET.dict(),
        state=request.session.get("fb_state"),
        remember=request.session.get("fb_remember")
    )

    # Facebook always prompts for Page selection
    if isinstance(step, ChooseAccount):
        request.session["fb_resume_token"] = step.resume_token
        csrf_token = request.COOKIES.get('csrftoken', '')
        
        html = "<h2>Select Facebook Page:</h2>"
        html += f"<form method='POST' action='/api/social/facebook/choose/'><input type='hidden' name='csrfmiddlewaretoken' value='{csrf_token}' />"
        for option in step.options:
            html += f"<button type='submit' name='account_id' value='{option.id}' style='margin:10px; padding:5px;'>Page: {option.name}</button><br>"
        html += "</form>"
        return HttpResponse(html)

    return redirect("social-connect-success")

@login_required
def choose_page_facebook(request):
    step = choose_facebook_page(
        account_id=request.POST["account_id"],
        resume_token=request.session.pop("fb_resume_token"),
        state=request.session.get("fb_state"),
        remember=request.session.get("fb_remember")
    )

    if isinstance(step, Finished):
        brand_id = request.session.pop("pending_brand_id", None)
        
        conn = SocialConnect.objects.filter(platform="facebook", user__isnull=True).order_by("-id").first()
        
        if conn:
            actual_user = None
            
            # 1. First try to match email
            if hasattr(request.user, 'email') and request.user.email:
                actual_user = DomainUser.objects.filter(email=request.user.email).first()
            
            # 2. If email do not find then match with username 
            if not actual_user and hasattr(request.user, 'username'):
                actual_user = DomainUser.objects.filter(name=request.user.username).first()
                
            # 3.If still user not found , pick the first one 
            if not actual_user:
                actual_user = DomainUser.objects.first()

            if actual_user:
                conn.user = actual_user
                if brand_id:
                    conn.brand_id = brand_id
                    
                conn.connected_at = timezone.now()
                conn.save()
                print(f" Connection saved with DomainUser: {actual_user}")
            else:
                print("There is no domain user in database .")

        return redirect("social-connect-success")

    return HttpResponseBadRequest("Unexpected step.")

@login_required
def connect_success(request):
        return redirect("http://localhost:5173/social-accounts")

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_get_social_accounts(request):
    try:
        accounts = SocialConnect.objects.filter(user=request.user, connection_status='Connected')
        
        data = []
        for acc in accounts:
            data.append({
                "platform": acc.platform,
                "connected": True,
                "accountName": acc.platform_account_id or acc.platform.capitalize(),
                "identifier": acc.platform_account_id,
            })
            
        return Response({"success": True, "accounts": data}, status=200)
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=500)
