# Photo Proxy

A Home Assistant add-on that serves random images from your Nextcloud server. This add-on provides endpoints to fetch random images, which can be used to display them in Home Assistant or other applications.

## Features

- Serves random images from your Nextcloud server
- Supports multiple directories
- Provides a status page with service information
- Health check endpoint
- Docker-based deployment
- Easy configuration through Home Assistant UI

## Installation

1. Add this repository to your Home Assistant instance:
   - Go to Settings > Add-ons > Add-on Store
   - Click the three dots menu in the top right
   - Select "Repositories"
   - Add the URL: `https://github.com/joergrs/photo-proxy`

2. Install the "Photo Proxy" add-on from the Add-on Store

3. Configure the add-on with your Nextcloud credentials:
   - Nextcloud URL: Your Nextcloud server URL
   - Username: Your Nextcloud username
   - Password: Your Nextcloud password
   - Directories: Comma-separated list of directories to fetch images from

4. Start the add-on

## Usage

The add-on provides the following endpoints:

- `http://[HOST]:[PORT:8181]/random` - Get a random image
- `http://[HOST]:[PORT:8181]/next` - Get the next image in sequence
- `http://[HOST]:[PORT:8181]/health` - Health check endpoint
- `http://[HOST]:[PORT:8181]/` - Status page with service information

### Using with Home Assistant Generic Camera

You can use the `/random` endpoint as an image source for a generic camera in Home Assistant. This allows you to display random images from your Nextcloud server in your dashboard or as a background.

Add the following to your `configuration.yaml`:

```yaml
camera:
  - platform: generic
    name: "Random Nextcloud Image"
    still_image_url: "http://[HOST]:[PORT:8181]/random"
    content_type: image/jpeg
    limit_refetch_to_url_change: true
    frame_interval: 60  # Optional: Update every 60 seconds
```

Replace `[HOST]` and `[PORT:8181]` with your actual host and port.

You can then add this camera to your dashboard using the Picture Entity card or as a background for other cards.

## Docker Support

The add-on can also be run as a standalone Docker container:

1. Create a `.env` file with your configuration:
   ```
   NEXTCLOUD_URL=your_nextcloud_url
   NEXTCLOUD_USERNAME=your_username
   NEXTCLOUD_PASSWORD=your_password
   NEXTCLOUD_DIRS=Pictures,Photos
   ```

2. Start the container:
   ```bash
   docker-compose up -d
   ```

The service will be available at `http://localhost:8181`.

## Development

To build and run locally:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration

4. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8181
   ```

## License

MIT License