import time
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
    **kwargs,
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
