Description
With ParkingLot API to create, user(admin), level(s), pricing (V(t) = a + b.t) and vehicle when it get in and out of parkingLot.

Dev
Luiz Almeida - All

Tecnologias
Black, Coverage, Django, Django Rest Framework and Ipdb.

Instalação
Use command python -m venv .venv to create a venv.
Use command source .venv/bin/activate to active de venv.
Use command pip install -r requirements.txt to install all tecnologies.
Use command ./manage.py makemigrations to configurate the tables.
Use command ./manage.py migrate to create the tables.
Use command ./manage.py runserver to start the server localy.

Rotas

ROOT - "/api/".
"/accounts" ["POST"] - To creater an admin user.

```
    Body request:
        {
            "username": "admin",
            "password": "1234",
            "is_superuser": true,
            "is_staff": true
        }

    Response Status: 201_CREATED
    Response:
        {
            "id": 1,
            "username": "admin",
            "is_superuser": true,
            "is_staff": true
        }
```

"login/" ["POST"] - To Authenticate admin user.

```
    Body Request:
        {
            "username": "admin",
            "password": "1234"
        }

    Response Status: 200_OK
    Response:
        {
            "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
        }
```

"levels/" ["POST"] - To create a level, must be logged as admin.

```
    Header -> Authorization: Token <admin-token>
    Body Request:
        {
            "name": "floor 1",
            "fill_priority": 2,
            "motorcycle_spaces": 20,
            "car_spaces": 50
        }

    Response Status: 201_CREATED
    Response:
        {
                "id": 1,
                "name": "floor 1",
                "fill_priority": 2,
                "available_spaces": {
                    "available_motorcycle_spaces": 20,
                    "available_car_spaces": 50
        }

```

"levels/" ["GET"] - To get level(s) list, must be logged as admin.

```
    Header -> Authorization: Token <admin-token>
    Response Status: 200_OK
    Response:
        [
            {
                "id": 1,
                "name": "floor 1",
                "fill_priority": 5,
                "available_spaces": {
                    "available_motorcycle_spaces": 20,
                    "available_car_spaces": 50
                }
            },
            {
                "id": 2,
                "name": "floor 2",
                "fill_priority": 3,
                "available_spaces": {
                    "available_motorcycle_spaces": 10,
                    "available_car_spaces": 30
                }
            }
        ]
```

"pricings/" ["POST"] - To register new pricing, must be logged as admin.

The Pricing will follow this equation

V(t) = a + b.t

Where:

- V is how much must be paid.

- a is the minium payment.

- b is the multiplier of time that vehicle stayed.

- t is the time that vehicle stayed.

```
    Header -> Authorization: Token <admin-token>
    Body Request:
        {
            "a_coefficient": 100,
            "b_coefficient": 100
        }

    Response Status: 201_CREATED
    Response:
        {
            "id": 1,
            "a_coefficient": 100,
            "b_coefficient": 100
        }
```

"vehicles/" ["POST"] - Register when vehicle get in the parkingLot, must be logged as admin.

Create level and pricing before register vehicle, otherwise will not be authorized to registe the vehicle.

The system will get the level based in the level's fill_priority, if it get a draw will get the level was register first.

If there is not any valiable space, it will return 404.

```
    Header -> Authorization: Token <admin-token>
    Body Request:
        {
            "vehicle_type": "car",
            "license_plate": "AYO1029"
        }

    Response Status: 201_CREATED
    Response:
        {
            "id": 1,
            "license_plate": "AYO1029",
            "vehicle_type": "car",
            "arrived_at": "2021-01-25T17:16:25.727541Z",
            "paid_at": null,
            "amount_paid": null,
            "space": {
                "id": 2,
                "variety": "car",
                "level_name": "floor 1"
            }
        }
```

"vehicles/<int:vehicle_id>/" ["PUT"] - Register when the vehicle is getting out of parkingLot and give how much the vehicle has to pay,
must be logged as admin.

```
    Response Status: 200_OK
    Response:
        {
            "license_plate": "AYO1029",
            "vehicle_type": "car",
            "arrived_at": "2021-01-21T19:36:55.364610Z",
            "paid_at": "2021-01-21T19:37:23.016452Z",
            "amount_paid": 100,
            "space": null
        }
```
