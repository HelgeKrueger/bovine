# Specification

### Goal of this document

My goal here is to provide an easily referencable index
of the [ActivityPub](https://www.w3.org/TR/activitypub/#actor-objects)
and related specs, in order to reference them in Bovine
tests

## FediVerse

These are things necessary for the instance to interoperate.

#### fedi-objects-are-accessible-via-id

So if a note is published via `"id":"https://my_domain/someid"`, your
server should answer to requests to `https://my_domain/someid`.

Content-Type should be `application/activity+json`

## ActivityPub

### [Actors](https://www.w3.org/TR/activitypub/#actor-objects)

#### ap-actor-inbox

OrderedCollection comprised of messages received by the actor.
MUST

#### ap-actor-outbox

OrderedCollection comprised of messages produced by the actor.
MUST

#### ap-actor-following

collection of the actors that this actor is following  
SHOULD

#### ap-actor-followers

collection of the actors that follow this actor  
SHOULD

#### ap-actor-like

collection of objects this actor has liked  
MAY

#### ap-actor-streams

list of supplementary Collections  
MAY

#### ap-actor-preferredUsername

A short username which may be used to refer to the actor  
MAY

#### ap-actor- endpoints

huh?  
MAY

#### ap-actor-endpoints-proxyUrl

x-www-form-urlencoded id  
MAY

#### ap-actor-endpoints-oauthAuthorizationEndpoint

...  
MAY

#### ap-actor-endpoints-oauthTokenEndpoint

...  
MAY

#### ap-actor-endpoints-provideClientKey

...  
MAY

#### ap-actor-endpoints-signClientKey

...  
MAY

#### ap-actor-endpoints-sharedInbox

...  
MAY

### [Collections](https://www.w3.org/TR/activitypub/#collections)

#### ap-collections-reverse-chronological-order

An OrderedCollection MUST be presented consistently in reverse chronological order.

#### ap-collections-outbox

The outbox MUST be an OrderedCollection.

#### ap-collections-inbox

The inbox MUST be an OrderedCollection.

#### ap-collections-inbox-filter

The server SHOULD filter content according to the requester's permission.

#### ap-collections-inbox-deduplication

The server MUST perform de-duplication of activities returned by the inbox. Such deduplication MUST be performed by comparing the id of the activities and dropping any activities already seen.

#### ap-collections-inbox-federations

Non-federated servers SHOULD return a 405 Method Not Allowed upon receipt of a POST request.

#### ap-collections-followers

The followers collection MUST be either an OrderedCollection or a Collection

#### ap-collections-followers-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-collections-following

The following collection MUST be either an OrderedCollection or a Collection

#### ap-collections-following-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-collections-liked

The liked collection MUST be either an OrderedCollection or a Collection

#### ap-collections-liked-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-public-no-delivery

Implementations MUST NOT deliver to the "public" special collection; it is not capable of receiving actual activities

#### ap-collections-likes

The likes collection MUST be either an OrderedCollection or a Collection

#### ap-collections-likes-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-collections-shares

The shares collection MUST be either an OrderedCollection or a Collection

#### ap-collections-shares-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.
