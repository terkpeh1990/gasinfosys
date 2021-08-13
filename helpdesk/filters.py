import django_filters
from django import forms
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class TicketFilter(django_filters.FilterSet):
    id = CharFilter(field_name='id', lookup_expr='exact', label='Ticket Id')
    start_date = DateFilter(field_name="ticket_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="ticket_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Ticket
        fields = ['start_date', 'end_date', 'status', 'prority',
                  'escalated', 'id', 'region', 'agent_team', 'agent']


class ReportFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="ticket_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="ticket_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Ticket
        fields = ['start_date', 'end_date', 'prority',
                  'escalated', 'region', 'agent_team', 'agent']


class AuditFilter(django_filters.FilterSet):
    id = CharFilter(field_name='id', lookup_expr='exact', label='Ticket Id')
    start_date = DateFilter(field_name="ticket_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="ticket_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Ticket
        fields = ['start_date', 'end_date', 'prority',
                  'escalated', 'region', 'agent_team', 'agent']
