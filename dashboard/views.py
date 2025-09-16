from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render
from django.http import JsonResponse

from activities.models.activity import Activity
from users.models.user import User


@login_required
def home(request):
    # KPI básicos (MVP sin periodos aún)
    leaderboard = (
        User.objects.filter(is_active=True)
        .annotate(total_points=Sum(F('activity__activity_type__points')))
        .order_by('-total_points')
    )

    my_points = (
        Activity.objects.filter(user=request.user)
        .aggregate(total=Sum(F('activity_type__points')))
        .get('total')
        or 0
    )

    my_activities_count = Activity.objects.filter(user=request.user).count()

    recent_activities = (
        Activity.objects.select_related('activity_type', 'user')
        .order_by('-created_at')[:10]
    )

    context = {
        'leaderboard': leaderboard,
        'my_points': my_points,
        'my_activities_count': my_activities_count,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard.html', context)


@login_required
def kpis(request):
    total_points = (
        Activity.objects.aggregate(total=Sum(F('activity_type__points'))).get('total')
        or 0
    )
    my_points = (
        Activity.objects.filter(user=request.user)
        .aggregate(total=Sum(F('activity_type__points')))
        .get('total')
        or 0
    )
    my_activities = Activity.objects.filter(user=request.user).count()
    return JsonResponse({
        'total_points': total_points,
        'my_points': my_points,
        'my_activities': my_activities,
    })
