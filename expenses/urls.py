from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, ExpenseViewSet, MonthlySummaryView

router = DefaultRouter()
router.register('expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('summary/monthly/', MonthlySummaryView.as_view()),
    path('', include(router.urls)),
]
