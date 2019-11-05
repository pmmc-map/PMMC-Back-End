docker build -t app_image .
docker run --network my-network -v "$(pwd):/app" --name app-server -d -p 5000:5000 app_image