# Project Name

## Description

Image analysis project using Python+DjangoREST and Google Cloud Vision API

## Table of Contents

- [API Usage](#api-usage)
- [Docker Usage](#docker-usage)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## API Usage

### /api/analyze-image

To analyze an image, make a POST request to `http://localhost:8000/api/analyze-image` endpoint with the following requirements:

- The request must be an image file, the supported formats are: 'JPEG', 'PNG','GIF', 'BMP', 'WEBP', 'RAW', 'ICO', 'PDF', 'TIFF', 'JPG'.
- The image file must be sent as the request body.
- The image dimensions needs to be a minimun of 640x480px
- The image size does not be larger than 20MB
- If the image does not contain objects or information a error will thrown

## Docker Usage

To run the project using Docker, follow these steps:

1. Make sure you have Docker installed on your machine.

2. Clone the repository:

   ```bash
   git clone https://github.com/abrahambrons/djangorest-image-analyzer.git
   ```

3. Navigate to the project directory:

   ```bash
   cd djangorest-image-analyzer
   ```

4. Build the Docker image:

   ```bash
   docker build -t image-analysis-api .
   ```

5. Run the Docker container:

   ```bash
   docker run -p 8000:8000 image-analysis-api
   ```

6. Add your own `credentials.json` file on the root of the project, you can generate one by creating a service account in google cloud console and enabling the google cloud vision API

7. Access the API at `http://localhost:8000/api/analyze-image`.

8. To stop the container, press `Ctrl + C`.

9. To remove the container, run:

   ```bash
   docker rm -f $(docker ps -aq --filter name=image-analysis-api)
   ```

10. To remove the Docker image, run:

```bash
docker rmi image-analysis-api
```

## Installation

git clone https://github.com/abrahambrons/djangorest-image-analyzer.git

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the original repository.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You can find the full text of the license in the [LICENSE](LICENSE) file.
