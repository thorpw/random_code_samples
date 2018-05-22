from IPython.display import clear_output

#create dictionary
considerations = {}

def numberOfMonths():
    counter = 0
    while True:
        try:
            #delete existing entry
            if 'months' in considerations:
                del considerations['months']
            #stop loop if a non numeric character is input 5 times
            if counter == 5:
                #reset counter
                counter = 0
                break
            #accept the number of months input from user
            months = input("Please enter number of months: ")
            clear_output()
            #add number of months to the dict
            considerations['months'] = months
            #try convert to integer
            considerations['months'] = int(considerations['months'])
        except ValueError:
            #print error message
            print('Error - Please enter an integer')        
            #increment wrong input counter
            counter += 1
            if counter == 5:
                #error message
                print('Too many failed attempts')        
            continue
        return int(months)
        break

def dailyRate():
    counter = 0
    while True:
        try:
            #delete existing entry
            if 'rate' in considerations:
                del considerations['rate']
            #stop loop if a non numeric character is input 5 times
            if counter == 5:
                #reset counter
                counter = 0
                break
            #accept the number of months input from user
            rate = input("Please enter your daily rate: ")
            clear_output()
            #add number of months to the dict
            considerations['rate'] = rate
            #try convert to integer
            considerations['rate'] = int(considerations['rate'])
        except ValueError:
            #print error message
            print('Error - Please enter an integer')        
            #increment wrong input counter
            counter += 1
            if counter == 5:
                #error message
                print('Too many failed attempts')        
            continue
        return int(rate)
        break

def numberOfDays():
    counter = 0
    while True:
        try:
            #delete existing entry
            if 'days' in considerations:
                del considerations['days']
            #stop loop if a non numeric character is input 5 times
            if counter == 5:
                #reset counter
                counter = 0
                break
            #accept the number of months input from user
            days = input("Please enter number of days you will work per month: ")
            clear_output()
            #add number of months to the dict
            considerations['days'] = days
            #try convert to integer
            considerations['days'] = float(considerations['days'])
        except ValueError:
            #print error message
            print('Error - Please enter an integer')        
            #increment wrong input counter
            counter += 1
            if counter == 5:
                #error message
                print('Too many failed attempts')        
            continue
        return float(days)
        break

amount = (numberOfDays() * dailyRate()) * numberOfMonths()

print("You will earn " + "€" + str(amount) + " annually")
