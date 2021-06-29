import re
# (^([A-Za-z]{2,25}(\s)?){3,5})
# p = "^([a-zA-Z0-9_\\-\\.]+)@(psau.edu.sa)$"
# status = ["a.salman@psau.edu.sa","aslman@psau","asalman.psau","a.salman.ahmad@psau.edu","a.salman@gmail.com"]

# u = [re.search(p,s) for s in status]
# print(u)
name = "ahmad salman"
name_regex = "(([^(\'u0600'-\'u06ff'\'u0750'-\'u077f'\'ufb50'-\'ufbc1'\'ufbd3'-\'ufd3f'\'ufd50'-\'ufd8f'\'ufd50'-\'ufd8f'\'ufe70'-\'ufefc'\'uFDF0'-\'uFDFD')(\s)?]{2,25}(\s)?){4,5})"
nameRegex = re.fullmatch(name_regex,name)
print(nameRegex)

