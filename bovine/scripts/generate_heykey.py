from bovine.utils.crypto.did_key import (
    generate_keys,
    private_key_to_hey_secret,
    private_key_to_secret,
    public_key_to_did_key,
    public_key_to_hey_key,
)

if __name__ == "__main__":
    print()
    print("Generating hey keys")

    private_key, public_key = generate_keys()

    print()
    print()
    print("Formats to copy and paste:")
    print("Did Format of Public Key:     ", public_key_to_did_key(public_key))
    print("Secret format of private key: ", private_key_to_secret(private_key))

    print()
    print("Formats to write down (the hey secret is enough)")
    print()
    print("Hey Key:    ", public_key_to_hey_key(public_key))
    print("Hey Secret: ", private_key_to_hey_secret(private_key))
    print()
