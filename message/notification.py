def send_notification():
    from push_notifications.models import GCMDevice
    devices = GCMDevice.objects.all()
    devices.send_message("Hey There", extra={"title": "New Notification"})
