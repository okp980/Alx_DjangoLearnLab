"""
Custom security middleware for the Bookshelf application.

This middleware implements Content Security Policy (CSP) headers and other
security-related HTTP headers to protect against XSS, clickjacking, and
other common web vulnerabilities.
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Custom middleware to add security headers to HTTP responses.
    
    This middleware implements:
    - Content Security Policy (CSP) headers
    - Additional security headers for enhanced protection
    - Configurable CSP policies based on Django settings
    """
    
    def process_response(self, request, response):
        """
        Add security headers to the HTTP response.
        
        Args:
            request: The HTTP request object
            response: The HTTP response object
            
        Returns:
            response: The HTTP response with security headers added
        """
        
        # SECURITY: Content Security Policy (CSP) Headers
        # Prevent XSS attacks by controlling resource loading
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_directives = []
            
            # Default source directive
            if settings.CSP_DEFAULT_SRC:
                csp_directives.append(f"default-src {' '.join(settings.CSP_DEFAULT_SRC)}")
            
            # Script source directive
            if hasattr(settings, 'CSP_SCRIPT_SRC') and settings.CSP_SCRIPT_SRC:
                csp_directives.append(f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}")
            
            # Style source directive
            if hasattr(settings, 'CSP_STYLE_SRC') and settings.CSP_STYLE_SRC:
                csp_directives.append(f"style-src {' '.join(settings.CSP_STYLE_SRC)}")
            
            # Image source directive
            if hasattr(settings, 'CSP_IMG_SRC') and settings.CSP_IMG_SRC:
                csp_directives.append(f"img-src {' '.join(settings.CSP_IMG_SRC)}")
            
            # Font source directive
            if hasattr(settings, 'CSP_FONT_SRC') and settings.CSP_FONT_SRC:
                csp_directives.append(f"font-src {' '.join(settings.CSP_FONT_SRC)}")
            
            # Connect source directive
            if hasattr(settings, 'CSP_CONNECT_SRC') and settings.CSP_CONNECT_SRC:
                csp_directives.append(f"connect-src {' '.join(settings.CSP_CONNECT_SRC)}")
            
            # Frame ancestors directive
            if hasattr(settings, 'CSP_FRAME_ANCESTORS') and settings.CSP_FRAME_ANCESTORS:
                csp_directives.append(f"frame-ancestors {' '.join(settings.CSP_FRAME_ANCESTORS)}")
            
            # Base URI directive
            if hasattr(settings, 'CSP_BASE_URI') and settings.CSP_BASE_URI:
                csp_directives.append(f"base-uri {' '.join(settings.CSP_BASE_URI)}")
            
            # Object source directive
            if hasattr(settings, 'CSP_OBJECT_SRC') and settings.CSP_OBJECT_SRC:
                csp_directives.append(f"object-src {' '.join(settings.CSP_OBJECT_SRC)}")
            
            # Add CSP header to response
            if csp_directives:
                response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        # SECURITY: Additional Security Headers
        
        # Cross-Origin Opener Policy (COOP)
        if hasattr(settings, 'SECURE_CROSS_ORIGIN_OPENER_POLICY'):
            response['Cross-Origin-Opener-Policy'] = settings.SECURE_CROSS_ORIGIN_OPENER_POLICY
        
        # Referrer Policy
        if hasattr(settings, 'SECURE_REFERRER_POLICY'):
            response['Referrer-Policy'] = settings.SECURE_REFERRER_POLICY
        
        # SECURITY: Log security-related events
        # Log any potential security issues or suspicious requests
        if request.path.startswith('/admin/') and not request.user.is_authenticated:
            # Log unauthorized admin access attempts
            import logging
            security_logger = logging.getLogger('django.security')
            security_logger.warning(
                f"Unauthorized admin access attempt from IP: {self.get_client_ip(request)} "
                f"to path: {request.path}"
            )
        
        return response
    
    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        
        Args:
            request: The HTTP request object
            
        Returns:
            str: The client's IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
