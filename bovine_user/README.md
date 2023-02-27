# bovine_user

`bovine_user` is my attempt at creating a user management system for bovine. It will provide a few features.

- [Hellō](https://www.hello.coop/index.html) will be used to provide authentication and initial authorization.
- There will be some management of public/private keys
- There probably will be a toml download for credentials to be used with the bovine ActivityPubActor ...
- There will be some management of data. A user will probably be able to choose some properties such as
  - `preferredUsername` ... which is used in the user part of the Fediverse handle `user@domain`. It is also used in webfinger, ...
  - `name` ... which is the summary
  - `summary` ... which corresponds to the bio on Mastodon

__FIXME__: Investigate if ActivityPub "servers" support multiple public keys in the `publicKey` field. See [here](https://docs.joinmastodon.org/spec/activitypub/#publicKey) and [here](https://w3c.github.io/vc-data-integrity/vocab/security/vocabulary.html#publicKey)...

__FIXME continued__:  Best to use something else to store multiple keys, e.g. a public key whose private key is known to bovine named `#server-key` and one whose private key is only known to the user named `#user-key`. However, I need to do some thinking about this stuff.
