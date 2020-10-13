import os

from authentication.models import User


def get_base_fixed_path(user_id):
    BASE_PATH = os.path.dirname(os.path.dirname(__file__))
    BASE_PATH = BASE_PATH.replace('\\', '/')
    common_path = BASE_PATH + "/media/user_" + \
        str(user_id) + "/"

    file_update_base_path = "user_" + str(user_id) + "/"

    return common_path, file_update_base_path


def check_file_path_exists_or_create_dir(pathfile):
    if not os.path.exists(pathfile):
        os.mkdir(pathfile)
