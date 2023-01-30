# Like Activity

Here, I discuss the implementation choices, I made when designing a like activity. First an example:

```
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Like",
  "id": "https://mymath.rocks/activitypub/helge/like-1234",
  "actor": "https://mymath.rocks/activitypub/helge",
  "content": "🐮",
  "object": "https://domain/users/name/activity",
  "to": ["https://domain/users/name"],
  "cc": ["https://www.w3.org/ns/activitystreams#Public"],
  "published": "2023-01-29T16:37:18.996Z"
}

```

All properties exist in the [ActivityStreams Specification](https://www.w3.org/ns/activitystreams).
Some of the background behind these choices can be found at [SocialHub](https://socialhub.activitypub.rocks/t/like-activity/2925).

## Display

Display is handled by the Like component in `buffalo/src/components/timeline/Like.js`.

## Properties

### Content

Following the choice made by MissKey / CalcKey, I use the content property to contain the emote. As bovine is bovine themed, the used emote is a cow face by default.

**FIXME**: Citation needed

### To property

As the activity is generated in the JavaScript code of `buffalo` and then send to the outbox, it is necessary to specify the `to` property of the like.

### cc as public

This is mainly an indication that I am ok with my Like being displayed to the world, e.g. as an increased like count on the object.
