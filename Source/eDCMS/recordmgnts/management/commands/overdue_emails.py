from django.core.management.base import BaseCommand
from recordmgnts.models import ContainerInstance
from django.core.mail import send_mail

# to run this command manually, use python manage.py custom_command
# this is a command to send emails to users who have not check in overdue containers
# set windows task scheduler to run this command everyday
# go to windows task scheduler and add a new task
# add your python .exe in the new task program/script under action tab
# run this command in cmd to find location of .exe python -c "import sys; print(sys.executable)"
# then find the location of manage.py file of your django project and add to add arguments(optional) under action tab
# example : "location of manage.py file of project" overdue-emails


class Command(BaseCommand):
    help = 'Sends email to user with overdue containers.'

    def handle(self, *args, **kwargs):
        checked_out_containers = ContainerInstance.objects.filter(status=False, email_sent=False)
        user_list = [container.user for container in checked_out_containers if container.is_overdue]
        if user_list:
            unique_user_list = list(set(user_list))
            for user in unique_user_list:
                containers_by_user = ContainerInstance.objects.filter(status=False, user=user, email_sent=False)
                overdue_containers = [str(container.container.container_serial_number) for container in containers_by_user
                                      if container.is_overdue]
                containers = ', '.join(overdue_containers)
                message = "According to our records, the items listed below which are currently " \
                          "checked out by you are overdue." \
                          "Please check in these containers at their respective warehouses as soon as possible.\n" \
                          "The containers are " + containers + \
                          "\nThis is an automated email, please do not reply."

                send_mail('Container Check Out Overdue',
                          message,
                          'edcmshyb@gmail.com',
                          [user.email],
                          fail_silently=False
                          )
                for container in containers_by_user:
                    if container.is_overdue:
                        container.email_sent = True
                        container.status = False
                        container.save()
                    else:
                        pass
        else:
            print("There is no overdue containers.")
