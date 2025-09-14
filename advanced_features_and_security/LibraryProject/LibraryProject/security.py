# LibraryProject/LibraryProject/security.py
class ContentSecurityPolicyMiddleware:
    """
    Adds a simple Content Security Policy header.
    Configure via settings.CSP_* variables.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            from django.conf import settings
            csp = f"default-src {settings.CSP_DEFAULT_SRC}; " \
                  f"img-src {settings.CSP_IMG_SRC}; " \
                  f"script-src {settings.CSP_SCRIPT_SRC}; " \
                  f"style-src {settings.CSP_STYLE_SRC}"
            response["Content-Security-Policy"] = csp
        except Exception:
            pass
        return response
