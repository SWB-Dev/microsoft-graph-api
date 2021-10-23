import os

from requests.models import Response

from src import IGraphResponse, SharepointConnection, SharepointGraphClient

def create_connection() -> SharepointConnection:
    conn = SharepointConnection(
        os.environ['TENANT_ID'],
        os.environ['CLIENT_ID'],
        os.environ['CLIENT_SECRET'],
        os.environ['SP_REFRESH_TOKEN'],
        'sites.manage.all'
    )

    return conn

def setup() -> SharepointGraphClient:
    conn = create_connection()
    return SharepointGraphClient(conn)

def report(response: IGraphResponse, client:SharepointGraphClient):
    for r in response.response:
        if isinstance(r, Response):
            print("=================REQUEST===================")
            print("Request:",r.request.url)
            print("Response:",r.json())
    
    print("Client request count:",len(client.requests))

def test_site_build_url():
    sp = setup()

    site_url = sp.sites("OrderToCash").build_url()
    print(site_url)

def test_list_build_url():
    sp = setup()

    list_url = sp.sites("OrderToCash/creditandcollections").lists("CreditHoldList").build_url()
    print(list_url)

def test_site_get():
    sp = setup()

    resp = sp.sites("OrderToCash").get()

    report(resp, sp)

def test_site_lists_get():
    sp = setup()

    resp = sp.sites("OrderToCash/creditandcollections").lists("CreditHoldList").get()

    report(resp, sp)

def test_lists_items_get():
    sp = setup()

    resp = sp.sites("OrderToCash/creditandcollections").lists("CreditHoldList").items().get()

    report(resp, sp)
