# Sources Used
# https://stackoverflow.com/questions/29815129/pandas-dataframe-to-list-of-dictionaries
# 

input_1 = (
    'state,solar,storage,energy_efficiency\n'
    'CA,active,inactive,active\n'
    'NV,inactive,active,active'
)

input_2 = (
    'product_type,is_active\n'
    'loan,true\n'
    'lease,true\n'
    'ppa,false\n'
    'cash,false\n'
)

def parse_csv_helper(row, col_headers):
    if (len(row) == len(col_headers)):
        d = dict()
        for j in range(0, len(row)):
            if(row[j].upper() == "TRUE"):
                d[col_headers[j]] = True
            elif (row[j].upper() == "FALSE"):
                d[col_headers[j]] = False
            else:
                d[col_headers[j]] = row[j]
    return d

def parse_csv(csv_input):
    # Remove "," or "\n" characters from beginning and end of input
    csv_input = csv_input.strip('\n,')

    # Split first on new line, then on ,
    arr = [x.split(",") for x in csv_input.split('\n')]
    # Headers are at index 0
    headers = arr[0]
    output = [parse_csv_helper(arr[i], headers) for i in range(1,len(arr))]
    return output

if __name__ == '__main__':
    output_1 = parse_csv(input_1)
    output_2 = parse_csv(input_2)

    ## Testing
    # Interacting with output object for some basic checks
    print(output_1[1].get("state") == "NV")
    print(output_1[0].get("state") == "CA")
    print(output_1[1].get("energy_efficiency") == "active")
    print(output_1[0].get("energy_efficiency") == "active")

    print(output_2[0].get("product_type") == "loan")
    print(output_2[1].get("product_type") == "lease")
    print(output_2[2].get("product_type") == "ppa")
    print(output_2[3].get("product_type") == "cash")

    # Implictly, requirement is to turn "true" and "false" strings into True and False booleans
    print(output_2[0].get("is_active") == True)
    print(output_2[1].get("is_active") == True)
    print(output_2[2].get("is_active") == False)
    print(output_2[3].get("is_active") == False)
    