from django.contrib import admin

# Register your models here.
from main.models import Loan_client
from main.models import Nutrition_client
class Loan_client_Admin(admin.ModelAdmin):
	list_display=["id","first_name","last_name","sex","loan_req_date","pre_approved","cause","age","receiving_income","loan_history","gross_income","net_income","max_monthly_payments","current_monthly_payments","monthly_payment","needed_loan","no_of_payments","interest","loan_cost"]
	list_per_page = 10

class Nutrition_client_Admin(admin.ModelAdmin):
	list_display=["id","first_name","last_name","email","age","sex","initial_weight","workout","avg_stress_level","diet","weight_1_month","weight_3_months"]
	list_per_page = 10

admin.site.register(Loan_client,Loan_client_Admin)
admin.site.register(Nutrition_client,Nutrition_client_Admin)