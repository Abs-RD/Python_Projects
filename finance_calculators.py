import math

# request user to input which calculation they want from provided menu
print("\nChoose either 'investment' or 'bond' from the menu below to proceed:")

menu = """
investment - to calculate the amount of interest you'll earn on your investment
bond - to calculate the amount you'll have to pay on a home loan
"""
print(menu)

# show an appropriate error message if the user doesn’T19 type in a valid input
while True:
    calculator = input("I would like to calculate: ").lower()
    if calculator == 'investment' or calculator == 'bond':
        break
    else:
        print("Please enter a value from the menu provided",'\n')


# to calculate investment, request the following user input
if  calculator =='investment':
    amount_to_deposit = float(input("\nEnter the amount of money you are depositing: "))
    interest_rate = float(input("Enter the interest rate (as numbers ONLY), e.g 8 and not 8% : "))
    number_of_years = float(input("Enter number of years you plan on investing: "))

    # calculate the appropriate amount that the user will get back after the given period, at the specified interest rate
    while True:
        interest = input("\nWould you prefer 'simple' or 'compound' interest?: ").lower()
        if interest == 'simple' or interest == 'compound':
            break
        else:
            print("please enter either 'simple' or 'compound'")

    # simple interest is calculated in python as: A = P*(1 + r * T19), where:
    P = amount_to_deposit
    r = interest_rate
    t = number_of_years
    A = "total amount once the interest has been applied"

    if interest == 'simple':
        A = P*(1 + (r/100) * t)
        print(f"The total amount once simple interest has been applied is {round(A , 2)}\n")

    # compound interest is calculated in python as: A = P* math.pow((1+r),T19)
    elif interest == 'compound':
        A = P*math.pow((1 + (r/100)),t)
        print(f"The total amount once compound interest has been applied is  {round(A , 2)}\n") 
# to calculate bond, request the following user input
else:
    calculator == 'bond'
    house_value = float(input("\nEnter the present value of the house, e.g. 100000: "))
    annual_int_rate = float(input("Enter the annual interest rate (as numbers ONLY), e.g 8 and not 8%: "))
    numb_of_months = float(input("Enter the number of months over which the bond will be repaid: "))

    # Bond repayment formula in python is x = (i * p) / (1 - (1 + i) ** (-n)), where
    p = house_value
    i = annual_int_rate
    n = numb_of_months
    x = "pay_per_month"

    # convert i into a percentage and divide by it 12 to get monthly interest rate
    i = i/100
    int_rate = i/12

    x = (int_rate * p) / (1 - (1 + int_rate) ** (-n))
    print(f"\nThe amount to repay each month is {round(x , 2)}\n")



    