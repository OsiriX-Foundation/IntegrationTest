import env
import rq_album
import rq_studies
import util


# TODO: Can these first three be moved to another (generic) file?

def test_init():
    env.initialize()


def test_get_token():
    print()
    token = util.get_token(username="titi@gmail.com", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto@gmail.com", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata@gmail.com", password="tata")
    env.env_var["USER_3_TOKEN"] = token
    token = util.get_token(username="karnak@gmail.com", password="karnak")
    env.env_var["USER_KARNAK_TOKEN"] = token


def test_register():
    util.register(token=env.env_var['USER_1_TOKEN'])
    util.register(token=env.env_var['USER_2_TOKEN'])
    util.register(token=env.env_var['USER_3_TOKEN'])
    util.register(token=env.env_var['USER_KARNAK_TOKEN'])


def test_new_album():
    album = rq_album.create(token=env.env_var.get("USER_1_TOKEN"))
    env.env_var["ALBUM_ID"] = album["album_id"]


def test_stow():
    params = {"album": env.env_var.get("ALBUM_ID")}
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), params=params)


def test_album_studies_list():
    params = {"album": env.env_var.get("ALBUM_ID")}
    rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=1)


def test_add_study_from_album_to_favorites():
    params = {"Album": env.env_var.get("ALBUM_ID")}

    rq_studies.add_favorite_from_album(env.env_var.get("USER_1_TOKEN"), params, env.env_var.get("ALBUM_ID"))

    # Fails here
    # params = {"favorite": True, "Album": env.env_var.get("ALBUM_ID")}
    params = {"Album": env.env_var.get("ALBUM_ID")}
    list_studies = rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params)

    # Get the study, check it's a favorite?
    assert len(list_studies) == 1


def test_remove_study_from_album_from_favorites():
    rq_studies.remove_favorite_from_album(env.env_var.get("USER_1_TOKEN"), env.env_var.get("STUDY_UID"),
                                          env.env_var.get("ALBUM_ID"))

    list_studies = rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"))

    # Get the study, check it's not a favorite?
    assert len(list_studies) == 0


# TODO
def test_add_study_to_inbox():
    rq_studies.add_in_inbox(env.env_var["USER_1_TOKEN"], env.env_var["STUDY_UID"], env.env_var["ALBUM_ID"])


def test_add_study_from_inbox_to_favorites():
    rq_studies.add_favorite_from_album(env.env_var.get("USER_1_TOKEN"), env.env_var.get("STUDY_UID"),
                                       env.env_var.get("ALBUM_ID"))

    params = {"Album": env.env_var.get("ALBUM_ID")}
    list_studies = rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params)

    assert len(list_studies) == 1

# def test_remove_study_from_inbox_from_favorites():


def test_clean_all():
    # rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])