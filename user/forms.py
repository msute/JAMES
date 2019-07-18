from django import forms

from user.models import Profile

#ModelForm可以跟model建立关联
class ProfieldForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location',
                  'min_distance',
                  'max_distance',
                  'min_dating_age',
                  'max_dating_age',
                  'dating_sex'
                  ]

        #all是直接可以连接所有字段
        # fields = '__all__'