import requests
import sys

endpoint = 'https://db.thegpu.guru/graphql'

if __name__ == '__main__':
    query_string = sys.argv[1]
    print ('Querying database for', query_string)

    pagination = ''
    while True:
        query = '''{
                search(query:"%QUERY",type:CARD,first:3%PAGE) {
                    edges {
                        node {
                            ... on Card {
                                name
                                asic {
                                    name
                                    transistorCount
                                }
                            }
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }'''
        query = query.replace("%PAGE", pagination)
        query = query.replace("%QUERY", query_string)

        r = requests.get(endpoint,params={
            'query': query
        })

        d = r.json()

        for card in d['data']['search']['edges']:
            card = card['node']
            print('Name', card['name'], 'uses ASIC', card['asic']['name'], 'with', card['asic']['transistorCount'], 'transistors')

        pageInfo = d['data']['search']['pageInfo']
        if pageInfo['hasNextPage']:
            # We have another page, pass the endCursor into the
            # search query
            pagination = f',after:"{pageInfo["endCursor"]}"'
        else:
            break