#!/usr/bin/python
import math

# ==========================================================================


# YOUR SUBMISSION GOES HERE


# ==========================================================================

## DO NOT MODIFY BEYOND THIS POINT!
## Submissions with modifications beyond this line will be given a 0 score
## We will check... we have the technology :-)
if __name__ == "__main__":
    myScore = 0

    # Test base account
    acct = Account('Chelsey', 1024.32)

    # test withdraw method overdraft
    if acct.withdraw(100000.00) == False:
        myScore += 5
    else:
        print("ERROR: Account.withdraw(ammount) did not return False.")

    # Test withdraw method balance OK
    if acct.withdraw(60.01) == 964.31:
        myScore += 5
    else:
        print("ERROR: Value returned when attempting to make a withdrawal was unexpected")

    # test deposit function
    if acct.deposit(36.50) == 1000.81:
        myScore += 5
    else:
        print("ERROR: The deposit function on Account class returned an unexpected value")

    # test transaction counter
    if len(acct) == 2:
        myScore += 5
    else:
        print("ERROR: The transaction counter returned an unexpected result when using len()")

    # Check toString()
    if str(acct) == 'Chelsey':
        myScore += 5
    else:
        print("ERROR: Converting Account to a string had an unexpected resule")

    # Test equivilance operator
    acct2 = Account('Sam', 1000.81)
    if acct == acct2:
        myScore += 5
    else:
        print("ERROR: Equivilance op test #1 failed")
    acct2.withdraw(1000.00)
    if acct == acct2:
        print("ERROR: Equivilance op test #2 failed")
    else:
        myScore += 5

    # Test the CreditAccount class
    acct = CreditAccount('Chelsey')

    # Test inherited methods
    if str(acct) == 'Chelsey':
        myScore += 5
    else:
        print("ERROR: When testing inherited methods for CreditAccount")
    
    # Test withdraw function
    if acct.withdraw(100000.00) == False:
        myScore += 5
    else:
        print("ERROR: CreditAccount.withdraw did not return expected false")
    if acct.withdraw(100.00) == 124.00:
        myScore += 5
    else:
        print("ERROR: CreditAccount.withdraw returned unexpected result")

    # test deposit function
    if acct.deposit(100.00) == 24.00:
        myScore += 5
    else:
        print("ERROR: CreditAccount.deposit returned unexpected result")
    
    # test transaction counter
    if len(acct) == 1:
        myScore += 5
    else:
        print("ERROR: CreditAccount length was incorrect")

    # test SavingsAccount
    acct1 = SavingsAccount('Hannah', 36.30)
    acct2 = SavingsAccount('Andrew', 156.33)
    if acct1.deposit(100.00) == 141.30:
        myScore += 5
    else:
        print("ERROR: deposit for savings account had unexpected return")

    # test accrue
    if acct1.accrue() == 148.365:
        myScore += 5
    else:
        print("ERROR: deposit for savings account had unexpected return")
print ("Grading complete: your score is %d out of 70" % (myScore) )