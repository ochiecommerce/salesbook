import string, random, json

def random_name():
    return ''.join([random.choice(string.ascii_lowercase)+random.choice(['a','e','i','o','u']) for i in range(4)]).capitalize()

def random_number():
    return str(random.randint(10000000,99999999))

def random_employer():
    employers = ['tsck','health','siaya county','kisumu county','vocational','oopmain','prison']
    return random.choice(employers)

rows =[]

for i in range(1000):
    row = {}
    row["name"] = random_name()+' '+random_name()
    row["id_number"] = random_number()
    row["phone"] = '07'+random_number()
    row["employer_name"] = random_employer()
    row["employment_number"] = random_number()
    row['status']='new'

    rows.append(row)
file = open('contacts.json','w+')
file.write(json.dumps(rows))


