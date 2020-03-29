from InstaSelenium import InstaSelenium
from config.public import insta_username, insta_password


def main():
    bot = InstaSelenium(insta_username, insta_password)
    bot.sign_in()

    ############################################
    # bot.comment_on_tags(tag_name='دختر_جنوبی')
    ############################################
    bot.like_tag(tag_name='girl')
    ############################################
    bot.follow_with_username('instagram')
    bot.quit()
    print('finish')


if __name__ == "__main__":
    # execute only if run as a script
    main()
