Deploy a Django application connected to Azure SQL using Docker and Azure App Service
#####################################################################################

:slug: deploy-a-django-application-connected-to-azure-sql-using-docker-and-azure-app-service
:date: 2017-05-02 18:24:42 UTC
:tags: docker, django, python
:category: DevOps
:cover: https://user-images.githubusercontent.com/4196091/119836899-662d0b80-bf02-11eb-8486-f2ea0bac2de1.png

In this post I would like to share my experience during the deployment
phase of a Django App connected to SQL Azure database. This was the
first time I used Azure to deploy my applications and I'd no idea which
approach to use. I had 2 way:

-  VM with specified size and O.S. (**IaaS**)
-  Azure App Service (**SaaS**)

Well, considering that I didn't want manage the server as whole, I
decided for the second one.

.. TEASER_END

Azure Web Apps enables you to build and host web applications in the
programming language of your choice without managing infrastructure; you
can choose several application types according to your needs and
technology.

What I used is Web App on Linux (App Service by Microsoft) and Docker.
Here a step-by-step guide try.

The database
------------

First of all let's create the database for your web project. On the
azure portal you can create your own DB (with users) using the
dashboard.

.. image:: /images/azure_db.png
   :width: 1396px
   :scale: 50 %
   :alt: azure db
   :align: center

`Here <https://docs.microsoft.com/en-us/azure/sql-database/sql-database-get-started-portal>`__ a tutorial on how to
create a SQL database in Azure. Azure SQL
Database is a “Database-as-a-Service” offering that enables you to run
and scale highly available SQL Server databases in the cloud. Once you
have a new DB you need to get the mandatory information to connect the DB to the django application.

.. image:: /images/dbazure1.png
   :align: center
   :alt: azure db


The Django App (optional if you have an existing application)
-------------------------------------------------------------

Usually with python is a best practice to use virtualenv. As *Kenneth Reitz* says:

    A Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating virtual Python environments for them. It solves the “Project X depends on version 1.x but, Project Y needs 4.x” dilemma, and keeps your global site-packages directory clean and manageable. For example, you can work on a project which requires Django 1.10 while also maintaining a project which requires Django 1.8.

So if you want to start with a new virtualenv for the project I suggest to follow
this `guide <http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/>`__; otherwise you can use the system wide
approach without create a virtual environment.

The first step is create your app with the built-in commands (in a virtualenv or not):

.. code:: bash

    $ pip install django
    $ django-admin startproject django_docker_azure

This will create a **django_docker_azure** directory in your current directory.

.. code:: bash

    django_docker_azure/
        manage.py
        django_docker_azure/
            __init__.py
            settings.py
            urls.py
            wsgi.py

Let’s verify your Django project works. Change into the outer django_docker_azure
directory, if you haven’t already, and run the following commands:

.. code:: bash

    $ python manage.py migrate # apply the migrations  on the default database
    $ python manage.py runserver

Now that the server’s running, visit
`http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`__ with your
Web browser. You’ll see a **“Welcome to Django”** page, in pleasant,
light-blue pastel. It worked!

Now we have to connect the Django app to the Azure SQL database; so we
need to install the ODBC driver on our machine. In this guide I used
Ubuntu Linux 16.04:

.. code:: bash

    $ sudo su
    $ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
    $ curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
    $ exit
    $ sudo apt-get update
    $ sudo ACCEPT_EULA=Y apt-get install msodbcsql=13.1.4.0-1 mssql-tools-14.0.3.0-1 unixodbc-dev
    $ echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
    $ echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
    $ source ~/.bashrc

If you are using other Linux distribution please refer
`here <https://docs.microsoft.com/en-us/sql/connect/odbc/linux/installing-the-microsoft-odbc-driver-for-sql-server-on-linux>`__
for more details. If you're using macosx please take a look `here: <https://docs.microsoft.com/en-us/sql/connect/odbc/mac/installing-the-microsoft-odbc-driver-for-sql-server-on-macos>`__

Let's check if installation was successfull and what drivers do we have:

