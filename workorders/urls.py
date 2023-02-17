from django.urls import path
from . import views

urlpatterns = [
    path("admin_home/", views.admin_home, name="admin_home"),
    path("client_home/", views.client_home, name="client_home"),
    path("client/show_order/<work_order_id>/", views.show_order, name="show_order_client"),
    path("admin/show_order/<work_order_id>/", views.show_order, name="show_order_admin"),
    path("client/add_order/", views.add_order, name="add_order"),  # only client can add the orders
    path("client/delete_order/<work_order_id>/", views.delete_order, name="delete_order"),  # only client have the authority to delete the orders..
    path("client/update_order/<work_order_id>/", views.update_order, name="update_order"),
    path("client/search_order/", views.search_order, name="search_order_client"),
    path("admin/search_order/", views.search_order, name="search_order_admin"),
    path("admin/make_bill/<work_order_id>/", views.make_bill, name="make_bill"),
    path("admin/all_bills/", views.all_bill, name="all_bill"),
    path("admin/delete_bill/<bill_id>/", views.delete_bill, name="delete_bill"),
    path("admin/update_bill/<bill_id>/", views.update_bill, name="update_bill"),
    path("admin/download_order/",views.download_order,name="admin_download_order"),
    path("client/download_order/",views.download_order,name="client_download_order"),
    path("admin/download_bill/",views.download_bill,name='download_bill'),
    path("admin/reject_order/<work_order_id>/",views.reject_order,name='reject_order'),
    path("admin/unreject_order/<work_order_id>",views.unreject_order,name='unreject_order'),
]
