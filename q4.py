import numpy as np
class BaseComission:
    def __init__(self, base, unit, increment):
        self.base = base
        self.unit = unit
        self.increment = increment

class CommissionTier(BaseComission):
    """
    base: (int) tier base
    unit: (string) tier unit; can be 'cost' or 'units_sold'
    increment: (int) tier increment
    max: (int) tier max
    """
    def __init__(self, base, unit, increment, max_value):
        super().__init__(base, unit, increment)
        self.max = max_value

class CommissionModel(BaseComission):
    """
    base: (int) commission base
    unit: (string) commission unit; can be '$' or '$/unit_sold'
    increment: (int) commission increment
    tier: (CommissionTier) commission tier
    """
    def __init__(self, base, unit, increment, tier):
        super().__init__(base, unit, increment)
        self.tier = tier

class Sale:
    """
    units_sold: (int) number of units sold
    cost: (int) total cost of the sale
    """
    def __init__(self, units_sold, cost):
        self.units_sold = units_sold
        self.cost = cost

# Assume all checks have already gone through get_commission amount
def get_commission_amount_cost_subtype(model, sale):
	# model.tier.base - minimum amount needed to earn commission.
	# model.tier.increment - interval over which new commission is earned.
	# model.tier.max - max possible commission
	
	# model.tier.max + model.tier.increment -- this bit is here because we want to keep the last model tier. Max is valid.
	tier_keys = np.array ([i for i in range(model.tier.base,model.tier.max + model.tier.increment,model.tier.increment)])
	
	
	# Cost type awards model.base + model.increment * (Num of tiers away from first tier)

	# Use the tier_keys to figure out which commission tier they belong to (using sale.cost)
	
	commission_amount = 0

	if(sale.cost < tier_keys[0]):
		return 0
	else:
		# Give base amount
		commission_amount = model.base

	# For every tier other than the base tier, grant model.increment to commission_amount if salesman surpassed that tier
	for i in range(1,len(tier_keys)):
		if(sale.cost > tier_keys[i]):
			commission_amount += model.increment
		else:
			# tier_keys will always be monotonically increasing, we can break here.
			break	

	return commission_amount


def get_commission_amount_units_subtype(model, sale):
	# print("Sale units sold")
	# print(sale.units_sold)
	tier_keys = [i for i in range(model.tier.base,model.tier.max + model.tier.increment,model.tier.increment)]
	num_tiers = len(tier_keys)



	active_comm_keys = [i for i in range(model.base, model.base + model.increment * num_tiers, model.tier.increment)]
	# print("tier_keys")
	# print(tier_keys)
	# print("active_comm_keys")
	# print(active_comm_keys)

	commission_amount = 0

	curr_tier_key_index = 0

	active_commission = 0
	for i in range(0, len(tier_keys)):
		if(sale.units_sold >= tier_keys[i]):
			active_commission = active_comm_keys[i]
	commission_amount = active_commission * sale.units_sold
	return commission_amount		




def get_commission_amount(model, sale):
	if(not issubclass(type(model), BaseComission)):
		print("Error, expected sub-type ",str(BaseComission))
		raise TypeError

	if(type(sale)!=Sale):
		print("Error, expected sub-type ",str(Sale))
		raise TypeError
		
	if(model.unit == '$' and model.tier.unit == 'units_sold'):
		print("Error, Model and Tier not of the same type")
		raise TypeError

	if(model.unit == '$/unit_sold' and model.tier.unit == 'cost'):	
		print("Error, Model and Tier not of the same type")
		raise TypeError

	if(model.unit == '$' and model.tier.unit == 'cost'):
		return get_commission_amount_cost_subtype(model, sale)
	elif(model.unit == '$/unit_sold' and model.tier.unit == 'units_sold'):
		return get_commission_amount_units_subtype(model, sale)




if __name__ == '__main__':
	tier_1 = CommissionTier(1000, 'cost', 1000, 5000)
	model_1 = CommissionModel(25, '$', 25, tier_1)
	tier_2 = CommissionTier(0, 'units_sold', 5, 15)
	model_2 = CommissionModel(30, '$/unit_sold', 5, tier_2)

	sale_1 = Sale(5,2500)
	sale_2 = Sale(1, 750)
	sale_3 = Sale(16,7500)
	
	print(get_commission_amount(model_1, sale_1) == 50)
	print(get_commission_amount(model_2, sale_1) == 175)
	print(get_commission_amount(model_1, sale_2) == 0)
	print(get_commission_amount(model_2, sale_2) == 30)
	print(get_commission_amount(model_1, sale_3) == 125)
	print(get_commission_amount(model_2,sale_3) == 720)

    