# Photo Proxy Home Assistant Add-on

A Home Assistant add-on that serves images from your Nextcloud server, either randomly or in sequence.

## Features

- Serves images from your Nextcloud server
- Random image selection
- Sequential image viewing
- Health check endpoint
- Configurable through Home Assistant UI

## Installation

1. Add this repository to your Home Assistant add-on store:
   - Go to Home Assistant → Settings → Add-ons → Add-on Store
   - Click the three dots menu in the top right
   - Select "Repositories"
   - Add the URL of this repository
   - Click "Add"

2. Install the "Photo Proxy" add-on from the add-on store

3. Configure the add-on:
   - Click on the add-on in the add-on store
   - Click "Install"
   - Configure the following required options:
     - `nextcloud_url`: Your Nextcloud server URL
     - `nextcloud_username`: Your Nextcloud username
     - `nextcloud_password`: Your Nextcloud password
     - `nextcloud_dirs`: Comma-separated list of directories to scan (default: "Pictures")

4. Start the add-on

## Usage

The add-on provides the following endpoints:

- `http://your-home-assistant:8181/random` - Get a random image from your Nextcloud server
- `http://your-home-assistant:8181/next` - Get the next image in sequence from your Nextcloud server
- `http://your-home-assistant:8181/health` - Health check endpoint

You can use these URLs in Home Assistant entities like:
- Picture entity cards
- Custom cards
- Automations
- Scripts

## Configuration

### Nextcloud Integration

The add-on requires the following configuration options:

- `nextcloud_url`: The URL of your Nextcloud server (required)
- `nextcloud_username`: Your Nextcloud username (required)
- `nextcloud_password`: Your Nextcloud password (required)
- `nextcloud_dirs`: Comma-separated list of directories to scan for images (default: "Pictures")

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.