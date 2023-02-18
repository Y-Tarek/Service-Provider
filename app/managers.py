from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, mobile, type, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not name:
            raise ValueError("Users must have an fullname")

        # if not email:
        #     raise ValueError('Users must have an email address')

        if not mobile:
            raise ValueError("Users must have an mobile number")

        user = self.model(
            name=name,
            email=email if email else None,
            mobile=mobile,
            type=type if type else 1
            # email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, name, mobile, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            name,
            None,
            mobile,
            3,
            password=password,
            
            
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, name, mobile, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            name,
            None,
            mobile,
             3,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
