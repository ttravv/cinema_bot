baida = 'page=1&limit=10&sortField=rating.imdb&sortType=-1&type=movie&votes.imdb=100000-6666666666666'

def test(baida: str) -> dict[str, str]:
    new_dict = {}
    for i in baida.split('&'):
        i_split = i.split('=')
        new_dict[i_split[0]] = i_split[1]
    return new_dict

print(test(baida))
    


