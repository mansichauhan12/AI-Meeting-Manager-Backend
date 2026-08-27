from django.urls import path
from .views import SemanticSearchView, AskQuestionView

urlpatterns = [
    path('', SemanticSearchView.as_view(), name='semantic_search'),
    path('ask/', AskQuestionView.as_view(), name='ask_question'),
]
