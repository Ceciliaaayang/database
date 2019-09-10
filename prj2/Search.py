

def standardization(querys):

    a = querys.split()
    space_querys = ' '
    for i in a:
        space_querys = space_querys + i + ' '
    space_querys = space_querys.strip()
    final_querys = remove_useless_space(space_querys)
    return final_querys

def remove_useless_space(space_querys):
    l = len(space_querys)
    IS_FIRST = 1
    query_list = []
    last = None
    for i in range(0, l):
        if (space_querys[i] == ' '):
            if ((space_querys[i-1].isalnum() or space_querys[i-1] == '%') and space_querys[i + 1].isalnum()or space_querys[i-1] == '%'):

                if(IS_FIRST == 1):# if it's first query
                    query_list.append(space_querys[:i].replace(' ',''))
                    IS_FIRST = 0
                    last = i
                else:
                    query_list.append(space_querys[last:i].replace(' ',''))
                    last = i
    query_list.append(space_querys[last:].replace(' ',''))
    return query_list
def isoperater(c):
    if(c == '>' or c == '<' or c == '='):
        return True
    else:
        return False

def parse_query(query):
    parse_list = []
    for i in range(0, len(query)):
        if( isoperater(query[i]) == True):
            if( query[i+1] == '='):
                parse_list.append(query[:i])
                parse_list.append(query[i] + '=')
                parse_list.append(query[i+2:])
                return parse_list
            else:
                parse_list.append(query[:i])
                parse_list.append(query[i])
                parse_list.append(query[i+1:])
                return parse_list
    parse_list.append(query)
    return parse_list



