from typing import List, Dict

def generate_status_page(images: List[Dict], nextcloud_url: str, nextcloud_username: str, nextcloud_dirs: List[str]) -> str:
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
            .recent-image {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.5rem 0;
                border-bottom: 1px solid #dee2e6;
                transition: all 0.2s ease;
            }}
            .recent-image:hover {{
                background-color: #f8f9fa;
            }}
            .recent-image:last-child {{
                border-bottom: none;
            }}
            .image-preview {{
                width: 100%;
                height: 200px;
                object-fit: cover;
                border-radius: 0.375rem;
                margin-top: 0.5rem;
            }}
            .preview-container {{
                display: none;
                margin-top: 0.5rem;
            }}
            .preview-container.active {{
                display: block;
            }}
            .loading {{
                display: none;
                text-align: center;
                padding: 1rem;
            }}
            .loading.active {{
                display: block;
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
                                <div class="col-md-6">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                                        <span class="status-badge">Running</span>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="bi bi-images me-2"></i>
                                        <span class="status-badge">Total Images: {len(images)}</span>
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

                    <div class="card">
                        <div class="card-header bg-warning text-dark">
                            <h2 class="h5 mb-0">Recent Images</h2>
                        </div>
                        <div class="card-body">
                            <div class="list-group list-group-flush">
                                {''.join(f'''
                                <div class="recent-image" data-url="/random">
                                    <i class="bi bi-image"></i>
                                    <div class="text-break">{img["name"]}</div>
                                </div>
                                <div class="preview-container" id="preview-{idx}">
                                    <div class="loading">
                                        <div class="spinner-border text-primary" role="status">
                                            <span class="visually-hidden">Loading...</span>
                                        </div>
                                    </div>
                                    <img class="image-preview" src="/random" alt="{img["name"]}">
                                </div>
                                ''' for idx, img in enumerate(images[:5]))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                // Handle image previews
                const recentImages = document.querySelectorAll('.recent-image');
                recentImages.forEach((image, index) => {{
                    image.addEventListener('click', function() {{
                        const previewContainer = document.getElementById(`preview-${{index}}`);
                        const loading = previewContainer.querySelector('.loading');
                        const preview = previewContainer.querySelector('.image-preview');

                        // Toggle preview
                        previewContainer.classList.toggle('active');

                        if (previewContainer.classList.contains('active')) {{
                            // Show loading state
                            loading.classList.add('active');
                            preview.style.display = 'none';

                            // Load image
                            preview.src = this.dataset.url + '?t=' + new Date().getTime();
                            preview.onload = function() {{
                                loading.classList.remove('active');
                                preview.style.display = 'block';
                            }};
                        }}
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    """