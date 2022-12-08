from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='Logout'),
    path('Dashboard/', views.dashboard, name='Dashboard'),
    path('addEmployee/', views.addEmployee, name='AddEmployee'),
    path('viewEmployee/', views.viewEmployee, name='ViewEmployee'),
    path('addOrder/', views.addOrder, name='AddOrder'),
    path('addFeedback/', views.addFeedback, name='AddFeedback'),
    path('editEmployee/<int:pk>/', views.editEmployee, name='EditEmployee'),
    path('deleteEmployee/<int:pk>/', views.deleteEmployee, name='DeleteEmployee'),
    path('editOrder/<int:pk>/', views.editOrder, name='EditOrder'),
    path('deleteOrder/<int:pk>/', views.deleteOrder, name='DeleteOrder'),
    path('addCustomer/', views.addCustomer, name='AddCustomer'),
    path('addMenu/', views.addMenu, name='AddMenu'),
    path('editCustomer/<int:pk>/', views.editCustomer, name='EditCustomer'),
    path('deleteCustomer/<int:pk>/', views.deleteCustomer, name='DeleteCustomer'),
    path('editMenu/<int:pk>/', views.editMenu, name='EditMenu'),
    path('deleteMenu/<int:pk>/', views.deleteMenu, name='DeleteMenu'),
    path('addLead/', views.addLead, name='AddLead'),
    path('editLead/<int:pk>/', views.editLead, name='EditLead'),
    path('deleteLead/<int:pk>/', views.deleteLead, name='DeleteLead'),
    path('viewCustomer/', views.viewCustomer, name='ViewCustomer'),
    path('addMenu/', views.addMenu, name='AddMenu'),
    path('viewMenu/', views.viewMenu, name='ViewMenu'),
    path('viewOrder/', views.viewOrder, name='ViewOrder'),
    path('viewFeedback/', views.viewFeedback, name='ViewFeedback'),
    path('deleteFeedback/<int:pk>/', views.deleteFeedback, name='DeleteFeedback'),
    path('viewLead/', views.viewLead, name='ViewLead'),
    path('composeMail/', views.composeMail, name='ComposeMail'),
    # path('addMenuRequest/', views.addMenuRequest, name='addMenuRequest')

]
