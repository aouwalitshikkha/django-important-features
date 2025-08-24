MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'blog.middleware.TrailingSlashMiddleware',
    'blog.middleware.RedirectMiddleware',
    'blog.middleware.NotFoundMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]