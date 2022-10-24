# Take Home Interviews

You have been provided a repository that contains a Django, Flask, or Rails application that hosts a few endpoints. We tried to keep our implementation as simple as possible, but you should feel free to revise our code to be uniform with the code you provide. Feel free to use any homegrown or third party utilities that you feel that you need. We would like you to complete the following tasks. Please write this code like you would write production code, whatever that means to you.

## Tasks

1. Implement Battery Swapping Shift

   At revel one of the main tasks for operations is keeping our vehicles charged. We do that with a van full of batteries that drives around and swaps out the batteries for vehicles. Swapping is done in shifts by one employee for a set number of vehicles. We need to create the basic endpoints that allow us to manage shifts and the swaps on them.

   Requirements

   - create shifts
   - add vehicles to shifts
   - review all vehicles in a shift
   - complete a battery swap for a vehicle
   - check if a swap has been completed for any vehicle in a shift
   - query shift to see if all vehicles in the shift have had their battery swaps

   Design and implement the database and api for the above

2. Implement automatic shift creation. Automatic shift creation should take a lat long that it uses as a start point. Your vehicle selection should select the 20 closest vehicles to that point. The vehicles should be in the order that they should be visited to reduce the amount of distance traveled. e.g. the first vehicle in the list should be the first vehicle that should be visited the second the second and so on. Please use euclidian distance vs drive distance for simplicity.

## Implementation

### Tech stack

- Django
- DJango Rest Framework
- `drf-yasg` for automatic OpenAPI generation
- SQLite for database
- `pip-tools` for managing dependencies

### Run in local

```
make init
# activate venv
make install
```
