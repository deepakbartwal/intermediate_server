## This was meant to be running at a wordpress server end, using wordpress database as its own database, modeling wordpress database into its own models to update the wordpress database with same users as those in any other remote server on request from that server using api calls.
- this handles updating user information such as username change, email change, name change, user creation etc.
- this handles user updating user passwords along with required hashing at the wordpress server.
- the password formed after hashing in this django app is same of that in wordpress and thus password will work in wordpress as well as django.

## This was used temporarily to update wordpress server.
## Wordpress api's served the purpose better, so, this is no longer used.
