from django.db import models
from datetime import date

# Create your models here.

HISTORY = (
	('ok','OK'),
	('not ok','NOT OK'),
)
STUDIES = (
	('elementary school', 'ELEMENTARY SCHOOL'),
	('high school', 'HIGH SCHOOL'),
	('bs/ba', 'BS/BA'),
	('master', 'MASTER'),
	('phd', 'PHD'),
)
INCOME = (
	('this bank', 'THIS BANK'),
	('other bank', 'OTHER BANK'),
)
SEXOPT = (
	('m', 'M'),
	('f', 'F'),
	('o', 'O'),
)
WORKOUT = (
	('once/week', 'ONCE/WEEK'),
	('twice/week', 'TWICE/WEEK'),
	('more','MORE')
)
STRESS = (
	('low', 'LOW'),
	('medium', 'MEDIUM'),
	('high', 'HIGH'),
)
DIET = (
	('low fat', 'LOW FAT'),
	('low carbs', 'LOW CARBS'),
	('both', 'BOTH'),
)

class Loan_client(models.Model):
	first_name=models.CharField(max_length=20)
	last_name=models.CharField(max_length=20)
	receiving_income = models.CharField(max_length=10, choices=INCOME)
	email=models.EmailField(unique=True)
	sex = models.CharField(max_length=1, choices=SEXOPT)
	loan_history=models.CharField(max_length=6, choices=HISTORY, help_text="official loan record obtained from loan office")
	birth_date=models.DateField()	
	education=models.CharField(max_length=18, choices=STUDIES)
	work_experience=models.IntegerField(default=0, help_text="official records of work experience (in years)")
	gross_income=models.IntegerField(default=0, help_text="use RON values")
	tax_percent=models.IntegerField(default=45, help_text="the percentage of all income taxes")
	dependents=models.IntegerField(default=0, help_text="the number of children + unemployed family members")
	current_monthly_payments=models.IntegerField(default=0, help_text="total loan payments in RON")
	loan_req_date = models.DateField(auto_now=True)
	needed_loan=models.IntegerField(default=20000, help_text="the amount requested by the client, in RON")
	return_period=models.IntegerField(default=2, help_text="the number of years to return the loan")

	def _calculate_age(self):
		today = date.today()
		return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
	
	age = property(_calculate_age)
	
	def _calculate_net_income(self):
		return int(self.gross_income*(1-(self.tax_percent/100)))
	
	net_income = property(_calculate_net_income)
	
	def _calculate_max_monthly_payments(self):
		return round(self.net_income*0.35,1)
	
	max_monthly_payments = property(_calculate_max_monthly_payments)
	
	def _calculate_rating(self):
		if self.current_monthly_payments>0:
			pp = self.current_monthly_payments/self.net_income
			if pp>=0.35:
				return [0, "big previous payments"]
		r = 1
		if 'not ok' in self.loan_history:
			return [0, "loan history"]
		if self.age<19 or self.age>65:
			return [0, "age"]
		elif self.age<22 or self.age>62:
			r-=0.2
		elif self.age<25 or self.age>59:
			r-=0.1
		if self.work_experience<2:
			return [0, "low work seniority"]
		elif self.work_experience<5:
			r-=0.1
		if 'this bank' in self.receiving_income:
			r+=0.1
		if 'elementary school' in self.education:
			r-=0.2
		elif 'high school' in self.education:
			r-=0.1
		elif 'master' in self.education:
			r+=0.1
		elif 'phd' in self.education:
			r+=0.2		
		if self.dependents>4:
			return [0, "too many dependents"]
		elif self.dependents>2:
			r-=0.2
		else:
			r-=(0.1*self.dependents)
		if r>=0.6:
			return [r, ""]
		else:
			return [0, "poor rating"]
	
	rating = property(_calculate_rating)
	
	def _calculate_interest(self):
		if self.rating[0]==0:
			return 0
		else:
			return round(7/self.rating[0],1)
	
	interest = property(_calculate_interest)
	
	def _calculate_no_of_payments(self):
		return 12*self.return_period
	
	no_of_payments = property(_calculate_no_of_payments)
	
	def _calculate_loan_cost(self):
		if self.interest != 0:
			r=self.interest/1200
			return round((r*self.no_of_payments*self.needed_loan)/(1-((1+r)**(-self.no_of_payments))),1)
		else:
			return 0
	
	loan_cost = property(_calculate_loan_cost)
	
	def _calculate_monthly_payment(self):
		if self.return_period != 0:
			return round(self.loan_cost/(12*self.return_period),1)
		else:
			return 0
	
	monthly_payment = property(_calculate_monthly_payment)
	
	def _evaluate_pre_approval(self):
		if self.rating[0]==0:
			return "no"
		else:
			if self.monthly_payment+self.current_monthly_payments>self.max_monthly_payments:
				return "no"
			else:
				return "yes"
	
	pre_approved = property(_evaluate_pre_approval)

	def _reflect_cause(self):
		if self.monthly_payment+self.current_monthly_payments>self.max_monthly_payments:
			return "big cumulated payments"
		else:
			return self.rating[1]

	cause = property(_reflect_cause)


class Nutrition_client(models.Model):
	first_name=models.CharField(max_length=20)
	last_name=models.CharField(max_length=20)
	email=models.EmailField(unique=True)
	age = models.IntegerField(default=0, help_text="years")
	sex = models.CharField(max_length=1, choices=SEXOPT)
	initial_weight=models.IntegerField(default=0, help_text="kg values")
	workout = models.CharField(max_length=10, choices=WORKOUT)
	avg_stress_level = models.CharField(max_length=6, choices=STRESS)
	diet = models.CharField(max_length=9, choices=DIET)
	weight_1_month=models.IntegerField(default=0, help_text="kg values")
	weight_3_months=models.IntegerField(default=0, help_text="kg values")

	def _calculate_lw1(self):
		return self.initial_weight-self.weight_1_month

	weight_lost_1 = property(_calculate_lw1)

	def _calculate_lw2(self):
		return self.initial_weight-self.weight_3_months

	weight_lost_2 = property(_calculate_lw2)