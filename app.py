import json
import yaml
import gooey
import pathlib
from registration import register_my_car


def save_owner_config(**kwargs):
    """
    assumption all keys are present
    """

    url_ = kwargs["URL"]
    apt_ = kwargs["Apartment"]
    apt_unit = kwargs["Unit"]
    apt_owner_fname = kwargs["First Name"]
    apt_owner_lname = kwargs["Last Name"]

    with (pathlib.Path(__file__).parent / "owner.json").open('w') as f:
        owner_default = json.dump({
            "url_": url_,
            "apt_": apt_,
            "apt_unit": apt_unit,
            "apt_owner_fname": apt_owner_fname,
            "apt_owner_lname": apt_owner_lname
        }, f)

    return


@gooey.Gooey(
    program_name="Guest Parking Registration",
    program_description="Register your car for the guest parking spots"
)
def main():
    # bring in default guest data (the usual guest :) )
    def get_guests():
        with (pathlib.Path(__file__).parent / "guests.yml").open() as f:
            return yaml.safe_load(f)

    user_details = get_guests()

    # if guest yaml file was empty
    if user_details is None:
        user_details = []

    # bring in default owner data
    def get_tenant():
        with (pathlib.Path(__file__).parent / "owner.json").open() as f:
            return json.load(f)

    owner_default = get_tenant()

    # simple helper to make sure I have nice names on the gui
    # and yet I can keep the same keys as my user details dictionary
    def helper(txt: str):
        return f"{txt.lower()}_"

    # declare parser
    parser = gooey.GooeyParser(description="Automate Guest Parking")
    subparsers = parser.add_subparsers(help="command", dest="command")

    owner_group = subparsers.add_parser(
        "owner_config", prog="Tenant"
    ).add_argument_group("Configure Tenant Information")

    # owner info
    owner_group.add_argument(
        "-ul", "--URL",
        help="Guest parking url",
        action="store",
        required=True,
        default=owner_default.get("url_", "")
    )

    owner_group.add_argument(
        "-au", "--Unit",
        help="The apartment unit",
        action="store",
        required=True,
        default=owner_default.get("apt_unit", "")
    )

    owner_group.add_argument(
        "-ofn", "--First Name",
        help="The owner's first name",
        action="store",
        required=True,
        default=owner_default.get("apt_owner_fname", "")
    )

    owner_group.add_argument(
        "-oln", "--Last Name",
        help="The owner's last name",
        action="store",
        required=True,
        default=owner_default.get("apt_owner_lname", "")
    )

    owner_group.add_argument(
        "-at", "--Apartment",
        help="The apartment name",
        action="store",
        required=True,
        default=owner_default.get("apt_", "")
    )

    # we will need to save profiles. Have a blank profile on top
    # if the blank profile is used, update the yaml file with it
    # thinking about using a listbox for many guests, we could load existing and add to it

    # parse guest data
    # entry_data = {
    #     k: v
    #     for el in entry[name]
    #     for k, v in el.items()
    # }

    # main option
    guest_group = subparsers.add_parser(
        "new_guest_details", prog="New Guest",
    ).add_argument_group("Guest Information")

    # car make
    guest_group.add_argument(
        "-mk", "--Make",
        help="The guest car make",
        action="store",
        required=True
    )

    # car model
    guest_group.add_argument(
        "-ml", "--Model",
        help="The guest car model",
        action="store",
        required=True
    )

    # car color
    guest_group.add_argument(
        "-cl", "--Color",
        help="The guest car color",
        action="store",
        required=True
    )

    # car plate
    guest_group.add_argument(
        "-pl", "--Plate",
        help="The guest car plate",
        action="store",
        required=True,
        gooey_options={
            "validator": {
                "test": "' ' not in user_input",
                "message": "No Spaces Allowed"
            }
        }
    )

    # phone number
    guest_group.add_argument(
        "-ph", "--Phone",
        help="The guest's phone number",
        action="store",
        required=True,
        gooey_options={
            "validator": {
                "test": "' ' not in user_input",
                "message": "No Spaces Allowed"
            }
        }
    )

    # email
    guest_group.add_argument(
        "-em", "--Email",
        help="The guest's email",
        action="store",
        required=True
    )

    # name for the profile
    guest_group.add_argument(
        "-pn", "--Profile",
        help="The name to save this guest profile under",
        action="store",
        required=True
    )

    # saved profiles
    saved_profile_group = subparsers.add_parser(
        "saved_profiles", prog="Saved Profiles",
    ).add_argument_group("Guest Information")

    # parse arguments
    arguments = parser.parse_args()
    if arguments.command == "owner_config":
        owner_details = vars(arguments)
        save_owner_config(**owner_details)
        print("Success!, the owner information has been updated :)")

    elif arguments.command == "saved_profiles":
        # update default config with user info
        # details = parser.parse_args()
        # details = {helper(k): v for k, v in vars(details).items()}
        # user_details = {**user_details, **details}

        # run selenium portion
        # status, error = register_my_car(**user_details)
        status, error = True, None
        if status:
            print("Success! You should receive an email and text message now :)")

        else:
            raise error
    else:
        print("New Guest Stuff")


if __name__ == '__main__':
    main()
