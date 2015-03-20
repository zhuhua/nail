from simpletor import application
from user import services as user_service

class Api():
    def __init__(self, auth=False):
        self.auth = auth
    
    def __call__(self, method):
        def __method(handler, *args, **kwds):
            headers = handler.request.headers
            if self.auth:
                if not headers.has_key('Authorization'):
                    handler.send_error(403)
                    return
                
                token = user_service.get_token(headers['Authorization'])
                if token is None:
                    handler.send_error(403)
                    return
                handler.user_id = token.user_id
            else:
                token = user_service.get_token(headers.get('Authorization'))
                if token is not None:
                    handler.user_id = token.user_id
            try:
                method(handler, *args, **kwds)
            except application.AppError, e:
                handler.set_status(400)
                handler.render_json(dict(message=e.value))
        return __method