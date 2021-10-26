# microsoft-graph-api

## Foreward

This is a work in progress package for utilizing Microsoft Graph for O365.

This project serves the purpose as a personal development project as well as a hopefully useful tool for the community.

Currently this project only supports SharePoint actions since this is my current need and not all SharePoint actions are implemented.

I'm using `Protocol` to define specific interfaces so others can create their own implmentations.

## Basic Usage

`import msgraph`

`conn = msgraph.SharepointConnection()`

`sp = msgraph.SharepointGraphClient(conn)`

`response = sp.sites("YourSite/YourSubSite").lists("YourList").items().get()`

#

# SharepointConnection

## SharepointConnection Constructor

The `SharepointConnection` object utilizes refresh tokens to gain authorization.  The constructor of this object takes the following:

- `tenant_id` - Your Microsoft Tenant ID
- `client_id` - Your Client ID setup in Azure
- `client_secret` - Your Client Secret created with your Client ID
- `refresh_token` - An issued refresh token generated with the tenant and client info.
- `scope` - The authorization scope.  The Client ID should have the same scope that's being requested.

## Gaining Authorization

When `conn.headers` is called, the `SharepointConnection` object checks if the current authorization is expired and will call `conn.get_sharepoint_authorization()`.  Expiration is tracked internally on `conn.expires` property.

#

# SharepointGraphClient

Extends the `SharepointGraphClientBase` class.

Implements the `ISharepointGraphClient` protocol.

## SharepointGraphClient Constructor

- `conn:SharepointConnection` - Required

## SharepointGraphClient Methods

### `add_request(IGraphResponse)`

This method adds an object that implements the IGraphResponse protocol to the list of requests that have been handled by the client.

### `sites(relative_site_url) -> ISharepointSite`

This method returns a `SharepointSite` object and uses the passed in `relative_site_url` for building the Graph URI.  The returning of a `SharepointSite` object is intended to be used to chain method calls together for readability of the Graph request.

#

# SharepointSite

Implements the `ISharepointSite` protocol.

## SharepointSite Constructor

- `relative_site_url:str` - Required
- `client:SharepointGraphClientBase` - Required

## SharepointSite Methods

### `lists(list_name) -> ISharepointList`

- `list_name:str` - Optional

### `filters(filter_func) -> IGraphAction`

- `filter_func:Callable[...,list[IGraphFilter]]` - Required

### `documents(library_name) -> ISharepointDocumentLibrary`

- `library_name:str` - Required

### `get(url) -> IGraphResponse`

- `url:str` - Optional

### `build_url() -> str`

Returns a string relative to the organization root for the `relative_site_url` passed to the constructor.

sites/root:/sites/`relative_site_url`:/

### `build_filter_query() -> str`

## SharepointSite Usage

Calling `filters()` from `SharepointSite` object returns the instance of `SharepointSite` since this implements the `get()` method found on `IGraphAction` protocol.

Calling `get()` will return a `GraphResponseBase` which has the `Response` object from `requests.models` package.  Sends HTTP request to the endpoint generated with the `build_url()` method.

#

# SharepointList

Implements the `ISharepointList` protocol.

## SharepointList Constructor

- `parent:ISharepointSite` - Required
- `client:SharepointGraphClientBase` - Required
- `list_name:str` - Optional

## SharepointList Methods

`item(id) -> ISharepointListItem`

- `id:int` - Required

`items() -> ISharepointListItem`

`filters(filter_func) -> IGraphAction`

- `filter_func:Callable[...,list[IGraphFilter]]` - Required

`get(url) -> IGraphResponse`

- `url:str` - Optional

`build_url() -> str`

`build_filter_query() - str`
