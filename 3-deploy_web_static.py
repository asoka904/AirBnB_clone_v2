#!/usr/bin/python3
from datetime import datetime
from fabric.api import local, put, run, env
import os.path

env.hosts = ['34.74.97.226', '18.209.18.155']
env.user = "ubuntu"


def do_pack():
    """Function to pack the contents of web_static folder
    """

    now = datetime.now()
    filename = "web_static_{}{}{}{}{}{}".format(now.year, now.month,
                                                now.day, now.hour,
                                                now.minute, now.second)
    local("mkdir -p versions")

    com = local(("tar -cvzf versions/{}.tgz web_static").format(filename))

    if com.failed is True:
        return None
    else:
        return ("versions/{}.tgz".format(filename))


def do_deploy(archive_path):
    '''distributes an archive to your web servers'''

    if os.path.exists(archive_path) is False:
        return False

    file_non_ver = archive_path.replace("versions/", "")
    file_non_ext = file_non_ver.replace(".tgz", "")
    p1 = "/data/web_static/releases/"

    try:
        put(archive_path, "/tmp/")

        run("mkdir -p /data/web_static/releases/{}/".
            format(file_non_ext))

        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(file_non_ver, file_non_ext))

        run("rm /tmp/{}".format(file_non_ver))

        run("mv {}{}/web_static/* {}{}/".
            format(p1, file_non_ext, p1, file_non_ext))

        run("rm -rf /data/web_static/releases/{}/web_static".
            format(file_non_ext))

        run("rm -rf /data/web_static/current")

        run("ln -s /data/web_static/releases/{} /data/web_static/current".
            format(file_non_ext))

        return True

    except:
        return False


def deploy():
    """Deploy an archive to servers
    """

    file_path = do_pack()

    if file_path is None:
        return False

    return do_deploy(file_path)
