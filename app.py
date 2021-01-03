import json
import yaml
import gooey
import typing
import pathlib
from registration import register_my_car

# constant
guest_path = pathlib.Path(__file__).parent / "guests.yml"


def save_owner_config(**kwargs):
    """
    assumption all keys are present
    """

    url_ = kwargs["URL"]
    apt_ = kwargs["Apartment"]
    apt_unit = kwargs["Unit"]
    apt_owner_fname = kwargs["First Name"]
    apt_owner_lname = kwargs["Last Name"]

    file_path = pathlib.Path(__file__).parent / "owner.json"

    with file_path.open('w') as f:
        json.dump({
            "url_": url_,
            "apt_": apt_,
            "apt_unit": apt_unit,
            "apt_owner_fname": apt_owner_fname,
            "apt_owner_lname": apt_owner_lname
        }, f)

    return


def get_guests():
    if not guest_path.exists():
        guest_path.touch()
        return []

    with guest_path.open() as f:
        output = yaml.safe_load(f)

    if output is None:
        return []

    return output


def get_tenant():
    file_path = pathlib.Path(__file__).parent / "owner.json"

    if not file_path.exists():
        file_path.touch()
        return {}

    with file_path.open() as f:
        output = json.load(f)

    if output is None:
        return {}

    return output


def dump(entry: typing.Dict[str, typing.List[typing.Dict[str, str]]]):
    output = """"""
    k, v = tuple(entry.items())[0]

    output += k
    output += "\n\t- "

    max_len = max(len(x) for y in v for _, x in y.items())

    for i, dct in enumerate(v):
        _, v_ = tuple(dct.items())[0]
        output += v_

        if i + 1 != len(v):
            output += "\n\t- "

    return output


@gooey.Gooey(
    program_name="Guest Parking Registration",
    program_description="Register your car for the guest parking spots"
)
def main():
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
        default=get_tenant().get("url_", "")
    )

    owner_group.add_argument(
        "-au", "--Unit",
        help="The apartment unit",
        action="store",
        required=True,
        default=get_tenant().get("apt_unit", "")
    )

    owner_group.add_argument(
        "-ofn", "--First Name",
        help="The owner's first name",
        action="store",
        required=True,
        default=get_tenant().get("apt_owner_fname", "")
    )

    owner_group.add_argument(
        "-oln", "--Last Name",
        help="The owner's last name",
        action="store",
        required=True,
        default=get_tenant().get("apt_owner_lname", "")
    )

    owner_group.add_argument(
        "-at", "--Apartment",
        help="The apartment name",
        action="store",
        required=True,
        default=get_tenant().get("apt_", "")
    )

    # main option
    guest_group = subparsers.add_parser(
        "new_guest_details", prog="New Guest",
    ).add_argument_group("Guest Information - you can overwrite profiles")

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

    # helper function to add entries to group
    def add_guests(group):
        for i, entry in enumerate(get_guests()):
            name = next(k for k in entry.keys())
            group.add_argument(
                f"--user_{i}",
                metavar=name,
                action="store_true"
            )

        return

    # saved profiles
    saved_profile_group = subparsers.add_parser(
        "saved_profiles", prog="Saved Profiles"
    ).add_argument_group("Profiles").add_mutually_exclusive_group(
        "Guest Profiles",
        gooey_options=dict(title="Choose one Profile")
    )

    # View a Profile
    view_a_profile_group = subparsers.add_parser(
        "view_profiles", prog="View a Profile"
    ).add_argument_group("Profiles").add_mutually_exclusive_group(
        "Guest Profiles",
        gooey_options=dict(title="Choose one Profile")
    )

    # Delete profiles
    delete_profiles_group = subparsers.add_parser(
        "delete_profiles", prog="Delete Profiles"
    ).add_argument_group("Profiles").add_mutually_exclusive_group(
        "Guest Profiles",
        gooey_options=dict(title="Choose one Profile")
    )

    # add entries
    add_guests(saved_profile_group)
    add_guests(view_a_profile_group)
    add_guests(delete_profiles_group)

    # parse arguments
    arguments = parser.parse_args()

    def get_selected(args=arguments):
        details = vars(arguments)
        selected = next(
            k
            for k, v in details.items()
            if k.startswith('user_')
            if v
        )

        selected = int(selected.replace("user_", ''))

        return get_guests()[selected], selected

    def register_selection(args=arguments):
        tenant_details = get_tenant()
        selected, _ = get_selected(arguments)
        profile = next(k for k in selected.keys())
        selected = {
            k: v
            for el in selected[profile]
            for k, v in el.items()
        }

        user_details = {**tenant_details, **selected}

        return user_details

    if arguments.command == "owner_config":
        # save teant info
        owner_details = vars(arguments)
        save_owner_config(**owner_details)
        print("Success!, the owner information has been updated :)")

    elif arguments.command == "saved_profiles":
        
        if len(get_tenant()) == 0:
            print("Please configure the tenant information :)")
            return

        # compile user details
        user_details = register_selection(arguments)

        # run selenium portion
        status, error = register_my_car(**user_details)

        if status:
            print("Success! You should receive an email and text message now :)")

        else:
            raise error

    elif arguments.command == "delete_profiles":
        # get selected profile
        selected, index = get_selected(arguments)
        selected = dump(selected)

        guests_list = get_guests()
        _ = guests_list.pop(index)

        try:
            with guest_path.open('w') as f:
                yaml.dump(guests_list, f)

            print("Successfully deleted profile:\n")
            print(selected)

        except Exception as e:
            print("Failed to delete the profile!\n")
            raise e

    elif arguments.command == "view_profiles":
        # get selected profile
        selected, _ = get_selected(arguments)
        selected = dump(selected)
        print(selected)
        print(
            "\n\nTo overwrite, go to 'New Guest' and add a profile with this profile name"
        )

    else:
        # identify guest info
        guest = vars(arguments)
        profile = guest["Profile"]

        # if this profile exists, pop it
        guest_list = get_guests()

        index = [
            i
            for i, v in enumerate(guest_list)
            if profile in v.keys()
        ]

        if len(index) > 0:
            _ = guest_list.pop(index[0])

        # now we can add the new item
        entry = {profile: []}
        keys_to_allow = ('Color', 'Email', 'Make', 'Model', 'Phone', 'Plate')

        for k, v in guest.items():
            if k not in keys_to_allow:
                continue

            entry[profile].append(
                {helper(k): v}
            )

        guest_list.append(entry)

        # save to guests yaml file
        try:
            with guest_path.open('w') as f:
                yaml.dump(guest_list, f)

            if len(index) > 0:
                print("Successfully updated the profile!")

            else:
                print("Successfully saved new profile!")

        except Exception as _:
            print("Unable to save this profile at the moment :(")

        # register
        guest_details = {
            helper(k): v
            for k, v in guest.items()
            if k in keys_to_allow
        }

        tenant_details = get_tenant()
        
        if len(tenant_details) == 0:
            print("Please configure the tenant information :)")
            return

        user_details = {**tenant_details, **guest_details}

        # run selenium portion
        status, error = register_my_car(**user_details)

        if status:
            print("Success! You should receive an email and text message now :)")

        else:
            raise error


if __name__ == '__main__':
    main()
