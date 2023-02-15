### Rooms

- /rooms .................................(GET✅, POST✅)
- /rooms/:pk .............................(PUT✅, DELETE✅)
- /rooms/:pk/amenities ...................(GET✅, POST✅)

- /amenities .............................(GET✅, POST✅)
- /amenities/:pk .........................(GET✅, PUT✅, DELETE✅)

- /rooms/:pk/reviews .....................(GET✅, POST✅, PUT❌, DELETE❌)
- /rooms/:pk/photos ......................(POST✅)

- /rooms/:pk/bookings ....................(GET✅, POST✅)
- /rooms/:pk/bookings/:pk ................(GET❌, PUT❌, DELETE❌)

- /medias/photos/:pk .....................(DELETE✅)

### Wishlists

- /wishlists .............................(GET✅, POST✅)
- /wishlists/:pk .........................(PUT✅, DELETE✅)

### Users

- /users/me ..............................(GET✅, PUT✅, DELETE❌)
- /users .................................(GET✅, POST✅)
- /users/change-password .................(PUT❌)
- /users/login ...........................(POST✅)
- /users/logout ..........................(POST)

- /users/@:username ......................(GET❌, PUT❌)
- /users/@:username/rooms ................(GET❌)
- /users/@:username/experiences ..........(GET❌)
- /users/@:username/bookings .............(GET❌)
- /users/@:username/reviews ..............(GET❌)

### Experiences

- /experiences ...........................(GET❌, POST❌)
- /experiences/:pk .......................(PUT❌, DELETE❌)
- /experiences/:pk/perks .................(GET❌, POST❌)

- /experiences/:pk/bookings ..............(GET❌, POST❌)
- /experiences/:pk/bookings/:pk ..........(GET❌, PUT❌, DELETE❌)

- /experiences/:pk/photos ................(POST❌)
