from time import sleep
def delay_request(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        print('delaying request for 5 seconds')
        sleep(5)
        response = get_response(request)
        return response

    return middleware