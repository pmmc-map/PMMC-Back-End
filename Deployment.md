# Map application deployment notes

General information and notes regarding the method of deployment for our map application for the Pacific Marine Mallan Center.

## Python Flask REST API

The backend is implemented as a REST api which has the ability to return, edit, and add multiple resources relevant to the application. Resources are accessible via GET requests to the various endpoints.

## Web deployment

In order to make our REST api accessable to the frontend of the application, we are hosting our application on an Ubuntu 18 EC2 instance using AWS.

### Application Server

We are using the **Gunicorn** WSGI application server to serve our application.

A simple command to run only the WSGI application:
`gunicorn --bind 0.0.0.0:80 wsgi:app`

Specifically in our application, our WSGI entry point exists in app.py. We specify our specific gunicorn installation (because Ubuntu defaults to a Gunicorn version using Python2) and bind our application to a network port:
`sudo /home/ubuntu/.local/bin/gunicorn --bind 0.0.0.0:80 app:app`

In practice (and specifically for our deployment), manually running this command is not necessary except during testing. This is because we have configured this command to run on boot using systemctl. Our `map-app.service` file exists on our server at `/etc/systemd/system/map-app.service`

```
[Unit]
Description=Gunicorn instance to spin up and serve map-app backend
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Branch-test/PMMC-Back-End
ExecStart=/usr/bin/sudo /home/ubuntu/.local/bin/gunicorn --bind unix:/tmp/map-app.sock -m 777 app:app

[Install]
WantedBy=multi-user.target
```

The most important part of the `map-app.service` file is the `ExecStart` command. After specifying the working directory, we run the gunicorn command to start the app.

Note: In the `--bind` parameter of gunicorn, we specify a location of the unix socket file that is created when gunicorn runs. This socket file is used to connect Nginx and the wsgi server. When the application server and web server exist on the same network, using a socket is preferred because it is (slightly) faster because there is no overhead because of a TCP connection. That being said, the network port alternative is even simpler - instead of specifying a unix socket, we can simply specify a network address like `localhost:5000` as an argument to `-bind`, and later tell Nginx to find our application at this network address rather than the file path of the unix socket.

Another note: Why is gunicorn (or any application server that isn't Flask's default server) necessary? It generally is not recommended to use the Flask _development_ server for production environments. WSGI servers like gunicorn call the Flask application code when necessary, serving application requests. Flask's default server is good for local development, however it can be easily abused with multiple requests (since it isn't a real web server!). Gunicorn can create several 'workers' that can handle requests asynchronously rather than Flask's slow sequential structure. That being said, gunicorn is not intended to be front-facing towards the internet either, which is why Nginx is necessary.

#### Gunicorn systemctl commands

To start the gunicorn wsgi server: `sudo systemctl start map-app`
To check the status of the server: `sudo systemctl status map-app`
To stop the server: `sudo systemctl stop map-app`
To restart the server: `sudo systemctl restart map-app`

### Web server

We are using the **Nginx** web server in front of our application server in order to deploy our application. The Nginx server makes our application accessible to the internet, sitting in front of our wsgi application server. In a production environment, involving Nginx is preferred in order to _only_ call the application server when necessary. Nginx has the ability to handle static content requests (like css, images, etc) on its own - however this is irrelevant for the REST api portion of the app. We are specifically using Nginx because of its domain routing and HTTPS/SSL capabilities, which gunicorn lacks.

Like our gunicorn application server, Nginx starts on boot using systemctl. The relevant nginx configuration file lives at `/etc/nginx/sites-available/map-app`

```
server {
    listen 80;
    server_name www.pmmc-map.xyz 13.52.69.10;

    location / {
        include proxy_params;
	    proxy_pass http://unix:/home/ubuntu/Branch-test/PMMC-Back-End/map-app.sock;
    }
}
```

Note that we are specifying our domain and IP addresses as well as our unix socket file path.

The commands to start and stop nginx are very similar to the gunicorn systemctl commands: `sudo systemctl start nginx`.

A note about HTTPS: In order to properly respond to calls from the frontend (specifically the Fetch API), our REST API needs to be hosted with a secure connection. We are using a self-signed certificate from https://letsencrypt.org/ to achieve this. Running the certbot program adds HTTPS/SSL specific commands to our nginx configuration file specifying the location of our certificates and handling redirection from http to https.

#### All together now

To start the application server and web servers (ultimately getting the REST api open to the internet), just run the commands:

```
>>> sudo systemctl restart map-app
>>> sudo systemctl restart nginx
```

After running these commands, the REST api is accessible at https://www.pmmc-map.xyz.

Of course, these commands are only ran once (and run at boot incase the ec2 instance restarts).
