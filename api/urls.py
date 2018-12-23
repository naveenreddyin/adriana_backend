from django.urls import path


from api.views import LoadJSONDataApiView, ListTopicsApiView

urlpatterns = [
    path('load/', LoadJSONDataApiView.as_view(),
         name='load_json_file_api_view'),
    path('topic/',
         ListTopicsApiView.as_view(), 
         name='get_first_topic_api_view'),
    path('topic/<int:parent_id>/<str:text>/',
         ListTopicsApiView.as_view(), 
         name='get_by_parent_id_and_text_topic_api_view'),
]