.. code:: bash

    $ odbcinst -d -q

An ouptput should be as follows:

::

    [ODBC Driver 13 for SQL Server]

Configure Django with Azure SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's configure Django to use Azure SQL Database:

For first you need to install the python packages with odbc module because Django doesn't have a built-in sql_server
module

.. code:: bash

   $ pip install pyodbc django-pyodbc-azure

Now let's put the right settings for the ODBC database (Azure SQL):

.. code:: bash

    $ cd django_docker_azure
    $ vim django_docker_azure/settings.py

Edit the DATABASES section to use the values from connection string (You
should find the connections string in the Azure portal on the SQL DB
section - see the previuos figure). It should look like this:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': '<DatabaseName>',
            'USER': '<UserName>',
            'PASSWORD': '{your_password_here}',
            'HOST': '<ServerName>',
            'PORT': '<ServerPort>',
            'OPTIONS': {
                'driver': 'ODBC Driver 13 for SQL Server',
                'MARS_Connection': 'True',
            }
        }
    }


.. note:: The ``USERNAME`` and ``PASSWORD`` you must insert are the credentials you enter during the server creation.

Now you have the new DB configured, let's migrate:

::

    $ python manage.py migrate

If you recieve an output like this:

::

    Operations to perform:
      Apply all migrations: contenttypes, admin, auth, sessions
    Running migrations:
      Rendering model states... DONE
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying Auth.0007_alter_validators_add_error_messages... OK
      Applying sessions.0001_initial... OK

everything was fine, but probably You will get an error:

::

    django.core.exceptions.ImproperlyConfigured: Error loading pyodbc module: libodbc.so.2: cannot open shared object file: No such file or directory

To fix it we need to create some symbolic links for libs: "newly
installed odbc libs are not in libs PATH".

.. code:: bash

   $ sudo ln -s /usr/lib64/libodbcinst.so.2 /lib/x86_64-linux-gnu/libodbcinst.so.2
   $ sudo ln -s /usr/lib64/libodbc.so.2 /lib/x86_64-linux-gnu/libodbc.so.2

Then load new config and check if libs are loaded:

.. code:: bash

   $ sudo ldconfig
   $ ldconfig -p | grep libodbc

The output should look like this:

.. code:: bash

   libodbcinst.so.2 (libc6,x86-64) => /lib/x86_64-linux-gnu/libodbcinst.so.2
   libodbc.so.2 (libc6,x86-64) => /lib/x86_64-linux-gnu/libodbc.so.2

Now running again the django server to check if the site is up and
running:

.. code:: bash

   $ python manage.py runserver

Now your application seems work; before create the Docker container you need to create a ``requirements.txt`` file ``ìn the root directory of the app`` with all
the python packages installed for the application:

.. code:: bash

   # requirements.txt content

   django
   pyodbc
   django-pyodbc-azure


Docker container
----------------

Before you start creating the Dockerfile for the app you need to install
Docker Engin (Community Edition) reading the installation guide on
`Docker
site <https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository>`__.

Once Docker is installed on your machine, the step to getting your app
ready to run Azure Web App for Linux using Docker is to add a Docker
File.

In the root directory of your Python App create a file called
Dockerfile:

.. code:: bash

    $ touch Dockerfile

and add the following code inside the Dockerfile:

