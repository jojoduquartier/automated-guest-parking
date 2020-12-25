# Automating Guest Parking Registration

Simple and Straight Forward python script to automate guest parking registration at my apartment. The `config.json` file added to `.gitignore` and has the following:

``` json
{
    "url_": "guests have to use this link to reserve parking spot",
    "apt_": "the name of my apartment complex",
    "apt_unit": "my apartment unit",
    "make_": "the make of the guest car, example: Fiat",
    "model_": "the model of the guest car, example: 500X",
    "color_": "the color of the guest car",
    "plate_": "the plate of the guest car",
    "phone_": "the guest phone number",
    "email_": "the guest email address",
    "apt_owner_fname": "my first name (i.e. the name on the lease)",
    "apt_owner_lname": "my last name"
}
```

It's late December 2020 and guests will be visiting (Holiday Season!). To make this parking registration app slightly more fun, I used [Gooey](https://github.com/chriskiehl/Gooey) to turn it into a real UI.

Start | Finish
----- | ------
![Start](/images/landing.png) | ![Finish](/images/finish.png)
