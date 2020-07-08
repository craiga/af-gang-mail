"""Last email view tests."""

from http import HTTPStatus

from af_gang_mail.views import last_email


def test_last_email(settings, fs, rf):
    """Test last_email."""

    settings.EMAIL_FILE_PATH = "/fake/path"
    fs.create_file("/fake/path/b_file", contents="this is the message").st_ctime = 99
    fs.create_file("/fake/path/a_file", contents="old message").st_ctime = 10
    response = last_email(rf.get("/lastemail/"))
    assert b"".join(response.streaming_content).decode("utf-8") == "this is the message"


def test_no_files(settings, fs, rf):
    """Test last_email when there are no files in the configured email directory."""

    settings.EMAIL_FILE_PATH = "/fake/path"
    fs.create_dir("/fake/path")
    response = last_email(rf.get("/lastemail/"))
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_no_directory(settings, rf):
    """Test last_email when the configured email directory doesn't exist."""

    settings.EMAIL_FILE_PATH = "/fake/path"
    response = last_email(rf.get("/lastemail/"))
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_email_file_path_not_set(settings, rf):
    """Test last_email when EMAIL_FILE_PATH isn't set."""

    del settings.EMAIL_FILE_PATH
    response = last_email(rf.get("/lastemail/"))
    assert response.status_code == HTTPStatus.NOT_FOUND
