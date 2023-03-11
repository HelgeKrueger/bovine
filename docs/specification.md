# Specification

## Introduction

### Goal of this document

My goal here is to provide an easily referencable index
of the [ActivityPub](https://www.w3.org/TR/activitypub/#actor-objects)
and related specs, in order to reference them in Bovine
tests

### Usage

This template is to be used in combination with the
`make_specification.py` script. It is meant to scan your implementation
for the usage of the here provided ids and then create a markdown
document `specification.md` containing links to the implementation.

## FediVerse

These are things necessary for the instance to interoperate.
Generally everything starting with `fedi-` corresponds to something
needed to be a citizen in the Fediverse, that I couldn't find
in any spec.

### General properties

#### fedi-objects-are-accessible-via-id

- [blog_test_env.py](../tests/utils/blog_test_env.py#L94)
- [test_create_note.py](../tests/tests/outbox/test_create_note.py#L43)

So if a note is published via `"id":"https://my_domain/someid"`, your
server should answer to requests to `https://my_domain/someid`.

#### fedi-objects-are-accessible-via-id-content-type

- [blog_test_env.py](../tests/utils/blog_test_env.py#L94)

Content-Type should be `application/activity+json`

#### fedi-objects-have-html-representations

- [test_create_note.py](../tests/tests/outbox/test_create_note.py#L54)

By requesting an object with `Accept` header `text/html` (or similar)
one is redirected to a webpage, featuring said activity.

### Webfinger

Webfinger is specified in [RFC-7033](https://datatracker.ietf.org/doc/html/rfc7033).

#### webfinger-subject

- [test_webfinger.py](../tests/tests/test_webfinger.py#L20)

[Subject](https://datatracker.ietf.org/doc/html/rfc7033#section-4.4.1) should be present.

#### webfinger-content-type

- [test_webfinger.py](../tests/tests/test_webfinger.py#L15)

[RFC-7033 Section 10.2](https://datatracker.ietf.org/doc/html/rfc7033#section-10.2) specifies
that the answer to a webfinger request should have content-type `application/jrd+json`.
Jrd stands for _JSON Resource Descriptor_.

#### fedi-webfinger-self

- [test_webfinger.py](../tests/tests/test_webfinger.py#L23)

The [links](https://datatracker.ietf.org/doc/html/rfc7033#section-4.4.4) of the webfinger
response contain an element with `"rel":"self"` and `"type":"application/activity+json"`
pointing to the activity pub actor profile.

#### fedi-webfinger-username-is-preferredUsername

- [test_webfinger.py](../tests/tests/test_webfinger.py#L33)

The entry of `preferredUsername` in the actor profile obtained above corresponds
to the username part of the account used in webfinger.

## ActivityPub

### [Actors](https://www.w3.org/TR/activitypub/#actor-objects)

#### ap-actor-inbox

- [test_actor.py](../tests/tests/test_actor.py#L16)

A reference to an ActivityStreams OrderedCollection comprised of all the messages received by the actor.
See [5.2 Inbox](https://www.w3.org/TR/activitypub/#inbox)

#### ap-collections-inbox-filter

The server SHOULD filter content according to the requester's permission.

#### ap-collections-inbox-deduplication

The server MUST perform de-duplication of activities returned by the inbox. Such deduplication MUST be performed by comparing the id of the activities and dropping any activities already seen.

#### ap-collections-inbox-federations

Non-federated servers SHOULD return a 405 Method Not Allowed upon receipt of a POST request.

#### ap-actor-outbox

- [test_actor.py](../tests/tests/test_actor.py#L20)

An ActivityStreams OrderedCollection comprised of all the messages produced by the actor;
see [5.1 Outbox](https://www.w3.org/TR/activitypub/#outbox).

#### ap-actor-following

- [test_actor.py](../tests/tests/test_actor.py#L23)

A link to an ActivityStreams collection of the actors that this actor is following;
see [5.4 Following Collection](https://www.w3.org/TR/activitypub/#following)

#### ap-collections-following

- [test_actor.py](../tests/tests/test_actor.py#L25)

The following collection MUST be either an OrderedCollection or a Collection

#### ap-collections-following-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-actor-followers

- [test_actor.py](../tests/tests/test_actor.py#L28)

A link to an \[ActivityStreams\] collection of the actors that follow this actor;
see [5.3 Followers Collection](https://www.w3.org/TR/activitypub/#followers)

#### ap-collections-followers

- [test_actor.py](../tests/tests/test_actor.py#L30)

The followers collection MUST be either an OrderedCollection or a Collection

#### ap-collections-followers-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-actor-like

A link to an \[ActivityStreams\] collection of objects this actor has liked;
see [5.5 Liked Collection](https://www.w3.org/TR/activitypub/#liked).

#### ap-collections-likes

The likes collection MUST be either an OrderedCollection or a Collection

#### ap-collections-likes-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-actor-streams

__MAY__: A list of supplementary Collections which may be of interest.

#### ap-actor-preferredUsername

- [test_actor.py](../tests/tests/test_actor.py#L12)

A short username which may be used to refer to the actor. Note due to [fedi-webfinger-username-is-preferredUsername](#fedi-webfinger-username-is-preferredUsername) the preferredUsername must be present for an application to federate.

#### ap-actor-endpoints

- [test_actor.py](../tests/tests/test_actor.py#L33)
- [test_actor.py](../tests/tests/test_actor.py#L36)

#### ap-actor-endpoints-proxyUrl

- [test_actor.py](../tests/tests/test_actor.py#L36)

#### ap-actor-endpoints-oauthAuthorizationEndpoint

#### ap-actor-endpoints-oauthTokenEndpoint

#### ap-actor-endpoints-provideClientKey

#### ap-actor-endpoints-signClientKey

#### ap-actor-endpoints-sharedInbox

### [Collections](https://www.w3.org/TR/activitypub/#collections)

#### ap-collections-reverse-chronological-order

- [test_create_many_notes.py](../tests/tests/outbox/test_create_many_notes.py#L35)
- [test_create_many_notes.py](../tests/tests/outbox/test_create_many_notes.py#L51)

An OrderedCollection MUST be presented consistently in reverse chronological order.

#### ap-collections-liked

The liked collection MUST be either an OrderedCollection or a Collection

#### ap-collections-liked-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

#### ap-public-no-delivery

Implementations MUST NOT deliver to the "public" special collection; it is not capable of receiving actual activities

#### ap-collections-shares

The shares collection MUST be either an OrderedCollection or a Collection

#### ap-collections-shares-filter

MAY be filtered on privileges of an authenticated user or as appropriate when no authentication is given.

### ActivityPub Client

These are found in [Client To Server](https://www.w3.org/TR/activitypub/#client-to-server-interactions)

#### ap-client-addressing

Clients SHOULD look at any objects attached to the new Activity via the object, target, inReplyTo and/or tag fields, retrieve their actor or attributedTo properties, and MAY also retrieve their addressing properties, and add these to the to or cc fields of the new Activity being created. Clients MAY recurse through attached objects, but if doing so, SHOULD set a limit for this recursion. (Note that this does not suggest that the client should "unpack" collections of actors being addressed as individual recipients).

Clients MAY give the user the chance to amend this addressing in the UI.

#### ap-client-provide-object-target

Clients submitting the following activities to an outbox MUST provide the object property in the activity: Create, Update, Delete, Follow, Add, Remove, Like, Block, Undo. Additionally, clients submitting the following activities to an outbox MUST also provide the target property: Add, Remove.

### [Client To Server](https://www.w3.org/TR/activitypub/#client-to-server-interactions)

#### ap-c2s-post

- [blog_test_env.py](../tests/utils/blog_test_env.py#L61)

Client to server interaction takes place through clients posting Activities to an actor's outbox. To do this, clients MUST discover the URL of the actor's outbox from their profile and then MUST make an HTTP POST request to this URL with the Content-Type of application/ld+json; profile="https://www.w3.org/ns/activitystreams". Servers MAY interpret a Content-Type or Accept header of application/activity+json as equivalent to application/ld+json; profile="https://www.w3.org/ns/activitystreams" for client-to-server interactions. The request MUST be authenticated with the credentials of the user to whom the outbox belongs. The body of the POST request MUST contain a single Activity (which MAY contain embedded objects), or a single non-Activity object which will be wrapped in a Create activity by the server.

#### ap-c2s-new-id

- [test_create_note.py](../tests/tests/outbox/test_create_note.py#L40)

If an Activity is submitted with a value in the id property, servers MUST ignore this and generate a new id for the Activity.

#### ap-c2s-status-code

- [test_follow_then_accept_added_to_following.py](../tests/tests/outbox/test_follow_then_accept_added_to_following.py#L34)
- [test_follow_then_accept_added_to_following_full_accept.py](../tests/tests/outbox/test_follow_then_accept_added_to_following_full_accept.py#L36)

Servers MUST return a 201 Created HTTP code, and unless the activity is transient, MUST include the new id in the Location header.

#### ap-c2s-no-bto-bcc

The server MUST remove the bto and/or bcc properties, if they exist, from the ActivityStreams object before delivery, but MUST utilize the addressing originally stored on the bto / bcc properties for determining recipients in delivery.

#### ap-c2s-add-to-outbox

- [test_create_note.py](../tests/tests/outbox/test_create_note.py#L24)

The server MUST then add this new Activity to the outbox collection. Depending on the type of Activity, servers may then be required to carry out further side effects. (However, there is no guarantee that time the Activity may appear in the outbox. The Activity might appear after a delay or disappear at any period). These are described per individual Activity below.

#### ap-c2s-create-attributedTo

When a Create activity is posted, the actor of the activity SHOULD be copied onto the object's attributedTo field.

#### ap-c2s-create-addressing

A mismatch between addressing of the Create activity and its object is likely to lead to confusion. As such, a server SHOULD copy any recipients of the Create activity to its object upon initial distribution, and likewise with copying recipients from the object to the wrapping Create activity. Note that it is acceptable for the object's addressing to be changed later without changing the Create's addressing (for example via an Update activity).

#### ap-c2s-post-non-activity

For client to server posting, it is possible to submit an object for creation without a surrounding activity. The server MUST accept a valid ActivityStreams object that isn't a subtype of Activity in the POST request to the outbox. The server then MUST attach this object as the object of a Create Activity. For non-transient objects, the server MUST attach an id to both the wrapping Create and its wrapped Object.

Any to, bto, cc, bcc, and audience properties specified on the object MUST be copied over to the new Create activity by the server.

#### ap-c2s-update-activity

The Update activity is used when updating an already existing object. The side effect of this is that the object MUST be modified to reflect the new structure as defined in the update activity, assuming the actor has permission to update this object.

#### ap-c2s-delete-activity

- [test_create_then_delete.py](../tests/tests/outbox/test_create_then_delete.py#L26)

The Delete activity is used to delete an already existing object. The side effect of this is that the server MAY replace the object with a Tombstone of the object that will be displayed in activities which reference the deleted object. If the deleted object is requested the server SHOULD respond with either the HTTP 410 Gone status code if a Tombstone object is presented as the response body, otherwise respond with a HTTP 404 Not Found.

#### ap-c2s-follow-activity

- [test_on_accept_is_added_to_followers.py](../tests/tests/outbox/test_on_accept_is_added_to_followers.py#L62)

The side effect of receiving this in an outbox is that the server SHOULD add the object to the actor's following Collection when and only if an Accept activity is subsequently received with this Follow activity as its object.

#### ap-c2s-add-activity

Upon receipt of an Add activity into the outbox, the server SHOULD add the object to the collection specified in the target property, unless:

#### ap-c2s-remove-activity

Upon receipt of a Remove activity into the outbox, the server SHOULD remove the object from the collection specified in the target property, unless:

#### ap-c2s-like-activity

The side effect of receiving this in an outbox is that the server SHOULD add the object to the actor's liked Collection.

#### ap-c2s-block-activity

The Block activity is used to indicate that the posting actor does not want another actor (defined in the object property) to be able to interact with objects posted by the actor posting the Block activity. The server SHOULD prevent the blocked user from interacting with any object posted by the actor.

Servers SHOULD NOT deliver Block Activities to their object.

#### ap-c2s-undo-activity

For example, Undo may be used to undo a previous Like, Follow, or Block. The undo activity and the activity being undone MUST both have the same actor. Side effects should be undone, to the extent possible.

#### [Server to Server](https://www.w3.org/TR/activitypub/#server-to-server-interactions)

#### ap-s2s-id

An Activity sent over the network SHOULD have an id, unless it is intended to be transient (in which case it MAY omit the id).

#### ap-s2s-content-type

POST requests (eg. to the inbox) MUST be made with a Content-Type of application/ld+json; profile="https://www.w3.org/ns/activitystreams" and GET requests (see also 3.2 Retrieving objects) with an Accept header of application/ld+json; profile="https://www.w3.org/ns/activitystreams". Servers SHOULD interpret a Content-Type or Accept header of application/activity+json as equivalent to application/ld+json; profile="https://www.w3.org/ns/activitystreams" for server-to-server interactions.

#### ap-s2s-has-object

- [test_on_accept_is_added_to_followers.py](../tests/tests/outbox/test_on_accept_is_added_to_followers.py#L96)

Servers performing delivery to the inbox or sharedInbox properties of actors on other servers MUST provide the object property in the activity: Create, Update, Delete, Follow, Add, Remove, Like, Block, Undo.

#### ap-s2s-has-target

Additionally, servers performing server to server delivery of the following activities MUST also provide the target property: Add, Remove.

#### ap-s2s-caching

HTTP caching mechanisms \[RFC7234\] SHOULD be respected when appropriate, both when receiving responses from other servers as well as sending responses to other servers.

#### ap-s2s-collection

If a recipient is a Collection or OrderedCollection, then the server MUST dereference the collection (with the user's credentials) and discover inboxes for each item in the collection

Servers MUST limit the number of layers of indirections through collections which will be performed, which MAY be one.

#### ap-s2s-deduplication

Servers MUST de-duplicate the final recipient list. Servers MUST also exclude actors from the list which are the same as the actor of the Activity being notified about. That is, actors shouldn't have their own activities delivered to themselves.

#### ap-s2s-arrival-at-inbox

An HTTP POST request (with authorization of the submitting user) is then made to the inbox, with the Activity as the body of the request. This Activity is added by the receiver as an item in the inbox OrderedCollection. Attempts to deliver to an inbox on a non-federated server SHOULD result in a 405 Method Not Allowed response.

#### ap-s2s-how-to-deliver

For federated servers performing delivery to a third party server, delivery SHOULD be performed asynchronously, and SHOULD additionally retry delivery to recipients if it fails due to network error.

#### ap-s2s-delivery

When objects are received in the outbox (for servers which support both Client to Server interactions and Server to Server Interactions), the server MUST target and deliver to:

> The to, bto, cc, bcc or audience fields if their values are individuals or Collections owned by the actor.

These fields will have been populated appropriately by the client which posted the Activity to the outbox.

#### ap-s2s-forwarding

When Activities are received in the inbox, the server needs to forward these to recipients that the origin was unable to deliver them to. To do this, the server MUST target and deliver to the values of to, cc, and/or audience if and only if all of the following are true:

> This is the first time the server has seen this Activity.
> The values of to, cc, and/or audience contain a Collection owned by the server.
> The values of inReplyTo, object, target and/or tag are objects owned by the server. The server SHOULD recurse through these values to look for linked objects owned by the server, and SHOULD set a maximum limit for recursion (ie. the point at which the thread is so deep the recipients followers may not mind if they are no longer getting updates that don't directly involve the recipient). The server MUST only target the values of to, cc, and/or audience on the original object being forwarded, and not pick up any new addressees whilst recursing through the linked objects (in case these addressees were purposefully amended by or via the client).

The server MAY filter its delivery targets according to implementation-specific rules (for example, spam filtering).

#### ap-s2s-delivery-shared-inbox

When an object is being delivered to the originating actor's followers, a server MAY reduce the number of receiving actors delivered to by identifying all followers which share the same sharedInbox who would otherwise be individual recipients and instead deliver objects to said sharedInbox.

#### ap-s2s-delivery-shared-inbox-public

Additionally, if an object is addressed to the Public special collection, a server MAY deliver that object to all known sharedInbox endpoints on the network.

#### ap-s2s-update

- [test_create_then_update_note.py](../tests/tests/inbox/test_create_then_update_note.py#L29)

For server to server interactions, an Update activity means that the receiving server SHOULD update its copy of the object of the same id to the copy supplied in the Update activity. Unlike the client to server handling of the Update activity, this is not a partial update but a complete replacement of the object.

#### ap-s2s-delete

- [test_flow_2_create_then_delete.py](../tests/tests/inbox/test_flow_2_create_then_delete.py#L18)

The side effect of receiving this is that (assuming the object is owned by the sending actor / server) the server receiving the delete activity SHOULD remove its representation of the object with the same id, and MAY replace that representation with a Tombstone object.

#### ap-s2s-follow

- [test_on_accept_is_added_to_followers.py](../tests/tests/outbox/test_on_accept_is_added_to_followers.py#L42)
- [test_on_accept_is_added_to_followers.py](../tests/tests/outbox/test_on_accept_is_added_to_followers.py#L61)

The side effect of receiving this in an inbox is that the server SHOULD generate either an Accept or Reject activity with the Follow as the object and deliver it to the actor of the Follow. The Accept or Reject MAY be generated automatically, or MAY be the result of user input (possibly after some delay in which the user reviews). Servers MAY choose to not explicitly send a Reject in response to a Follow, though implementors ought to be aware that the server sending the request could be left in an intermediate state. For example, a server might not send a Reject to protect a user's privacy.

#### ap-s2s-follow-accept

- [test_on_accept_is_added_to_followers.py](../tests/tests/outbox/test_on_accept_is_added_to_followers.py#L61)

In the case of receiving an Accept referencing this Follow as the object, the server SHOULD add the actor to the object actor's Followers Collection. In the case of a Reject, the server MUST NOT add the actor to the object actor's Followers Collection.

#### ap-s2s-accept

- [test_follow_then_accept_added_to_following_full_accept.py](../tests/tests/outbox/test_follow_then_accept_added_to_following_full_accept.py#L59)

If the object of an Accept received to an inbox is a Follow activity previously sent by the receiver, the server SHOULD add the actor to the receiver's Following Collection.

#### ap-s2s-reject

If the object of a Reject received to an inbox is a Follow activity previously sent by the receiver, this means the recipient did not approve the Follow request. The server MUST NOT add the actor to the receiver's Following Collection.

#### ap-s2s-add

Upon receipt of an Add activity into the inbox, the server SHOULD add the object to the collection specified in the target property, unless:

#### ap-s2s-remove

Upon receipt of a Remove activity into the inbox, the server SHOULD remove the object from the collection specified in the target property, unless:

#### ap-s2s-like

The side effect of receiving this in an inbox is that the server SHOULD increment the object's count of likes by adding the received activity to the likes collection if this collection is present.

#### ap-s2s-announce

Upon receipt of an Announce activity in an inbox, a server SHOULD increment the object's count of shares by adding the received activity to the shares collection if this collection is present.

#### ap-s2s-undo

The Undo activity is used to undo the side effects of previous activities. See the ActivityStreams documentation on Inverse Activities and "Undo".
