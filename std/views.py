import pytz
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from .models import User, Role_Used
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.views import View
from faker import Faker
import random


class HomeView(View):
    def get(self, request):
        # User.objects.all().delete()
        # user = User.objects.all()
        try:
            user = User.objects.all().order_by('-created_at')
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return render(request, "std/home.html", {'user': user})


class AddUserView(View):
    def get(self, request):
        try:
            roles = Role_Used.objects.all()
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return render(request, "std/add_std.html", {'roles': roles})

    def post(self, request):
        user_id = request.POST.get("user_id")
        user_name = request.POST.get("user_name")
        user_email = request.POST.get("user_email")
        user_cur_status = request.POST.get("user_cur_status")
        user_role_title = request.POST.get("user_role")

        u = User()
        u.userid = user_id
        u.name = user_name
        u.email = user_email
        u.status = user_cur_status

        user_role = Role_Used.objects.get(title=user_role_title)
        u.role = user_role

        ist = pytz.timezone('Asia/Kolkata')
        current_time_ist = timezone.now().astimezone(ist)
        u.created_at = current_time_ist

        try:
            u.full_clean()
            u.save()
        except ValidationError as e:
            error_messages = e.message_dict.values()
            flat_error_messages = [message for sublist in error_messages for message in sublist]
            print(flat_error_messages)
            response_content = f"<h1>Error:</h1><ul>{''.join([f'<li>{error}</li>' for error in flat_error_messages])}</ul>"

            return HttpResponse(response_content)

        return redirect("/std/home")


class DeleteUserView(View):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
        except User.DoesNotExist:
            err_mssg = f"<h1>User with ID {id} not found.</h1>"
            return HttpResponseNotFound(err_mssg)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return redirect("/std/home")


class CurrentUserView(View):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            err_mssg = f"<h1>User with ID {id} not found.</h1>"
            return HttpResponseNotFound(err_mssg)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return render(request, "std/cur_user.html", {'user': user})


class UpdateUserView(View):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            roles = Role_Used.objects.all()
        except User.DoesNotExist:
            err_mssg = f"<h1>User with ID {id} not found.</h1>"
            return HttpResponseNotFound(err_mssg)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return render(request, "std/update_std.html", {'user': user, 'roles': roles})


class ConfirmUpdateUserView(View):
    def post(self, request, id):
        user_id = request.POST.get("user_id")
        user_name = request.POST.get("user_name")
        user_email = request.POST.get("user_email")
        user_cur_status = request.POST.get("user_cur_status")
        user_role_title = request.POST.get("user_role")

        u = User.objects.get(pk=id)
        u.userid = user_id
        u.name = user_name
        u.email = user_email
        u.status = user_cur_status
        user_role = Role_Used.objects.get(title=user_role_title)
        u.role = user_role

        ist = pytz.timezone('Asia/Kolkata')
        current_time_ist = timezone.now().astimezone(ist)
        u.created_at = current_time_ist
        try:
            u.full_clean()
            u.save()
        except ValidationError as e:
            error_messages = e.message_dict.values()
            flat_error_messages = [message for sublist in error_messages for message in sublist]
            print(flat_error_messages)
            response_content = f"<h1>Error:</h1><ul>{''.join([f'<li>{error}</li>' for error in flat_error_messages])}</ul>"

            return HttpResponse(response_content)

        return redirect("/std/home")


class AddMultipleUser(View):
    def get(self, request):
        fake = Faker()

        try:
            for _ in range(100):
                user = User()
                user.userid = fake.user_name()
                user.name = fake.name()
                user.email = fake.email()
                user.status = random.choice(['Active', 'Inactive', 'Not Present', 'Suspected'])

                user_role_title = random.choice([1, 2, 3, 4, 5, 6])

                user_role = Role_Used.objects.get(pk=user_role_title)
                user.role = user_role
                ist = pytz.timezone('Asia/Kolkata')
                current_time_ist = timezone.now().astimezone(ist)
                user.created_at = current_time_ist
                user.save()

        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return redirect("/std/home")


