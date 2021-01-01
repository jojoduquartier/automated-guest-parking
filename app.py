import json
import time
import gooey
import pathlib
from selenium import webdriver


def register_my_car(
    url_,
    apt_,
    make_,
    model_,
    color_,
    plate_,
    phone_,
    email_,
    apt_unit,
    apt_owner_fname,
    apt_owner_lname,
):
    """
    Literally every step is spelled out but that is ok. Simple site.
    """
    # xattr -d com.apple.quarantine /usr/local/bin/chromedriver
    driver = webdriver.Chrome()
    driver.get(url_)

    try:
        # apartment community
        apt_input = driver.find_element_by_class_name("input__field")
        apt_input.send_keys(apt_)

        # after sending the apt there should be option to select
        time.sleep(1)
        xpath = "/html/body/div/div[2]/form/div[1]/div/div/div/ul/li"
        to_click = driver.find_element_by_xpath(xpath)
        to_click.click()

        # resident info
        xpath = "/html/body/div/div[2]/form/div[2]/div/div[1]/div/div/input"
        f_name = driver.find_element_by_xpath(xpath)
        f_name.send_keys(apt_owner_fname)

        xpath = "/html/body/div/div[2]/form/div[2]/div/div[2]/div/div/input"
        l_name = driver.find_element_by_xpath(xpath)
        l_name.send_keys(apt_owner_lname)

        xpath = "/html/body/div/div[2]/form/div[2]/div/div[3]/div/div/input"
        unit = driver.find_element_by_xpath(xpath)
        unit.send_keys(apt_unit)

        # guest info
        xpath = "/html/body/div/div[2]/form/div[3]/div/div[1]/div/div/input"
        make = driver.find_element_by_xpath(xpath)
        make.send_keys(make_)

        xpath = "/html/body/div/div[2]/form/div[3]/div/div[2]/div/div/input"
        model = driver.find_element_by_xpath(xpath)
        model.send_keys(model_)

        xpath = "/html/body/div/div[2]/form/div[3]/div/div[3]/div/div/input"
        color = driver.find_element_by_xpath(xpath)
        color.send_keys(color_)

        xpath = "/html/body/div/div[2]/form/div[3]/div/div[4]/div/div/input"
        plate = driver.find_element_by_xpath(xpath)
        plate.send_keys(plate_)

        # guest contact
        xpath = "/html/body/div/div[2]/form/div[4]/div/div[1]/div/div/input"
        phone = driver.find_element_by_xpath(xpath)
        phone.send_keys(phone_)

        xpath = "/html/body/div/div[2]/form/div[4]/div/div[2]/div[2]/div/input"
        email = driver.find_element_by_xpath(xpath)
        email.send_keys(email_)

        # submit
        submit = driver.find_element_by_tag_name("button")
        submit.submit()

    except Exception as e:
        return False, e

    finally:
        time.sleep(1)
        driver.close()

    return True, None


def save_owner_config(**kwargs):
    """
    assumption all keys are present
    """

    url_ = kwargs["URL"]
    apt_ = kwargs["Apartment"]
    apt_unit = kwargs["Unit"]
    apt_owner_fname = kwargs["First Name"]
    apt_owner_lname = kwargs["Last Name"]

    print(kwargs)
    return None


@gooey.Gooey(
    tabbed_groups=True,
    program_name="Guest Parking Registration",
    program_description="Register your car for the guest parking spots"
)
def main():
    # bring in default guest data (the usual guest :) )
    with (pathlib.Path(__file__).parent / "config.json").open() as f:
        user_details = json.load(f)

    # simple helper to make sure I have nice names on the gui
    # and yet I can keep the same keys as my user details dictionary
    def helper(txt: str):
        return f"{txt.lower()}_"

    # declare parser
    parser = gooey.GooeyParser(description="Automate Guest Parking")
    guest_group = parser.add_argument_group("Guest Information")
    owner_group = parser.add_argument_group("Configure Tenant Information")

    # owner info
    owner_group.add_argument(
        "-ul", "--URL",
        help="Guest parking url",
        action="store"
    )

    owner_group.add_argument(
        "-au", "--Unit",
        help="The apartment unit",
        action="store"
    )

    owner_group.add_argument(
        "-ofn", "--First Name",
        help="The owner's first name",
        action="store"
    )

    owner_group.add_argument(
        "-oln", "--Last Name",
        help="The owner's last name",
        action="store"
    )

    owner_group.add_argument(
        "-at", "--Apartment",
        help="The apartment name",
        action="store"
    )

    # we will need to save profiles. Have a blank profile on top
    # if the blank profile is used, update the yaml file with it
    # thinking about using a listbox for many guests, we could load existing and add to it

    # parse guest data
    guest_group.add_argument(
        "-mk", "--Make",
        help="The guest car make",
        action="store",
        default=user_details["make_"]
    )
    guest_group.add_argument(
        "-ml", "--Model",
        help="The guest car model",
        action="store",
        default=user_details["model_"]
    )
    guest_group.add_argument(
        "-cl", "--Color",
        help="The guest car color",
        action="store",
        default=user_details["color_"]
    )
    guest_group.add_argument(
        "-pl", "--Plate",
        help="The guest car plate",
        action="store",
        default=user_details["plate_"],
        gooey_options={
            "validator": {
                "test": "' ' not in user_input",
                "message": "No Spaces Allowed"
            }
        }
    )
    guest_group.add_argument(
        "-ph", "--Phone",
        help="The guest's phone number",
        action="store",
        default=user_details["phone_"],
        gooey_options={
            "validator": {
                "test": "' ' not in user_input",
                "message": "No Spaces Allowed"
            }
        }
    )
    guest_group.add_argument(
        "-em", "--Email",
        help="The guest's email",
        action="store",
        default=user_details["email_"]
    )

    # owner config
    owner_details = parser.parse_args()

    # update default config with user info
    details = parser.parse_args()
    details = {helper(k): v for k, v in vars(details).items()}
    user_details = {**user_details, **details}

    # run selenium portion
    # status, error = register_my_car(**user_details)
    status, error = True, None
    if status:
        print("Success! You should receive an email and text message now :)")

    else:
        raise error


if __name__ == '__main__':
    main()
