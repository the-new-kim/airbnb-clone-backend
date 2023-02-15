### Rooms

- /rooms ........................(GET✅, POST✅)
- /rooms/:pk ....................(PUT✅, DELETE✅)
- /rooms/:pk/amenities ..........(GET✅, POST✅)

- /amenities ....................(GET✅, POST✅)
- /amenities/:pk ................(GET✅, PUT✅, DELETE✅)

- /rooms/:pk/reviews ............(GET✅, POST✅, PUT, DELETE)
- /rooms/:pk/photos .............(POST✅)

- /rooms/:pk/bookings ...........(GET✅, POST✅)
- /rooms/:pk/bookings/:pk .......(GET, PUT, DELETE)

- /medias/photos/:pk ............(DELETE✅)

### Wishlists

- /wishlists ....................(GET, POST)
- /wishlists/:pk ................(PUT, DELETE)

### Users

- /users ........................(GET, POST)
- /users/rooms ..................(GET)
- /users/experiences ............(GET)
- /users/bookings ...............(GET)
- /users/:pk ....................(GET, PUT)
- /users/:pk/reviews ............(GET)

### Experiences

- /experiences ..................(GET, POST)
- /experiences/:pk ..............(PUT, DELETE)
- /experiences/:pk/perks ........(GET, POST)

- /experiences/:pk/bookings .....(GET, POST)
- /experiences/:pk/bookings/:pk .(GET, PUT, DELETE)

- /experiences/:pk/photos .......(POST)
