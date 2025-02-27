from django import forms
from django.contrib.auth.forms import UserCreationForm
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserBankAccount,UserAddress





class UserRegistrationForm(UserCreationForm):
    birth_date= forms.DateField(widget=forms.DateInput(attrs={'type':"date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type= forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)
    class Meta:
        # extra characteristics add kore
        model=User
        fields=['username','password1','password2','first_name','last_name','email',
        'account_type','birth_date','gender','street_address','postal_code','city','country']
    def save(self,commit=True):
        our_user=super().save(commit=False) #ami database e data save korbo na ekhon
        # creates an instance of the model (user in this case) without saving it to the database.

        if commit==True:
            our_user.save() #user model e data save korlam
            account_type= self.cleaned_data.get('account_type')
            gender= self.cleaned_data.get('gender')
            birth_date= self.cleaned_data.get('birth_date')
            postal_code= self.cleaned_data.get('postal_code')
            street_address= self.cleaned_data.get('street_address')
            city= self.cleaned_data.get('city')
            country= self.cleaned_data.get('country')

            UserAddress.objects.create(
                user= our_user,
                postal_code = postal_code,
                country = country,
                city=city,
                street_address=street_address

            )
            #  It's a shortcut that creates and saves an object in database
            UserBankAccount.objects.create(
                 user= our_user,
                 account_type = account_type,
                 gender= gender,
                 birth_date = birth_date,
                 account_no = 100000+our_user.id
            )
        return our_user    
        

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            # print(field)
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-300 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            }) 

            # jodi user er account thake 
        if self.instance:
            try:
                user_account=self.instance.account #account model er data
                user_address = self.instance.address   
            except UserBankAccount.DoesNotExist:
                user_account=None
                user_address=None

        #    zodi user account thake
            if user_account:
                self.fields['account_type'].initial= user_account.account_type
                self.fields['gender'].initial = user_account.gender
               
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country 

            def save(self,commit=True):
                user=super.save(commit=False)  

                if commit:
                    user.save()

                    user_account,created= UserBankAccount.objects.get_or_create(user=user)
                    # user account thake pabo,ar zodi na thake tahole created hobe
                    # zodi account thake tahole seta user_account e zabe ,zodi account na thake
                    #create hobe ar seta created er moddehe zabe
                    user_address, created = UserAddress.objects.get_or_create(user=user) 

                    user_account.account_type = self.cleaned_data['account_type']
                    user_account.gender = self.cleaned_data['gender']
                    user_account.birth_date = self.cleaned_data['birth_date']
                    user_account.save()

                    user_address.street_address = self.cleaned_data['street_address']
                    user_address.city = self.cleaned_data['city']
                    user_address.postal_code = self.cleaned_data['postal_code']
                    user_address.country = self.cleaned_data['country']
                    user_address.save()

                return user

    



