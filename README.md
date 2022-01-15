# How to run it?

```bash
# to database migrations and load fixtures to see something
make loadfixtures

# to run django development server
make run
```

For other possibilities run `make all` or read the `Makefile`.

# visitors-book
Visits of restaurants online as a book for other people to get knowledge where to go for a good meal

* [x] **I. Django**
  * [x] application *Restaurant visit diary*
  * [x] model Restaurant
    * [x] name
    * [x] place (GEO location)
    * [x] type (type of cousine)
  * [x] model Visit
    * [x] date (of the visit)
    * [x] expense (price)
    * [x] note (where the user can write down what he / she has given and other findings)
    * [x] evaluation (1 to 5)

***

* [ ] **II. DRF**
  * [x] **registration, login, refresh** views via API, use [JWT](https://github.com/davesque/django-rest-framework-simplejwt)
  * [x] viewsets to list, create, edit, delete **Restaurants**
  * [x] POST view to create a **Visit** of **Restaurant** - with permission given only to **User** who is also the **Creator**
  * [x] **Restaurant** listing view - showing
    * [x] all dates of **Visits**
    * [x] average rating of the **Restaurant**
    * [x] amount of time of all the visits spend in the **Restaurant**
  * [x] **Restaurant** detail view - the same as above
  * [ ] **Bonuses**
    * [ ] 1. online **REST API** documentation ([drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) or [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) use to automatically generate documentation)
    * [ ] 2. sending email when forgetting the password([write/log email to console](https://docs.djangoproject.com/en/2.2/topics/email/#console-backend))
    * [ ] 3. connect to 3rd party API (eg Zomato, which could list restaurants in a location)

***

* [x] **III. Tests**
  * [x] suggest a way to run tests
  * [x] use django unittest module and or / pousks(what is that???)
  * [x] **Bonuses**
    * [x]  use fixtures in testing

***

* [x] **IV. Project Launch**
  * [x] use **docker** (DockerFile, docker-compose, docker-compose.yml) to run **Django** and **PostgreSQL**
  * [x] script for easy execution - **Makefile**
  * [x] **Bonuses**
    * [x] pass env variables to differenciate between development and production startup
