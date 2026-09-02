"""IIC-IEM – Council Admin"""
from django.contrib import admin
from .models import CouncilYear, CouncilMember

class CouncilMemberInline(admin.TabularInline):
    model = CouncilMember
    extra = 1

@admin.register(CouncilYear)
class CouncilYearAdmin(admin.ModelAdmin):
    list_display = ['year_label', 'is_current']
    inlines = [CouncilMemberInline]

@admin.register(CouncilMember)
class CouncilMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'member_type', 'council_year', 'order_no']
    list_filter = ['member_type', 'council_year']
    search_fields = ['name', 'role']
