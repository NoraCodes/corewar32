# Arch

Basically a 5 page system:

* Home page with submission link
* Submission results page with competition times
* Login page for admin interface
* Competition setup page
* Round results page


How the rounds work:
1. Warriors selected from setup page (only people AT the booth are entered)
1. Warriors are paired or quadded up and compete against each other in n rounds
1. Overall winners are autoentered into a new round (much cause for fanfare)

This continues until there are 5 or 4 warriors left (given an even or odd starting lineup).
At that point we move to the graphical MARS for a best-of-three.

Implement in this order:
1. Single round (w -> w/2 warriors via n rounds)
1. Parse metadata in warrior
1. Insert/retrieve from database
1. Interface for submitting warriors
1. Interface for picking warriors for a tournament
1. Single round -> new single round in interface
