from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

User._meta.get_field('email').blank = False
