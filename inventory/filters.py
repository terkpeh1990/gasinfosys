import django_filters
from django import forms
from django_filters import DateFilter , CharFilter, NumberFilter
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'


class RequisitionFilter(django_filters.FilterSet):
    id = CharFilter(field_name='id', lookup_expr='exact', label='Batch No')
    start_date = DateFilter(field_name="requisition_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="requisition_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Requisition
        fields = ['start_date', 'end_date', 'department', 'status',
                  'id']


class ForcastFilter(django_filters.FilterSet):
   
    class Meta:
        model = Product
        fields = ['requisition_details__detail_date', ]
