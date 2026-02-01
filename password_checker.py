import string

password = "P12rivate@345" 

upercase = any([1 if c in string.ascii_uppercase else 0 for c in password])
lowercase = any([1 if c in string.ascii_lowercase else 0 for c in password])
digit = any([1 if c in string.digits else 0 for c in password])
special_char = any([1 if c in string.punctuation else 0 for c in password]) 

characters =[upercase,lowercase,digit,special_char]

length = len(password)

score = 0
if length >=8:
    score +=1
if length >=12:
    score +=1
if length >=15:
    score +=1
if length >=3:
    score +=1
if length >=6:
    score +=1
print(f"password length is {str(length)}, adding {str(score)} Points")

if sum(characters) > 1:
    score += 1
if sum(characters) > 2:
    score += 1
if sum(characters) > 3:
    score += 1
    print(f"password has {str(sum(characters))} character types, adding {str(sum(characters)-1)} Points")
    
    if score <=3:
        print(f"Password Strength: Weak score:{str(score)}/7")
    elif score == 4:
        print(f"Password Strength: Moderate score:{str(score)}/7")
    elif score >=5: 
        print(f"Password Strength: Strong score:{str(score)}/7")