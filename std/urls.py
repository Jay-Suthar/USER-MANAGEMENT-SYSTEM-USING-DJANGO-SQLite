from django.urls import path

from . views import *

urlpatterns = [

    path("", HomeView.as_view(), name="home"),
    path("home/", HomeView.as_view(), name="home"),
    path("add-std/", AddUserView.as_view(), name="add_user"),
    path("delete-std/<int:id>/", DeleteUserView.as_view(), name="delete_user"),
    path("update-std/<int:id>/", UpdateUserView.as_view(), name="update_user"),
    path("user-view/<int:id>/", CurrentUserView.as_view(), name="user-view"),
    path("confirm-update-std/<int:id>/", ConfirmUpdateUserView.as_view(), name="confirm_update_user"),
    path("add-multiple-user/", AddMultipleUser.as_view(), name="add-multiple-user"),
    path("show-roles/", ShowAllRoles.as_view(), name="show-roles"),
    path("add-multiple-roles/", AddMultipleRole.as_view(), name="add-multiple-roles"),
    path("all_users_with_role/<str:title>/", ShowAllUsersForRole.as_view(), name="all_users_with_role"),
    path("show-status/", ShowAllStatus.as_view(), name="show-status"),
    path("all_users_with_status/<str:status>/", ShowAllUsersForStatus.as_view(), name="all_users_with_status"),
]






# path("",home),
# path("home/",home),
# path("add-std/",add_std),
# path("delete-std/<int:id>",delete_std),
# path("update-std/<int:id>", update_std),
# path("confirm-update-std/<int:id>", confirm_update_std),