.. code-block:: dockerfile

   FROM ubuntu:16.04

   #Layer for python and gdal support
   RUN apt-get update && apt-get install -y software-properties-common curl \
       && add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get update \
       && apt-get install -y python3-pip libssl-dev libffi-dev python3-gdal \
       && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
       && update-alternatives --install /usr/bin/pip    pip    /usr/bin/pip3    10 \
       && rm -rf /var/lib/apt/lists/*

   #Begin of mandatory layers for Microsoft ODBC Driver 13 for Linux

   RUN apt-get update && apt-get install -y apt-transport-https wget

   RUN sh -c 'echo "deb [arch=amd64] https://apt-mo.trafficmanager.net/repos/mssql-ubuntu-xenial-release/ xenial main" > /etc/apt/sources.list.d/mssqlpreview.list'
   RUN apt-key adv --keyserver apt-mo.trafficmanager.net --recv-keys 417A0893
   RUN apt-get update -y
   RUN apt-get install -y libodbc1-utf16 unixodbc-utf16 unixodbc-dev-utf16
   RUN ACCEPT_EULA=Y apt-get install -y msodbcsql
   RUN apt-get install -y locales

   RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

   RUN locale-gen
   #End of mandatory layers for Microsoft ODBC Driver 13 for Linux

   RUN apt-get remove -y curl

   #Layers for the django app
   RUN mkdir /code
   WORKDIR /code
   ADD . /code/
   RUN pip install pip --upgrade
   RUN pip install -r requirements.txt

   EXPOSE 8002
   WORKDIR /code/django_docker_azure
   ENTRYPOINT ["python", "/code/manage.py", "runserver", "0.0.0.0:8002"]

Let me now explain the code whitin the Dockerfile. It uses the official ubuntu(16.04) base image; then creates a layer
where install the mandatory packages to run python3 app and the gdal library for GIS support.
Naturally if you do not need the gdal you can remove it from the installation command in the dockerfile layer

The layers following contain the same instruction used before to install
the ODBC Driver for Linux. The Dockerfie then creates a folder code and
copies all the files from the current directory into the docker image.
Next, it runs pip which installs all the library dependencies from the
requirements file (in the case of this tutorial that would just be
Django).

It opens the port 8002 and finally runs the command that launches the
website.

Build the Docker image
~~~~~~~~~~~~~~~~~~~~~~

To get your app ready for Deployment you need to build your docker
image. Run the following commands in the folder where you created your
Dockerfile:

.. code:: bash

    $ docker build -f Dockerfile -t django_docker_azure:latest .

This will download the Ubuntu base docker image (if not already local),
perform the actions in your Dockerfile (install packages, copy the
files/run pip etc...) and then assigns a tag *django_docker_azure* to the new docker
image. The part ``:latest`` is the version tag you're giving.

The build process should be finish without error messages. In this case
you can use ``docker images`` command to list the docker images builded
on your local machine.

.. code:: bash

    $ docker images # images list on your local machine

    # EXPECTED OUTPUT
    REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
    django_docker_azure          latest              accdb9539bdd        3 mins ago          848 MB
    django_gunicorn              v2                  accdb9539bdd        6 days ago          848 MB
    ubuntu                       16.04               6a2f32de169d        3 weeks ago         117 MB

To actually run and test your new docker image, run the newly created
image using docker and you should get an output like the following:

.. code:: bash

    $ docker run -p 8002:8002 -it django_docker_azure

    #should get output similar to this:

    Performing system checks...

    System check identified no issues (0 silenced).
    May 08, 2017 - 21:14:06
    Django version 1.10.6, using settings 'django_docker_azure.settings'
    Starting development server at http://127.0.0.1:8002/
    Quit the server with CONTROL-C.

You can now navigate to
`http://localhost:8002/ <http://localhost:8002/>`__ and you
should see the same page as before, but now your Django App is running inside a ``docker container``.

Well, this way to run the django app is using the built-in server that
is not a proper mode to serve the web site. In the next steps I will
explain how edit the Dockerfile to ensure that the application runs with
``gunicorn``.

First of all you need to edit the ``settings.py`` file and set the STATIC_ROOT directory to be sure that all the
static files will be collected in the specified path:

.. code:: python

   # in the settings.py file

   STATIC_ROOT = '/code/static'

Another important parameter to set in settings.py is ``ALLOWED_HOST``; it's a list of strings representing the
host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks,
which are possible even under many seemingly-safe web server configurations.

In our case the value will be ``'*'``, not safe but for this example could be fine.
I recommend you to go further reading `this part of django doc <https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts>`__.

.. code:: python

   ALLOWED_HOSTS = ['*']

Here the new Dockefile:

.. code-block:: dockerfile

   FROM ubuntu:16.04
   #Layer for python and gdal support
   RUN apt-get update && apt-get install -y software-properties-common curl \
        && add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get update \
        && apt-get install -y python3-pip libssl-dev libffi-dev python3-gdal \
        && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
        && update-alternatives --install /usr/bin/pip    pip    /usr/bin/pip3    10 \
        && rm -rf /var/lib/apt/lists/*

   #Begin of mandatory layers for Microsoft ODBC Driver 13 for Linux

   RUN apt-get update && apt-get install -y apt-transport-https wget

   RUN sh -c 'echo "deb [arch=amd64] https://apt-mo.trafficmanager.net/repos/mssql-ubuntu-xenial-release/ xenial main" > /etc/apt/sources.list.d/mssqlpreview.list'
   RUN apt-key adv --keyserver apt-mo.trafficmanager.net --recv-keys 417A0893
   RUN apt-get update -y
   RUN apt-get install -y libodbc1-utf16 unixodbc-utf16 unixodbc-dev-utf16
   RUN ACCEPT_EULA=Y apt-get install -y msodbcsql
   RUN apt-get install -y locales
   #End of mandatory layers for Microsoft ODBC Driver 13 for Linux

   RUN apt-get remove -y curl

   #Layers for the django app
   RUN mkdir /code
   WORKDIR /code
   ADD . /code/
   RUN pip install pip --upgrade
   RUN pip install -r requirements.txt
   RUN pip install gunicorn
   RUN pip install whitenoise

   RUN python manage.py collectstatic --noinput

   #Layer for exposing the app through gunicorn
   EXPOSE 8002
   COPY entrypoint.sh /code/
   WORKDIR /code
   ENTRYPOINT ["sh", "entrypoint.sh"]


As you can see in the last part of the file there are some new layer of
the container. I installed ``gunicorn`` and ``whitenoise`` via pip tool,
than run the ``collectstatic`` management Django command to be sure the
static files will be collected in the directory specified in the
settings file.

In this case I need also an entrypoint script:

.. code-block:: shell

   #!/bin/bash

   # Prepare log files and start outputting logs to stdout
   mkdir -p /code/logs
   touch /code/logs/gunicorn.log
   touch /code/logs/gunicorn-access.log
   tail -n 0 -f /code/logs/gunicorn*.log &

   export DJANGO_SETTINGS_MODULE=django_docker_azure.settings

   exec gunicorn django_docker_azure.wsgi:application \
        --name django_docker_azure \
        --bind 0.0.0.0:8002 \
        --workers 5 \
        --log-level=info \
        --log-file=/code/logs/gunicorn.log \
        --access-logfile=/code/logs/gunicorn-access.log \
   "$@"

In this *.sh* file there is the ``gunicorn`` run command for the app,
and some basig command to keep track the logs of the application.

Now rebuild the Dcokerfile:

.. code:: bash

    $ docker build -f Dockerfile -t django_docker_azure:latest .

.. code:: bash

    $ docker run -p 8002:8002 -it django_docker_azure


    #should get output similar to this:

    ==> /code/logs/gunicorn-access.log <==

    ==> /code/logs/gunicorn.log <==
    [2017-05-08 22:23:35 +0000] [1] [INFO] Starting gunicorn 19.7.1
    [2017-05-08 22:23:35 +0000] [1] [INFO] Listening at: http://0.0.0.0:8002 (1)
    [2017-05-08 22:23:35 +0000] [1] [INFO] Using worker: sync
    [2017-05-08 22:23:35 +0000] [12] [INFO] Booting worker with pid: 12
    [2017-05-08 22:23:35 +0000] [14] [INFO] Booting worker with pid: 14
    [2017-05-08 22:23:35 +0000] [16] [INFO] Booting worker with pid: 16
    [2017-05-08 22:23:35 +0000] [17] [INFO] Booting worker with pid: 17
    [2017-05-08 22:23:36 +0000] [19] [INFO] Booting worker with pid: 19

The app is up and running with ``gunicorn`` and the static files are
served by `whitenoise <http://whitenoise.evans.io/en/stable/>`__,
that allows your web app to serve its own static files, making it a
self-contained unit that can be deployed anywhere without relying on
nginx, Amazon S3 or any other external service.(Especially useful on
PaaS providers.)

Publish the Docker image
------------------------

The next step is to publish the docker image to a location where Azure
Web Apps can pull it to use inside your custom environment within the
cloud provider.

If your app is open source then you can host it in the public Docker
Hub, which is what will do in this guide. Otherwise, there are many
options for hosting a private Docker image such as `Azure Container
Service <https://azure.microsoft.com/en-us/services/container-service/>`__
or `Docker Hub
Enterprice <https://www.docker.com/pricing#/pricing_cloud>`__.

If you don't have an account on Docker Hub you have to sign up
`here <https://hub.docker.com/>`__

Next, you can tag the existing image with your Docker Hub username:

.. code:: bash

    $ docker images

    REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
    django_docker_azure          latest              f4635cafa48e        7 hours ago         848 MB
    ubuntu                       16.04               6a2f32de169d        3 weeks ago         117 MB

.. note::
   Replace the id and user name below with yours: use the ``IMAGE ID`` of the image you wanna tag and your ``username`` on dockerhub.

.. code:: bash

    $ docker tag f4635cafa48e ernestoarbitrio/django_docker_azure

Running again the ``docker images`` command you should have:

.. code:: bash

    REPOSITORY                          TAG                 IMAGE ID            CREATED             SIZE
    ernestoarbitrio/django_docker_azure latest              a27432fb588d        2 minutes ago       848 MB
    django_docker_azure                 latest              f4635cafa48e        7 hours ago         848 MB
    ubuntu                              16.04               6a2f32de169d        3 weeks ago         117 MB

Now that your image is tagged, you need to login into Docker Hub and
push the image:

.. code:: bash

    $ docker login # follow the prompt hints
    $ docker push ernestoarbitrio/django_docker_azure

and now you should now see the image on your docker hub repository.

.. image:: /images/docker_hub.png
   :alt: Docker Hub

Create the Azure Web Application
--------------------------------

Once logged in the Azure portal click the Add (+) button in the top left
corner and search for ``Web App for Linux``:

.. image:: /images/azure_step_1.png
   :alt: Azure step 1


Then select ``Web App on Linux (preview)`` and a new tab will be open.
Here you need to fill in the app ``name``, ``subscription``, ``resource group`` and
``App Service`` as in the image below.

.. note::
   The ``name`` you choose for you webapp will be the prefix of the url that Azure will assing to your web application.
   e.g. name: ``djangoazure11`` -> ``http://djangoazure11.azurewebsites.net``

.. image:: /images/azure_step_2.png
   :alt: Azure step 2


When you get to the ``Configure Container`` section you then have the
option to use a preconfigured image, Docker Hub, or private Registry. In
this example, we will choose Docker Hub and then fill in the image name
with the docker image name we just pushed in the previous step (in my
case ``ernestoarbitrio/django_docker_azure``).

Click **Ok** and then **Create**. Azure will then create the Web App for Linux
using your docker image. *It will take a couple of minutes more or less*.

We have not finished yet because we need to configure the app to use
port 8002 specified in our Dockerfile.

.. image:: /images/azure_step_3.png
   :alt: Azure step 3


Now on the `Overview` of your app click on the `URL` |url1| and your app will be shown in a new tab of the browser.

.. |url1| image:: /images/url_ref.png
          :class: inline-image

Conclusion
----------
In this tutorial, we created a new Django Web app, added a Dockerfile and then deployed the built image to an Azure Web
App for Linux. Of course you can use your favourite framework making few changes; and the same basic principles would
ork for several languages.

A complete example of this app is on `this github repository <https://github.com/ernestoarbitrio/django_docker_azure>`_.


References
----------
Part of this post is inspired by:

* http://www.jamessturtevant.com/posts/Deploying-Python-Website-To-Azure-Web-with-Docker/,
* https://lnx.azurewebsites.net/django-and-azure-sql-database-on-ubuntu-14-04-lts/