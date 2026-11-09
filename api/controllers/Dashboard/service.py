# api/controllers/Dashboard/service.py
from domain.models import Product, ScheduledPost, GeneratedContent

def get_dashboard_stats(user):
    """
    User ke liye dashboard ki saari values calculate karta hai.
    """
    # Debugging ke liye print
    print(f"Checking stats for user: {user}")
    
    # 1. Total Products 
    user_products = Product.objects.filter(brand__user=user)
    
    total_products = user_products.count()
    
    # 2. Drafts
    drafts = user_products.filter(status__iexact='draft').count()
    if drafts == 0:
        drafts = user_products.filter(status__iexact='Draft').count()
    
    # 3. Generated Content 
    generated = GeneratedContent.objects.filter(product__in=user_products).count()
    
    # 4. Published, Scheduled, Pending (Schedule model)
    try:
        published = ScheduledPost.objects.filter(user=user, status='published').count()
        scheduled = ScheduledPost.objects.filter(user=user, status='scheduled').count()
        pending = ScheduledPost.objects.filter(user=user, status='pending').count()
    except Exception:
        published = ScheduledPost.objects.filter(product__brand__user=user, status='published').count()
        scheduled = ScheduledPost.objects.filter(product__brand__user=user, status='scheduled').count()
        pending = ScheduledPost.objects.filter(product__brand__user=user, status='pending').count()
    
    return {
        "total_products": total_products,
        "generated": generated,
        "published": published,
        "drafts": drafts,
        "pending": pending,
        "scheduled": scheduled,
    }