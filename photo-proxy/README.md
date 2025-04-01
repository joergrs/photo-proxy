# Photo Proxy

A Home Assistant add-on that serves images from Nextcloud as a proxy. This is useful for displaying images from Nextcloud in Home Assistant dashboards or other applications that don't support WebDAV authentication.

## Features

- Serves images from Nextcloud via HTTP
- Supports multiple directories
- Image processing features:
  - Automatic EXIF rotation
  - Image scaling (configurable max size)
  - Optional JPG conversion with quality control
- Status page showing service information and recent images
- Slideshow mode with:
  - Automatic image transitions every 10 seconds
  - Smooth fade effects between images
  - Play/pause controls
  - Manual next image button
  - Auto-hiding controls when mouse is not in the lower screen area
  - Error handling for failed image loads

## Installation

1. Add the repository to your Home Assistant instance
2. Install the add-on
3. Configure the add-on with your Nextcloud credentials and settings
4. Start the add-on

## Configuration

The add-on can be configured through the Home Assistant UI or by editing the `config.yaml` file:

```yaml
nextcloud_url: "https://your-nextcloud-instance.com"
nextcloud_username: "your-username"
nextcloud_password: "your-password"
nextcloud_dirs: "Pictures"  # Comma-separated list of directories
max_image_size: 1920       # Maximum width/height for scaled images
jpg_quality: 85           # Quality for JPG conversion (1-100)
convert_to_jpg: true      # Whether to convert all images to JPG
```

## Usage

The add-on provides several endpoints:

- `/` - Status page showing service information and recent images
- `/random` - Returns a random image from the configured directories
- `/next` - Returns the next image in sequence
- `/slideshow` - A full-screen slideshow page with automatic transitions and controls

### Image URLs

Images can be accessed using the following URL pattern:
```
http://your-home-assistant:8181/random
```

The image will be:
1. Automatically rotated based on EXIF data
2. Scaled if larger than `max_image_size`
3. Converted to JPG if `convert_to_jpg` is enabled

### Slideshow Mode

The `/slideshow` endpoint provides a full-screen slideshow experience:
- Images automatically transition every 10 seconds with a smooth fade effect
- Controls appear when the mouse is in the lower quarter of the screen
- Play/pause button to control automatic transitions
- Next button to manually advance to the next image
- Countdown timer showing seconds until next transition
- Controls automatically hide when the mouse leaves the screen area

## Development

The add-on is built using:
- FastAPI for the web server
- Pillow for image processing
- webdav4-client for Nextcloud communication

## License

MIT License - see LICENSE file for details