class ShowAllRoles(View):
    def get(self, request):
        try:
            roles = Role_Used.objects.all()
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return render(request, "std/all_roles.html", {'roles': roles})


class AddMultipleRole(View):
    def get(self, request, *args, **options):
        roles = [
            {'title': 'Engineer', 'description': 'Description for Engineer'},
            {'title': 'Senior Engineer', 'description': 'Description for Senior Engineer'},
            {'title': 'Manager', 'description': 'Description for Manager'},
            {'title': 'Senior Manager', 'description': 'Description for Senior Manager'},
            {'title': 'Head of Department', 'description': 'Description for Head of Department'},
            {'title': 'Company Head', 'description': 'Description for Company Head'},
        ]

        for role_data in roles:
            Role_Used.objects.create(**role_data)
        return redirect("/std/show-roles")


class ShowAllUsersForRole(View):
    def get(self, request, title):
        try:
            user = User.objects.filter(role__title=title)

            if not user.exists():
                raise User.DoesNotExist

        except User.DoesNotExist:
            err_mssg = f"<h1>User with Role: {title} not found.</h1>"
            return HttpResponseNotFound(err_mssg)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return render(request, "std/all_users_with_role.html", {'user': user, 'title': title})


class ShowAllStatus(View):
    def get(self, request):
        try:
            return render(request, "std/all_status.html")
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")


class ShowAllUsersForStatus(View):
    def get(self, request, status):
        try:
            user = User.objects.filter(status=status)
            if not user.exists():
                raise User.DoesNotExist

        except User.DoesNotExist:
            err_mssg = f"<h1>User with Status: {status} not found.</h1>"
            return HttpResponseNotFound(err_mssg)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")

        return render(request, "std/all_users_with_role.html", {'user': user, 'title': status})













# def home(request):
#     user = User.objects.all()
#     return render(request, "std/home.html", {'user': user})


# def add_std(request):
#     if request.method == 'POST':
#         print("Added")
#         user_id = request.POST.get("user_id")
#         user_name = request.POST.get("user_name")
#         user_email = request.POST.get("user_email")
#         user_cur_status = request.POST.get("user_cur_status")
#         user_role = request.POST.get("user_role")
#
#         u = User()
#         u.userid = user_id
#         u.name = user_name
#         u.email = user_email
#         u.status = user_cur_status
#         u.role = user_role
#         ist = pytz.timezone('Asia/Kolkata')
#
#         # Get the current time in IST
#         current_time_ist = timezone.now().astimezone(ist)
#
#         # Update the created_at field with the current IST time
#         u.created_at = current_time_ist
#         u.save()
#         return redirect("/std/home")
#
#     return render(request, "std/add_std.html", {})

# def delete_std(request, id):
#     user = User.objects.get(pk=id)
#     user.delete()
#
#     return redirect("/std/home/")

# def update_std(request, id):
#     user = User.objects.get(pk=id)
#     return render(request, "std/update_std.html", {'user': user})
#
#
# def confirm_update_std(request, id):
#     user_id = request.POST.get("user_id")
#     user_name = request.POST.get("user_name")
#     user_email = request.POST.get("user_email")
#     user_cur_status = request.POST.get("user_cur_status")
#     user_role = request.POST.get("user_role")
#
#     u = User.objects.get(pk=id)
#     u.userid = user_id
#     u.name = user_name
#     u.email = user_email
#     u.status = user_cur_status
#     u.role = user_role
#     ist = pytz.timezone('Asia/Kolkata')
#
#     # Get the current time in IST
#     current_time_ist = timezone.now().astimezone(ist)
#
#     # Update the created_at field with the current IST time
#     u.created_at = current_time_ist
#
#     u.save()
#     return redirect("/std/home")
