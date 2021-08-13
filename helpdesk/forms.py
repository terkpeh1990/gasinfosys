from django import forms
from .import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from datetime import date
from .models import Technician,  Team, Technician, WaitingEscalate, Supervisor, Checkid, Ticket, Ticket_Comments,Escalate
from inventory.models import *
from .models import Ticket
User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class UserTicket(forms.ModelForm):
    """docstring for UserTicket."""

    class Meta:
        model = Ticket
        
        fields = ('subject', 'description', 'region', 'district')

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Subject...'}),
            'description': forms.Textarea(attrs={'placeholder': 'Type a message...'}),
        }

        labels = {
            'subject': 'Subject',
            'description': 'Description',
            'region': 'Region/Office Location',
            'district': 'Section/Branch/District',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(
                    region_id=region_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.region.district_set.order_by(
                'districtname')


class ViewTicket(forms.ModelForm):
    """docstring for UserTicket."""

    class Meta():
        model = Ticket
        fields = ('subject', 'ticket_date', 'description', 'status', 'agent')

        widgets = {
            'ticket_date': DateInput(attrs={'readonly': 'readonly'}),
            'subject': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'readonly': 'readonly'}),
            'status': forms.TextInput(attrs={'readonly': 'readonly'}),
            'agent': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        labels = {
            'ticket_date': 'Ticket Date',
            'subject': 'Subject',
            'description': 'Description',
            'status': 'Ticket Status',
            'agent': 'Assigned Agent',

        }


class Agent_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():
        model = Ticket
        fields = ('subject', 'agent_team', 'agent', 'prority',
                  'description', 'status', 'region', 'district')

        widgets = {
            'ticket_date': DateInput(),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject...'}),
            'description': forms.Textarea(attrs={'placeholder': 'Type a message...'}),

        }

        labels = {
            'subject': 'Subject',
            'ticket_date': 'Date',
            'agent_team': 'Team',
            'agent': 'Agent',
            'prority': 'Prority',
            'district': 'Branch/District/Unit',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = Technician.objects.none()
        self.fields['district'].queryset = District.objects.none()

        if 'agent_team' in self.data:
            try:
                agent_id = int(self.data.get('agent_team'))
                self.fields['agent'].queryset = Technician.objects.filter(
                    team=agent_id)
            except (ValueError, TypeError):
                pass
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(
                    region_id=region_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.region.district_set.order_by(
                'districtname')


class Edit_helpdesk_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():
        model = Ticket
        fields = ('subject', 'agent_team', 'agent', 'prority',
                  'description', 'astatus', 'status')

        widgets = {
            'ticket_date': DateInput(attrs={'readonly': 'readonly'}),
            'subject': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'readonly': 'readonly'}),
            'astatus': forms.TextInput(attrs={'readonly': 'readonly'}),
            'expected_date': DateInput(),
        }

        labels = {
            'subject': 'Subject',
            'agent_team': 'Team',
            'agent': 'Agent',
            'prority': 'Prority',
            'status': 'Ticket Status',
            'astatus': 'Agent Status',

        }


class Edit_Agent_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():
        model = Ticket
        fields = ('subject', 'ticket_date', 'agent_team', 'agent',
                  'prority', 'expected_date', 'description', 'astatus', 'status')

        widgets = {
            'ticket_date': DateInput(attrs={'readonly': 'readonly'}),
            'subject': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'readonly': 'readonly'}),
            'agent_team': forms.TextInput(attrs={'readonly': 'readonly'}),
            'agent': forms.TextInput(attrs={'readonly': 'readonly'}),
            'status': forms.TextInput(attrs={'readonly': 'readonly'}),
            'prority': forms.TextInput(attrs={'readonly': 'readonly'}),
            'expected_date': DateInput(attrs={'readonly': 'readonly'}),
        }

        labels = {
            'subject': 'Subject',
            'ticket_date': 'Date',
            'agent_team': 'Team',
            'agent': 'Agent',
            'prority': 'Prority',
            'status': 'Ticket Status',
            'astatus': 'Agent Status',
            'expected_date': 'Estimated Date',
        }


class agent_detail_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():

        model = Ticket
        fields = ('status', 'prority', 'escalated')

        labels = {

            'escalated': 'Status',
            'agent_team': 'Team',
            'agent': 'Agent',
            'prority': 'Prority',

        }


class Ticket_comment(forms.ModelForm):
    content = forms.CharField(label=False, widget=forms.Textarea(
        attrs={'placeholder': 'Type a message...'}))
    """docstring for AgentTicket."""

    class Meta():
        model = Ticket_Comments
        fields = ('content',)


class Escalade(forms.ModelForm):
    reason = forms.CharField(label=False, widget=forms.Textarea(
        attrs={'placeholder': 'Type a message...'}))
    """docstring for AgentTicket."""

    class Meta():
        model = Escalate
        fields = ('agent', 'agent_team', 'reason')

        labels = {
            'agent': 'Agent',
            'agent_team': 'Team',
            'reason': 'Reason'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = Technician.objects.none()

        if 'agent_team' in self.data:
            try:
                agent_id = int(self.data.get('agent_team'))
                self.fields['agent'].queryset = Technician.objects.filter(
                    team=agent_id)
            except (ValueError, TypeError):
                pass


class WaitingEscaladeForm(forms.ModelForm):
    reason = forms.CharField(label=False, widget=forms.Textarea(
        attrs={'placeholder': 'Type a message...'}))
    """docstring for AgentTicket."""

    class Meta():
        model = WaitingEscalate
        fields = ('supervisor', 'agent_team', 'reason')

        labels = {
            'agent_team': 'Team',
            'supervisor': 'Supervisor',
            'reason': 'Reason'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supervisor'].queryset = Supervisor.objects.none()

        if 'agent_team' in self.data:
            try:
                agent_id = int(self.data.get('agent_team'))
                self.fields['supervisor'].queryset = Supervisor.objects.filter(
                    team=agent_id)
            except (ValueError, TypeError):
                pass


