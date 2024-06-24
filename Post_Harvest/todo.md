farmer

1. signup (
     - getting the phone number
     - saving the user [
        set a random email for a farmer
        set a random password (hashed)
     ]
)

2. verify (
    - recieve code
    - query user from the DB with that code
)




func for setting random email for farmer 

    randomNumber = random.randInt(1000,78874)

    email = f"{randomNumber}@gmail.com"

    request.data["email"] = email


status codes for responses(
    ok : 200,
    update: 202,
    create: 201,
    bad: 400
)

