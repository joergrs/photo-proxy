from typing import List, Dict

def generate_status_page(images: List[Dict], nextcloud_url: str, nextcloud_username: str, nextcloud_dirs: List[str], max_image_size: int, jpg_quality: int, convert_to_jpg: bool, crop_portrait_to_square: bool, cache_stats: Dict[str, int], debug_logging: bool) -> str:
    """Generate a status page with information about the service using Bootstrap 5."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Photo Proxy Status</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body {{
                background-color: #f8f9fa;
            }}
            .card {{
                box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
            }}
            .endpoint {{
                background-color: #f8f9fa;
                border-radius: 0.375rem;
                padding: 0.75rem;
                margin-bottom: 0.5rem;
                transition: all 0.2s ease;
            }}
            .endpoint:hover {{
                background-color: #e9ecef;
                transform: translateY(-1px);
            }}
            .endpoint a {{
                text-decoration: none;
                color: inherit;
            }}
            .status-badge {{
                font-size: 0.875rem;
            }}
        </style>
    </head>
    <body>
        <div class="container py-4">
            <div class="row justify-content-center">
                <div class="col-md-10">
                    <h1 class="mb-4">Photo Proxy Status</h1>

                    <div class="card mb-4">
                        <div class="card-header bg-primary text-white">
                            <h2 class="h5 mb-0">Service Status</h2>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                                        <span class="status-badge">Running</span>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-images me-2"></i>
                                        <span class="status-badge">Total Images: {len(images)}</span>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-hdd me-2"></i>
                                        <span class="status-badge">Cache Size: {cache_stats['size']}/{cache_stats['max_size']}</span>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-bug me-2"></i>
                                        <span class="status-badge">Debug Logging: {'Enabled' if debug_logging else 'Disabled'}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-check-circle me-2"></i>
                                        <span class="status-badge">Cache Hits: {cache_stats['hits']}</span>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-x-circle me-2"></i>
                                        <span class="status-badge">Cache Misses: {cache_stats['misses']}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-graph-up me-2"></i>
                                        <span class="status-badge">Cache Hit Ratio: {cache_stats['hit_ratio']}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card mb-4">
                        <div class="card-header bg-info text-white">
                            <h2 class="h5 mb-0">Nextcloud Configuration</h2>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label class="form-label text-muted">Server URL</label>
                                        <div class="text-break">{nextcloud_url}</div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label class="form-label text-muted">Username</label>
                                        <div>{nextcloud_username}</div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label class="form-label text-muted">Directories</label>
                                        <div>{', '.join(nextcloud_dirs)}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card mb-4">
                        <div class="card-header bg-secondary text-white">
                            <h2 class="h5 mb-0">Image Processing Configuration</h2>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label class="form-label text-muted">Max Image Size</label>
                                        <div>{max_image_size}px</div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label class="form-label text-muted">JPG Quality</label>
                                        <div>{jpg_quality}%</div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label class="form-label text-muted">Convert to JPG</label>
                                        <div>{'Yes' if convert_to_jpg else 'No'}</div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="mb-3">
                                        <label class="form-label text-muted">Crop Portrait to Square</label>
                                        <div>{'Yes' if crop_portrait_to_square else 'No'}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header bg-success text-white">
                            <h2 class="h5 mb-0">Available Endpoints</h2>
                        </div>
                        <div class="card-body">
                            <div class="endpoint">
                                <a href="/random" target="_blank">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-shuffle me-2"></i>
                                        <div>
                                            <strong>GET /random</strong>
                                            <div class="text-muted small">Get a random image from your Nextcloud server</div>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="endpoint">
                                <a href="/next" target="_blank">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-arrow-right-circle me-2"></i>
                                        <div>
                                            <strong>GET /next</strong>
                                            <div class="text-muted small">Get the next image in sequence</div>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="endpoint">
                                <a href="/slideshow" target="_blank">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-play-circle me-2"></i>
                                        <div>
                                            <strong>GET /slideshow</strong>
                                            <div class="text-muted small">View images in a slideshow presentation</div>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="endpoint">
                                <a href="/health" target="_blank">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-heart-pulse me-2"></i>
                                        <div>
                                            <strong>GET /health</strong>
                                            <div class="text-muted small">Health check endpoint</div>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """